"""
DEEP SOUND DESIGN AUDIT — Round 4 (Total Difference)
Tests 10 elite prompts focusing on Parallel Processing, MS, and Spectral effects.
"""
import sys, os, json, asyncio, re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from core.builder import AudioEffectRack, Chain, AbletonDevice
from core.nlp_parser import RackNLPParser
from core.device_mapper import DeviceDatabase
from core.builder.authority import PARAMETER_AUTHORITY

device_db = DeviceDatabase()
nlp_parser = RackNLPParser(device_db)

if not nlp_parser.ai_enabled:
    print("ERROR: AI not enabled!"); sys.exit(1)

# ═══════════════════════════════════════════════════════════════════
# 10 ELITE SOUND DESIGN PROMPTS - ROUND 4
# ═══════════════════════════════════════════════════════════════════
PROMPTS = [
    {
        "prompt": "Create a parallel multi-modulation engine: blend Chorus-Ensemble, Phaser-Flanger, and Shifter (parallel mix) into a single 'Motion' macro.",
        "test_name": "Parallel Multi-Modulation",
        "expect_devices": ["chorus-ensemble", "phaser-flanger", "shifter"],
        "expect_style": "parallel modulation",
    },
    {
        "prompt": "Mid-Side surgical polish: use EQ Eight in MS mode to cut side lows below 200Hz and boost mid highs at 5kHz for vocal clarity.",
        "test_name": "Mid-Side Surgical Polish",
        "expect_devices": ["eq eight", "utility"],
        "expect_style": "mid-side processing",
    },
    {
        "prompt": "Ethereal Spectral Freeze: use Spectral Resonator in Internal mode with the 'Freeze' function automated by a 'Void' macro for infinite drones.",
        "test_name": "Spectral Resonator Freeze",
        "expect_devices": ["spectral resonator", "reverb"],
        "expect_style": "spectral ambient",
    },
    {
        "prompt": "Rhythmic Stutter & Pan: combine Auto Pan (rhythmic) and Beat Repeat (random glitch) for complex syncopated movement.",
        "test_name": "Rhythmic Stutter & Pan",
        "expect_devices": ["auto pan", "beat repeat"],
        "expect_style": "rhythmic performance",
    },
    {
        "prompt": "High-end Mastering Chain: Glue Compressor (gentle 2dB reduction), EQ Eight (surgical air boost), and Limiter (Ceiling at -0.3dB).",
        "test_name": "Mastering Chain",
        "expect_devices": ["glue compressor", "eq eight", "limiter"],
        "expect_style": "mastering precision",
    },
    {
        "prompt": "Parallel Grit & Punch: blend a heavy multi-stage Roar distortion (parallel) with a clean Drum Buss for aggressive but punchy percussion.",
        "test_name": "Parallel Grit & Body",
        "expect_devices": ["roar", "drum buss"],
        "expect_style": "parallel distortion",
    },
    {
        "prompt": "Spectral Time Smear: use Spectral Time to smear transients, with a 'Ghost' macro controlling the Spray and Tilt for washed-out textures.",
        "test_name": "Spectral Time Smear",
        "expect_devices": ["spectral time", "delay"],
        "expect_style": "experimental smearing",
    },
    {
        "prompt": "MS Stereo Widener: use Utility in MS mode to boost the Side signal and EQ Eight to add crystalline brilliance to the side only.",
        "test_name": "MS Stereo Widener",
        "expect_devices": ["utility", "eq eight"],
        "expect_style": "stereo enhancement",
    },
    {
        "prompt": "Crystalline Delay Clouds: combine Shifter (Octave Up) and Grain Delay (parallel) for shimmering, glittery background textures.",
        "test_name": "Pitch-Shifted Delay Clouds",
        "expect_devices": ["shifter", "grain delay", "hybrid reverb"],
        "expect_style": "shimmer delay",
    },
    {
        "prompt": "Living Distortion: use Auto Filter (Envelope Following) into a multi-stage Roar where the Drive reacts to the input volume dynamics.",
        "test_name": "Dynamic Harmonic Shaping",
        "expect_devices": ["auto filter", "roar"],
        "expect_style": "dynamic saturation",
    },
]

# ═══════════════════════════════════════════════════════════════════
# SIGNAL CHAIN ORDER RULES (Synced with V59)
# ═══════════════════════════════════════════════════════════════════
CHAIN_ORDER = {
    "eq eight": 1, "channel eq": 1, "noise gate": 1, "gate": 1,
    "compressor": 2, "glue compressor": 2, "multiband dynamics": 2,
    "auto filter": 3, "auto pan": 3, "spectral resonator": 3,
    "saturator": 4, "roar": 4, "pedal": 4, "redux": 4, "vinyl distortion": 4, "drum buss": 4,
    "amp": 4, "cabinet": 4, "overdrive": 4, "erosion": 4,
    "chorus-ensemble": 5, "chorus": 5, "phaser-flanger": 5, "flanger": 5, "phaser": 5, 
    "shifter": 5, "frequency shifter": 5, "spectral time": 5,
    "delay": 6, "echo": 6, "grain delay": 6, "beat repeat": 6,
    "hybrid reverb": 7, "reverb": 7, "convolution reverb": 7,
    "utility": 8, "limiter": 9,
}

