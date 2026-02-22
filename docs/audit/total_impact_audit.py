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
from backend.core.device_mapper import DeviceDatabase

# Wrapper for legacy code in test
class AIParser:
    def __init__(self):
        self.db = DeviceDatabase()
        self.parser = RackNLPParser(self.db)
    async def parse(self, p):
        return await self.parser.parse(p)

PROMPTS = [
    {
        "id": "impact_1",
        "name": "Cinematic Spectral Purgatory",
        "prompt": "Create a cinematic spectral processing rack. It must use Spectral Resonator for frequency freezing, Spectral Time for granular delays, and Hybrid Reverb for a massive convolution space. I want 8 macros that allow me to transition from a clean signal to a 'ghostly purgatory' texture. Focus on high-end imaging and lack of phase muddiness."
    },
    {
        "id": "impact_2",
        "name": "Industrial Overkill Engine",
        "prompt": "An aggressive industrial distortion engine. Combine Roar (in multiband mode), Saturator (with soft clipping), and Multiband Dynamics for surgical OTT-style control. The rack must have 8 macros: 4 for distortion character (heat, grit, bias, stage) and 4 for dynamics/tone (punch, air, low-end focus, master polish). Must remain phase-coherent."
    },
    {
        "id": "impact_3",
        "name": "Lofi Analog Flutter",
        "prompt": "Create a lofi analog degradation rack. Use Echo for wow/flutter simulation, Vinyl Distortion for mechanical surface noise, and Auto Filter for warm 24dB vintage filtering. I want 8 macros: 'Age', 'Dust', 'Mechanical Flutter', 'Filtered Nostalgia', 'VHS Saturation', 'Output Air', 'Compactor', and 'Master Mix'. Must sound 'expensive' lofi."
    },
    {
        "id": "impact_4",
        "name": "Psychoacoustic Hyper-Width",
        "prompt": "A pro-grade psychoacoustic widening rack. Use Utility for Mid/Side balance, Echo (set to Haas mode), and Chorus-Ensemble for modern thickening. Then add EQ Eight for surgical side-only brightening. 8 macros for imaging: 'Stereo Basis', 'Haas Offset', 'Space thickening', 'Side Brightness', 'Phase Safety', 'Center Depth', 'Envelope Width', 'Final Imaging'."
    },
    {
        "id": "impact_5",
        "name": "Glitch Resampling Sculptor",
        "prompt": "A complex glitch/resampling sculptor. Use Beat Repeat for rhythmic stutters, Redux for digital bit-crushing, and Spectral Resonator for pitch-shifting stutters. Add a final Limiter for safety. 8 macros: 'Stutter Rate', 'Glitch Chance', 'Bit Grit', 'Pitch Warp', 'Spectral Chaos', 'Rhythmic Gate', 'Transient Clamp', 'Master Impact'."
    }
]

async def run_total_impact_evaluation():
    parser = AIParser()
    results = []

    print("="*70)
    print("      PHASE 15: TOTAL IMPACT EVALUATION (V70) - FINAL GATE")
    print("="*70)

    for i, p in enumerate(PROMPTS):
        print(f"\n[{i+1}/{len(PROMPTS)}] Evaluating: {p['name']}")
        start_time = time.time()
        
        try:
            # 1. AI Parsing & Specification Generation
            spec = await parser.parse(p['prompt'])
            
            # 2. Extract Key Performance Indicators (KPIs)
            devices = spec.get("devices", [])
            surgical = spec.get("surgical_devices", [])
            macros_raw = spec.get("macro_details", [])
            macro_indices = set(m.get('macro') for m in macros_raw)
            
            print(f"  > Devices: {', '.join(devices)}")
            print(f"  > Surgical Depth: {len(surgical)} devices custom configured")
            print(f"  > Macros Used: {len(macro_indices)} / 8")
            
            # 3. Analyze Macro Groups (Gestures)
            macro_groups = {}
            for m in macros_raw:
                idx = m.get('macro')
                if idx not in macro_groups: macro_groups[idx] = []
                macro_groups[idx].append(f"{m.get('target_device')}.{m.get('target_parameter')}")
            
            multi_mapped = [idx for idx, params in macro_groups.items() if len(params) > 1]
            print(f"  > Multi-Mapped Macros: {len(multi_mapped)} (Indices: {multi_mapped})")
            
            # 4. Evaluation Heuristics
            efficiency_score = 10 if len(devices) > 2 else 7
            sd_quality = 10 if len(surgical) >= len(devices)/2 else 5
            usability = 10 if len(macro_indices) == 8 else (len(macro_indices)/8)*10
            
            avg_score = (efficiency_score + sd_quality + usability) / 3
            print(f"  > MUSICAL IMPACT SCORE: {avg_score:.1f}/10")
            
            duration = time.time() - start_time
            print(f"  Complete in {duration:.1f}s")

            results.append({
                "name": p["name"],
                "score": avg_score,
                "summary": spec.get("musical_logic_explanation", "No explanation provided.")
            })

        except Exception as e:
            print(f"  FAILED: {str(e)}")
            traceback.print_exc()

    print("\n" + "="*70)
    print(f"  TOTAL IMPACT AUDIT COMPLETE: Avg Score {sum(r['score'] for r in results)/len(results):.1f}/10")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(run_total_impact_evaluation())
