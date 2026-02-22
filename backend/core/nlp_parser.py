"""
NLP Parser - Extract rack specifications from natural language using Gemini
"""

import re
import json
import os
from typing import Dict, List, Optional
from core.builder import AudioEffectRack, Chain, AbletonDevice
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class RackNLPParser:
    """Parse natural language into rack specifications using AI or Regex"""
    
    def __init__(self, device_db):
        self.device_db = device_db
        self.device_patterns = self._build_device_patterns()
        
        # Initialize Gemini 2.0+ Client
        api_key = os.getenv("GOOGLE_API_KEY")
        self.ai_enabled = False
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                self.model_id = 'gemini-2.0-flash'
                self.ai_enabled = True
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini Client: {e}")

        # V50 KNOWLEDGE INJECTION
        self.knowledge_base = ""
        try:
            kb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge', 'MANUAL_EXTRACT.txt')
            if os.path.exists(kb_path):
                with open(kb_path, 'r', encoding='utf-8') as f:
                    self.knowledge_base = f.read()
                print(f"SUCCESS: Loaded Knowledge Base ({len(self.knowledge_base)} chars)")
            else:
                print("Warning: MANUAL_EXTRACT.txt not found.")
        except Exception as e:
            print(f"Warning: Failed to load Knowledge Base: {e}")

        # V51 PROTOCOL INJECTION
        self.behavior_protocol = ""
        try:
            proto_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge', 'AI_BEHAVIOR_PROTOCOL.md')
            if os.path.exists(proto_path):
                with open(proto_path, 'r', encoding='utf-8') as f:
                    self.behavior_protocol = f.read()
                print(f"SUCCESS: Loaded AI Behavior Protocol ({len(self.behavior_protocol)} chars)")
            else:
                print("Warning: AI_BEHAVIOR_PROTOCOL.md not found.")
        except Exception as e:
            print(f"Warning: Failed to load AI Behavior Protocol: {e}")

    def _build_device_patterns(self) -> List[str]:
        """Build regex patterns for deterministic fallback"""
        all_names = list(self.device_db.get_all_devices().keys())
        all_aliases = list(self.device_db.aliases.keys())
        all_terms = sorted(list(set(all_names + all_aliases)), key=len, reverse=True)
        return [re.escape(term.lower()) for term in all_terms]

    async def parse(self, text: str) -> Dict:
        """Parse user input, preferring AI if enabled"""
        if self.ai_enabled:
            return await self._parse_with_ai(text)
        return self._parse_with_regex(text)

    async def _parse_with_ai(self, text: str) -> Dict:
        """Use Gemini with V7 Surgical Prompt"""
        available_devices = list(self.device_db.get_all_devices().keys()) + list(self.device_db.aliases.keys())
        
        # V47 Dynamic Surgical Dictionary
        surgical_dict_text = ""
        if hasattr(self.device_db, "get_parameter_aliases"):
            aliases = self.device_db.get_parameter_aliases()
            for dev, params in aliases.items():
                for alias, target in params.items():
                    surgical_dict_text += f'        - "{alias}" -> Use `{target}` (for {dev})\n'

        # V62: RESTRUCTURED PROMPT FOR STABILITY
        system_prompt = f"""
ROLE: You are the Ultimate Ableton Sound Design Specialist. 
TASK: Generate a complex, professional-grade Audio Effect Rack.

{self.behavior_protocol}

## 📚 REFERENCE KNOWLEDGE (OFFICIAL MANUAL):
{self.knowledge_base[:50000]} 

## 🔧 SURGICAL PARAMETER DICTIONARY:
{surgical_dict_text}

## 🎛️ AVAILABLE DEVICES:
{", ".join(sorted(set(available_devices)))}

## 🏁 FINAL CONSTRAINTS (MANDATORY):
1. **ALWAYS 8 MACROS**: Even if the user only asks for 1 mapping, you MUST fill all 8 slots with professional sound design gestures.
2. **MULTI-DEVICE DENSITY**: At least 4 out of 8 macros MUST control parameters across multiple devices.
3. **GAIN STAGING**: Any 'Drive' or 'Threshold' mapping MUST have inverse 'Output Gain' compensation on the same knob.
4. **JSON ONLY**: Return strictly valid JSON. No preamble.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{system_prompt}\n\nUSER PROMPT: {text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1, # Keep it deterministic and focused
                )
            )
            
            # Clean and Log Raw JSON for Debugging
            raw_text = response.text.strip()
            
            # V64: Robust Sanitization for non-standard JSON (handles -inf, inf, nan with any whitespace)
            import re
            raw_text = re.sub(r':\s*-?inf(inity)?\b', ': -999.0', raw_text, flags=re.IGNORECASE)
            raw_text = re.sub(r':\s*nan\b', ': 0.0', raw_text, flags=re.IGNORECASE)
            
            with open("last_ai_response_raw.json", "w", encoding='utf-8') as f:
                f.write(raw_text)
            
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(raw_text)
            
            # V65: Log the final processed spec for debugging
            with open("last_spec_debug.json", "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            # V40 Robustness: If AI returns a list, take the first element
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            
            if not isinstance(data, dict):
                print(f"WARNING: AI returned non-dict JSON: {type(data)}")
                return self._parse_with_regex(text)
            
            # V41 RESOLUTION ENGINE: Hyper-Robust Device Extraction
            
            # V42 INSTANCE-BASED RESOLUTION: Support multiple devices of same type
            resolved_devices = []
            valid_canonical_names = []
            
            # Helper to process any device entry and return its resolved state
            def resolve_item(item):
                if not item: return None
                name = ""
                params = {}
                if isinstance(item, dict):
                    name = item.get("name") or item.get("target_device") or ""
                    params = item.get("parameters") or {}
                elif isinstance(item, str):
                    name = item
                
                if name:
                    canon = self.device_db.resolve_alias(str(name))
                    if canon:
                        return {"name": canon, "parameters": params}
                return None

            # Stage 1: Preserve order and multiplicity from AI "devices" list
            raw_devs = data.get("devices", [])
            if isinstance(raw_devs, str): raw_devs = [raw_devs]
            
            for d in raw_devs:
                resolved = resolve_item(d)
                if resolved:
                    resolved_devices.append(resolved)
                    valid_canonical_names.append(resolved["name"])
            
            # Stage 2: Sync with surgical_devices (if AI provided specific initial states)
            surg_devs = data.get("surgical_devices", [])
            for s in surg_devs:
                res_s = resolve_item(s)
                if not res_s: continue
                # Match by name and update existing resolved devices (first match that has empty params or same name)
                # This is a heuristic: if AI listed devices then surgical_devices, we pair them up.
                for r in resolved_devices:
                    if r["name"] == res_s["name"] and not r["parameters"]:
                        r["parameters"].update(res_s["parameters"])
                        break
                else:
                    # If not found in primary list, add it as a new instance
                    resolved_devices.append(res_s)
                    valid_canonical_names.append(res_s["name"])

            # Stage 3: Merge implicit devices from macro_details
            for m in data.get("macro_details", []):
                d_name = m.get("target_device")
                if d_name:
                    canon = self.device_db.resolve_alias(d_name)
                    if canon and canon not in valid_canonical_names:
                        resolved_devices.append({"name": canon, "parameters": {}})
                        valid_canonical_names.append(canon)

            # Deduplicate macro_details:
            # Pass 1: Remove identical (macro, device, param) combos
            # Pass 2: Remove cross-macro duplicates
            raw_macro_details = data.get("macro_details", [])
            seen_same_macro = set()
            seen_cross_macro = set()
            deduped_macro_details = []
            for m in raw_macro_details:
                macro_num = m.get("macro")
                dev_key = str(m.get("target_device", "")).lower().strip()
                param_key = str(m.get("target_parameter", "")).lower().strip()
                
                same_key = (macro_num, dev_key, param_key)
                cross_key = (dev_key, param_key)
                
                if same_key in seen_same_macro: continue
                if cross_key in seen_cross_macro: continue
                
                seen_same_macro.add(same_key)
                seen_cross_macro.add(cross_key)
                deduped_macro_details.append(m)
            
            return {
                "creative_name": data.get("creative_name", "Precision Rack"),
                "devices": valid_canonical_names,
                "surgical_devices": resolved_devices, 
                "macro_count": data.get("macro_count", 8),
                "sound_intent": data.get("sound_intent", ""),
                "macro_details": deduped_macro_details,
                "ai_powered": True,
                "model": self.model_id,
                "explanation": data.get("explanation") or data.get("musical_logic_explanation", ""),
                "tips": data.get("tips", [])
            }
        except Exception as e:
            print(f"AI Parse failed: {e}")
            return self._parse_with_regex(text)

    def _parse_with_regex(self, text: str) -> Dict:
        """Deterministic fallback"""
        spec = {"devices": [], "macro_count": 8, "ai_powered": False}
        text_lower = text.lower()
        found = []
        for pattern in self.device_patterns:
             if re.search(r'\b' + pattern + r'\b', text_lower):
                  term = pattern.replace('\\', '')
                  canon = self.device_db.resolve_alias(term)
                  if canon and canon not in found: found.append(canon)
        spec["devices"] = found
        spec["surgical_devices"] = [{"name": d, "parameters": {}} for d in found]
        return spec

    def is_ready(self) -> bool: return True
