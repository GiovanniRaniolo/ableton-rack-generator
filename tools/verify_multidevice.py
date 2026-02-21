import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from core.builder import AudioEffectRack, Chain, AbletonDevice
from core.device_mapper import DeviceDatabase

def test_multidevice_mapping():
    print("🚀 Starting Multi-Device Instance Verification (V38.0)...")
    device_db = DeviceDatabase()
    
    # Simulate a dual-filter request from NLP
    nlp_resp = {
        "creative_name": "Dual Filter Test",
        "devices": ["Auto Filter", "Auto Filter"],
        "surgical_devices": [
            {
                "name": "Auto Filter",
                "parameters": {"Filter_Type": 1.0} # OSR for high-pass
            },
            {
                "name": "Auto Filter",
                "parameters": {"Filter_Type": 0.0} # Classic for low-pass
            }
        ],
        "macro_details": [
            { "macro": 1, "name": "HPF Sweep", "target_device": "Auto Filter", "target_parameter": "Filter_Frequency", "min": 200.0, "max": 8000.0 },
            { "macro": 2, "name": "LPF Sweep", "target_device": "Auto Filter", "target_parameter": "Filter_Frequency", "min": 8000.0, "max": 200.0 }
        ]
    }
    
    rack = AudioEffectRack(name="Dual Filter Test", device_db=device_db)
    chain = Chain(name="Main Chain")
    
    # Create devices with unique IDs (as main.py now does)
    filter1 = rack.create_device("Auto Filter")
    filter2 = rack.create_device("Auto Filter")
    
    chain.add_device(filter1)
    chain.add_device(filter2)
    rack.add_chain(chain)
    
    print(f"DEBUG: Filter 1 ID: {filter1.device_id}")
    print(f"DEBUG: Filter 2 ID: {filter2.device_id}")
    
    # Trigger mapping
    rack.auto_map_macros(nlp_resp)
    
    # VERIFICATION 1: Surgical Parameters
    print("\n--- VERIFICATION 1: Surgical Parameters ---")
    if filter1.parameter_overrides.get("Filter_Type") == 1.0:
        print("✅ Filter 1 configured as OSR")
    else:
        print(f"❌ Filter 1 configuration FAILED: {filter1.parameter_overrides.get('Filter_Type')}")

    if filter2.parameter_overrides.get("Filter_Type") == 0.0:
        print("✅ Filter 2 configured as Classic")
    else:
        print(f"❌ Filter 2 configuration FAILED: {filter2.parameter_overrides.get('Filter_Type')}")

    # VERIFICATION 2: Independent Mapping
    print("\n--- VERIFICATION 2: Independent Mapping ---")
    # Check if Macro 1 is on Filter 1 and Macro 2 is on Filter 2
    f1_mappings = [m.macro_index for m in filter1.mappings.values()]
    f2_mappings = [m.macro_index for m in filter2.mappings.values()]
    
    print(f"Filter 1 Macros: {f1_mappings}")
    print(f"Filter 2 Macros: {f2_mappings}")
    
    if 0 in f1_mappings and 1 in f2_mappings:
        print("✅ SUCCESS: Independent mapping confirmed!")
    else:
        print("❌ FAILURE: Mappings are cross-pollinated or missing.")

    # VERIFICATION 3: XML Inspection
    print("\n--- VERIFICATION 3: XML Inspection ---")
    xml_data = rack.to_xml()
    xml_str = xml_data.decode('utf-8') if isinstance(xml_data, bytes) else xml_data
    
    # print(xml_str[:1000]) # Print first 1000 chars
    
    # Check if there are two different Auto Filter IDs in the XML
    if 'Id="1"' in xml_str and 'Id="2"' in xml_str:
        print("✅ XML contains unique device IDs")
    else:
        print("❌ XML missing unique device IDs")
        # Let's find what IDs are actually there
        import re
        ids = re.findall(r'Id="(\d+)"', xml_str)
        print(f"Found IDs in XML: {ids}")

if __name__ == "__main__":
    test_multidevice_mapping()
