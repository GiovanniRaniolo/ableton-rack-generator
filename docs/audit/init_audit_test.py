import asyncio
import json
import time
import os
import traceback
import sys

# Internal imports
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from core.nlp_parser import RackNLPParser
from core.builder.rack import AudioEffectRack
from core.builder.chain import Chain
from core.device_mapper import DeviceDatabase

# Wrapper for legacy code in test
class AIParser:
    def __init__(self):
        self.db = DeviceDatabase()
        self.parser = RackNLPParser(self.db)
    async def parse(self, p):
        return await self.parser.parse(p)

PROMPTS = [
    {
        "id": "init_1",
        "name": "Lush Granular Shimmer",
        "prompt": "Create a lush shimmer rack for ambient textures using Spectral Resonator, Hybrid Reverb, and Shifter. Focus on granular clouds and crystalline tails. Ensure 8 macros for deep evolution."
    },
    {
        "id": "init_2",
        "name": "Industrial Multiband Distortion",
        "prompt": "A heavy industrial saturation engine using Roar and Multiband Dynamics. Focus on precise crossover control and staged clipping. Needs 8 macros for heat and movement."
    },
    {
        "id": "init_3",
        "name": "Lo-Fi VHS Nostalgia",
        "prompt": "Authentic lofi VHS degradation using Redux, Erosion, Vinyl Distortion, and a warm Delay. Focus on mechanical noise and fluttering age. 8 macros for 'wear and tear'."
    },
    {
        "id": "init_4",
        "name": "Psychoacoustic Wide Engine",
        "prompt": "A pro-grade stereo widening rack using Utility, Echo, and Spectral Time. Focus on Haas effect, phase-coherent width, and spectral dispersion. 8 macros for imaging."
    },
    {
        "id": "init_5",
        "name": "Neuro Bass Sculptor",
        "prompt": "Aggressive neuro bass shaper using Roar, Auto Filter (OSR mode), and sidechained compression. Focus on growl movement and sharp transients. 8 macros for bass warfare."
    }
]

async def run_initialization_audit():
    parser = AIParser()
    device_db = DeviceDatabase()
    results = []

    print("="*60)
    print("      PHASE 14: SURGICAL INITIALIZATION AUDIT (V68)")
    print("="*60)

    for i, p in enumerate(PROMPTS):
        print(f"\n[{i+1}/{len(PROMPTS)}] Auditing: {p['name']}")
        start_time = time.time()
        
        try:
            # 1. AI Parsing
            spec = await parser.parse(p['prompt'])
            
            # 2. Analyze Surgical Configuration
            surgical = spec.get("surgical_devices", [])
            print(f"  Surgical Devices found: {len(surgical)}")
            
            logic_score = 0
            findings = []
            
            # Heuristic Analysis of "Sound Designer Intent"
            for s_dev in surgical:
                name = s_dev.get("name", "")
                params = s_dev.get("parameters", {})
                print(f"    - {name}: {len(params)} custom initial params")
                
                # Check for "Musical Logic" in unmapped params
                if "Reverb" in name:
                    if any("Decay" in k for k in params): findings.append(f"[INTENT] Reverb Decay initialized to {params.get('Decay') or params.get('Algorithm_Decay')}")
                if "Roar" in name:
                    if any("Tone" in k for k in params): findings.append(f"[INTENT] Roar Tone initialized for frequency focus")
                if "Utility" in name:
                    if "StereoWidth" in params: findings.append(f"[INTENT] Utility width initialized")

            # 3. Macro Adherence
            macros = spec.get("macro_details", [])
            print(f"  Macros Designed: {len(set(m.get('macro') for m in macros))}")
            
            duration = time.time() - start_time
            print(f"  Complete in {duration:.1f}s")
            
            for f in findings:
                print(f"      {f}")

            results.append({
                "id": p["id"],
                "name": p["name"],
                "surgical_count": len(surgical),
                "macro_count": len(set(m.get('macro') for m in macros)),
                "findings": findings
            })

        except Exception as e:
            print(f"  FAILED: {str(e)}")
            traceback.print_exc()

    print("\n" + "="*60)
    print("  SURGICAL AUDIT COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_initialization_audit())
