# Authority for devices with peculiar rhythm or logic parameters
SPECIALIZED_MAP = {
    "BeatRepeat": {
        "grid": "Grid", "interval": "Interval", "gate": "Gate", "pitch": "Pitch", 
        "chance": "Chance", "var": "GridChance", "jump": "Interval", "chaos": "GridChance",
        "fill": "Interval", "repeat": "Grid", "variation": "GridChance"
    },
    "Saturator": {
        "drive": "PreDrive", "amount": "PreDrive", "color": "ColorDepth", 
        "color_amount": "ColorDepth", "colordepth": "ColorDepth",
        "drywet": "DryWet", "mix": "DryWet"
    },
    "Roar": {
        "drive": "Stage1_Shaper_Trim", "amount": "Stage1_Shaper_Amount", 
        "cutoff": "Stage1_Filter_Frequency", "freq": "Stage1_Filter_Frequency",
        "res": "Stage1_Filter_Resonance", "bias": "Stage1_Shaper_Bias",
        "grit": "Stage1_Shaper_Amount", "tone": "Stage1_Filter_Frequency",
        "space": "Feedback_FeedbackAmount", "output": "Output_OutputGain",
        "gain": "Output_OutputGain"
    },
    "Hybrid": {
        "decay": "Algorithm_Decay", "size": "Algorithm_Size", "shimmer": "Algorithm_Shimmer",
        "damping": "Algorithm_Damping", "predelay": "PreDelay_FeedbackTime",
        "stereo": "StereoWidth", "width": "StereoWidth", "drywet": "DryWet", "blend": "ConvoAlgoBlend"
    },
    "SpectralResonator": {
        "brightness": "Brightness", "decay": "Decay", "structure": "Structure",
        "density": "Density", "feedback": "Feedback", "volume": "OutputGain",
        "drywet": "DryWet", "frequency": "Frequency", "transpose": "Transpose"
    },
    "Spectral": {
        "feedback": "Delay_Feedback", "drywet": "DryWet", "freeze": "Freezer_FreezeOn",
        "time": "Delay_TimeSeconds", "tilt": "Delay_Tilt", "spray": "Delay_Spray"
    },
    "PhaserNew": {
        "doubler": "DoublerDelayTime",
        "color": "Warmth",
        "sync": "Modulation_Sync",
        "rate": "Modulation_Frequency",
        "depth": "Modulation_Amount",
        "mix": "DryWet",
        "stereo": "Vibrato_Phase"
    },
    "Chorus2": {
        "depth": "Amount", "rate": "Rate", "mix": "DryWet", "width": "Width", "delay": "DelayTime",
        "drywet": "DryWet"
    },
    "FilterDelay": {
        "drywet": "DryVolume", "mix": "DryVolume", "feedback": "Feedback1",
        "freq": "MidFreq1", "resonance": "BandWidth1"
    },
    "Looper": {
        "feed": "Feedback", "speed": "TempoControl", "reverse": "Reverse"
    }
}
