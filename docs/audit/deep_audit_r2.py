"""
DEEP SOUND DESIGN AUDIT — Round 2
Tests 10 advanced prompts across 12 analysis dimensions:
  1. Signal chain order     7. Macro coverage depth
  2. Parameter musicality   8. DryWet sanity
  3. Naming creativity      9. Creative coherence
  4. Device appropriateness 10. Range utilization
  5. Gain staging          11. Adjacency (legacy)
  6. Multi-device intelligence 12. Parameter diversity
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
# 10 ADVANCED SOUND DESIGN PROMPTS
# Each targets different SD competencies
# ═══════════════════════════════════════════════════════════════════
PROMPTS = [
    # 1. VAGUE/MINIMAL — tests inference, initiative, device selection
    {
        "prompt": "Make it warm and fat",
        "test_name": "Vague Prompt - Warmth",
        "expect_devices": ["saturator", "eq", "compressor"],  # reasonable expectations
        "expect_style": "warm analog character",
    },
    # 2. GENRE-SPECIFIC — tests genre awareness, appropriate FX
    {
        "prompt": "Techno kick drum processing: hard, punchy, with sidechain-like pumping",
        "test_name": "Genre: Techno Kick",
        "expect_devices": ["compressor", "drum buss", "saturator", "eq"],
        "expect_style": "aggressive dynamics",
    },
    # 3. MASTERING CHAIN — tests signal chain ORDER knowledge
    {
        "prompt": "Create a mastering chain with EQ, compression, saturation, stereo imaging, and limiting",
        "test_name": "Mastering Chain Order",
        "expect_devices": ["eq eight", "compressor", "saturator", "utility", "limiter"],
        "expect_style": "mastering signal flow",
    },
    # 4. INSTRUMENT-SPECIFIC — tests instrument awareness
    {
        "prompt": "Electric bass processing: tight low end, growly mids, controlled dynamics",
        "test_name": "Instrument: Electric Bass",
        "expect_devices": ["eq eight", "compressor", "saturator"],
        "expect_style": "bass frequency focus",
    },
    # 5. ABSTRACT/CREATIVE — tests creative interpretation
    {
        "prompt": "Make it sound like being underwater in a cathedral",
        "test_name": "Abstract: Underwater Cathedral",
        "expect_devices": ["auto filter", "hybrid reverb", "chorus"],
        "expect_style": "atmospheric immersive",
    },
    # 6. MANY DEVICES STRESS — tests handling 5+ devices
    {
        "prompt": "Full mix bus chain with EQ Eight, Glue Compressor, Saturator, Utility for width, Limiter, and subtle Hybrid Reverb",
        "test_name": "Stress: 6 Device Mix Bus",
        "expect_devices": ["eq eight", "glue compressor", "saturator", "utility", "limiter", "hybrid reverb"],
        "expect_style": "mix bus cohesion",
    },
    # 7. SPECIFIC PARAM REQUEST — tests parameter targeting accuracy
    {
        "prompt": "Filter modulation rack: I want one macro for cutoff sweep, one for resonance peak, and one for LFO rate on the filter",
        "test_name": "Specific Params Requested",
        "expect_devices": ["auto filter"],
        "expect_style": "precise parameter control",
    },
    # 8. MIXING UTILITY — tests utility/tool-focused design
    {
        "prompt": "Create a utility mixing toolkit with mono bass below 200Hz, mid-side EQ, and output gain staging",
        "test_name": "Mixing Utility Toolkit",
        "expect_devices": ["utility", "eq eight"],
        "expect_style": "engineering precision",
    },
    # 9. EXPERIMENTAL/GLITCH — tests creative effects choices
    {
        "prompt": "Radiohead-style experimental texture: bitcrushed, granular, with pitch shifting artifacts",
        "test_name": "Experimental: Radiohead Texture",
        "expect_devices": ["redux", "grain delay", "shifter"],
        "expect_style": "experimental texture",
    },
    # 10. PARALLEL CONCEPT — tests understanding of parallel processing
    {
        "prompt": "New York style parallel compression rack for drums with a dirty parallel channel",
        "test_name": "Parallel Compression Concept",
        "expect_devices": ["compressor", "saturator"],
        "expect_style": "parallel dynamics",
    },
]

# ═══════════════════════════════════════════════════════════════════
# SIGNAL CHAIN ORDER RULES (higher position = later in chain)
# ═══════════════════════════════════════════════════════════════════
CHAIN_ORDER = {
    # Pre-processing (first)
    "eq eight": 1, "channel eq": 1,
    # Dynamics (early)
    "compressor": 2, "glue compressor": 2, "multiband dynamics": 2,
    # Tone shaping
    "auto filter": 3, "auto pan": 3, "phaser": 3, "phaser-flanger": 3,
    # Character / Saturation
    "saturator": 4, "overdrive": 4, "pedal": 4, "amp": 4,
    "roar": 4, "vinyl distortion": 4, "drum buss": 4, "redux": 4,
    # Modulation
    "chorus-ensemble": 5, "chorus": 5, "flanger": 5, "frequency shifter": 5,
    "shifter": 5, "spectral resonator": 5, "spectral time": 5,
    # Time-based
    "echo": 6, "delay": 6, "grain delay": 6, "beat repeat": 6,
    # Space
    "hybrid reverb": 7, "reverb": 7, "convolution reverb": 7,
    # Utility (near end)
    "utility": 8,
    # Limiter (LAST)
    "limiter": 9,
}

# ═══════════════════════════════════════════════════════════════════
# PARAMETER SWEET SPOTS — defines musically useful ranges
# ═══════════════════════════════════════════════════════════════════
SWEET_SPOTS = {
    "Filter_Frequency": {"min_range": 200, "max_range": 18000, "warn_if_below": 20, "warn_if_above": 20000},
    "Filter_Resonance": {"min_range": 0.0, "max_range": 1.0, "warn_if_above": 0.95},
    "DryWet": {"ideal_max": 0.75, "warn_if_full_wet": True},
    "Feedback": {"warn_if_above": 0.95},
    "DecayTime": {"warn_if_above": 60.0},
}

# ═══════════════════════════════════════════════════════════════════
# ANALYSIS ENGINE
# ═══════════════════════════════════════════════════════════════════
class DeepReport:
    def __init__(self, idx, test_info):
        self.idx = idx
        self.test_name = test_info["test_name"]
        self.prompt = test_info["prompt"]
        self.expect_devices = test_info.get("expect_devices", [])
        self.expect_style = test_info.get("expect_style", "")
        
        self.creative_name = ""
        self.devices_used = []
        self.macro_count = 0
        self.macro_details = []
        self.groups = {}
        
        # 12 analysis dimensions
        self.scores = {}
        self.findings = []
        self.error = None
    
    def analyze(self, spec):
        self.creative_name = spec.get("creative_name", "N/A")
        self.devices_used = spec.get("devices", [])
        self.macro_details = spec.get("macro_details", [])
        
        # Normalize device names
        dev_names = []
        for d in self.devices_used:
            name = d.get("name") if isinstance(d, dict) else d
            dev_names.append(str(name).lower() if name else "")
        
        self.groups = {}
        for item in self.macro_details:
            m = item.get("macro", 0)
            if m not in self.groups: self.groups[m] = {"name": item.get("name", "?"), "params": []}
            self.groups[m]["params"].append(item)
        self.macro_count = len(self.groups)
        
        self._analyze_chain_order(dev_names)
        self._analyze_param_musicality()
        self._analyze_naming()
        self._analyze_device_appropriateness(dev_names)
        self._analyze_gain_staging()
        self._analyze_multi_device()
        self._analyze_macro_coverage()
        self._analyze_drywet()
        self._analyze_creative_coherence()
        self._analyze_range_utilization()
        self._analyze_adjacency()
        self._analyze_param_diversity()
    
    def _analyze_chain_order(self, dev_names):
        """1. Is the signal chain in the correct order?"""
        score = 10.0
        inversions = 0
        for i in range(len(dev_names) - 1):
            pos_a = CHAIN_ORDER.get(dev_names[i], 5)
            pos_b = CHAIN_ORDER.get(dev_names[i + 1], 5)
            if pos_a > pos_b:
                inversions += 1
                self.findings.append(f"CHAIN-ORDER: '{dev_names[i]}' (pos {pos_a}) before '{dev_names[i+1]}' (pos {pos_b}) — inverted")
        score -= inversions * 2.5
        if dev_names and "limiter" in dev_names and dev_names[-1] != "limiter" and dev_names[-1] != "utility":
            self.findings.append("CHAIN-ORDER: Limiter should be last (or second-to-last before Utility)")
            score -= 2.0
        self.scores["chain_order"] = max(0, min(10, round(score, 1)))
    
    def _analyze_param_musicality(self):
        """2. Are parameter ranges in musical sweet spots?"""
        score = 10.0
        issues = 0
        for item in self.macro_details:
            param = str(item.get("target_parameter", ""))
            mn = float(item.get("min", 0) or 0)
            mx = float(item.get("max", 0) or 0)
            
            # Check for zero-width ranges (useless macros)
            if abs(mx - mn) < 0.001 and mx != 0:
                issues += 1
                self.findings.append(f"MUSICALITY: {param} range [{mn:.3f}, {mx:.3f}] — zero width, macro does nothing")
            
            # Check for full-range sweeps (lazy mapping)
            if "frequency" in param.lower() or "freq" in param.lower():
                if mn <= 20 and mx >= 20000:
                    self.findings.append(f"MUSICALITY: {param} full spectrum sweep [{mn}, {mx}] — too wide, consider musical sub-range")
                    issues += 1
            
            # Feedback > 95% = dangerous self-oscillation
            if "feedback" in param.lower() and mx > 0.95:
                self.findings.append(f"MUSICALITY: {param} max={mx:.2f} — feedback near 1.0 causes runaway oscillation")
                issues += 1
        
        score -= issues * 1.5
        self.scores["param_musicality"] = max(0, min(10, round(score, 1)))
    
    def _analyze_naming(self):
        """3. Are macro names evocative and musical?"""
        score = 10.0
        
        TECHNICAL_WORDS = {
            "frequency", "resonance", "threshold", "ratio", "attack", "release",
            "drywet", "dry wet", "mix", "gain", "volume", "feedback", "decay",
            "delay", "rate", "amount", "filter", "lfo", "eq", "band", "output",
            "input", "pitch", "time", "size", "width", "compressor", "saturator",
            "reverb", "eq eight", "auto filter", "chorus", "drive", "bass", "treble",
            "mid", "type", "mode", "cutoff", "speed", "depth"
        }
        
        tech_count = 0
        generic_count = 0
        for m, group in self.groups.items():
            name = group["name"].lower().strip()
            name_clean = name.replace("_", " ").replace("-", " ")
            
            # Direct technical name
            if name_clean in TECHNICAL_WORDS:
                tech_count += 1
                self.findings.append(f"NAMING: M{m} '{group['name']}' is a raw technical name")
            
            # Generic/boring names
            GENERIC = {"macro", "control", "knob", "parameter", "effect", "setting", "adjust"}
            if name_clean in GENERIC or any(name_clean == g for g in GENERIC):
                generic_count += 1
                self.findings.append(f"NAMING: M{m} '{group['name']}' is generic/boring")
            
            # Too short (single word < 4 chars)
            if len(name.replace(" ", "")) < 4 and name not in {"air", "ice", "fog", "glow", "heat", "silk"}:
                self.findings.append(f"NAMING: M{m} '{group['name']}' too short — needs more character")
                generic_count += 1
        
        score -= tech_count * 2.0
        score -= generic_count * 1.5
        self.scores["naming"] = max(0, min(10, round(score, 1)))
    
    def _analyze_device_appropriateness(self, dev_names):
        """4. Did the AI pick devices that make sense for the request?"""
        score = 10.0
        matches = 0
        
        for expected in self.expect_devices:
            exp_lower = expected.lower()
            found = any(exp_lower in d for d in dev_names)
            if found:
                matches += 1
        
        if self.expect_devices:
            match_ratio = matches / len(self.expect_devices)
            if match_ratio < 0.5:
                self.findings.append(f"DEVICE-CHOICE: Only {matches}/{len(self.expect_devices)} expected devices found")
                score -= (1 - match_ratio) * 5.0
        
        # Check for unnecessary devices
        if len(dev_names) > 6:
            self.findings.append(f"DEVICE-CHOICE: {len(dev_names)} devices — may be overloaded")
            score -= 1.0
        
        # Check if Utility was added (good practice for gain staging)
        has_distortion = any(d in dev_names for d in ["saturator", "roar", "pedal", "overdrive", "vinyl distortion", "redux"])
        has_utility = "utility" in dev_names
        if has_distortion and not has_utility:
            self.findings.append("DEVICE-CHOICE: Has distortion but no Utility for gain staging")
            score -= 1.5
        
        self.scores["device_choice"] = max(0, min(10, round(score, 1)))
    
    def _analyze_gain_staging(self):
        """5. Is there proper gain compensation after saturation/distortion?"""
        score = 10.0
        
        distortion_devs = set()
        gain_devs = set()
        
        for item in self.macro_details:
            dev = str(item.get("target_device", "")).lower()
            param = str(item.get("target_parameter", "")).lower()
            
            if any(d in dev for d in ["saturator", "roar", "pedal", "overdrive", "redux", "vinyl"]):
                distortion_devs.add(dev)
                if "output" in param or "gain" in param or "postgain" in param:
                    gain_devs.add(dev)
        
        if distortion_devs and not gain_devs:
            self.findings.append(f"GAIN-STAGING: Distortion ({', '.join(distortion_devs)}) without output gain control — no compensation")
            score -= 3.0
        
        # Check for utility gain at the end
        has_end_gain = any(
            str(item.get("target_device", "")).lower() == "utility"
            and "gain" in str(item.get("target_parameter", "")).lower()
            for item in self.macro_details
        )
        if distortion_devs and not has_end_gain:
            self.findings.append("GAIN-STAGING: No master output gain control on Utility")
            score -= 1.5
        
        self.scores["gain_staging"] = max(0, min(10, round(score, 1)))
    
    def _analyze_multi_device(self):
        """6. Do multi-device macros make musical sense?"""
        score = 10.0
        md_count = 0
        
        for m, group in self.groups.items():
            devs = set(str(p.get("target_device", "")) for p in group["params"])
            if len(devs) > 1:
                md_count += 1
                params = [str(p.get("target_parameter", "")) for p in group["params"]]
                # Check if the cross-device mapping makes sense
                has_drywet = any("drywet" in p.lower() or "dry_wet" in p.lower() for p in params)
                has_gain = any("gain" in p.lower() or "volume" in p.lower() or "output" in p.lower() for p in params)
                all_same_type = len(set(p.split("_")[0] if "_" in p else p for p in params)) == 1
                
                if has_drywet or has_gain or all_same_type:
                    pass  # Good cross-device mapping
                else:
                    # Check if related params
                    self.findings.append(f"MULTI-DEV: M{m} '{group['name']}' maps {len(devs)} devices — verify musical coherence")
        
        if md_count == 0 and self.macro_count >= 6:
            self.findings.append("MULTI-DEV: No cross-device macros — missed opportunity for cohesive gestures")
            score -= 2.0
        
        self.scores["multi_device"] = max(0, min(10, round(score, 1)))
    
    def _analyze_macro_coverage(self):
        """7. Are the most important parameters of each device covered?"""
        score = 10.0
        
        KEY_PARAMS = {
            "auto filter": ["filter_frequency", "filter_resonance"],
            "compressor": ["threshold", "ratio"],
            "saturator": ["drive"],
            "hybrid reverb": ["decay", "drywet", "size"],
            "eq eight": ["band"],
            "chorus-ensemble": ["rate", "amount"],
            "roar": ["drive", "feedback"],
            "echo": ["drywet", "feedback"],
            "utility": ["gain"],
            "limiter": ["gain", "ceiling"],
        }
        
        # Build map of device -> mapped params
        dev_params = {}
        for item in self.macro_details:
            dev = str(item.get("target_device", "")).lower()
            param = str(item.get("target_parameter", "")).lower()
            if dev not in dev_params: dev_params[dev] = set()
            dev_params[dev].add(param)
        
        for dev, mapped in dev_params.items():
            if dev in KEY_PARAMS:
                for key_p in KEY_PARAMS[dev]:
                    found = any(key_p in p for p in mapped)
                    if not found:
                        self.findings.append(f"COVERAGE: {dev} missing key param '{key_p}'")
                        score -= 1.0
        
        # Macro count
        if self.macro_count < 6:
            self.findings.append(f"COVERAGE: Only {self.macro_count}/8 macros used — under-utilizing")
            score -= 2.0
        
        self.scores["coverage"] = max(0, min(10, round(score, 1)))
    
    def _analyze_drywet(self):
        """8. Are DryWet values sensible?"""
        score = 10.0
        
        for item in self.macro_details:
            param = str(item.get("target_parameter", "")).lower()
            if "drywet" in param or "dry_wet" in param:
                mn = float(item.get("min", 0) or 0)
                mx = float(item.get("max", 1) or 1)
                dev = str(item.get("target_device", "")).lower()
                
                # Full wet on reverb/delay is usually bad for mixing
                if mx >= 0.99 and any(d in dev for d in ["reverb", "hybrid", "echo", "delay"]):
                    self.findings.append(f"DRYWET: {dev} DryWet max={mx:.2f} — full wet on time-based FX kills the dry signal")
                    score -= 1.5
                
                # DryWet starting at 0 = no effect at macro min
                if mn <= 0.01 and "reverb" in dev:
                    self.findings.append(f"DRYWET: {dev} DryWet min={mn:.2f} — reverb completely off at macro min")
                    score -= 0.5
        
        self.scores["drywet"] = max(0, min(10, round(score, 1)))
    
    def _analyze_creative_coherence(self):
        """9. Does the rack tell a coherent sound design story?"""
        score = 10.0
        
        # Check creative name quality
        name = self.creative_name
        if not name or name in ["N/A", "?", "Custom Rack", ""]:
            self.findings.append("COHERENCE: No creative name — rack feels generic")
            score -= 3.0
        elif len(name.split()) < 2:
            self.findings.append(f"COHERENCE: Name '{name}' is too short — needs more identity")
            score -= 1.0
        
        # Check if macro names tell a story (are they thematically connected?)
        macro_names = [g["name"] for g in self.groups.values()]
        if len(set(macro_names)) < len(macro_names) * 0.7:
            self.findings.append("COHERENCE: Duplicate/similar macro names — lazy naming")
            score -= 2.0
        
        self.scores["coherence"] = max(0, min(10, round(score, 1)))
    
    def _analyze_range_utilization(self):
        """10. Are parameter ranges deep enough (not too narrow or too wide)?"""
        score = 10.0
        narrow_count = 0
        
        for item in self.macro_details:
            mn = float(item.get("min", 0) or 0)
            mx = float(item.get("max", 1) or 1)
            param = str(item.get("target_parameter", ""))
            
            # Check for very narrow ranges (< 10% of total)
            total_range = abs(mx - mn)
            if total_range > 0 and total_range < 0.05:
                narrow_count += 1
                self.findings.append(f"RANGE: {param} [{mn:.3f}, {mx:.3f}] — very narrow, macro barely moves")
        
        score -= narrow_count * 2.0
        self.scores["range_util"] = max(0, min(10, round(score, 1)))
    
    def _analyze_adjacency(self):
        """11. Legacy adjacency check"""
        score = 10.0
        dev_pos = {}
        for m, group in self.groups.items():
            devs = set(str(p.get("target_device", "")).lower() for p in group["params"])
            for d in devs:
                if d not in dev_pos: dev_pos[d] = []
                if m not in dev_pos[d]: dev_pos[d].append(m)
        
        violations = 0
        for dev, positions in dev_pos.items():
            positions.sort()
            for i in range(1, len(positions)):
                if positions[i] - positions[i-1] > 1:
                    violations += 1
        
        score -= violations * 1.5
        self.scores["adjacency"] = max(0, min(10, round(score, 1)))
    
    def _analyze_param_diversity(self):
        """12. Are we using diverse parameter types (not just DryWet everywhere)?"""
        score = 10.0
        
        param_types = set()
        for item in self.macro_details:
            param = str(item.get("target_parameter", "")).lower()
            if "frequency" in param or "freq" in param: param_types.add("frequency")
            elif "resonance" in param or "q" in param: param_types.add("resonance")
            elif "drywet" in param or "dry_wet" in param: param_types.add("drywet")
            elif "gain" in param or "volume" in param or "output" in param: param_types.add("gain")
            elif "drive" in param or "amount" in param: param_types.add("drive")
            elif "time" in param or "decay" in param or "delay" in param: param_types.add("time")
            elif "rate" in param or "speed" in param: param_types.add("rate")
            elif "feedback" in param: param_types.add("feedback")
            elif "width" in param or "stereo" in param: param_types.add("stereo")
            elif "threshold" in param or "ratio" in param: param_types.add("dynamics")
            else: param_types.add("other")
        
        if len(param_types) < 3:
            self.findings.append(f"DIVERSITY: Only {len(param_types)} param types — needs more variety")
            score -= 3.0
        elif len(param_types) < 5:
            self.findings.append(f"DIVERSITY: {len(param_types)} param types — decent but could be wider")
            score -= 1.0
        
        self.scores["diversity"] = max(0, min(10, round(score, 1)))
    
    def overall_score(self):
        if not self.scores: return 0
        return round(sum(self.scores.values()) / len(self.scores), 1)

# ═══════════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════════
all_reports = []

async def run_test(idx, test_info):
    report = DeepReport(idx + 1, test_info)
    print(f"\n{'='*70}")
    print(f"TEST {idx+1}/10: {test_info['test_name']}")
    print(f"  Prompt: \"{test_info['prompt']}\"")
    print(f"{'='*70}")
    
    try:
        spec = await nlp_parser.parse(test_info["prompt"])
        if not spec.get("devices"):
            report.error = "No devices returned"
            report.findings.append("FATAL: No devices")
            all_reports.append(report)
            return
        
        report.analyze(spec)
        
        # Build rack
        rack = AudioEffectRack(name=f"R2_{idx+1}", device_db=device_db)
        chain = Chain(name="Main")
        for d in spec.get("devices", []):
            name = d.get("name") if isinstance(d, dict) else d
            if name:
                try: chain.add_device(rack.create_device(name))
                except: pass
        rack.add_chain(chain)
        rack.macro_count = 8
        rack.auto_map_macros(spec)
        out = os.path.join(os.path.dirname(__file__), "backend", "generated", f"R2_TEST_{idx+1}.adg")
        rack.save(out)
        
        # Print results
        devs_str = ", ".join(d.get("name") if isinstance(d, dict) else d for d in report.devices_used)
        print(f"  Name: {report.creative_name}")
        print(f"  Devices: {devs_str}")
        print(f"  Macros: {report.macro_count}/8 | Params: {len(report.macro_details)}")
        print(f"\n  SCORES:")
        for dim, val in report.scores.items():
            bar = "█" * int(val) + "░" * (10 - int(val))
            icon = "✅" if val >= 7 else "⚠️" if val >= 5 else "❌"
            print(f"    {icon} {dim:20} {bar} {val}/10")
        print(f"    {'='*40}")
        print(f"    Overall: {report.overall_score()}/10")
        
        if report.findings:
            print(f"\n  FINDINGS ({len(report.findings)}):")
            for f in report.findings[:8]:
                print(f"    ⚠ {f}")
            if len(report.findings) > 8:
                print(f"    ... +{len(report.findings) - 8} more")
    
    except Exception as e:
        report.error = str(e)
        report.findings.append(f"FATAL: {e}")
        import traceback; traceback.print_exc()
    
    all_reports.append(report)

async def main():
    for i, info in enumerate(PROMPTS):
        await run_test(i, info)
        if i < len(PROMPTS) - 1: await asyncio.sleep(1)
    
    # ═══════════════════════════════════════════════════════════════
    # FINAL REPORT
    # ═══════════════════════════════════════════════════════════════
    print(f"\n\n{'='*80}")
    print(f"    DEEP SOUND DESIGN AUDIT — FINAL REPORT")
    print(f"{'='*80}")
    
    dims = ["chain_order", "param_musicality", "naming", "device_choice", "gain_staging",
            "multi_device", "coverage", "drywet", "coherence", "range_util", "adjacency", "diversity"]
    
    # Dimension averages
    print(f"\n  DIMENSION AVERAGES (across 10 tests):")
    dim_totals = {d: 0 for d in dims}
    valid_count = sum(1 for r in all_reports if not r.error)
    
    for r in all_reports:
        if r.error: continue
        for d in dims:
            dim_totals[d] += r.scores.get(d, 0)
    
    for d in dims:
        avg = dim_totals[d] / max(1, valid_count)
        bar = "█" * int(avg) + "░" * (10 - int(avg))
        icon = "✅" if avg >= 7 else "⚠️" if avg >= 5 else "❌"
        print(f"    {icon} {d:20} {bar} {avg:.1f}/10")
    
    overall = sum(dim_totals.values()) / (max(1, valid_count) * len(dims))
    print(f"    {'─'*40}")
    print(f"    OVERALL AVERAGE:     {overall:.1f}/10")
    
    # Per-test summary
    print(f"\n  PER-TEST SCORES:")
    print(f"  {'#':>2} | {'Test':30} | {'Name':25} | {'Score':>5} | {'Findings':>8}")
    print(f"  {'-'*2}-+-{'-'*30}-+-{'-'*25}-+-{'-'*5}-+-{'-'*8}")
    for r in all_reports:
        name = (r.creative_name or "ERROR")[:25]
        tname = r.test_name[:30]
        scr = r.overall_score() if not r.error else "ERR"
        finds = len(r.findings)
        print(f"  {r.idx:2} | {tname:30} | {name:25} | {str(scr):>5} | {finds:8}")
    
    # Issue frequency
    print(f"\n  ISSUE FREQUENCY:")
    categories = {}
    for r in all_reports:
        for f in r.findings:
            cat = f.split(":")[0]
            if cat not in categories: categories[cat] = {"count": 0, "tests": []}
            categories[cat]["count"] += 1
            if r.idx not in categories[cat]["tests"]:
                categories[cat]["tests"].append(r.idx)
    
    sorted_cats = sorted(categories.items(), key=lambda x: x[1]["count"], reverse=True)
    print(f"  {'Category':25} | {'Count':>5} | {'Tests':30}")
    print(f"  {'-'*25}-+-{'-'*5}-+-{'-'*30}")
    for cat, data in sorted_cats:
        tests = ", ".join(f"#{t}" for t in data["tests"])
        print(f"  {cat:25} | {data['count']:5} | {tests}")
    
    # Save raw
    raw = []
    for r in all_reports:
        raw.append({
            "test": r.idx, "test_name": r.test_name, "prompt": r.prompt,
            "creative_name": r.creative_name, "devices": r.devices_used,
            "macro_count": r.macro_count, "total_params": len(r.macro_details),
            "scores": r.scores, "overall": r.overall_score(),
            "findings": r.findings, "error": r.error
        })
    with open(os.path.join(os.path.dirname(__file__), "deep_audit_r2.json"), "w") as f:
        json.dump(raw, f, indent=2)
    print(f"\n  Raw results → deep_audit_r2.json")

asyncio.run(main())
