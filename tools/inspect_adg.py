import gzip
import xml.etree.ElementTree as ET
import os

def analyze_adg_proof(filepath):
    print(f"🍰 Counter-Proof Deep Analysis for: {os.path.basename(filepath)}")
    
    if not os.path.exists(filepath):
        print(f"❌ Error: File not found at {filepath}")
        return

    try:
        with gzip.open(filepath, 'rb') as f:
            content = f.read()
            root = ET.fromstring(content)
            
            # 1. Macro Labels (Found in AudioEffectGroupDevice)
            rack = root.find(".//AudioEffectGroupDevice")
            if rack is not None:
                print("\n🎛️ Macro Labels:")
                for i in range(16):
                    dn = rack.find(f"MacroDisplayNames.{i}")
                    if dn is not None and dn.get("Value"):
                        print(f"  Macro {i+1}: {dn.get('Value')}")

            # 2. Extract ALL devices regardless of nesting
            print("\n📊 Detailed Device Analysis:")
            
            # These are the tags for devices we expect
            target_tags = ["AutoFilter2", "Echo", "Roar", "GlueCompressor", "Utility", "Saturator"]
            
            for tag in target_tags:
                instances = root.findall(f".//{tag}")
                if instances:
                    print(f"\n✅ Found {len(instances)} instances of <{tag}>:")
                    for i, dev in enumerate(instances):
                        dev_id = dev.get("Id")
                        
                        surgical = ""
                        if tag == "AutoFilter2":
                            # Check Filter Type (HPF=1, LPF=0)
                            # Parameters are often direct children or in a 'Parameter' folder
                            # We'll look for anything matching 'Filter_Type' or similar
                            # In my builder, it's <Filter_Type><Manual Value="1.0" ...
                            ft_node = dev.find(".//Filter_Type/Manual")
                            ft_val = ft_node.get("Value") if ft_node is not None else "N/A"
                            surgical += f" [Filter_Type: {ft_val}]"
                            
                        # Check Mappings
                        mappings = []
                        for m in dev.findall(".//MacroControlConnector"):
                            source = m.find("SourceEnum")
                            if source is not None:
                                macro_idx = int(source.get("Value")) + 1
                                mappings.append(f"M{macro_idx}")
                        
                        print(f"  [{i+1}] Id: {dev_id}{surgical} | Mappings: {list(set(mappings))}")

    except Exception as e:
        import traceback
        print(f"❌ Critical Error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    path = "backend/generated/LIVE_MASTER_DJ-FX_PERFECT_10.adg"
    analyze_adg_proof(path)
