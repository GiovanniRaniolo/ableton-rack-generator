
import json

DB_PATH = "backend/data/devices.json"

def sanitize():
    with open(DB_PATH, "r") as f:
        db = json.load(f)
    
    deleted_count = 0
    
    # 1. Sanitize EQ Eight (No Feedback)
    # Check both keys just in case
    for key in ["EQ Eight", "Eq8"]:
        if key in db["devices"]["audio_effects"]:
            dev = db["devices"]["audio_effects"][key]
            suggestions = dev.get("macro_suggestions", [])
            
            # Filter out "Feedback"
            new_suggestions = [s for s in suggestions if s["param_name"] != "Feedback"]
            
            if len(new_suggestions) < len(suggestions):
                diff = len(suggestions) - len(new_suggestions)
                print(f"[{key}] Removed {diff} phantom 'Feedback' suggestions.")
                dev["macro_suggestions"] = new_suggestions
                deleted_count += diff

    # 2. Sanitize Roar (No PreDrive if Stage1_Shaper_Amount exists)
    if "Roar" in db["devices"]["audio_effects"]:
        dev = db["devices"]["audio_effects"]["Roar"]
        suggestions = dev.get("macro_suggestions", [])
        
        # Check if we have old names
        new_suggestions = []
        for s in suggestions:
            if s["param_name"] == "PreDrive":
                print("[Roar] Removing obsolete 'PreDrive' suggestion.")
                deleted_count += 1
                continue # Skip it
            if s["param_name"] == "Coarse":
                print("[Roar] Removing obsolete 'Coarse' suggestion.")
                deleted_count += 1
                continue
            new_suggestions.append(s)
            
        dev["macro_suggestions"] = new_suggestions

    # 3. NUKE EMPTY SHELLS & UNSTABLE DEVICES
    # "Forbidden Icon" is caused by devices that are just placeholders (generic tags, no params).
    # We also nuked Echo/Corpus as they are complex and failed testing.
    
    explicit_ban_list = [] # All devices verified via 'analyze-rest.adg'! 🚀
    
    current_keys = list(db["devices"]["audio_effects"].keys())
    for k in current_keys:
        dev = db["devices"]["audio_effects"][k]
        param_count = len(dev.get("parameters", []))
        
        # Condition 1: Explicit Ban
        if k in explicit_ban_list:
            print(f"[NUKE] Banned Device: {k}")
            del db["devices"]["audio_effects"][k]
            deleted_count += 1
            continue
            
        # Condition 2: Empty Shell (Placeholder)
        # Real devices have many params. Placeholders usually have 0-2 (On, DryWet).
        # We set threshold at 4 to be safe.
        if param_count < 4:
            print(f"[NUKE] Empty Shell: {k} ({param_count} params)")
            del db["devices"]["audio_effects"][k]
            deleted_count += 1

    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)
        
    print(f"Sanitization complete. Removed {deleted_count} bad entries.")

if __name__ == "__main__":
    sanitize()
