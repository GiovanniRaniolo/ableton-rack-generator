
import gzip
import xml.etree.ElementTree as ET
import json
import os

FILES = [
    r"C:\Users\ginoj\Documents\Ableton\User Library\Presets\Audio Effects\Audio Effect Rack\analyze-fino-a-limiter.adg",
    r"C:\Users\ginoj\Documents\Ableton\User Library\Presets\Audio Effects\Audio Effect Rack\analize-rest.adg"
]

OUTPUT_FILE = "backend/data/cloned_devices_dna.json"

def clone_all():
    master_db = {}
    
    for filepath in FILES:
        if not os.path.exists(filepath):
            print(f"[SKIP] File not found: {filepath}")
            continue
            
        print(f"Cloning from: {filepath}...")
        try:
            with gzip.open(filepath, 'rb') as f:
                xml_content = f.read()
            
            root = ET.fromstring(xml_content)
            all_devices = root.findall(".//Device")
            
            ignored_tags = ["AudioEffectGroupDevice", "InstrumentGroupDevice", "AudioBranchMixerDevice", "ChainMixer", 
                           "PreHearAudioBranchMixerDevice", "MxDeviceAudioEffect", "ProxyAudioEffectDevice"]
            
            count = 0
            for dev_container in all_devices:
                for device_elem in dev_container:
                    tag = device_elem.tag
                    if tag in ignored_tags: continue
                    
                    # Logic directly from clone_devices.py
                    print(f"  -> Found: {tag}")
                    
                    parameters = []
                    for param_elem in device_elem:
                        if param_elem.tag in ["LomId", "LomIdView", "IsExpanded", "Booleanness", "UserName", "Annotation", "SourceContext", "Branches", "DevicePresets"]:
                            continue
                        
                        manual = param_elem.find("Manual")
                        if manual is not None:
                            val_str = manual.get("Value", "0").lower()
                            val = 1.0 if val_str == "true" else (0.0 if val_str == "false" else 0.0)
                            try: val = float(val_str)
                            except: pass
                            
                            min_val = 0.0
                            max_val = 1.0
                            rng = param_elem.find("MidiControllerRange")
                            if rng is not None:
                                min_val = float(rng.find("Min").get("Value", 0))
                                max_val = float(rng.find("Max").get("Value", 1))
                            else:
                                if param_elem.find("MidiCCOnOffThresholds") is not None: max_val = 1.0

                            parameters.append({
                                "name": param_elem.tag,
                                "default": val,
                                "min": min_val,
                                "max": max_val
                            })
                    
                    if tag not in master_db:
                        master_db[tag] = {
                            "xml_tag": tag,
                            "class_name": tag,
                            "type": "audio_effect",
                            "parameters": parameters,
                            "macro_suggestions": []
                        }
                        count += 1
            
            print(f"  -> Extracted {count} unique devices from this file.")
            
        except Exception as e:
            print(f"ERROR reading {filepath}: {e}")

    # Save Master DB
    with open(OUTPUT_FILE, "w") as f:
        json.dump(master_db, f, indent=2)
    
    print(f"\nCOMPLETED. Total unique devices cloned: {len(master_db)}")

if __name__ == "__main__":
    clone_all()