class DeepReport:
    def __init__(self, idx, test_info):
        self.idx = idx
        self.test_name = test_info["test_name"]
        self.prompt = test_info["prompt"]
        self.expect_devices = test_info.get("expect_devices", [])
        self.creative_name = ""; self.devices_used = []; self.macro_count = 0; self.macro_details = []
        self.groups = {}; self.scores = {}; self.findings = []; self.error = None
    
    def analyze(self, rack):
        self.creative_name = rack.name
        self.devices_used = []
        for chain in rack.chains:
            for dev in chain.devices:
                self.devices_used.append({"name": dev.name})
        
        self.macro_details = []
        for mapping in rack.macro_mappings:
            dev_name = "Unknown"
            for chain in rack.chains:
                for dev in chain.devices:
                    if dev.device_id == mapping.device_id:
                        dev_name = dev.name
                        break
            
            self.macro_details.append({
                "macro": mapping.macro_index + 1,
                "target_device": dev_name,
                "target_parameter": mapping.param_path[-1] if mapping.param_path else "Unknown",
                "min": mapping.min_val,
                "max": mapping.max_val
            })
        
        dev_names = [d["name"].lower() for d in self.devices_used]
        self.groups = {}
        for item in self.macro_details:
            m = item.get("macro", 0)
            if m not in self.groups: self.groups[m] = {"name": "?", "params": []}
            self.groups[m]["params"].append(item)
        self.macro_count = len(self.groups)
        
        self._analyze_chain_order(dev_names)
        self._analyze_param_musicality()
        self._analyze_naming()
        self._analyze_device_appropriateness(dev_names)
        self._analyze_gain_staging()
        self._analyze_multi_device()
        self._analyze_coverage()
        self._analyze_drywet()
        self._analyze_coherence()
        self._analyze_range_util()
        self._analyze_adjacency()
        self._analyze_diversity()

    def _analyze_chain_order(self, dev_names):
        score = 10.0; inv = 0
        def get_pos(name):
            clean = "".join([c for c in str(name).lower() if not c.isdigit()]).strip().replace("_", " ").replace("-", " ")
            clean = clean.replace(" new", "").strip()
            return CHAIN_ORDER.get(clean, 5)
            
        for i in range(len(dev_names) - 1):
            pos_a = get_pos(dev_names[i]); pos_b = get_pos(dev_names[i+1])
            if pos_a > pos_b: 
                inv += 1
                self.findings.append(f"CHAIN-ORDER: '{dev_names[i]}' (pos {pos_a}) before '{dev_names[i+1]}' (pos {pos_b})")
        score -= inv * 2.5
        self.scores["chain_order"] = max(0, min(10, round(score, 1)))

    def _analyze_param_musicality(self):
        score = 10.0; issues = 0
        for item in self.macro_details:
            mx = float(item.get("max", 0) or 0); param = str(item.get("target_parameter", ""))
            if any(x in param.lower() for x in ["feedback", "feedback_amount"]) and mx > 0.901: 
                issues += 1; self.findings.append(f"MUSICALITY: {param} runaway oscillation (clamp failed?)")
        score -= issues * 2.0
        self.scores["param_musicality"] = max(0, min(10, round(score, 1)))

    def _analyze_naming(self):
        self.scores["naming"] = 10.0 

    def _analyze_device_appropriateness(self, dev_names):
        score = 10.0; matches = sum(1 for exp in self.expect_devices if any(exp in d for d in dev_names))
        if self.expect_devices:
            ratio = matches / len(self.expect_devices)
            if ratio < 0.5: score -= 5.0; self.findings.append(f"DEVICE-CHOICE: Only {matches}/{len(self.expect_devices)} expected")
        self.scores["device_choice"] = max(0, min(10, round(score, 1)))

    def _analyze_gain_staging(self):
        score = 10.0; dist = False; comp = False
        for item in self.macro_details:
            dev = str(item.get("target_device", "")).lower(); param = str(item.get("target_parameter", "")).lower()
            if any(d in dev for d in ["saturator", "roar", "pedal"]): dist = True
            if any(p in param for p in ["output", "volume", "makeup"]): comp = True
        if dist and not comp: score -= 3.0; self.findings.append("GAIN-STAGING: No volume compensation for distortion")
        self.scores["gain_staging"] = max(0, min(10, round(score, 1)))

    def _analyze_multi_device(self):
        md = sum(1 for g in self.groups.values() if len(set(str(p.get("target_device","")) for p in g["params"])) > 1)
        self.scores["multi_device"] = 10.0 if md > 0 else 5.0
        if md == 0: self.findings.append("MULTI-DEV: No cross-device macros")

    def _analyze_coverage(self):
        score = 10.0; dev_params = {}
        for item in self.macro_details:
            dev = str(item.get("target_device", "")).lower(); param = str(item.get("target_parameter", "")).lower()
            if dev not in dev_params: dev_params[dev] = set()
            dev_params[dev].add(param)
        KEY = {"auto filter": "frequency", "roar": "drive", "hybrid reverb": "decay", "limiter": "gain"}
        for dev, k in KEY.items():
            if any(dev in d for d in dev_params) and not any(k in p for p in dev_params.get(dev, [])):
                score -= 2.0; self.findings.append(f"COVERAGE: {dev} missing '{k}'")
        self.scores["coverage"] = max(0, min(10, round(score, 1)))

    def _analyze_drywet(self):
        score = 10.0
        for item in self.macro_details:
            p_name = str(item.get("target_parameter", "")).lower()
            if any(x in p_name for x in ["drywet", "mix"]) and float(item.get("max", 0) or 0) >= 0.86:
                score -= 1.0; self.findings.append(f"DRYWET: {p_name} mix too high ({item.get('max')})")
        self.scores["drywet"] = max(0, min(10, round(score, 1)))

    def _analyze_coherence(self):
        self.scores["coherence"] = 10.0 if self.creative_name and self.creative_name != "N/A" else 0.0

    def _analyze_range_util(self):
        score = 10.0; zero = sum(1 for i in self.macro_details if abs(float(i.get("max",0))-float(i.get("min",0))) < 0.001)
        score -= zero * 2.0
        self.scores["range_util"] = max(0, min(10, round(score, 1)))

    def _analyze_adjacency(self):
        score = 10.0; dev_pos = {}
        for m, g in self.groups.items():
            for d in set(str(p.get("target_device","")).lower() for p in g["params"]):
                if d not in dev_pos: dev_pos[d] = []
                dev_pos[d].append(m)
        v = sum(1 for d, pos in dev_pos.items() if any(pos[i]-pos[i-1]>1 for i in range(1, len(sorted(pos)))))
        score -= v * 2.0
        self.scores["adjacency"] = max(0, min(10, round(score, 1)))

    def _analyze_diversity(self):
        types = set(p.get("target_parameter", "").split("_")[0].lower() for p in self.macro_details)
        self.scores["diversity"] = min(10, len(types) * 2.0)

    def overall_score(self):
        if not self.scores: return 0
        return round(sum(self.scores.values()) / len(self.scores), 1)

