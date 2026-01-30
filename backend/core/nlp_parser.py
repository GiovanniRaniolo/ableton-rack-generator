"""
NLP Parser - Extract rack specifications from natural language using Gemini 1.5 Pro
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
        
        # Initialize Gemini 2.0+ Client (Modern SDK)
        api_key = os.getenv("GOOGLE_API_KEY")
        self.ai_enabled = False
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                self.model_id = 'gemini-2.5-pro' # Flagship Elite
                self.ai_enabled = True
                print(f"SUCCESS: {self.model_id} (Modern SDK) Parser Initialized")
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
        """Use Gemini 1.5 Pro to understand complex sound design instructions"""
        available_devices = list(self.device_db.get_all_devices().keys()) + list(self.device_db.aliases.keys())
        
        system_prompt = f"""
        Sei il World-Class Ableton Live Sound Design Engine (AI Expert Mode). 
        Il tuo obiettivo è trasformare descrizioni creative in una specifica tecnica di Rack professionale (.adg) 
        fornendo insight tecnici profondi in LINGUA ITALIANA.
        
        AVAILABLE ABLETON DEVICES:
        {", ".join(sorted(set(available_devices)))}
        
        LINEE GUIDA RIGIDE:
        1. LINGUA: Rispondi SEMPRE in ITALIANO tecnico e professionale.
        2. PERSONALITÀ: Agisci come un fonico/sound designer esperto. Sii preciso e visionario.
        3. SEMANTIC MAPPING: Se l'utente usa termini astratti o creativi (es. 'transizioni', 'aria', 'calore', 'movimento'), 
           utilizza la tua conoscenza professionale per selezionare i dispositivi più adatti dalla lista AVAILABLE.
           *Esempio: 'transizioni' -> Reverb (decay lungo) + Auto Filter (sweep frequenze).*
           *CRITICAL SAFETY RULE: For 'Transition' requests, ALWAYS use 'Delay' (NOT Echo) and 'Reverb' (NOT Grain Delay).*
        4. MACRO: Spiega esattamente cosa succede al segnale. NON usare 'Generic mapping'.
           Esempio: "M1 (Crunch): Aumenta il Drive del Saturator, aggiungendo armoniche medie e saturazione analogica."
        5. SOUND INTENT: Descrivi l'impatto sonoro complessivo in modo tecnico.
        6. TIPS: Fornisci 2-3 consigli da studio professionale.
        
        RESPONSE FORMAT (STRICT JSON):
        {{
            "creative_name": "Nome evocativo e creativo (es. 'Glacial Void')",
            "devices": ["Device 1", "Device 2"],
            "macro_count": 8,
            "chains": 1,
            "sound_intent": "Spiegazione tecnica dell'impatto sul segnale (Italiano)",
            "macro_details": [
                {{
                    "macro": 1,
                    "name": "Nome (es. 'Space')",
                    "target_device": "Device Name (es. 'Reverb')",
                    "target_parameter": "Parameter Name (es. 'Decay Time')",
                    "description": "Spiegazione tecnica (Italiano)"
                }}
            ],
            "parallel_logic": "Logica di routing (Italiano)",
            "tips": ["Tip 1", "Tip 2"],
            "explanation": "Analisi discorsiva finale (Italiano)"
        }}
        """
        
        try:
            # Gemini 2.0+ (Modern SDK)
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{system_prompt}\n\nUSER PROMPT: {text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            # The modern SDK uses .text or .parsed for JSON depending on config
            response_text = response.text
            print(f"DEBUG AI Response: {response_text}")
            data = json.loads(response_text)
            
            # Resolve aliases to canonical names
            valid_devices = []
            for d in data.get("devices", []):
                canon = self.device_db.resolve_alias(d)
                if canon:
                    valid_devices.append(canon)
            
            return {
                "creative_name": data.get("creative_name", "Custom Rack"),
                "devices": valid_devices,
                "macro_count": data.get("macro_count", 8),
                "chains": data.get("chains", 1),
                "sound_intent": data.get("sound_intent", "Standard signal processing."),
                "macro_details": data.get("macro_details", []),
                "parallel_logic": data.get("parallel_logic", ""),
                "tips": data.get("tips", []),
                "ai_powered": True,
                "model": self.model_id,
                "explanation": data.get("explanation", "")
            }
        except Exception as e:
            print(f"AI Parse (Modern SDK) failed: {e}")
            return self._parse_with_regex(text)

    def _parse_with_regex(self, text: str) -> Dict:
        """Deterministic fallback parser using regex"""
        spec = {
            "devices": [],
            "macro_count": 8,
            "chains": 1,
            "ai_powered": False
        }
        
        text_lower = text.lower()
        found_devices = []
        for pattern in self.device_patterns:
             if re.search(r'\b' + pattern + r'\b', text_lower):
                 term = pattern.replace('\\', '')
                 canonical = self.device_db.resolve_alias(term)
                 if canonical and canonical not in found_devices:
                     found_devices.append(canonical)
        
        spec["devices"] = found_devices
        
        macro_match = re.search(r'(\d+)\s*macro', text_lower)
        if macro_match:
            spec["macro_count"] = int(macro_match.group(1))
            
        return spec

    def is_ready(self) -> bool:
        return True
