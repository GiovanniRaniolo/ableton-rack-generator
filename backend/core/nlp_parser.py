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
        # ABLETON LIVE 12.3 MUSICAL SURGICAL ENGINE (V40)
        
        You are a Master Audio Design AI. Your task is to generate perfectly calibrated Audio Effect Racks. 
        You MUST follow the "Musical Semantic Protocols" to ensure mappings are expressive and safe.

        ## 🏛️ MUSICAL SEMANTIC PROTOCOLS:
        1. **Hz PROTOCOL (Frequencies)**:
           - NEVER use linear math. Use Logarithmic context.
           - High-Pass sweep: min=20.0, max=18000.0. 
           - Sub-bass focus: min=20.0, max=250.0. 
        2. **dB PROTOCOL (Volumes/Gain)**:
           - SAFETY FLOOR: Never start a gain macro at -inf unless it's a "Mute".
           - Neutral Trim: min=-36.0, max=6.0. 
           - Heavy Drive: min=0.0, max=24.0.
        You MUST follow the "Musical Semantic Protocols" for all values.

        ## 📖 SURGICAL PARAMETER DICTIONARY (LABEL -> INTERNAL):
        Use these internal names for mapping even if the user uses manual labels:
{surgical_dict_text}

        ## 🔬 MUSICAL SEMANTIC PROTOCOLS:
        1. **Hz Protocol**: Use logarithmic scaling (20Hz to 18kHz). Filters sweep UP (40 -> 18k) or DOWN (18k -> 40).
        2. **dB Protocol**: Gain ranges MUST NOT start at -inf. Use a safety floor (e.g., -36dB to 0dB or -70dB to 6dB).
        3. **Discrete Protocol**: Beat Repeat Grid (0-15), Auto Filter Type (0-9). Do NOT use floating points for these.
        4. **Sidechain Law**: When "Ducking" or "Sidechain" is mentioned, prioritize mapping `Sidechain_Gain` or `Sidechain_Mix`.

        ## 📝 RESPONSE FORMAT (STRICT JSON):
        {{
            "creative_name": "Surgical Rack",
            "devices": ["Auto Filter", "Compressor"],
            "surgical_devices": [{{ "name": "Auto Filter", "parameters": {{ "Filter_Frequency": 1000.0 }} }}],
            "macro_details": [
                {{
                    "macro": 1,
                    "name": "The Void",
                    "target_device": "Auto Filter",
                    "target_parameter": "Filter_Frequency",
                    "min": 18000.0,
                    "max": 40.0
                }}
            ],
            "sound_intent": "Dark, industrial, and glitchy atmosphere.",
            "musical_logic_explanation": "Technical reasoning for ranges and unit choices."
        }}

        Available Devices: {", ".join(sorted(set(available_devices)))}
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
