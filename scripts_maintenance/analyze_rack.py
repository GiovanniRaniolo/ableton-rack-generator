
import gzip
import xml.etree.ElementTree as ET
import sys
import json

def analyze_rack(filepath):
    print(f"Reading {filepath}...")
    try:
        with gzip.open(filepath, 'rb') as f:
            xml_content = f.read()
            
        root = ET.fromstring(xml_content)
        
        # Traverse recursively to find ALL devices
        devices_found = []
        
        # Helper to recursively search
        def recursive_search(elem, hierarchy=""):
            # Check if this element is a Device
            # Heuristic: It's inside a <Device> tag container?
            # Or assume standard tags
            
            tag = elem.tag
            
            # Common Ableton Device Tags (blacklist containers)
            CONTAINERS = ["Ableton", "GroupDevicePreset", "Device", "BranchPresets", "DevicePresets", "AudioEffectGroupDevice", "InstrumentGroupDevice", "AudioEffectBranch", "AudioBranchMixerDevice", "PreHearAudioBranchMixerDevice"]
            
            # Check if parent was <Device> 
            # (XML traversal in ElementTree doesn't give parent easily, so we check child of 'Device')
            
            pass 

        # Better approach: Find all children of <Device> tags
        # XPath: .//Device/*
        
        all_devices = root.findall(".//Device")
        unique_tags = {}
        
        for dev_container in all_devices:
            for child in dev_container:
                # The child tag is the Device Name (e.g. "AutoFilter", "Eq8")
                xml_tag = child.tag
                
                # Filter out pure containers if possible
                if xml_tag in ["AudioEffectGroupDevice", "InstrumentGroupDevice", "DrumGroupDevice", "MidiEffectGroupDevice"]:
                    continue # Skip nested racks
                    
                if xml_tag in ["AudioBranchMixerDevice", "PreHearAudioBranchMixerDevice", "ChainMixer"]:
                    continue # Skip mixers
                    
                # Store it
                # We don't know the "User Name" (e.g. "Auto Filter"), only the XML Tag ("AutoFilter")
                # But the user said "from A to L", so we can list them in order of appearance
                
                # Check if it has a User Name property? <UserName Value="..." />
                user_name = ""
                un_elem = child.find("UserName")
                if un_elem is not None:
                    user_name = un_elem.get("Value", "")
                    
                # To map back to "English Name", we might need to guess or use the class name
                # But knowing the XML Tag is the most important part.
                
                if xml_tag not in unique_tags:
                    unique_tags[xml_tag] = user_name
                    devices_found.append({"tag": xml_tag, "user_name": user_name})

        # Save to JSON
        with open("backend/data/analyzed_rack_devices.json", "w") as f:
            json.dump(devices_found, f, indent=2)
            
        print("FOUND DEVICES:")
        for d in devices_found:
            print(f"- {d['tag']} ({d['user_name']})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_rack(sys.argv[1])
    else:
        print("Usage: python analyze_rack.py <file.adg>")
