import sys
import os
import glob

# Add parent dir to path to reuse audit_device logic if needed,
# But easier to just subprocess it or reimplement simple loop.

DEVICES_DIR = r"backend\data\devices"
MANUAL_PATH = r"backend\data\knowledge\MANUAL_EXTRACT.txt"

def get_devices_in_batch(batch_char_start, batch_char_end):
    all_files = sorted(glob.glob(os.path.join(DEVICES_DIR, "*.json")))
    batch = []
    for f in all_files:
        name = os.path.basename(f).replace(".json", "")
        first_char = name[0].upper()
        if batch_char_start <= first_char <= batch_char_end:
            batch.append(name)
    return batch

def batch_audit(start_char, end_char):
    devices = get_devices_in_batch(start_char.upper(), end_char.upper())
    output_file = f"batch_audit_{start_char}_{end_char}.txt"
    
    print(f"--- BATCH AUDIT: {start_char}-{end_char} ---")
    print(f"Found {len(devices)} devices: {devices}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"BATCH AUDIT REPORT: {start_char}-{end_char}\n")
        f.write("="*50 + "\n\n")

    for device in devices:
        print(f"Running audit for: {device}")
        # Append to file
        os.system(f"python tools/audit_device.py \"{device}\" >> {output_file}")
        
        # Add separator
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "-"*50 + "\n")

    print(f"Audit complete. Report saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tools/batch_audit.py [StartChar] [EndChar]")
        print("Example: python tools/batch_audit.py A C")
    else:
        batch_audit(sys.argv[1], sys.argv[2])