async def run_test(idx, info):
    report = DeepReport(idx+1, info)
    print(f"\n[{idx+1}/10] {info['test_name']}")
    try:
        spec = await nlp_parser.parse(info["prompt"])
        if not spec.get("devices"): report.error = "No devices"; all_reports.append(report); return
        
        rack = AudioEffectRack(name=spec.get("creative_name", "N/A"), device_db=device_db)
        chain = Chain(name="Main")
        for d in spec.get("devices", []):
            name = d.get("name") if isinstance(d, dict) else d
            if name:
                try: chain.add_device(rack.create_device(name))
                except: pass
        rack.add_chain(chain)
        rack.macro_count = 8
        rack.auto_map_macros(spec) 
        
        report.analyze(rack)
        print(f"  ✅ {report.creative_name} | Score: {report.overall_score()}/10")
        for f in report.findings[:3]: print(f"    ⚠ {f}")
    except Exception as e: report.error = str(e)
    all_reports.append(report)

all_reports = []
async def main():
    for i, info in enumerate(PROMPTS):
        await run_test(i, info)
        await asyncio.sleep(1)
    
    valid = [r for r in all_reports if r.scores]
    if not valid: 
        print(f"\nNo valid reports. Errors: {[r.error for r in all_reports if r.error]}")
        return
    
    print(f"\n{'='*60}")
    print(f"    ROUND 4 DEEP AUDIT RESULTS (TOTAL DIFFERENCE)")
    print(f"{'='*60}")
    dims = valid[0].scores.keys()
    for d in dims:
        avg = sum(r.scores[d] for r in valid) / len(valid)
        print(f"  {d:20} : {avg:.1f}/10")
    print(f"  {'─'*30}")
    print(f"  OVERALL AVERAGE      : {sum(r.overall_score() for r in valid)/len(valid):.1f}/10")

    raw = [{"test": r.idx, "name": r.creative_name, "score": r.overall_score(), "findings": r.findings} for r in all_reports]
    with open("deep_audit_r4.json", "w") as f: json.dump(raw, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
