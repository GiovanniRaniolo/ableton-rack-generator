PARAMETER_AUTHORITY = {
    "DelayLine_TimeL": "normalized_time_5s",
    "DelayLine_TimeR": "normalized_time_5s",
    "DelayLine_Time": "normalized_time_5s",
    "Filter_Frequency": "hz_physical",
    "Freq": "hz_physical",
    "PreDrive": "db_physical",
    "PostDrive": "db_physical",
    "Threshold": "db_physical",
    "Volume": "db_physical",
    "Gain": "linear_amplitude",       # V55: Utility Gain is LINEAR (1.0=0dB), NOT dB!
    "LegacyGain": "db_physical",      # V55: LegacyGain IS actually dB (-35 to +35)
    "OutputGain": "linear_amplitude",  # V55: Most OutputGain params are linear amplitude
    "Input_InputGain": "linear_amplitude",  # V55: Roar Input Gain is linear
    "StereoWidth": "stereo_width_linear",   # V55: 0-4 where 1.0=100%
    "MidSideBalance": "stereo_width_linear", # V55: 0-2 where 1.0=center
    "Amount": "percentage",
    "DryWet": "percentage",
    "Stage1_Shaper_Amount": "percentage",
    "Feedback": "percentage",
    "Rate": "hz_physical",
    "Grid": "discrete",
    "Interval": "discrete",
    "Gate": "discrete",
    "Chance": "percentage",
    "FilterOn": "boolean",
    "On": "boolean",
    "Speaker": "boolean",
    "Softclip": "boolean",
    "Mode": "enum",
    "Type": "enum",
    "FilterType": "enum",
    "ShaperType": "enum",
    "Routing": "enum",
    "Method": "enum"
}

ENUM_AUTHORITY = {
    "classic": 0.0, "fade": 1.0, "repitch": 2.0, "digital": 0.0,
    "single": 0.0, "serial": 1.0, "parallel": 2.0, "multiband": 3.0, "feedback": 4.0,
    "chorus": 0.0, "ensemble": 1.0, "vibrato": 2.0, "modern": 1.0,
    "on": 1.0, "off": 0.0, "true": 1.0, "false": 0.0, "enabled": 1.0, "disabled": 0.0
}
