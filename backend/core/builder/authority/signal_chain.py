# Signal Chain Hierarchy Authority (V58)
# Higher number = later in the chain.

SIGNAL_CHAIN_HIERARCHY = {
    # 1. Correction & Prep
    "eq eight": 1,
    "channel eq": 1,
    "noise gate": 1,
    "gate": 1,
    
    # 2. Dynamics (Clean)
    "compressor": 2,
    "glue compressor": 2,
    "multiband dynamics": 2,
    
    # 3. Tone & Filter
    "auto filter": 3,
    "auto pan": 3,
    "spectral resonator": 3,
    
    # 4. Character & Saturation
    "saturator": 4,
    "roar": 4,
    "pedal": 4,
    "redux": 4,
    "vinyl distortion": 4,
    "drum buss": 4,
    "amp": 4,
    "cabinet": 4,
    "overdrive": 4,
    "erosion": 4,

    # 5. Modulation
    "chorus-ensemble": 5,
    "chorus": 5,
    "phaser-flanger": 5,
    "flanger": 5,
    "phaser": 5,
    "shifter": 5,
    "frequency shifter": 5,
    "spectral time": 5,
    
    # 6. Time & Space
    "delay": 6,
    "echo": 6,
    "grain delay": 6,
    "beat repeat": 6,
    "hybrid reverb": 7,
    "reverb": 7,
    "convolution reverb": 7,
    
    # 8. Output & Polish
    "utility": 8,
    "limiter": 9
}
