import json
import os
import sys

DEVICES_DIR = r"backend\data\devices"
MANUAL_PATH = r"backend\data\knowledge\MANUAL_EXTRACT.txt"

def audit_device(device_name):
    # Load Device JSON
    json_path = os.path.join(DEVICES_DIR, f"{device_name}.json")
    if not os.path.exists(json_path):
        print(f"Error: {device_name}.json not found in {DEVICES_DIR}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        device_data = json.load(f)

    print(f"\n{'='*40}")
    print(f" AUDIT REPORT: {device_name}")
    print(f"{'='*40}")
    
    print("\n[INTERNAL PARAMETERS]")
    for p in device_data.get("parameters", []):
        print(f" - {p['name']:<30} (Min: {p.get('min', 'N/A')}, Max: {p.get('max', 'N/A')})")

    # Load Manual Extract
    manual_extract = ""
    if os.path.exists(MANUAL_PATH):
        with open(MANUAL_PATH, 'r', encoding='utf-8') as f:
            manual_extract = f.read()

    print(f"\n[MANUAL CONTEXT] (Searching for '{device_name}' in Manual...)")
    
    # Simple context search: Find paragraphs containing device name
    # This is rough, but helpful.
    excerpt_lines = []
    lines = manual_extract.split('\n')
    found_section = False
    buffer = []
    
    for line in lines:
        if device_name.lower() in line.lower() and len(line) < 100: # Header-ish detection
             found_section = True
             buffer = [f"\n--- POSSIBLE HEADER MATCH: {line.strip()} ---"]
        
        if found_section:
            buffer.append(line)
            if len(buffer) > 30: # Snapshot length
                if any(device_name.lower() in l.lower() for l in buffer):
                     excerpt_lines.extend(buffer)
                found_section = False
                buffer = []
    
    if excerpt_lines:
        print("\n".join(excerpt_lines[:20])) # Print first match snippet
        print("... (Run manual search for full context)")
    else:
        print("No specific section header found easily.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/audit_device.py [DeviceName]")
    else:
        audit_device(sys.argv[1])
