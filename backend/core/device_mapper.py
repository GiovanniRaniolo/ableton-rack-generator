"""
Device Database - Maps device names to XML structure and parameters
"""

import json
import os
from typing import Dict, List, Optional


class DeviceDatabase:
    """Database of Ableton device configurations"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.join(
            os.path.dirname(__file__), '..', 'data', 'devices.json'
        )
        self.extracted_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'extracted_parameters.json'
        )
        self.cloned_dna_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'cloned_devices_dna.json'
        )
        self.devices_dir = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'devices'
        )
        self.devices = self._load_database()
        self.extracted_params = self._load_extracted()
        self.cloned_dna = self._load_cloned_dna()
        
        # Ensure hierarchy exists
        if "devices" not in self.devices: self.devices["devices"] = {}
        if "audio_effects" not in self.devices["devices"]: self.devices["devices"]["audio_effects"] = {}
        
        audio_effects = self.devices["devices"]["audio_effects"]
        
        # Priority 1: Cloned DNA (Most accurate Physical Ranges)
        if self.cloned_dna:
            for d_name, d_info in self.cloned_dna.items():
                audio_effects[d_name] = d_info
        
        # Device name aliases for NLP
        self.aliases = {
            "comp": "Compressor",
            "compressor": "Compressor",
            "eq": "EQ Eight",
            "eq8": "EQ Eight",
            "eq eight": "EQ Eight",
            "reverb": "Reverb",
            "verb": "Reverb",
            "rev": "Reverb",
            "delay": "Delay",
            "saturator": "Saturator",
            "sat": "Saturator",
            "saturation": "Saturator",
            "filter": "Auto Filter",
            "auto filter": "Auto Filter",
            "gate": "Gate",
            "limiter": "Limiter",
            "glue": "Glue Compressor",
            "glue compressor": "Glue Compressor",
            "multiband": "Multiband Dynamics",
            "chorus": "Chorus",
            "flanger": "Flanger",
            "phaser": "Phaser",
            "pan": "Auto Pan",
            "auto pan": "Auto Pan",
            "erosion": "Erosion",
            "echo": "Echo",
            "hybrid reverb": "Hybrid Reverb",
            "hybrid": "Hybrid Reverb",
            "roar": "Roar",
            "spectral time": "Spectral Time",
            "spectral": "Spectral Time",
            "multiband dynamics": "Multiband Dynamics",
            "autofilter": "Auto Filter",
            "eq8": "EQ Eight",
            "phaser-flanger": "PhaserNew",
            "phaser new": "PhaserNew",
            "audio effect rack": "Audio Effect Rack",
            "audio effect rack": "Audio Effect Rack",
            "rack": "Audio Effect Rack"
        }

        # V47 SURGICAL PARAMETER ALIASES (Manual -> Internal)
        self.parameter_aliases = {
            "Hybrid": {
                "Decay": "Algorithm_Decay",
                "Size": "Algorithm_Size",
                "Shimmer": "Algorithm_Shimmer",
                "Damping": "Algorithm_Damping",
                "Pre Delay": "PreDelay_FeedbackTime",
                "Stereo": "StereoWidth",
                "Width": "StereoWidth",
                "Dry/Wet": "DryWet",
                "Blend": "ConvoAlgoBlend"
            },
            "AutoFilter": {
                "Frequency": "Filter_Frequency",
                "Freq": "Filter_Frequency",
                "Resonance": "Filter_Resonance",
                "Res": "Filter_Resonance",
                "Drive": "Filter_Drive",
                "LFO Amount": "Lfo_Amount",
                "LFO Rate": "Lfo_Frequency"
            },
            "Auto Filter": {
                "Frequency": "Filter_Frequency",
                "Freq": "Filter_Frequency",
                "Resonance": "Filter_Resonance",
                "Res": "Filter_Resonance",
                "Drive": "Filter_Drive",
                "LFO Amount": "Lfo_Amount",
                "LFO Rate": "Lfo_Frequency"
            },
            "AutoShift": {
                "Shift": "PitchShift_ShiftSemitones",
                "Glide": "MidiInput_Glide",
                "Fine": "PitchShift_Detune",
                "Formant": "PitchShift_FormantShift",
                "Scale": "Quantizer_Active",
                "Dry/Wet": "Global_DryWet"
            },
            "GrainDelay": {
                "Time": "MsDelay",
                "Spray": "Spray",
                "Pitch": "Pitch",
                "Frequency": "Freq",
                "Random": "RandomPitch",
                "Feedback": "Feedback",
                "Dry/Wet": "NewDryWet"
            },
            "BeatRepeat": {
                "Grid": "Grid",
                "Density": "Grid",
                "Interval": "Interval",
                "Chance": "Chance",
                "Gate": "Gate",
                "Pitch": "BasePitch",     # FIXED V53: Internal name is BasePitch
                "Transpose": "BasePitch",
                "Variation": "Variation",
                "Var": "Variation"
            },
            "Roar": {
                "Drive": "Stage1_Shaper_Trim",
                "Tone": "Input_ToneAmount",
                "Color": "Input_ColorOn",
                "Bias": "Stage1_Shaper_Bias",
                "Filter Freq": "Stage1_Filter_Frequency",
                "Resonance": "Stage1_Filter_Resonance",
                "Amount": "Stage1_Shaper_Amount",
                "Trim": "Stage1_Shaper_Trim"
            },
            "PhaserNew": {
                "Doubler": "DoublerDelayTime",
                "Color": "Warmth",
                "Sync": "Modulation_Sync",
                "Rate": "Modulation_Frequency"
            },
            "Corpus": {
                "Tune": "Transpose",
                "Coarse": "Transpose",
                "Fine": "FineTranspose",
                "Spread": "StereoWidth",
                "Width": "StereoWidth",
                "Opening": "TubeOpening",
                "Ratio": "Ratio",
                "Brightness": "Radius",  # Heuristic mapping based on common usage
                "Hit": "ExcitationX",    # Position of hit
                "Listening": "ListeningXL" # Position of listening
            },
            "Drum Buss": {
                "Drive": "DriveAmount",
                "Crunch": "CrunchAmount",
                "Boom": "BoomAmount",
                "Boom Freq": "BoomFrequency",
                "Transients": "TransientShaping",
                "Damp": "DampingFrequency"
            },
            "EQ Eight": {
                "Gain": "GlobalGain"
            },
            "Gate": {
                "Floor": "Gain",
                "Attenuation": "Gain"
            },
            "Glue Compressor": {
                "Clip": "PeakClipIn"
            },
            "Multiband Dynamics": {
                "Amount": "GlobalAmount",
                "Time": "GlobalTime",
                "Output": "OutputGain"
            },
            "Pedal": {
                "Type": "Type",
                "Gain": "Gain",
                "Bass": "Bass",
                "Mid": "Mid",
                "Treble": "Treble"
            },
            "Shifter": {
                "Pitch": "PitchShift_ShiftSemitones",
                "Fine": "PitchShift_Detune",
                "Formant": "PitchShift_FormantShift",
                "Window": "PitchShift_WindowSize",
                "Delay": "Delay_Time"
            },
            "Saturator": {
                "Drive": "Drive",
                "Base": "Base",
                "Freq": "Frequency",
                "Width": "Width",
                "Depth": "Depth",
                "Output": "Output"
            },
            "Vocoder": {
                "Formant": "FormantShift",
                "Bands": "Bands",
                "Range": "Range",
                "Depth": "Depth",
                "Release": "Release"
            }
        }

    def _load_database(self) -> Dict:
        """Load device database from split JSON files (V52)"""
        devices_map = {"devices": {"audio_effects": {}, "instruments": {}}}
        
        try:
            # Priority: Split Files
            if os.path.exists(self.devices_dir):
                count = 0
                for filename in os.listdir(self.devices_dir):
                    if filename.endswith(".json"):
                        path = os.path.join(self.devices_dir, filename)
                        try:
                            with open(path, 'r', encoding='utf-8') as f:
                                device_data = json.load(f)
                                # Use filename as key (sanitized)
                                key_name = os.path.splitext(filename)[0]
                                devices_map["devices"]["audio_effects"][key_name] = device_data
                                count += 1
                        except Exception as e:
                            print(f"Failed to load {filename}: {e}")
                
                if count > 0:
                    print(f"V52: Loaded {count} devices from split modules.")
                    return devices_map
                    
        except Exception as e:
            print(f"Warning: Could not load device database: {e}")
            
        return devices_map

    def _load_cloned_dna(self) -> Dict:
        """Load high-precision DNA from cloned_devices_dna.json"""
        try:
            if os.path.exists(self.cloned_dna_path):
                with open(self.cloned_dna_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cloned_devices_dna.json: {e}")
        return {}

    def _load_extracted(self) -> Dict:
        """Load extracted parameters from JSON"""
        try:
            if os.path.exists(self.extracted_path):
                with open(self.extracted_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load extracted parameters: {e}")
        return {}

    def get_device(self, name: str) -> Optional[Dict]:
        """Get device configuration by name, merging with extracted params"""
        audio_effects = self.devices.get("devices", {}).get("audio_effects", {})
        
        # Resolve canonical name using aliases first (case-insensitive)
        canon = name
        search_name = name.lower().strip()
        
        if search_name in self.aliases:
            canon = self.aliases[search_name]
        else:
            # Check if it's a direct match (case-insensitive)
            found = False
            for k in audio_effects.keys():
                if k.lower() == search_name:
                    canon = k
                    found = True
                    break
            
        device = audio_effects.get(canon)
        if not device:
            # Try to build a basic device from extracted params if it exists there
            actual_key = None
            for k in self.extracted_params.keys():
                if k.lower() == search_name:
                    actual_key = k
                    break
            
            if actual_key:
                # V24: Crucial fix - Don't create an empty skeleton. 
                # Populate with extracted parameter names so adg_builder can create the XML nodes.
                params_list = []
                if actual_key in self.extracted_params:
                    for p_name in self.extracted_params[actual_key]:
                        params_list.append({
                            "name": p_name,
                            "default": 0.5,
                            "min": 0.0,
                            "max": 1.0
                        })
                
                device = {
                    "xml_tag": actual_key,
                    "class_name": actual_key,
                    "type": "audio_effect",
                    "parameters": params_list
                }
                canon = actual_key
            else:
                return None

        # Merge in extracted parameters that aren't already defined
        # SMART MERGE: Re-enabled to support devices missing from devices.json (GrainDelay, Echo)
        # BUT with strict filtering to prevent 'Ghost Parameter' crashes.
        # V44 SURGICAL INTELLIGENCE: Inject Virtual Parameters and Aliases
        xml_tag = device.get("xml_tag", canon)
        
        # 1. Virtual Parameter Injection (Sidechain / Advanced Controls)
        VIRTUAL_P = {
            "AutoFilter2": [
                {"name": "Sidechain_Gain", "default": 1.0, "min": 0.0, "max": 10.0},
                {"name": "Sidechain_Mix", "default": 1.0, "min": 0.0, "max": 1.0}
            ],
            "Compressor2": [
                {"name": "Sidechain_Gain", "default": 1.0, "min": 0.0, "max": 10.0},
                {"name": "Sidechain_Mix", "default": 1.0, "min": 0.0, "max": 1.0}
            ],
            "Gate": [
                {"name": "Sidechain_Gain", "default": 1.0, "min": 0.0, "max": 10.0},
                {"name": "Sidechain_Mix", "default": 1.0, "min": 0.0, "max": 1.0}
            ],
            "BeatRepeat": [
                {"name": "Variation", "default": 0.0, "min": 0.0, "max": 10.0},
                {"name": "Mix_Mode", "default": 0.0, "min": 0.0, "max": 2.0}
            ]
        }
        
        if xml_tag in VIRTUAL_P:
            existing_names = {p["name"] for p in device.get("parameters", [])}
            for p in VIRTUAL_P[xml_tag]:
                if p["name"] not in existing_names:
                    device["parameters"].append(p)

        # 2. Smart Merge with Extracted Params
        if xml_tag in self.extracted_params:
            # Re-read existing names after virtual injection
            existing_names = {p["name"] for p in device.get("parameters", [])}
            
            BLACKLIST = {"LegacyGain", "BranchSelectorRange", "WarpWait", "LaunchWait"}
            for p_name in self.extracted_params[xml_tag]:
                if p_name in existing_names or p_name in BLACKLIST: continue
                if "." in p_name and p_name.split(".")[-1].isdigit(): continue 
                
                device["parameters"].append({
                    "name": p_name,
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0
                })
        
        return device
    
    def get_all_devices(self) -> Dict:
        """Get all available devices"""
        return self.devices.get("devices", {}).get("audio_effects", {})
    
    def device_count(self) -> int:
        """Get total number of devices"""
        return len(self.get_all_devices())
    
    def get_macro_suggestions(self, device_name: str) -> List[Dict]:
        """Get suggested macro mappings for a device"""
        device = self.get_device(device_name)
        if not device:
            return []
        
        suggestions = device.get("macro_suggestions", [])
        
        # If no suggestions, use first few parameters
        if not suggestions and device.get("parameters"):
            params = device["parameters"][:3]  # First 3 params
            suggestions = []
            for i, param in enumerate(params):
                suggestions.append({
                    "param_index": i,
                    "param_name": param["name"],
                    "min": param.get("min", 0.0),
                    "max": param.get("max", 1.0)
                })
        
        return suggestions
    
    def resolve_alias(self, name: str) -> str:
        """Resolve device alias to canonical name"""
        search_name = name.lower().strip()
        
        # 1. Direct Alias
        if search_name in self.aliases:
            return self.aliases[search_name]
            
        # 2. Direct casing match in audio_effects
        audio_effects = self.devices.get("devices", {}).get("audio_effects", {})
        for k in audio_effects.keys():
            if k.lower() == search_name:
                return k
                
        return name

    def get_parameter_aliases(self) -> Dict[str, Dict[str, str]]:
        """Get all parameter aliases for NLP prompt injection"""
        return self.parameter_aliases
