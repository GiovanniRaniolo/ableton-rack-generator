"""
NLP Parser - Extract rack specifications from natural language using Gemini
"""

import re
import json
import os
from typing import Dict, List, Optional
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
                print(f"SUCCESS: {self.model_id} (Surgical V7) Parser Initialized")
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
        
        system_prompt = f"""
        # ABLETON LIVE 12.3 SURGICAL DESIGN ENGINE (V7)
        
        You are a Master Audio Engineer. You have absolute authority over every parameter of every device.
        Your goal is technical perfection and creative sound design.

        ## SURGICAL MISSIONS:
        1. **Deep Init**: You MUST set initial values for device parameters to achieve the requested vibe, even if they aren't mapped to macros.
        2. **Skill-Based Logic**: Implement specific techniques (e.g., set Delay to PING-PONG mode, or Roar to ASYMMETRIC shaper).
        3. **Creative Labeling**: Every macro MUST have a descriptive name that reflects your sound design intent.
        4. **Multi-Lang**: Respond in the user's language with professional clarity.

        ## TECHNICAL REFS:
        - Devices: {", ".join(sorted(set(available_devices)))}
        - Core Params: ROAR (Stage1_Shaper_Amount, Stage1_Filter_Frequency), ECHO (Delay_TimeL, Feedback, Filter_Frequency), REVERB (DecayTime, RoomSize), DRUM_BUSS (DriveAmount, TransientShaping), SATURATOR (PreDrive, PostDrive).
        - PHYSICAL PRECISION: You HAVE SURGICAL AUTHORITY. If the user asks for "18 kHz to 600 Hz", set 'min': 18000.0 and 'max': 600.0. Use physical units for Hz, dB (-36.0 to 36.0), ms, %.
        - DEFAULT RANGES: Use 'min': 0.0 and 'max': 1.0 ONLY if you want the system to auto-scale to the full physical device range.
        - INVERSE MAPPING: Set 'min' > 'max' (e.g. 18000 to 600) to invert the knob behavior.

        ## RESPONSE FORMAT (STRICT JSON):
        {{
            "creative_name": "Pro Name",
            "devices": [
                {{
                    "name": "Exact Device Name",
                    "parameters": {{
                        "ParameterName": 123.45
                    }}
                }}
            ],
            "macro_count": 8,
            "sound_intent": "Deep technical analysis.",
            "macro_details": [
                {{
                    "macro": 1,
                    "name": "Creative Label (e.g. 'Stardust')",
                    "target_device": "Exact Device Name",
                    "target_parameter": "Exact Parameter Key",
                    "min": 0.0,
                    "max": 1.0,
                    "description": "Technical impact."
                }}
            ],
            "parallel_logic": "Routing details.",
            "tips": ["Tip"],
            "explanation": "Summary."
        }}

        IMPORTANT: If you want a parameter to move across a wide range, provide 'min' and 'max' values. If not provided, the system will use physical defaults.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{system_prompt}\n\nUSER PROMPT: {text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            data = json.loads(response.text)
            
            # Resolve aliases and handle V7 structure
            resolved_devices = []
            valid_canonical_names = []
            
            # The AI might give a list of strings or a list of objects (V7)
            raw_devices = data.get("devices", [])
            for item in raw_devices:
                name = item.get("name") if isinstance(item, dict) else item
                params = item.get("parameters", {}) if isinstance(item, dict) else {}
                
                canon = self.device_db.resolve_alias(name)
                if canon:
                    resolved_devices.append({"name": canon, "parameters": params})
                    valid_canonical_names.append(canon)
            
            return {
                "creative_name": data.get("creative_name", "Custom Rack"),
                "devices": valid_canonical_names, # For legacy compatibility in some parts
                "surgical_devices": resolved_devices, # New V7 structure
                "macro_count": data.get("macro_count", 8),
                "sound_intent": data.get("sound_intent", ""),
                "macro_details": data.get("macro_details", []),
                "parallel_logic": data.get("parallel_logic", ""),
                "tips": data.get("tips", []),
                "ai_powered": True,
                "model": self.model_id,
                "explanation": data.get("explanation", "")
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
