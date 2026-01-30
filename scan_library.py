
import os
import gzip
import xml.etree.ElementTree as ET
import json
import glob

LIBRARY_PATH = r"C:\Users\ginoj\Documents\Ableton\User Library\Presets\Audio Effects"
OUTPUT_FILE = "backend/data/detected_devices_map.json"

print(f"Scanning Library: {LIBRARY_PATH}")

device_map = {}

# List of known container tags to ignore (we want the FX inside)
IGNORE_TAGS = ["Ableton", "GroupDevicePreset", "DevicePresets", "Device", "PresetRef", "AbletonDefaultPresetRef", "FileRef"]

def scan_adg(filepath):
    try:
        with gzip.open(filepath, 'rb') as f:
            xml_content = f.read()
            
        # Parse XML
        root = ET.fromstring(xml_content)
        
        # Navigate to find the main device
        # Usually: GroupDevicePreset -> Device -> [THE_DEVICE]
        # Or: GroupDevicePreset -> BranchPresets -> ...
        
        # Strategy: Find first child of "Device" that is NOT "AudioEffectGroupDevice" (unless it's a Rack file)
        
        # Let's search recursively for ANY tag that looks like a Device
        # We assume the name of the folder usually matches the functionality
        
        # For simplicity, let's look for known specific tags or just dumping the first meaningful tag under <Device>
        
        # Path commonly: Ableton -> GroupDevicePreset -> Device -> [XYZ]
        
        device_container = root.find(".//Device")
        if device_container is not None:
             for child in device_container:
                 tag = child.tag
                 if tag not in ["AudioEffectGroupDevice", "InstrumentGroupDevice"]:
                     return tag
                 else:
                     # It's a Rack. Is it an "Audio Effect Rack" file?
                     # If the filename suggests "Audio Effect Rack", then valid.
                     # But we are scanning specific folders like "Auto Filter".
                     return tag
        
        return None

    except Exception as e:
        # print(f"Error reading {filepath}: {e}")
        return None

# Iterate subfolders
subfolders = [f.path for f in os.scandir(LIBRARY_PATH) if f.is_dir()]

print(f"Found {len(subfolders)} device categories.")

for folder in subfolders:
    folder_name = os.path.basename(folder)
    print(f"Scanning {folder_name}...", end="")
    
    # Find first ADG in this folder to use as reference
    adg_files = glob.glob(os.path.join(folder, "**/*.adg"), recursive=True)
    
    if not adg_files:
        print(" [NO FILES]")
        continue
        
    # check getting a few files to be sure
    detected_tags = []
    for f in adg_files[:3]:
        tag = scan_adg(f)
        if tag: detected_tags.append(tag)
        
    if detected_tags:
        # Majority vote
        best_tag = max(set(detected_tags), key=detected_tags.count)
        device_map[folder_name] = best_tag
        print(f" -> {best_tag}")
    else:
        print(" -> [UNKNOWN]")

print("\nSAVING MAP...")
with open(OUTPUT_FILE, 'w') as f:
    json.dump(device_map, f, indent=2)

print(f"Saved to {OUTPUT_FILE}")
