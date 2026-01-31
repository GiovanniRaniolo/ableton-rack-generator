# --- V23 MASTER PARAMETER AUTHORITY ---
PARAMETER_AUTHORITY = {
    "DelayLine_TimeL": "normalized_time_5s",
    "DelayLine_TimeR": "normalized_time_5s",
    "DelayLine_Time": "normalized_time_5s",
    "Filter_Frequency": "hz_physical",
    "Freq": "hz_physical",
    "PreDrive": "db_physical",
    "PostDrive": "db_physical",
    "Stage1_Shaper_Amount": "percentage",
    "Feedback": "percentage",
    "Rate": "hz_physical",
    "On": "boolean",
    "Speaker": "boolean",
    "Mode": "enum",
    "Type": "enum",
    "FilterType": "enum",
    "ShaperType": "enum",
    "Routing": "enum",
    "Method": "enum"
}

# --- V23 MASTER ENUM AUTHORITY ---
ENUM_AUTHORITY = {
    "classic": 0.0, "fade": 1.0, "repitch": 2.0, "digital": 0.0,
    "single": 0.0, "serial": 1.0, "parallel": 2.0, "multiband": 3.0, "feedback": 4.0,
    "chorus": 0.0, "ensemble": 1.0, "vibrato": 2.0, "modern": 1.0,
    "on": 1.0, "off": 0.0, "true": 1.0, "false": 0.0, "enabled": 1.0, "disabled": 0.0
}

# --- V36 MASTER SEMANTIC RESOLVER MAP ---
# Maps AI intent (fuzzy keys) to technical Ableton parameter names.
SEMANTIC_MAP = {
    "Compressor2": {
        "thresh": "Threshold", "ratio": "Ratio", "attack": "Attack", "release": "Release", "gain": "Gain"
    },
    "GlueCompressor": {
        "thresh": "Threshold", "ratio": "Ratio", "makeup": "Makeup", "range": "Range", "attack": "Attack",
        "focus": "Threshold", "sub": "Threshold", "compress": "Threshold"
    },
    "Limiter": {
        "ceiling": "Ceiling", "gain": "Gain", "look": "Lookahead"
    },
    "MultibandDynamics": {
        "ott": "GlobalAmount", "amount": "GlobalAmount", "time": "GlobalTime",
        "output": "OutputGain", "mix": "GlobalAmount"
    },
    "Gate": {
        "thresh": "Threshold", "return": "Return", "attack": "Attack", "hold": "Hold", "release": "Release"
    },
    "DrumBuss": {
        "drive": "DriveAmount", "crunch": "CrunchAmount", "boom": "BoomAmount", 
        "transient": "TransientShaping", "damp": "DampingFrequency", "trim": "InputTrim"
    },
    "Roar": {
        "drive": "Stage1_Shaper_Amount", "amount": "Stage1_Shaper_Amount", 
        "cutoff": "Stage1_Filter_Frequency", "freq": "Stage1_Filter_Frequency",
        "res": "Stage1_Filter_Resonance", "bias": "Stage1_Shaper_Bias",
        "grit": "Stage1_Shaper_Amount", "tone": "Stage1_Filter_Frequency"
    },
    "Saturator": {
        "drive": "PreDrive", "depth": "ColorDepth", "curve": "WsCurve", "color": "ColorOn", "output": "PostDrive"
    },
    "Delay": {
        "time": "DelayLine_TimeL", "feedback": "Feedback", "drywet": "DryWet", "filter": "Filter_Frequency"
    },
    "Overdrive": {
        "drive": "Drive", "tone": "Tone", "band": "Bandwidth", "center": "MidFreq"
    },
    "Pedal": {
        "gain": "Gain", "drive": "Gain", "bass": "Bass", "mid": "Mid", "treble": "Treble", "output": "Output"
    },
    "Amp": {
        "gain": "Gain", "volume": "Volume", "bass": "Bass", "middle": "Middle", "treble": "Treble", "presence": "Presence"
    },
    "Cabinet": {
        "type": "CabinetType", "mic": "MicrophonePosition", "mix": "DryWet"
    },
    "Tube": {
        "drive": "PreDrive", "bias": "Bias", "tone": "Tone"
    },
    "Vinyl": {
        "crackle": "CracleVolume", "density": "CracleDensity", "drive": "Drive", "pinch": "BandFreq2"
    },
    "Erosion": {
        "amount": "Amplitude", "width": "BandQ", "freq": "Freq"
    },
    "Redux2": {
        "bits": "BitDepth", "crush": "BitDepth", "rate": "SampleRate", "jitter": "Jitter"
    },
    "AutoFilter2": {
        "cutoff": "Filter_Frequency", "freq": "Filter_Frequency", "res": "Filter_Resonance", 
        "lfo": "Lfo_Amount", "rate": "Lfo_Frequency", "drive": "Filter_Drive"
    },
    "Chorus2": {
        "rate": "Rate", "amount": "Amount", "width": "Width", "warmth": "Warmth", "feed": "Feedback"
    },
    "PhaserNew": {
        "rate": "Modulation_Frequency", "amount": "Modulation_Amount", "feed": "Feedback", "color": "Modulation_Amount"
    },
    "AutoPan2": {
        "rate": "Modulation_Frequency", "amount": "Modulation_Amount", "width": "Modulation_PhaseOffset"
    },
    "Shifter": {
        "coarse": "Pitch_Coarse", "fine": "Pitch_Fine", "ring": "ModBasedShifting_RingMod_Drive", 
        "rate": "Lfo_RateHz", "amount": "Lfo_Amount"
    },
    "Echo": {
        "time": "Delay_TimeL", "feedback": "Feedback", "drywet": "DryWet", 
        "reverb": "Reverb_Level", "wobble": "Wobble_Amount", "noise": "Noise_Amount",
        "drive": "InputGain", "predrive": "InputGain", "grit": "InputGain",
        "cutoff": "Filter_Frequency", "filter": "Filter_Frequency", "freq": "Filter_Frequency"
    },
    "Reverb": {
        "decay": "DecayTime", "tail": "DecayTime", "coda": "DecayTime", 
        "size": "RoomSize", "diff": "Diffusion", "predelay": "PreDelay",
        "mix": "DryWet", "drywet": "DryWet"
    },
    "Eq8": {
        "freq": "Freq", "gain": "GlobalGain", "q": "AdaptiveQ",
        "low": "Freq", "high": "Freq"
    },
    "GrainDelay": {
        "spray": "Spray", "pitch": "Pitch", "freq": "Freq", "random": "RandomPitch", "feed": "Feedback"
    },
    "Spectral": {
        "freeze": "Freezer_On", "spray": "Delay_Spray", "shift": "Delay_FrequencyShift", "feedback": "Delay_Feedback"
    },
    "Resonator": {
        "decay": "ResDecay", "color": "ResColor", "gain": "GlobalGain", "width": "Width"
    },
    "Corpus": {
        "freq": "Frequency", "tune": "Frequency", "coarse": "Frequency", "pitch": "Frequency",
        "decay": "Decay", "res": "Decay", "feedback": "Decay",
        "bright": "Brightness", "material": "Material",
        "ratio": "Ratio",
        "mix": "DryWet", "amount": "DryWet"
    },
    "BeatRepeat": {
        "grid": "Grid", "interval": "Interval", "gate": "Gate", "pitch": "Pitch", "chance": "Chance", "var": "GridChance"
    },
    "Looper": {
        "feed": "Feedback", "speed": "TempoControl", "reverse": "Reverse"
    }
}
