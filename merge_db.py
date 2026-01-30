
import json
import os

DB_PATH = "backend/data/devices.json"
DNA_PATH = "backend/data/cloned_devices_dna.json"

def merge_db():
    print("Merging DNA into Device Database...")
    
    with open(DB_PATH, "r") as f:
        db = json.load(f)
        
    with open(DNA_PATH, "r") as f:
        dna = json.load(f)
        
    count = 0
    
    # We need to map DNA keys (XmlTags) to DB keys (English Names)
    # This is tricky because DB uses "Auto Filter" but DNA uses "AutoFilter2".
    # Strategy: 
    # 1. Iterate through DB devices.
    # 2. If DB device has an "xml_tag" that matches a DNA key, UPDATE IT.
    # 3. If NO match, check if any DNA key looks similar? 
    #    Actually, we previously updated DB tags in `devices.json` to be "AutoFilter" (V1).
    #    Now we want to Update them to "AutoFilter2" AND update parameters.
    
    # Let's create a reverse lookup from DNA: Tag -> DNA_Entry
    
    # We iterate the DB.
    # For "Auto Filter":
    #   Old Tag: "AutoFilter" (or "AutoFilter2" if we reverted).
    #   We want to find the DNA entry that corresponds to this.
    #   DNA has "AutoFilter2".
    
    # Hardcoded Mapping for critical devices based on our findings
    MAPPING = {
        "Auto Filter": "AutoFilter2",
        "Compressor": "Compressor2",
        "Chorus-Ensemble": "Chorus2", # In DB it might be Chorus-Ensemble or Chorus
        "EQ Eight": "Eq8",
        # Add others as needed or rely on fuzzy match
    }
    
    # Also iterate DNA and see if we can Auto-Match by simple name containment
    
    for category in db["devices"]:
        for dev_name, dev_data in db["devices"][category].items():
            
            target_tag = None
            
            # 1. Check explicit mapping
            if dev_name in MAPPING:
                target_tag = MAPPING[dev_name]
            
            # 2. Check if current xml_tag is in DNA
            elif dev_data["xml_tag"] in dna:
                target_tag = dev_data["xml_tag"]
                
            # 3. Check if any DNA tag is close to the name
            # (Simple heuristic: DNA tag in device name without spaces?)
            
            if not target_tag:
                # Try to find corresponding DNA
                # e.g. dev_name="Auto Pan", dna has "AutoPan2"
                n = dev_name.replace(" ", "")
                for dna_tag in dna:
                    if dna_tag.startswith(n):
                         target_tag = dna_tag
                         break
            
            if target_tag and target_tag in dna:
                print(f"Updating {dev_name} using DNA [{target_tag}]")
                dna_entry = dna[target_tag]
                
                # Update critical fields
                dev_data["xml_tag"] = dna_entry["xml_tag"]
                dev_data["parameters"] = dna_entry["parameters"]
                # Keep existing class_name and type and macro_suggestions
                
                # Mark as processed in DNA so we know what's left
                dna[target_tag]["_processed"] = True
                count += 1
                
    # Phase 2: Add NEW devices from DNA that were not matched
    print("Phase 2: Adding new devices...")
    for dna_tag, dna_entry in dna.items():
        if dna_entry.get("_processed"): continue
        
        # Add to DB under audio_effects
        # Use Tag as Name
        new_name = dna_tag
        print(f"Adding NEW device: {new_name}")
        
        # Ensure minimal fields
        if "class_name" not in dna_entry: dna_entry["class_name"] = dna_tag
        if "type" not in dna_entry: dna_entry["type"] = "audio_effect"
        if "macro_suggestions" not in dna_entry: dna_entry["macro_suggestions"] = []
        
        db["devices"]["audio_effects"][new_name] = dna_entry
        count += 1
    
    # Save
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)
        
    print(f"Merged {count} devices (Updates + New).")

if __name__ == "__main__":
    merge_db()
