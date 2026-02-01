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
                self.model_id = 'gemini-2.0-flash' # REVERTED TO STABLE FLASH (V43)
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

        system_prompt = f"""
        {self.behavior_protocol}

        ## 📚 REFERENCE KNOWLEDGE (OFFICIAL MANUAL):
        Use this knowledge to set accurate parameter values and types.
        {self.knowledge_base[:300000]} 

        ## 🔧 SURGICAL PARAMETER DICTIONARY (USER CUSTOM ALIASES):
        Use these internal mappings to ensure precision:
        {surgical_dict_text}

        ## 🎛️ AVAILABLE DEVICES:
        {", ".join(sorted(set(available_devices)))}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{system_prompt}\n\nUSER PROMPT: {text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            # Clean prose/markdown if present
            raw_text = response.text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(raw_text)
            
            # V40 Robustness: If AI returns a list, take the first element
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            
            if not isinstance(data, dict):
                print(f"WARNING: AI returned non-dict JSON: {type(data)}")
                return self._parse_with_regex(text)
            
            # V41 RESOLUTION ENGINE: Hyper-Robust Device Extraction
            device_map = {} # canon_name -> parameters
            
            # Helper to process any device entry
            def process_entry(item):
                if not item: return
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
                        if canon in device_map:
                            device_map[canon].update(params)
                        else:
                            device_map[canon] = params

            # Stage 1: Raw devices list
            raw_devs = data.get("devices", [])
            if isinstance(raw_devs, str): raw_devs = [raw_devs]
            for d in raw_devs: process_entry(d)
            
            # Stage 2: Surgical devices list
            surg_devs = data.get("surgical_devices", [])
            if isinstance(surg_devs, str): surg_devs = [surg_devs]
            for d in surg_devs: process_entry(d)
            
            # Stage 3: Macro details (Implicit devices)
            for m in data.get("macro_details", []):
                d_name = m.get("target_device")
                if d_name:
                    canon = self.device_db.resolve_alias(d_name)
                    if canon and canon not in device_map:
                        device_map[canon] = {}

            resolved_devices = [{"name": k, "parameters": v} for k, v in device_map.items()]
            valid_canonical_names = list(device_map.keys())
            
            return {
                "creative_name": data.get("creative_name", "Precision Rack"),
                "devices": valid_canonical_names,
                "surgical_devices": resolved_devices, 
                "macro_count": data.get("macro_count", 8),
                "sound_intent": data.get("sound_intent", ""),
                "macro_details": data.get("macro_details", []),
                "ai_powered": True,
                "model": self.model_id,
                "ai_powered": True,
                "model": self.model_id,
                "explanation": data.get("explanation") or data.get("musical_logic_explanation", "")
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
