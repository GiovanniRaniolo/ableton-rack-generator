
import gzip
import xml.etree.ElementTree as ET
import sys
import json

def clone_devices(filepath):
    print(f"Cloning DNA from {filepath}...")
    try:
        with gzip.open(filepath, 'rb') as f:
            xml_content = f.read()
            
        root = ET.fromstring(xml_content)
        all_devices = root.findall(".//Device")
        
        cloned_db = {}
        
        ignored_tags = ["AudioEffectGroupDevice", "InstrumentGroupDevice", "AudioBranchMixerDevice", "ChainMixer", 
                       "PreHearAudioBranchMixerDevice", "MxDeviceAudioEffect", "ProxyAudioEffectDevice"]

        for dev_container in all_devices:
            for device_elem in dev_container:
                tag = device_elem.tag
                if tag in ignored_tags: continue
                
                # Check for UserName to map to "English Name"
                # If UserName is empty, we use the Tag as the Name for now.
                # Or we can try to match with existing DB.
                
                user_name_elem = device_elem.find("UserName")
                user_name = user_name_elem.get("Value") if user_name_elem is not None else tag
                if not user_name: user_name = tag
                
                # Cleanup user name (remove specific instance names if possible, but hard to know)
                # For now, key by TAG is safer for the DB "xml_tag" field.
                
                print(f"Scanning {tag}...")
                
                parameters = []
                
                # Find all "Manual" values which represent parameters
                # Structure: Device -> [ParamName] -> Manual Value="..."
                
                for param_elem in device_elem:
                    # Skip metadata tags
                    if param_elem.tag in ["LomId", "LomIdView", "IsExpanded", "Booleanness", "UserName", "Annotation", "SourceContext", "Branches", "DevicePresets"]:
                        continue
                        
                    # Check if it looks like a parameter (has Manual or Value)
                    manual = param_elem.find("Manual")
                    if manual is not None:
                        val_str = manual.get("Value", "0").lower()
                        if val_str == "true":
                            val = 1.0
                        elif val_str == "false":
                            val = 0.0
                        else:
                            try:
                                val = float(val_str)
                            except ValueError:
                                # Fallback for weird values
                                val = 0.0
                        
                        # Try to find min/max if present (MidiControllerRange)
                        min_val = 0.0
                        max_val = 1.0 # default bool
                        
                        rng = param_elem.find("MidiControllerRange")
                        if rng is not None:
                            min_val = float(rng.find("Min").get("Value", 0))
                            max_val = float(rng.find("Max").get("Value", 1))
                        else:
                            # Maybe it's a bool with OnOffThresholds
                            thresh = param_elem.find("MidiCCOnOffThresholds")
                            if thresh is not None:
                                max_val = 1.0
                        
                        parameters.append({
                            "name": param_elem.tag,
                            "default": val,
                            "min": min_val,
                            "max": max_val
                        })
                
                # Store in DB format
                if tag not in cloned_db:
                    cloned_db[tag] = {
                        "xml_tag": tag,
                        "class_name": tag, # Assume class name matches tag for modern devices
                        "type": "audio_effect",
                        "parameters": parameters,
                        "macro_suggestions": [] # We can't infer this easily, keep empty
                    }

        # Save result
        with open("backend/data/cloned_devices_dna.json", "w") as f:
            json.dump(cloned_db, f, indent=2)
            
        print(f"Cloned {len(cloned_db)} devices to backend/data/cloned_devices_dna.json")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        clone_devices(sys.argv[1])
    else:
        print("Usage: python clone_devices.py <file.adg>")
