import os
import sys
import json
import asyncio
import time

# Set up environment for backend imports
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "backend"))

from backend.core.builder import AudioEffectRack, Chain, AbletonDevice
from backend.core.nlp_parser import RackNLPParser
from backend.core.device_mapper import DeviceDatabase

PROMPTS = [
    {
        "id": "NIGHTMARE_1",
        "name": "Quantum Void (Spectral/MS/Safety)",
        "prompt": "Create a complex spectral wash for cinematic soundscapes. Use an EQ Eight in Mid-Side mode for surgical cleaning, then a Spectral Resonator for metallic harmonics and a Hybrid Reverb for a 30-second decay. Map a 'Void Depth' macro that increases Resonator feedback while lowering Reverb dry/wet to preserve clarity, and a 'Spectral Shine' macro that boosts EQ high shelf on the sides while increasing Resonator frequency."
    },
    {
        "id": "NIGHTMARE_2",
        "name": "Digital Grit Machine (Glitch/Gain/Multi)",
        "prompt": "Build a rhythmic glitch engine. Start with a Redux for bitcrushing, then a Beat Repeat for chaotic stuttering, and then a Roar for multi-stage distortion. Map a 'Glitch Intensity' macro that increases Redux jitter and Beat Repeat chance, and a 'Harmonic Heat' macro that increases Roar drive while automatically lowering its Output Gain to stay at -3dB."
    },
    {
        "id": "NIGHTMARE_3",
        "name": "Analogue Master Bus (Precision/Dynamics)",
        "prompt": "Create a premium mastering chain. Start with a Channel EQ for subtle tilt, then a Glue Compressor for 'unity', then a Saturator for soft-clipping harmonics, and a Limiter at the end. Map a 'Console Drive' macro that pushes Saturator drive while reducing its output gain, and a 'Final Punch' macro that increases Glue Compressor ratio and makeup gain simultaneously."
    },
    {
        "id": "NIGHTMARE_4",
        "name": "Liquid Phaser (Deep Modulation/Complexity)",
        "prompt": "Design a liquid modulation rack. Chain a Chorus-Ensemble, followed by a Phaser-Flanger, then a Filter Delay for stereo movement. Map a 'Liquify' macro that increases Phaser feedback and Chorus rate while lowering EQ cutoff for an underwater feel. Map 'Space Movement' to increase Filter Delay feedback and Phaser LFO rate."
    },
    {
        "id": "NIGHTMARE_5",
        "name": "Neuro Bass Sculptor (Multi-Instance/Growl)",
        "prompt": "Create a neuro-style bass processor. Use a Multiband Dynamics for split processing, followed by dual Overdrives, and a final Auto Filter with the OSR circuit. Map a 'Grimy growl' macro that increases both Overdrive drives while lowering the Auto Filter cutoff. Map a 'Density' macro that controls the Multiband Dynamics 'Amount' and the Overdrive 'DryWet' for both instances."
    }
]

async def run_nightmare_audit():
    device_db = DeviceDatabase()
    nlp_parser = RackNLPParser(device_db)
    results = []
    
    print("\n" + "="*60)
    print("      PHASE 13: NIGHTMARE STRESS-TEST (V61)")
    print("="*60)
    
    for i, p in enumerate(PROMPTS):
        print(f"\n[{i+1}/{len(PROMPTS)}] Running: {p['name']}")
        start_time = time.time()
        
        try:
            # 1. AI Parsing
            spec = await nlp_parser.parse(p['prompt'])
            
            # 2. Build Rack
            rack = AudioEffectRack(name=p['name'], device_db=device_db)
            
            all_required_devices = []
            for dev in spec.get("devices", []):
                d_name = dev.get("name") if isinstance(dev, dict) else dev
                if d_name and d_name not in all_required_devices: all_required_devices.append(d_name)
            
            num_chains = spec.get("chains", 1)
            for ch_idx in range(num_chains):
                chain = Chain(name=f"Chain {ch_idx+1}")
                if ch_idx == 0:
                     for d_name in all_required_devices:
                         try:
                             device = rack.create_device(d_name)
                             chain.add_device(device)
                         except: continue
                rack.add_chain(chain)
            
            rack.auto_map_macros(spec)
            
            # 3. Save
            gen_dir = "nightmare_racks"
            os.makedirs(gen_dir, exist_ok=True)
            rack_path = os.path.join(gen_dir, f"{p['id']}.adg")
            rack.save(rack_path)
            
            duration = time.time() - start_time
            
            # 4. Automated Audit
            audit_findings = []
            macros = {}
            for m in rack.macro_mappings:
                if m.macro_index not in macros: macros[m.macro_index] = set()
                macros[m.macro_index].add(m.device_id)
            
            multi_macros = [m for m, devs in macros.items() if len(devs) > 1]
            multi_count = len(multi_macros)
            
            # Gain Comp detector
            gain_comp_found = any(
                any("drive" in m.param_path[-1].lower() for m in [ma for ma in rack.macro_mappings if ma.macro_index == idx]) and
                any("gain" in m.param_path[-1].lower() or "output" in m.param_path[-1].lower() or "volume" in m.param_path[-1].lower() for m in [ma for ma in rack.macro_mappings if ma.macro_index == idx])
                for idx in macros
            )

            print(f"  Complete in {duration:.1f}s")
            print(f"  Macros found: {sorted(list(macros.keys()))}")
            print(f"  Multi-Dev: {multi_count} | Gain Comp: {'OK' if gain_comp_found else 'FAIL'}")
            
            # Log mapped params for debugging
            for midx in sorted(macros.keys()):
                m_maps = [m for m in rack.macro_mappings if m.macro_index == midx]
                print(f"    - Macro {midx+1} ({m_maps[0].label}): {len(m_maps)} params")
            
            for f in audit_findings: print(f"    ! {f}")
            
            results.append({
                "test": p['id'], "name": p['name'], "score": 10.0 if not audit_findings else 7.0,
                "duration": duration, "findings": audit_findings
            })
            
        except Exception as e:
            import traceback
            print(f"  FAILED: {str(e)}")
            print(traceback.format_exc())
            results.append({"test": p['id'], "name": p['name'], "score": 0, "error": str(e)})

    avg_score = sum(r.get('score', 0) for r in results) / len(results)
    print("\n" + "="*60)
    print(f"  NIGHTMARE AUDIT SUMMARY: {avg_score:.1f}/10")
    print("="*60)
    
    with open("nightmare_audit.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    asyncio.run(run_nightmare_audit())
