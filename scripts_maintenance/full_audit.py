
import json

def audit_all():
    with open("backend/data/cloned_devices_dna.json", "r") as f:
        db = json.load(f)
        
    with open("device_audit_full.txt", "w") as out:
        out.write("FULL DEVICE PARAMETER AUDIT\n")
        out.write("===========================\n\n")
        
        for device_name in sorted(db.keys()):
            dev = db[device_name]
            params = [p['name'] for p in dev['parameters']]
            
            out.write(f"DEVICE: {device_name}\n")
            out.write(f"  Tag: {dev.get('xml_tag')}\n")
            out.write(f"  Params ({len(params)}): {', '.join(params)}\n")
            out.write("-" * 50 + "\n")
            
    print("Audit written to device_audit_full.txt")

if __name__ == "__main__":
    audit_all()
