"""
MULTI-DEVICE MACRO STRESS TEST
Specialized audit to troubleshoot the 'multi_device' mapping score.
"""
import sys, os, json, asyncio, re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from core.builder import AudioEffectRack, Chain, AbletonDevice
from core.nlp_parser import RackNLPParser
from core.device_mapper import DeviceDatabase

device_db = DeviceDatabase()
nlp_parser = RackNLPParser(device_db)

PROMPTS = [
    {
        "prompt": "Create a 'Macro-Destruction' knob that simultaneously increases Saturator Drive, reduces EQ Eight Low Cut frequency, and increases Redux Bit-depth.",
        "test_name": "Triple-Device Destruction",
        "expect_devices": ["saturator", "eq eight", "redux"],
    },
    {
        "prompt": "A single 'Space Morph' macro that increases Reverb Decay while simultaneously closing an Auto Filter frequency and reducing its Resonance.",
        "test_name": "Morphing Space",
        "expect_devices": ["reverb", "auto filter"],
    },
    {
        "prompt": "High-end 'Air Presence' macro: increases EQ Eight High Shelf gain while simultaneously adding gentle Glue Compression makeup gain.",
        "test_name": "Air & Compression",
        "expect_devices": ["eq eight", "glue compressor"],
    },
    {
        "prompt": "One 'Sub Dub' macro that increases Compressor Threshold (lowering volume) while boosting the drive on a Pedal and cutting highs on an Auto Filter.",
        "test_name": "Complex Tone Shift",
        "expect_devices": ["compressor", "pedal", "auto filter"],
    },
    {
        "prompt": "A 'Glitch Weaver' macro mapping that increases Beat Repeat Chance while simultaneously increasing Shifter Pitch and reducing the Auto Pan amount.",
        "test_name": "Hybrid Performance Macro",
        "expect_devices": ["beat repeat", "shifter", "auto pan"],
    },
]

class MacroAudit:
    def __init__(self, idx, info):
        self.idx = idx
        self.test_name = info["test_name"]
        self.prompt = info["prompt"]
        self.raw_mappings = []
        self.multi_device_found = False
        self.error = None

    def analyze(self, rack):
        macro_map = {}
        for mapping in rack.macro_mappings:
            m = mapping.macro_index
            if m not in macro_map: macro_map[m] = []
            
            # Resolve device name
            dev_name = f"ID:{mapping.device_id}"
            for chain in rack.chains:
                for dev in chain.devices:
                    if str(dev.device_id) == str(mapping.device_id):
                        dev_name = dev.name
                        break
            
            macro_map[m].append(dev_name)
            param_name = mapping.param_path[-1] if isinstance(mapping.param_path, list) else mapping.param_path
            self.raw_mappings.append(f"M{m+1} -> {dev_name} ({param_name})")

        for m, devices in macro_map.items():
            # SUCCESS IF DIFFERENT DEVICE NAMES (e.g. Saturator, EQ Eight)
            # OR DIFFERENT DEVICE IDS (even if same name like 'Utility', 'Utility')
            if len(set(devices)) > 1 or len(devices) > 1:
                # Actually, same name but different IDs is common for 'Utility'
                # Let's count IDs instead
                ids = []
                for mapping in rack.macro_mappings:
                    if mapping.macro_index == m:
                        ids.append(mapping.device_id)
                if len(set(ids)) > 1:
                    self.multi_device_found = True
                    break

async def run_test(idx, info):
    audit = MacroAudit(idx+1, info)
    print(f"\n[{idx+1}/5] {info['test_name']}")
    try:
        spec = await nlp_parser.parse(info["prompt"])
        rack = AudioEffectRack(name=spec.get("creative_name", "Test"), device_db=device_db)
        chain = Chain(name="Main")
        for d in spec.get("devices", []):
            name = d.get("name") if isinstance(d, dict) else d
            try: chain.add_device(rack.create_device(name))
            except: pass
        rack.add_chain(chain)
        rack.macro_count = 8
        rack.auto_map_macros(spec)
        
        audit.analyze(rack)
        status = "✅ PASS (Multi-Device Found)" if audit.multi_device_found else "❌ FAIL (Only Single-Device per Macro)"
        print(f"  {status}")
        for m in audit.raw_mappings: print(f"    - {m}")
        
    except Exception as e:
        print(f"  🔥 ERROR: {e}")
        audit.error = str(e)
    return audit

async def main():
    results = []
    for i, info in enumerate(PROMPTS):
        results.append(await run_test(i, info))
        await asyncio.sleep(1)
    
    success_count = sum(1 for r in results if r.multi_device_found)
    print(f"\n{'='*40}")
    print(f"  MULTI-DEVICE MACRO SCORE: {success_count}/5")
    print(f"{'='*40}")

if __name__ == "__main__":
    asyncio.run(main())
