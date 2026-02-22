# 🧬 THE ULTIMATE ABLETON PARAMETER SCHEMA (V43)

This report contains a recursive analysis of all 43+ core Ableton Audio Effects and their parameters.

## 📦 Amp
- **XML Tag**: `Amp`
- **Class**: `Amp`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| AmpType | 0.00 | 6.00 | 2.00 | Discrete/Enum |
| Bass | 0.00 | 10.00 | 5.00 | Linear |
| Middle | 0.00 | 10.00 | 5.00 | Linear |
| Treble | 0.00 | 10.00 | 5.00 | Linear |
| Presence | 0.00 | 10.00 | 5.00 | Linear |
| Gain | 0.00 | 10.00 | 5.00 | dB |
| Volume | 0.00 | 10.00 | 9.00 | dB |
| DualMono | 0.00 | 1.00 | 0.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Auto Filter
- **XML Tag**: `AutoFilter2`
- **Class**: `AutoFilter`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Filter_Frequency | 20.00 | 20000.00 | 10000.00 | Hz (Log) |
| Filter_Resonance | 0.00 | 1.00 | 0.00 | % / Normalized |
| Filter_Morph | 0.00 | 1.00 | 0.00 | % / Normalized |
| Filter_Type | 0.00 | 9.00 | 0.00 | Discrete/Enum |
| Filter_Slope | 0.00 | 1.00 | 1.00 | % / Normalized |
| Filter_MorphSlope | 0.00 | 3.00 | 2.00 | Linear |
| Filter_Circuit | 0.00 | 3.00 | 0.00 | Linear |
| Filter_Drive | 0.00 | 1.00 | 0.00 | % / Normalized |
| Filter_DjControl | -1.00 | 1.00 | 0.00 | Linear |
| Filter_VowelPitch | -36.00 | 36.00 | 0.00 | Linear |
| Filter_VowelFormant | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lfo_Amount | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lfo_Waveform | 0.00 | 7.00 | 0.00 | Linear |
| Lfo_TimeMode | 0.00 | 5.00 | 0.00 | Seconds |
| Lfo_Frequency | 0.10 | 60.00 | 1.00 | Hz (Log) |
| Lfo_Time | 0.10 | 200.00 | 1.00 | ms |
| Lfo_SyncedRate | 0.00 | 21.00 | 4.00 | Linear |
| Lfo_Sixteenth | 1.00 | 64.00 | 16.00 | Linear |
| Lfo_Phase | 0.00 | 360.00 | 4.00 | Linear |
| Lfo_PhaseOffset | 0.00 | 360.00 | 0.00 | Linear |
| Lfo_StereoMode | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lfo_Spin | 0.00 | 0.50 | 0.00 | Linear |
| Lfo_Morph | -1.00 | 1.00 | 0.00 | Linear |
| Lfo_Smoothing | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lfo_QuantizationMode | 0.00 | 2.00 | 0.00 | Linear |
| Lfo_Steps | 2.00 | 64.00 | 8.00 | Linear |
| Lfo_SahRate | -6.00 | 0.00 | -4.00 | Linear |
| Envelope_Amount | -1.00 | 1.00 | 0.00 | Linear |
| Envelope_Attack | 0.00 | 0.10 | 0.00 | Seconds |
| Envelope_HoldOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| Envelope_Release | 0.00 | 3.00 | 0.25 | Seconds |
| Envelope_SahOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Envelope_SahRate | -6.00 | 0.00 | -4.00 | Linear |
| Output | 0.00 | 1.00 | 1.00 | % / Normalized |
| SoftClipOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| SideChainEq_On | 0.00 | 1.00 | 0.00 | % / Normalized |
| SideChainEq_Mode | 0.00 | 5.00 | 5.00 | Linear |
| SideChainEq_Freq | 30.00 | 15000.00 | 200.00 | Hz (Log) |
| SideChainEq_Q | 0.10 | 12.00 | 0.71 | Linear |
| SideChainEq_Gain | -15.00 | 15.00 | 0.00 | dB |

---

## 📦 Auto Pan
- **XML Tag**: `AutoPan2`
- **Class**: `AutoPan`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Mode | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_Amount | 0.00 | 1.00 | 0.50 | % / Normalized |
| Modulation_Waveform | 0.00 | 8.00 | 0.00 | Linear |
| Modulation_Invert | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_TimeMode | 0.00 | 5.00 | 0.00 | Seconds |
| Modulation_Frequency | 0.10 | 60.00 | 1.00 | Hz (Log) |
| Modulation_Time | 0.10 | 200.00 | 1.00 | ms |
| Modulation_SyncedRate | 0.00 | 21.00 | 6.00 | Linear |
| Modulation_Sixteenth | 1.00 | 64.00 | 16.00 | Linear |
| Modulation_Phase | 0.00 | 360.00 | 180.00 | Linear |
| Modulation_PhaseOffset | 0.00 | 360.00 | 0.00 | Linear |
| Modulation_StereoMode | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_Spin | 0.00 | 0.50 | 0.00 | Linear |
| PanningWaveformShape | 0.00 | 1.00 | 0.00 | % / Normalized |
| TremoloWaveformShape | -1.00 | 1.00 | 0.00 | Linear |
| AttackTime | 0.00 | 5.00 | 0.00 | Seconds |
| DynamicFrequencyModulation | -1.00 | 1.00 | 0.00 | Hz (Log) |
| HarmonicMode | 0.00 | 1.00 | 0.00 | % / Normalized |
| VintageMode | 0.00 | 1.00 | 0.00 | % / Normalized |

---

## 📦 AutoShift
- **XML Tag**: `AutoShift`
- **Class**: `AutoShift`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Global_InputGain | -24.00 | 24.00 | 0.00 | dB |
| Global_DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| Global_UseScale | 0.00 | 1.00 | 0.00 | % / Normalized |
| MidiInput_Glide | 0.00 | 2.00 | 0.00 | Linear |
| MidiInput_PitchBendRange | 0.00 | 48.00 | 6.00 | Linear |
| MidiInput_AttackTime | 0.00 | 1.00 | 0.02 | Seconds |
| MidiInput_ReleaseTime | 0.00 | 5.00 | 0.02 | Seconds |
| MidiInput_Latch | 0.00 | 1.00 | 0.00 | % / Normalized |
| PitchShift_ShiftSemitones | -12.00 | 12.00 | 0.00 | Linear |
| PitchShift_ShiftScaleDegrees | -12.00 | 12.00 | 0.00 | Linear |
| PitchShift_Detune | -100.00 | 100.00 | 0.00 | Linear |
| PitchShift_FormantShift | -1.00 | 1.00 | 0.00 | Linear |
| PitchShift_FormantFollow | 0.00 | 1.00 | 0.00 | % / Normalized |
| Quantizer_Active | 0.00 | 1.00 | 1.00 | % / Normalized |
| Quantizer_Smooth | 0.00 | 1.00 | 1.00 | % / Normalized |
| Quantizer_SmoothingTime | 0.00 | 0.20 | 0.05 | Seconds |
| Quantizer_Amount | 0.00 | 1.00 | 1.00 | % / Normalized |
| Quantizer_RootNote | 0.00 | 11.00 | 0.00 | Linear |
| Quantizer_InternalScale | 0.00 | 36.00 | 0.00 | Linear |
| Lfo_Enabled | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lfo_OnsetRetrigger | 0.00 | 1.00 | 1.00 | % / Normalized |
| Lfo_Delay | 0.00 | 1.50 | 0.00 | Linear |
| Lfo_Attack | 0.00 | 2.00 | 0.00 | Seconds |
| Lfo_Waveform | 0.00 | 8.00 | 1.00 | Linear |
| Lfo_SyncOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lfo_RateHz | 0.01 | 20.00 | 0.50 | Linear |
| Lfo_SyncedRate | 0.00 | 21.00 | 12.00 | Linear |
| Vibrato_Attack | 0.00 | 2.00 | 0.00 | Seconds |
| Vibrato_RateHz | 2.00 | 15.00 | 6.00 | Linear |
| Vibrato_Amount | 0.00 | 200.00 | 0.00 | Linear |
| Vibrato_Humanization | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_LfoToPitchModAmount | 0.00 | 12.00 | 0.00 | Linear |
| Modulation_LfoToFormantModAmount | -1.00 | 1.00 | 0.00 | Linear |
| Modulation_LfoToVolumeModAmount | 0.00 | 1.00 | 0.00 | dB |
| Modulation_LfoToPanModAmount | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_MidiToPitchModSource | 0.00 | 6.00 | 0.00 | Linear |
| Modulation_MidiToFormantModSource | 0.00 | 6.00 | 0.00 | Linear |
| Modulation_MidiToVolumeModSource | 0.00 | 6.00 | 0.00 | dB |
| Modulation_MidiToPanModSource | 0.00 | 6.00 | 0.00 | Linear |
| Modulation_MidiToPitchModAmount | 0.00 | 12.00 | 0.00 | Linear |
| Modulation_MidiToFormantModAmount | -1.00 | 1.00 | 0.00 | Linear |
| Modulation_MidiToVolumeModAmount | 0.00 | 1.00 | 0.00 | dB |
| Modulation_MidiToPanModAmount | 0.00 | 1.00 | 0.00 | % / Normalized |

---

## 📦 BeatRepeat
- **XML Tag**: `BeatRepeat`
- **Class**: `BeatRepeat`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Chance | 0.00 | 1.00 | 1.00 | % / Normalized |
| Interval | 0.00 | 7.00 | 5.00 | Discrete/Enum |
| Offset | 0.00 | 15.00 | 0.00 | Linear |
| Grid | 0.00 | 15.00 | 7.00 | Discrete/Enum |
| BlockTripplets | 0.00 | 1.00 | 0.00 | % / Normalized |
| GridChance | 0.00 | 10.00 | 0.00 | Discrete/Enum |
| GridChanceType | 0.00 | 4.00 | 0.00 | Discrete/Enum |
| Gate | 0.00 | 18.00 | 6.00 | Linear |
| DampVolume | 0.00 | 1.00 | 0.00 | dB |
| DampPitch | 0.00 | 1.00 | 0.00 | % / Normalized |
| BasePitch | 0.00 | 12.00 | 0.00 | Linear |
| MixType | 0.00 | 2.00 | 0.00 | Discrete/Enum |
| WetLevel | 0.00 | 2.00 | 1.00 | Linear |
| FilterOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| MidFreq | 50.00 | 18000.00 | 1000.00 | Hz (Log) |
| BandWidth | 0.50 | 9.00 | 4.00 | Linear |
| InstantRepeat | 0.00 | 1.00 | 0.00 | % / Normalized |

---

## 📦 Cabinet
- **XML Tag**: `Cabinet`
- **Class**: `Cabinet`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| CabinetType | 0.00 | 4.00 | 0.00 | Discrete/Enum |
| MicrophoneTypeSwitch | 0.00 | 1.00 | 0.00 | Discrete/Enum |
| MicrophonePosition | 0.00 | 2.00 | 0.00 | Linear |
| DualMono | 0.00 | 1.00 | 0.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Channel EQ
- **XML Tag**: `ChannelEq`
- **Class**: `ChannelEq`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| HighpassOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| LowShelfGain | 0.18 | 5.60 | 1.00 | dB |
| MidGain | 0.25 | 4.00 | 1.00 | dB |
| MidFrequency | 120.00 | 7500.00 | 1500.00 | Hz (Log) |
| HighShelfGain | 0.18 | 5.60 | 1.00 | dB |
| Gain | 0.25 | 4.00 | 1.00 | dB |

---

## 📦 Chorus
- **XML Tag**: `Chorus2`
- **Class**: `Chorus`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Mode | 0.00 | 2.00 | 0.00 | Linear |
| Shaping | 0.00 | 1.00 | 0.00 | % / Normalized |
| Rate | 0.10 | 15.00 | 0.90 | Linear |
| Amount | 0.00 | 1.00 | 0.50 | % / Normalized |
| Feedback | 0.00 | 0.99 | 0.00 | Linear |
| InvertFeedback | 0.00 | 1.00 | 0.00 | % / Normalized |
| VibratoOffset | 0.00 | 180.00 | 0.00 | Linear |
| HighpassEnabled | 0.00 | 1.00 | 0.00 | % / Normalized |
| HighpassFrequency | 20.00 | 2000.00 | 50.00 | Hz (Log) |
| Width | 0.00 | 2.00 | 1.00 | Linear |
| Warmth | 0.00 | 1.00 | 0.00 | % / Normalized |
| OutputGain | 0.00 | 2.00 | 1.00 | dB |
| DryWet | 0.00 | 1.00 | 0.50 | % / Normalized |

---

## 📦 Chorus-Ensemble
- **XML Tag**: `Chorus2`
- **Class**: `Chorus`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Mode | 0.00 | 2.00 | 0.00 | Linear |
| Shaping | 0.00 | 1.00 | 0.00 | % / Normalized |
| Rate | 0.10 | 15.00 | 0.90 | Linear |
| Amount | 0.00 | 1.00 | 0.50 | % / Normalized |
| Feedback | 0.00 | 0.99 | 0.00 | Linear |
| InvertFeedback | 0.00 | 1.00 | 0.00 | % / Normalized |
| VibratoOffset | 0.00 | 180.00 | 0.00 | Linear |
| HighpassEnabled | 0.00 | 1.00 | 0.00 | % / Normalized |
| HighpassFrequency | 20.00 | 2000.00 | 50.00 | Hz (Log) |
| Width | 0.00 | 2.00 | 1.00 | Linear |
| Warmth | 0.00 | 1.00 | 0.00 | % / Normalized |
| OutputGain | 0.00 | 2.00 | 1.00 | dB |
| DryWet | 0.00 | 1.00 | 0.50 | % / Normalized |

---

## 📦 Compressor
- **XML Tag**: `Compressor2`
- **Class**: `Compressor`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Threshold | 0.00 | 2.00 | 1.00 | dB |
| Ratio | 1.00 | 340282326356119256160033759537265639424.00 | 4.00 | Hz (Log) |
| ExpansionRatio | 1.00 | 2.00 | 1.15 | Linear |
| Attack | 0.01 | 1000.00 | 1.00 | ms |
| Release | 1.00 | 3000.00 | 30.00 | Hz (Log) |
| AutoReleaseControlOnOff | 0.00 | 1.00 | 0.00 | Seconds |
| Gain | -36.00 | 36.00 | 0.00 | dB |
| GainCompensation | 0.00 | 1.00 | 0.00 | dB |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| Model | 0.00 | 2.00 | 1.00 | Linear |
| LegacyModel | 0.00 | 2.00 | 1.00 | Linear |
| LogEnvelope | 0.00 | 1.00 | 1.00 | % / Normalized |
| LegacyEnvFollowerMode | 0.00 | 2.00 | 0.00 | Linear |
| Knee | 0.00 | 18.00 | 6.00 | Linear |
| LookAhead | 0.00 | 2.00 | 0.00 | Linear |
| SideListen | 0.00 | 1.00 | 0.00 | % / Normalized |
| SideChainEq_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| SideChainEq_Mode | 0.00 | 5.00 | 5.00 | Linear |
| SideChainEq_Freq | 30.00 | 15000.00 | 80.00 | Hz (Log) |
| SideChainEq_Q | 0.10 | 12.00 | 0.71 | Linear |
| SideChainEq_Gain | -15.00 | 15.00 | 0.00 | dB |

---

## 📦 Corpus
- **XML Tag**: `Corpus`
- **Class**: `Corpus`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| ResonanceType | 0.00 | 6.00 | 0.00 | Discrete/Enum |
| ResonatorQuality | 0.00 | 3.00 | 2.00 | Linear |
| Frequency | 0.00 | 1.00 | 0.50 | Hz (Log) |
| Transpose | -48.00 | 48.00 | 0.00 | Linear |
| FineTranspose | -50.00 | 50.00 | 0.00 | Linear |
| Detune | -1.00 | 1.00 | 0.00 | Linear |
| Decay | 0.00 | 1.00 | 0.50 | Seconds |
| FreqDamping | -1.00 | 1.00 | 0.00 | Hz (Log) |
| Radius | 0.00 | 1.00 | 0.50 | % / Normalized |
| AmpFreq | -1.00 | 1.00 | 0.00 | Hz (Log) |
| Inharmonics | -1.00 | 1.00 | 0.00 | Linear |
| TubeOpening | 0.00 | 1.00 | 1.00 | % / Normalized |
| Ratio | 0.00 | 1.00 | 0.50 | % / Normalized |
| ExcitationX | 0.00 | 1.00 | 0.50 | % / Normalized |
| ListeningXL | 0.00 | 1.00 | 0.10 | % / Normalized |
| ListeningXR | 0.00 | 1.00 | 0.90 | % / Normalized |
| LfoOnOff | 0.00 | 1.00 | 0.00 | % / Normalized |
| LfoType | 0.00 | 6.00 | 0.00 | Discrete/Enum |
| LfoSync | 0.00 | 1.00 | 0.00 | % / Normalized |
| LfoRate | 0.00 | 1.00 | 0.50 | % / Normalized |
| LfoSyncRate | 0.00 | 21.00 | 4.00 | Linear |
| LfoStereoMode | 0.00 | 1.00 | 0.00 | % / Normalized |
| LfoSpin | 0.00 | 0.50 | 0.00 | Linear |
| LfoPhase | 0.00 | 360.00 | 180.00 | Linear |
| LfoOffset | 0.00 | 360.00 | 0.00 | Linear |
| LfoAmount | 0.00 | 1.00 | 0.00 | % / Normalized |
| FilterOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| FilterMidFreq | 50.00 | 18000.00 | 1000.00 | Hz (Log) |
| FilterBandWidth | 0.50 | 9.00 | 4.00 | Linear |
| MidiPitch | 0.00 | 1.00 | 0.00 | % / Normalized |
| MidiMode | 0.00 | 1.00 | 0.00 | % / Normalized |
| PitchBendRange | 0.00 | 24.00 | 5.00 | Linear |
| MidiGate | 0.00 | 1.00 | 0.00 | % / Normalized |
| DecayOnNoteOff | 0.00 | 1.00 | 0.00 | Seconds |
| Drive | 0.00 | 1.00 | 0.50 | % / Normalized |
| StereoWidth | 0.00 | 1.00 | 1.00 | % / Normalized |
| Bleed | 0.00 | 1.00 | 0.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 0.50 | % / Normalized |

---

## 📦 Delay
- **XML Tag**: `Delay`
- **Class**: `Delay`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| DelayLine_SmoothingMode | 0.00 | 2.00 | 0.00 | Linear |
| DelayLine_Link | 0.00 | 1.00 | 1.00 | % / Normalized |
| DelayLine_PingPong | 0.00 | 1.00 | 0.00 | % / Normalized |
| DelayLine_SyncL | 0.00 | 1.00 | 1.00 | % / Normalized |
| DelayLine_SyncR | 0.00 | 1.00 | 1.00 | % / Normalized |
| DelayLine_TimeL | 0.00 | 5.00 | 0.37 | Seconds |
| DelayLine_TimeR | 0.00 | 5.00 | 0.37 | Seconds |
| DelayLine_SimpleDelayTimeL | 1.00 | 300.00 | 100.00 | ms |
| DelayLine_SimpleDelayTimeR | 1.00 | 300.00 | 100.00 | ms |
| DelayLine_PingPongDelayTimeL | 1.00 | 999.00 | 1.00 | ms |
| DelayLine_PingPongDelayTimeR | 1.00 | 999.00 | 1.00 | ms |
| DelayLine_SyncedSixteenthL | 0.00 | 7.00 | 2.00 | Linear |
| DelayLine_SyncedSixteenthR | 0.00 | 7.00 | 3.00 | Linear |
| DelayLine_OffsetL | -0.33 | 0.33 | 0.00 | Linear |
| DelayLine_OffsetR | -0.33 | 0.33 | 0.00 | Linear |
| Feedback | 0.00 | 0.95 | 0.50 | Linear |
| Freeze | 0.00 | 1.00 | 0.00 | % / Normalized |
| Filter_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Filter_Frequency | 50.00 | 18000.01 | 1000.00 | Hz (Log) |
| Filter_Bandwidth | 0.50 | 9.00 | 8.00 | Linear |
| Modulation_Frequency | 0.01 | 40.00 | 0.50 | Hz (Log) |
| Modulation_AmountTime | 0.00 | 1.00 | 0.00 | Seconds |
| Modulation_AmountFilter | 0.00 | 1.00 | 0.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 0.50 | % / Normalized |

---

## 📦 Drum Buss
- **XML Tag**: `DrumBuss`
- **Class**: `DrumBuss`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| EnableCompression | 0.00 | 1.00 | 0.00 | % / Normalized |
| DriveAmount | 0.00 | 1.00 | 0.20 | % / Normalized |
| DriveType | 0.00 | 2.00 | 0.00 | Discrete/Enum |
| CrunchAmount | 0.00 | 1.00 | 0.00 | % / Normalized |
| DampingFrequency | 500.00 | 20000.00 | 9200.00 | Hz (Log) |
| TransientShaping | -1.00 | 1.00 | 0.00 | Linear |
| BoomFrequency | 30.00 | 90.00 | 50.00 | Hz (Log) |
| BoomAmount | 0.00 | 1.00 | 0.00 | % / Normalized |
| BoomDecay | 0.00 | 1.00 | 1.00 | Seconds |
| BoomAudition | 0.00 | 1.00 | 0.00 | % / Normalized |
| InputTrim | 0.00 | 1.00 | 1.00 | Linear |
| OutputGain | 0.01 | 1.41 | 1.00 | dB |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Dynamic Tube
- **XML Tag**: `Tube`
- **Class**: `Tube`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| PreDrive | -15.00 | 15.00 | 0.00 | Linear |
| PostDrive | -15.00 | 15.00 | 0.00 | Linear |
| Bias | 0.00 | 1.00 | 0.00 | % / Normalized |
| AutoBias | -3.00 | 3.00 | 0.00 | Linear |
| AutoBiasAttack | 1.00 | 400.00 | 5.00 | ms |
| AutoBiasRelease | 1.00 | 1500.00 | 35.00 | Hz (Log) |
| Tone | -1.00 | 1.00 | 0.00 | Linear |
| Type | 0.00 | 2.00 | 0.00 | Discrete/Enum |

---

## 📦 EQ Eight
- **XML Tag**: `Eq8`
- **Class**: `Eq8`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| GlobalGain | -12.00 | 12.00 | 0.00 | dB |
| Scale | -2.00 | 2.00 | 1.00 | Linear |
| AdaptiveQ | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 EQ Three
- **XML Tag**: `FilterEQ3`
- **Class**: `FilterEQ3`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| GainLo | 0.00 | 2.00 | 1.00 | dB |
| GainMid | 0.00 | 2.00 | 1.00 | dB |
| GainHi | 0.00 | 2.00 | 1.00 | dB |
| FreqLo | 50.00 | 5000.00 | 250.00 | Hz (Log) |
| FreqHi | 200.00 | 18000.00 | 2500.00 | Hz (Log) |
| LowOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| MidOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| HighOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| Slope | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Echo
- **XML Tag**: `Echo`
- **Class**: `Echo`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Delay_SyncL | 0.00 | 1.00 | 1.00 | % / Normalized |
| Delay_TimeL | 0.00 | 2.50 | 0.38 | Seconds |
| Delay_SyncedDivisionL | -6.00 | 0.00 | -3.00 | Linear |
| Delay_SyncedSixteenthL | 1.00 | 16.00 | 3.00 | Linear |
| Delay_SyncModeL | 0.00 | 3.00 | 2.00 | Linear |
| Delay_OffsetL | -0.33 | 0.33 | 0.00 | Linear |
| Delay_TimeR | 0.00 | 2.50 | 0.38 | Seconds |
| Delay_SyncR | 0.00 | 1.00 | 1.00 | % / Normalized |
| Delay_SyncedDivisionR | -6.00 | 0.00 | -3.00 | Linear |
| Delay_SyncedSixteenthR | 1.00 | 16.00 | 3.00 | Linear |
| Delay_SyncModeR | 0.00 | 3.00 | 2.00 | Linear |
| Delay_OffsetR | -0.33 | 0.33 | 0.00 | Linear |
| Delay_TimeLink | 0.00 | 1.00 | 1.00 | Seconds |
| Delay_Repitch | 0.00 | 1.00 | 1.00 | % / Normalized |
| Delay_RepitchSmoothingTime | 0.01 | 1.00 | 0.40 | Seconds |
| Feedback | 0.00 | 1.50 | 0.50 | Linear |
| FeedbackInvert | 0.00 | 1.00 | 0.00 | % / Normalized |
| ChannelMode | 0.00 | 2.00 | 0.00 | Linear |
| InputGain | -40.00 | 40.00 | 0.00 | dB |
| OutputGain | 0.00 | 4.00 | 1.00 | dB |
| Clipper_Dry | 0.00 | 1.00 | 0.00 | % / Normalized |
| Gate_On | 0.00 | 1.00 | 0.00 | % / Normalized |
| Gate_Threshold | -60.00 | 0.00 | 0.00 | dB |
| Gate_Release | 0.00 | 3.00 | 0.05 | Seconds |
| Ducking_On | 0.00 | 1.00 | 0.00 | % / Normalized |
| Ducking_Threshold | -60.00 | 0.00 | 0.00 | dB |
| Ducking_Release | 0.02 | 1.50 | 0.10 | Seconds |
| Filter_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Filter_HighPassFrequency | 20.00 | 20000.00 | 50.00 | Hz (Log) |
| Filter_HighPassResonance | 0.00 | 0.30 | 0.00 | Linear |
| Filter_LowPassFrequency | 20.00 | 20000.00 | 5000.00 | Hz (Log) |
| Filter_LowPassResonance | 0.00 | 0.30 | 0.00 | Linear |
| Modulation_Waveform | 0.00 | 5.00 | 0.00 | Linear |
| Modulation_Frequency | 0.01 | 40.00 | 2.00 | Hz (Log) |
| Modulation_Sync | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_SyncedRate | 0.00 | 21.00 | 12.00 | Linear |
| Modulation_PhaseOffset | 0.00 | 180.00 | 90.00 | Linear |
| Modulation_EnvelopeMix | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_AmountDelay | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_AmountFilter | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_AmountDelayTimesFour | 0.00 | 1.00 | 0.00 | Seconds |
| Reverb_Level | 0.00 | 1.00 | 0.00 | % / Normalized |
| Reverb_Decay | 0.00 | 1.00 | 0.50 | Seconds |
| Reverb_Location | 0.00 | 2.00 | 1.00 | Linear |
| Noise_On | 0.00 | 1.00 | 0.00 | % / Normalized |
| Noise_Amount | 0.00 | 1.00 | 0.00 | % / Normalized |
| Noise_Type | 0.00 | 1.00 | 0.00 | Discrete/Enum |
| Wobble_On | 0.00 | 1.00 | 0.00 | % / Normalized |
| Wobble_Amount | 0.00 | 1.00 | 0.00 | % / Normalized |
| Wobble_Type | 0.00 | 1.00 | 0.00 | Discrete/Enum |
| StereoWidth | 0.00 | 2.00 | 1.00 | Linear |
| DryWet | 0.00 | 1.00 | 0.70 | % / Normalized |

---

## 📦 Erosion
- **XML Tag**: `Erosion`
- **Class**: `Erosion`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Mode | 0.00 | 2.00 | 2.00 | Linear |
| Freq | 300.00 | 18000.00 | 5450.00 | Hz (Log) |
| Amplitude | 0.00 | 200.00 | 0.00 | Linear |
| BandQ | 0.10 | 2.50 | 0.30 | Linear |

---

## 📦 Filter Delay
- **XML Tag**: `FilterDelay`
- **Class**: `FilterDelay`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| On1 | 0.00 | 1.00 | 1.00 | % / Normalized |
| FilterOn1 | 0.00 | 1.00 | 1.00 | % / Normalized |
| MidFreq1 | 50.00 | 18000.00 | 704.00 | Hz (Log) |
| BandWidth1 | 0.50 | 9.00 | 4.00 | Linear |
| DelayTimeSwitch1 | 0.00 | 1.00 | 1.00 | Seconds |
| BeatDelayEnum1 | 0.00 | 7.00 | 2.00 | Linear |
| BeatDelayOffset1 | -0.33 | 0.33 | 0.00 | Linear |
| DelayTime1 | 1.00 | 999.00 | 10.00 | ms |
| Feedback1 | 0.00 | 1.00 | 0.21 | % / Normalized |
| Pan1 | -1.00 | 1.00 | -1.00 | Linear |
| Volume1 | 0.00 | 2.00 | 1.58 | dB |
| On2 | 0.00 | 1.00 | 1.00 | % / Normalized |
| FilterOn2 | 0.00 | 1.00 | 1.00 | % / Normalized |
| MidFreq2 | 50.00 | 18000.00 | 449.00 | Hz (Log) |
| BandWidth2 | 0.50 | 9.00 | 4.00 | Linear |
| DelayTimeSwitch2 | 0.00 | 1.00 | 1.00 | Seconds |
| BeatDelayEnum2 | 0.00 | 7.00 | 0.00 | Linear |
| BeatDelayOffset2 | -0.33 | 0.33 | 0.00 | Linear |
| DelayTime2 | 1.00 | 999.00 | 10.00 | ms |
| Feedback2 | 0.00 | 1.00 | 0.46 | % / Normalized |
| Pan2 | -1.00 | 1.00 | 0.00 | Linear |
| Volume2 | 0.00 | 2.00 | 0.63 | dB |
| On3 | 0.00 | 1.00 | 1.00 | % / Normalized |
| FilterOn3 | 0.00 | 1.00 | 1.00 | % / Normalized |
| MidFreq3 | 50.00 | 18000.00 | 918.00 | Hz (Log) |
| BandWidth3 | 0.50 | 9.00 | 4.00 | Linear |
| DelayTimeSwitch3 | 0.00 | 1.00 | 1.00 | Seconds |
| BeatDelayEnum3 | 0.00 | 7.00 | 4.00 | Linear |
| BeatDelayOffset3 | -0.33 | 0.33 | 0.00 | Linear |
| DelayTime3 | 1.00 | 999.00 | 10.00 | ms |
| Feedback3 | 0.00 | 1.00 | 0.24 | % / Normalized |
| Pan3 | -1.00 | 1.00 | 1.00 | Linear |
| Volume3 | 0.00 | 2.00 | 2.00 | dB |
| DryVolume | 0.00 | 1.00 | 0.56 | dB |

---

## 📦 Gate
- **XML Tag**: `Gate`
- **Class**: `Gate`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Threshold | 0.00 | 2.00 | 0.25 | dB |
| Attack | 0.02 | 150.00 | 3.50 | ms |
| Hold | 1.00 | 1500.00 | 10.00 | Hz (Log) |
| Release | 0.10 | 3000.00 | 15.00 | Hz (Log) |
| Return | 0.00 | 24.00 | 3.00 | Linear |
| Gain | -75.00 | 0.00 | -40.00 | dB |
| SideListen | 0.00 | 1.00 | 0.00 | % / Normalized |
| FlipMode | 0.00 | 1.00 | 0.00 | % / Normalized |
| LookAhead | 0.00 | 2.00 | 1.00 | Linear |

---

## 📦 Glue Compressor
- **XML Tag**: `GlueCompressor`
- **Class**: `GlueCompressor`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Threshold | -40.00 | 0.00 | 0.00 | dB |
| Range | 0.00 | 70.00 | 70.00 | Linear |
| Makeup | 0.00 | 20.00 | 0.00 | Linear |
| Attack | 0.00 | 6.00 | 3.00 | Seconds |
| Ratio | 0.00 | 2.00 | 1.00 | Linear |
| Release | 0.00 | 6.00 | 3.00 | Seconds |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| PeakClipIn | 0.00 | 1.00 | 0.00 | % / Normalized |

---

## 📦 Grain Delay
- **XML Tag**: `GrainDelay`
- **Class**: `GrainDelay`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Spray | 0.00 | 500.00 | 0.00 | Linear |
| Freq | 1.00 | 150.00 | 60.00 | Hz (Log) |
| Pitch | -36.00 | 12.00 | 0.00 | Linear |
| RandomPitch | 0.00 | 161.20 | 0.00 | Linear |
| Feedback | 0.00 | 0.95 | 0.00 | Linear |
| NewDryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| SyncMode | 0.00 | 1.00 | 1.00 | % / Normalized |
| BeatDelayEnum | 0.00 | 7.00 | 1.00 | Linear |
| BarDelayOffset | -0.33 | 0.33 | 0.00 | Linear |
| MsDelay | 1.00 | 128.00 | 40.00 | Linear |

---

## 📦 Hybrid
- **XML Tag**: `Hybrid`
- **Class**: `Hybrid`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| PreDelay_Sync | 0.00 | 1.00 | 0.00 | % / Normalized |
| PreDelay_Time | 0.00 | 4.00 | 0.01 | Seconds |
| PreDelay_Sixteenth | 0.00 | 16.00 | 2.00 | Linear |
| PreDelay_FeedbackTime | 0.00 | 0.95 | 0.00 | Seconds |
| PreDelay_FeedbackSixteenth | 0.00 | 0.95 | 0.00 | Linear |
| Algorithm_Type | 0.00 | 4.00 | 0.00 | Discrete/Enum |
| Algorithm_Delay | 0.00 | 1.00 | 0.00 | % / Normalized |
| Algorithm_Freeze | 0.00 | 1.00 | 0.00 | % / Normalized |
| Algorithm_FreezeIn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Algorithm_Decay | 0.10 | 60.00 | 3.50 | Seconds |
| Algorithm_Size | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_Damping | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_Diffusion | 0.00 | 1.00 | 1.00 | % / Normalized |
| Algorithm_Modulation | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_Shape | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_BassMultiplier | 0.25 | 4.00 | 1.00 | Linear |
| Algorithm_BassCrossover | 80.00 | 1000.00 | 440.00 | Linear |
| Algorithm_Shimmer | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_PitchShift | -12.00 | 12.00 | 12.00 | Linear |
| Algorithm_TidesAmount | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_TidesRate | 0.00 | 29.00 | 22.00 | Linear |
| Algorithm_TidesWaveform | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_TidesPhaseOffset | 0.00 | 180.00 | 90.00 | Linear |
| Algorithm_Quartz_LowDamping | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_Quartz_Distance | 0.00 | 1.00 | 0.50 | % / Normalized |
| Algorithm_Prism_HighMultiplier | 0.10 | 5.00 | 1.00 | Linear |
| Algorithm_Prism_LowMultiplier | 0.10 | 5.00 | 1.00 | Linear |
| Algorithm_Prism_CrossoverFrequency | 400.00 | 5500.00 | 800.00 | Hz (Log) |
| Algorithm_Prism_Sixth | 0.00 | 1.00 | 0.00 | % / Normalized |
| Algorithm_Prism_Seventh | 0.00 | 1.00 | 0.00 | % / Normalized |
| Eq_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Eq_PreAlgo | 0.00 | 1.00 | 0.00 | % / Normalized |
| Eq_LowBandType | 0.00 | 1.00 | 0.00 | Discrete/Enum |
| Eq_LowBandFrequency | 20.00 | 20000.00 | 80.00 | Hz (Log) |
| Eq_LowBandGain | 0.25 | 4.00 | 1.00 | dB |
| Eq_LowBandSlope | 0.00 | 9.00 | 1.00 | Linear |
| Eq_Peak1Frequency | 20.00 | 20000.00 | 700.00 | Hz (Log) |
| Eq_Peak1Gain | 0.25 | 4.00 | 1.00 | dB |
| Eq_Peak1Q | 0.10 | 4.00 | 0.71 | Linear |
| Eq_Peak2Frequency | 20.00 | 20000.00 | 1500.00 | Hz (Log) |
| Eq_Peak2Gain | 0.25 | 4.00 | 1.00 | dB |
| Eq_Peak2Q | 0.10 | 4.00 | 0.71 | Linear |
| Eq_HighBandType | 0.00 | 1.00 | 1.00 | Discrete/Enum |
| Eq_HighBandFrequency | 20.00 | 20000.00 | 5000.00 | Hz (Log) |
| Eq_HighBandGain | 0.25 | 4.00 | 1.00 | dB |
| Eq_HighBandSlope | 0.00 | 9.00 | 4.00 | Linear |
| Send | 0.00 | 1.00 | 1.00 | % / Normalized |
| Routing | 0.00 | 3.00 | 1.00 | Linear |
| ConvoAlgoBlend | 0.00 | 1.00 | 0.50 | % / Normalized |
| Vintage | 0.00 | 4.00 | 0.00 | Linear |
| StereoWidth | 0.00 | 2.00 | 1.00 | Linear |
| BassMono | 0.00 | 1.00 | 0.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 0.50 | % / Normalized |

---

## 📦 Limiter
- **XML Tag**: `Limiter`
- **Class**: `Limiter`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Gain | -24.00 | 24.00 | 0.00 | dB |
| Ceiling | -24.00 | 0.00 | -0.30 | Linear |
| Release | 0.01 | 3000.00 | 100.00 | Hz (Log) |
| AutoRelease | 0.00 | 1.00 | 0.00 | Seconds |
| LinkAmount | 0.00 | 1.00 | 1.00 | % / Normalized |
| LinkAmountMidSide | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lookahead | 0.00 | 2.00 | 0.00 | Linear |
| Routing | 0.00 | 1.00 | 0.00 | % / Normalized |
| Mode | 0.00 | 2.00 | 0.00 | Linear |
| Maximize | 0.00 | 1.00 | 0.00 | % / Normalized |
| MaximizeThreshold | -24.00 | 0.00 | -0.30 | dB |
| MaximizeOutput | -24.00 | 0.00 | 0.00 | Linear |

---

## 📦 Looper
- **XML Tag**: `Looper`
- **Class**: `Looper`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| State | 0.00 | 3.00 | 0.00 | Linear |
| Feedback | 0.00 | 1.00 | 1.00 | % / Normalized |
| Reverse | 0.00 | 1.00 | 0.00 | % / Normalized |
| Monitor | 0.00 | 3.00 | 0.00 | Linear |
| Pitch | -36.00 | 36.00 | 0.00 | Linear |
| LocalQuantization | 0.00 | 14.00 | 0.00 | Linear |
| SongControl | 0.00 | 2.00 | 1.00 | Linear |
| TempoControl | 0.00 | 2.00 | 2.00 | Linear |

---

## 📦 Multiband Dynamics
- **XML Tag**: `MultibandDynamics`
- **Class**: `MultibandDynamics`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| SplitLowMid | 30.00 | 3000.00 | 120.00 | Hz (Log) |
| SplitMidHigh | 300.00 | 15000.00 | 2500.00 | Hz (Log) |
| SoftKnee | 0.00 | 1.00 | 1.00 | % / Normalized |
| EnvelopeIsPeak | 0.00 | 1.00 | 0.00 | % / Normalized |
| OutputGain | -24.00 | 24.00 | 0.00 | dB |
| GlobalAmount | 0.00 | 1.00 | 1.00 | % / Normalized |
| GlobalTime | 0.10 | 10.00 | 1.00 | Seconds |
| GainLow | -24.00 | 24.00 | 0.00 | dB |
| GainMid | -24.00 | 24.00 | 0.00 | dB |
| GainHigh | -24.00 | 24.00 | 0.00 | dB |
| InputGainLow | -24.00 | 24.00 | 0.00 | dB |
| InputGainMid | -24.00 | 24.00 | 0.00 | dB |
| InputGainHigh | -24.00 | 24.00 | 0.00 | dB |
| ActiveLow | 0.00 | 1.00 | 1.00 | % / Normalized |
| ActiveMid | 0.00 | 1.00 | 1.00 | % / Normalized |
| ActiveHigh | 0.00 | 1.00 | 1.00 | % / Normalized |
| AboveThresholdLow | -80.00 | 0.00 | -20.00 | dB |
| AboveThresholdMid | -80.00 | 0.00 | -20.00 | dB |
| AboveThresholdHigh | -80.00 | 0.00 | -20.00 | dB |
| BelowThresholdLow | -80.00 | 0.00 | -60.00 | dB |
| BelowThresholdMid | -80.00 | 0.00 | -60.00 | dB |
| BelowThresholdHigh | -80.00 | 0.00 | -60.00 | dB |
| AboveRatioLow | -1.00 | 1.00 | 0.00 | Linear |
| AboveRatioMid | -1.00 | 1.00 | 0.00 | Linear |
| AboveRatioHigh | -1.00 | 1.00 | 0.00 | Linear |
| BelowRatioLow | -3.00 | 1.00 | 0.00 | Linear |
| BelowRatioMid | -3.00 | 1.00 | 0.00 | Linear |
| BelowRatioHigh | -3.00 | 1.00 | 0.00 | Linear |
| AttackLow | 0.10 | 5000.00 | 50.00 | Hz (Log) |
| AttackMid | 0.10 | 5000.00 | 10.00 | Hz (Log) |
| AttackHigh | 0.10 | 5000.00 | 5.00 | Hz (Log) |
| ReleaseLow | 0.10 | 5000.00 | 300.00 | Hz (Log) |
| ReleaseMid | 0.10 | 5000.00 | 200.00 | Hz (Log) |
| ReleaseHigh | 0.10 | 5000.00 | 100.00 | Hz (Log) |

---

## 📦 Overdrive
- **XML Tag**: `Overdrive`
- **Class**: `Overdrive`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| MidFreq | 50.00 | 20000.00 | 1250.00 | Hz (Log) |
| BandWidth | 0.50 | 9.00 | 6.50 | Linear |
| Drive | 0.00 | 100.00 | 50.00 | Linear |
| DryWet | 0.00 | 100.00 | 50.00 | Linear |
| Tone | 0.00 | 100.00 | 50.00 | Linear |
| PreserveDynamics | 0.00 | 1.00 | 0.50 | % / Normalized |

---

## 📦 Pedal
- **XML Tag**: `Pedal`
- **Class**: `Pedal`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Type | 0.00 | 2.00 | 0.00 | Discrete/Enum |
| Gain | 0.00 | 1.00 | 0.00 | dB |
| Output | -20.00 | 20.00 | 0.00 | Linear |
| Bass | -1.00 | 1.00 | 0.00 | Linear |
| Mid | -1.00 | 1.00 | 0.00 | Linear |
| Treble | -1.00 | 1.00 | 0.00 | Linear |
| MidFreq | 0.00 | 2.00 | 1.00 | Hz (Log) |
| Sub | 0.00 | 1.00 | 0.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Phaser
- **XML Tag**: `PhaserNew`
- **Class**: `Phaser`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_Amount | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_Waveform | 0.00 | 9.00 | 1.00 | Linear |
| Modulation_Frequency | 0.01 | 40.00 | 0.20 | Hz (Log) |
| Modulation_Frequency2 | 0.01 | 40.00 | 0.20 | Hz (Log) |
| Modulation_Sync | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_Sync2 | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_SyncedRate | 0.00 | 21.00 | 4.00 | Linear |
| Modulation_SyncedRate2 | 0.00 | 21.00 | 4.00 | Linear |
| Modulation_PhaseOffset | 0.00 | 360.00 | 180.00 | Linear |
| Modulation_SpinEnabled | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_Spin | 0.00 | 0.50 | 0.00 | Linear |
| Modulation_DutyCycle | -1.00 | 1.00 | 0.00 | Linear |
| Modulation_LfoBlend | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_EnvelopeEnabled | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_EnvelopeAmount | -1.00 | 1.00 | 0.00 | Linear |
| Modulation_EnvelopeAttack | 0.00 | 0.03 | 0.01 | Seconds |
| Modulation_EnvelopeRelease | 0.00 | 0.40 | 0.20 | Seconds |
| Mode | 0.00 | 2.00 | 0.00 | Linear |
| Notches | 1.00 | 42.00 | 4.00 | Linear |
| FlangerDelayTime | 0.00 | 0.02 | 0.00 | Seconds |
| DoublerDelayTime | 0.02 | 0.15 | 0.08 | Seconds |
| ModulationBlend | 0.00 | 1.00 | 0.00 | % / Normalized |
| CenterFrequency | 70.00 | 18500.00 | 1000.00 | Hz (Log) |
| Spread | 0.00 | 1.00 | 0.50 | % / Normalized |
| Feedback | 0.00 | 0.99 | 0.00 | Linear |
| Warmth | 0.00 | 1.00 | 0.00 | % / Normalized |
| SafeBassFrequency | 5.00 | 3000.00 | 100.00 | Hz (Log) |
| InvertWet | 0.00 | 1.00 | 0.00 | % / Normalized |
| OutputGain | 0.00 | 2.00 | 1.00 | dB |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Phaser-Flanger
- **XML Tag**: `PhaserNew`
- **Class**: `Phaser`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_Amount | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_Waveform | 0.00 | 9.00 | 1.00 | Linear |
| Modulation_Frequency | 0.01 | 40.00 | 0.20 | Hz (Log) |
| Modulation_Frequency2 | 0.01 | 40.00 | 0.20 | Hz (Log) |
| Modulation_Sync | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_Sync2 | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_SyncedRate | 0.00 | 21.00 | 4.00 | Linear |
| Modulation_SyncedRate2 | 0.00 | 21.00 | 4.00 | Linear |
| Modulation_PhaseOffset | 0.00 | 360.00 | 180.00 | Linear |
| Modulation_SpinEnabled | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_Spin | 0.00 | 0.50 | 0.00 | Linear |
| Modulation_DutyCycle | -1.00 | 1.00 | 0.00 | Linear |
| Modulation_LfoBlend | 0.00 | 1.00 | 0.00 | % / Normalized |
| Modulation_EnvelopeEnabled | 0.00 | 1.00 | 1.00 | % / Normalized |
| Modulation_EnvelopeAmount | -1.00 | 1.00 | 0.00 | Linear |
| Modulation_EnvelopeAttack | 0.00 | 0.03 | 0.01 | Seconds |
| Modulation_EnvelopeRelease | 0.00 | 0.40 | 0.20 | Seconds |
| Mode | 0.00 | 2.00 | 0.00 | Linear |
| Notches | 1.00 | 42.00 | 4.00 | Linear |
| FlangerDelayTime | 0.00 | 0.02 | 0.00 | Seconds |
| DoublerDelayTime | 0.02 | 0.15 | 0.08 | Seconds |
| ModulationBlend | 0.00 | 1.00 | 0.00 | % / Normalized |
| CenterFrequency | 70.00 | 18500.00 | 1000.00 | Hz (Log) |
| Spread | 0.00 | 1.00 | 0.50 | % / Normalized |
| Feedback | 0.00 | 0.99 | 0.00 | Linear |
| Warmth | 0.00 | 1.00 | 0.00 | % / Normalized |
| SafeBassFrequency | 5.00 | 3000.00 | 100.00 | Hz (Log) |
| InvertWet | 0.00 | 1.00 | 0.00 | % / Normalized |
| OutputGain | 0.00 | 2.00 | 1.00 | dB |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Redux
- **XML Tag**: `Redux2`
- **Class**: `Redux`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| SampleRate | 20.00 | 40000.00 | 40000.00 | Hz (Log) |
| Jitter | 0.00 | 1.00 | 0.00 | % / Normalized |
| BitDepth | 1.00 | 16.00 | 16.00 | Linear |
| QuantizerShape | 0.00 | 1.00 | 0.00 | % / Normalized |
| QuantizerDcShift | 0.00 | 1.00 | 0.00 | % / Normalized |
| EnablePreFilter | 0.00 | 1.00 | 0.00 | % / Normalized |
| EnablePostFilter | 0.00 | 1.00 | 0.00 | % / Normalized |
| PostFilterValue | -4.00 | 4.00 | 0.00 | Linear |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Resonator
- **XML Tag**: `Resonator`
- **Class**: `Resonator`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| InFilterOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| InFilterFreq | 50.00 | 8000.00 | 500.00 | Hz (Log) |
| InFilterMode | 0.00 | 3.00 | 2.00 | Linear |
| ResMode | 0.00 | 1.00 | 1.00 | % / Normalized |
| ResDecay | 0.00 | 100.00 | 50.00 | ms |
| ResConst | 0.00 | 1.00 | 1.00 | % / Normalized |
| ResColor | 0.00 | 100.00 | 90.00 | Linear |
| Width | 0.00 | 1.00 | 1.00 | % / Normalized |
| DryWet | 0.00 | 1.00 | 0.50 | % / Normalized |
| GlobalGain | -15.00 | 15.00 | 0.00 | dB |
| UseCurrentScale | 0.00 | 1.00 | 0.00 | % / Normalized |
| ResOn1 | 0.00 | 1.00 | 1.00 | % / Normalized |
| ResNote | 12.00 | 84.00 | 48.00 | Linear |
| ResNoteScaleDegrees | -21.00 | 21.00 | 0.00 | Linear |
| ResTune1 | -50.00 | 50.00 | 0.00 | Linear |
| ResGain1 | 0.00 | 2.00 | 1.00 | dB |
| ResOn2 | 0.00 | 1.00 | 1.00 | % / Normalized |
| ResPitch2 | -24.00 | 24.00 | 0.00 | Linear |
| ResPitchScaleDegrees2 | -21.00 | 21.00 | 0.00 | Linear |
| ResTune2 | -50.00 | 50.00 | 0.00 | Linear |
| ResGain2 | 0.00 | 2.00 | 1.00 | dB |
| ResOn3 | 0.00 | 1.00 | 1.00 | % / Normalized |
| ResPitch3 | -24.00 | 24.00 | 0.00 | Linear |
| ResPitchScaleDegrees3 | -21.00 | 21.00 | 0.00 | Linear |
| ResTune3 | -50.00 | 50.00 | 0.00 | Linear |
| ResGain3 | 0.00 | 2.00 | 1.00 | dB |
| ResOn4 | 0.00 | 1.00 | 1.00 | % / Normalized |
| ResPitch4 | -24.00 | 24.00 | 0.00 | Linear |
| ResPitchScaleDegrees4 | -21.00 | 21.00 | 0.00 | Linear |
| ResTune4 | -50.00 | 50.00 | 0.00 | Linear |
| ResGain4 | 0.00 | 2.00 | 1.00 | dB |
| ResOn5 | 0.00 | 1.00 | 1.00 | % / Normalized |
| ResPitch5 | -24.00 | 24.00 | 0.00 | Linear |
| ResPitchScaleDegrees5 | -21.00 | 21.00 | 0.00 | Linear |
| ResTune5 | -50.00 | 50.00 | 0.00 | Linear |
| ResGain5 | 0.00 | 2.00 | 1.00 | dB |

---

## 📦 Reverb
- **XML Tag**: `Reverb`
- **Class**: `Reverb`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| PreDelay | 0.50 | 250.00 | 2.50 | Linear |
| BandHighOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| BandLowOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| BandFreq | 50.00 | 18000.01 | 830.00 | Hz (Log) |
| BandWidth | 0.50 | 9.00 | 5.85 | Linear |
| SpinOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| EarlyReflectModFreq | 0.07 | 1.30 | 0.30 | Hz (Log) |
| EarlyReflectModDepth | 2.00 | 55.00 | 17.50 | Linear |
| DiffuseDelay | 0.00 | 1.00 | 0.50 | % / Normalized |
| ShelfHighOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| HighFilterType | 0.00 | 1.00 | 0.00 | Discrete/Enum |
| ShelfHiFreq | 20.00 | 16000.00 | 4500.00 | Hz (Log) |
| ShelfHiGain | 0.20 | 1.00 | 0.70 | dB |
| ShelfLowOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| ShelfLoFreq | 20.00 | 15000.00 | 90.00 | Hz (Log) |
| ShelfLoGain | 0.20 | 1.00 | 0.75 | dB |
| ChorusOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| SizeModFreq | 0.01 | 8.00 | 0.02 | Hz (Log) |
| SizeModDepth | 0.01 | 4.00 | 0.02 | Linear |
| DecayTime | 200.00 | 60000.00 | 1200.00 | Hz (Log) |
| AllPassGain | 0.00 | 0.96 | 0.60 | dB |
| AllPassSize | 0.05 | 1.00 | 0.40 | Linear |
| FreezeOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| FlatOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| CutOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| RoomSize | 0.22 | 500.00 | 100.00 | Linear |
| SizeSmoothing | 0.00 | 2.00 | 2.00 | Linear |
| StereoSeparation | 0.00 | 120.00 | 100.00 | Linear |
| RoomType | 0.00 | 3.00 | 1.00 | Discrete/Enum |
| MixReflect | 0.03 | 2.00 | 1.00 | Linear |
| MixDiffuse | 0.03 | 2.00 | 1.00 | Linear |
| MixDirect | 0.00 | 1.00 | 0.55 | % / Normalized |

---

## 📦 Roar
- **XML Tag**: `Roar`
- **Class**: `Roar`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Input_InputGain | 0.06 | 15.85 | 1.00 | dB |
| Input_ToneAmount | -1.00 | 1.00 | 0.00 | Linear |
| Input_ToneFrequency | 80.00 | 2000.00 | 180.00 | Hz (Log) |
| Input_ColorOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Input_Blend | 0.00 | 1.00 | 0.50 | % / Normalized |
| Input_LowMidCrossover | 20.00 | 5000.00 | 200.00 | Hz (Log) |
| Input_MidHighCrossover | 200.00 | 18000.01 | 2000.00 | Hz (Log) |
| Stage1_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage1_Shaper_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage1_Shaper_Type | 0.00 | 11.00 | 0.00 | Discrete/Enum |
| Stage1_Shaper_Amount | 0.00 | 1.00 | 0.00 | % / Normalized |
| Stage1_Shaper_Bias | -1.00 | 1.00 | 0.00 | Linear |
| Stage1_Shaper_Trim | 0.06 | 15.85 | 1.00 | Linear |
| Stage1_Filter_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage1_Filter_Type | 0.00 | 8.00 | 0.00 | Discrete/Enum |
| Stage1_Filter_Frequency | 20.00 | 20000.00 | 16000.00 | Hz (Log) |
| Stage1_Filter_Resonance | 0.00 | 1.00 | 0.10 | % / Normalized |
| Stage1_Filter_Morph | 0.00 | 1.00 | 0.00 | % / Normalized |
| Stage1_Filter_PeakGain | 0.25 | 3.98 | 1.00 | dB |
| Stage1_Filter_PreOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Stage2_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage2_Shaper_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage2_Shaper_Type | 0.00 | 11.00 | 0.00 | Discrete/Enum |
| Stage2_Shaper_Amount | 0.00 | 1.00 | 0.00 | % / Normalized |
| Stage2_Shaper_Bias | -1.00 | 1.00 | 0.00 | Linear |
| Stage2_Shaper_Trim | 0.06 | 15.85 | 1.00 | Linear |
| Stage2_Filter_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage2_Filter_Type | 0.00 | 8.00 | 0.00 | Discrete/Enum |
| Stage2_Filter_Frequency | 20.00 | 20000.00 | 16000.00 | Hz (Log) |
| Stage2_Filter_Resonance | 0.00 | 1.00 | 0.10 | % / Normalized |
| Stage2_Filter_Morph | 0.00 | 1.00 | 0.00 | % / Normalized |
| Stage2_Filter_PeakGain | 0.25 | 3.98 | 1.00 | dB |
| Stage2_Filter_PreOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Stage3_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage3_Shaper_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage3_Shaper_Type | 0.00 | 11.00 | 0.00 | Discrete/Enum |
| Stage3_Shaper_Amount | 0.00 | 1.00 | 0.00 | % / Normalized |
| Stage3_Shaper_Bias | -1.00 | 1.00 | 0.00 | Linear |
| Stage3_Shaper_Trim | 0.06 | 15.85 | 1.00 | Linear |
| Stage3_Filter_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Stage3_Filter_Type | 0.00 | 8.00 | 0.00 | Discrete/Enum |
| Stage3_Filter_Frequency | 20.00 | 20000.00 | 16000.00 | Hz (Log) |
| Stage3_Filter_Resonance | 0.00 | 1.00 | 0.10 | % / Normalized |
| Stage3_Filter_Morph | 0.00 | 1.00 | 0.00 | % / Normalized |
| Stage3_Filter_PeakGain | 0.25 | 3.98 | 1.00 | dB |
| Stage3_Filter_PreOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Feedback_FeedbackAmount | 0.00 | 1.00 | 0.00 | % / Normalized |
| Feedback_FeedbackTimeMode | 0.00 | 4.00 | 0.00 | Seconds |
| Feedback_FeedbackTime | 0.00 | 0.50 | 0.02 | Seconds |
| Feedback_FeedbackSyncedRate | -7.00 | 0.00 | -4.00 | Linear |
| Feedback_FeedbackNote | 12.00 | 84.00 | 33.00 | Linear |
| Feedback_FeedbackFrequency | 50.00 | 18000.01 | 1000.00 | Hz (Log) |
| Feedback_FeedbackBandwidth | 0.50 | 9.00 | 8.00 | Linear |
| Feedback_FeedbackInvert | 0.00 | 1.00 | 0.00 | % / Normalized |
| Feedback_FeedbackGateOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| ModulationSources_Lfo1_RateMode | 0.00 | 4.00 | 1.00 | Linear |
| ModulationSources_Lfo1_Rate | 0.01 | 10.00 | 1.00 | Linear |
| ModulationSources_Lfo1_SyncedRate | -6.00 | 3.00 | 0.00 | Linear |
| ModulationSources_Lfo1_Sixteenth | 1.00 | 64.00 | 8.00 | Linear |
| ModulationSources_Lfo1_Waveform | 0.00 | 4.00 | 1.00 | Linear |
| ModulationSources_Lfo1_Morph | -1.00 | 1.00 | 0.00 | Linear |
| ModulationSources_Lfo1_SmoothingAmount | 0.00 | 1.00 | 0.05 | % / Normalized |
| ModulationSources_Lfo2_RateMode | 0.00 | 4.00 | 1.00 | Linear |
| ModulationSources_Lfo2_Rate | 0.01 | 10.00 | 1.00 | Linear |
| ModulationSources_Lfo2_SyncedRate | -6.00 | 3.00 | 0.00 | Linear |
| ModulationSources_Lfo2_Sixteenth | 1.00 | 64.00 | 8.00 | Linear |
| ModulationSources_Lfo2_Waveform | 0.00 | 4.00 | 1.00 | Linear |
| ModulationSources_Lfo2_Morph | -1.00 | 1.00 | 0.00 | Linear |
| ModulationSources_Lfo2_SmoothingAmount | 0.00 | 1.00 | 0.05 | % / Normalized |
| ModulationSources_Envelope_Amount | 1.00 | 63.10 | 1.00 | Linear |
| ModulationSources_Envelope_Attack | 0.00 | 0.10 | 0.00 | Seconds |
| ModulationSources_Envelope_HoldOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| ModulationSources_Envelope_Release | 0.01 | 3.00 | 0.10 | Seconds |
| ModulationSources_Envelope_Threshold | 0.00 | 1.00 | 0.00 | dB |
| ModulationSources_Envelope_Frequency | 50.00 | 18000.01 | 1000.00 | Hz (Log) |
| ModulationSources_Envelope_Width | 0.50 | 9.00 | 8.00 | Linear |
| ModulationSources_Noise_RateMode | 0.00 | 4.00 | 1.00 | Linear |
| ModulationSources_Noise_Rate | 0.01 | 10.00 | 1.00 | Linear |
| ModulationSources_Noise_SyncedRate | -6.00 | 3.00 | -2.00 | Linear |
| ModulationSources_Noise_Sixteenth | 1.00 | 64.00 | 4.00 | Linear |
| ModulationSources_Noise_Type | 0.00 | 3.00 | 0.00 | Discrete/Enum |
| ModulationSources_Noise_SmoothingAmount | 0.00 | 1.00 | 0.05 | % / Normalized |
| GlobalModulationAmount | 0.00 | 2.00 | 1.00 | Linear |
| Output_CompressionAmount | 0.00 | 1.00 | 0.25 | % / Normalized |
| Output_CompressorHighpassFilterOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| Output_OutputGain | 0.00 | 3.98 | 1.00 | dB |
| Output_DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Saturator
- **XML Tag**: `Saturator`
- **Class**: `Saturator`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| PreDrive | -36.00 | 36.00 | 0.00 | Linear |
| PreDcFilter | 0.00 | 1.00 | 0.00 | % / Normalized |
| Type | 0.00 | 7.00 | 0.00 | Discrete/Enum |
| ColorOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| BaseDrive | -36.00 | 36.00 | 0.00 | Linear |
| ColorFrequency | 30.00 | 18500.00 | 1000.00 | Hz (Log) |
| ColorWidth | 0.00 | 1.00 | 0.30 | % / Normalized |
| ColorDepth | -24.00 | 24.00 | 0.00 | Linear |
| PostClip | 0.00 | 2.00 | 0.00 | Linear |
| PostDrive | -36.00 | 0.00 | 0.00 | Linear |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| BassShaperThreshold | -50.00 | 0.00 | -50.00 | dB |
| WsDrive | 0.00 | 1.00 | 1.00 | % / Normalized |
| WsLin | 0.00 | 1.00 | 0.50 | % / Normalized |
| WsCurve | 0.00 | 1.00 | 0.05 | % / Normalized |
| WsDamp | 0.00 | 1.00 | 0.00 | % / Normalized |
| WsPeriod | 0.00 | 1.00 | 0.00 | % / Normalized |
| WsDepth | 0.00 | 1.00 | 0.00 | % / Normalized |

---

## 📦 Shifter
- **XML Tag**: `Shifter`
- **Class**: `Shifter`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Lfo_Amount | 0.00 | 5000.00 | 0.00 | Hz (Log) |
| Lfo_AmountPitch | 0.00 | 24.00 | 0.00 | Linear |
| Lfo_Waveform | 0.00 | 9.00 | 1.00 | Linear |
| Lfo_SyncOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lfo_RateHz | 0.01 | 50.00 | 0.50 | Linear |
| Lfo_SyncedRate | 0.00 | 21.00 | 12.00 | Linear |
| Lfo_SpinOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| Lfo_PhaseOffset | 0.00 | 360.00 | 180.00 | Linear |
| Lfo_SpinAmount | 0.00 | 0.50 | 0.00 | Linear |
| Lfo_Offset | 0.00 | 360.00 | 0.00 | Linear |
| Lfo_SHWidth | 0.00 | 1.00 | 0.00 | % / Normalized |
| Lfo_DutyCycle | -1.00 | 1.00 | 0.00 | Linear |
| Pitch_Coarse | -24.00 | 24.00 | 0.00 | Linear |
| Pitch_Fine | -1.00 | 1.00 | 0.00 | Linear |
| Pitch_WindowSize | 0.01 | 0.35 | 0.08 | Linear |
| ModBasedShifting_Fine | -500.00 | 500.00 | 0.00 | Linear |
| ModBasedShifting_FShift_Coarse | -10000.00 | 10000.00 | 0.00 | Hz (Log) |
| ModBasedShifting_RingMod_Coarse | 1.00 | 10000.00 | 1000.00 | Hz (Log) |
| ModBasedShifting_RingMod_Drive | 0.00 | 1.00 | 0.00 | % / Normalized |
| ModBasedShifting_RingMod_DriveAmount | 0.00 | 24.00 | 0.00 | Linear |
| MidiPitch_Glide | 0.00 | 20.00 | 0.00 | Linear |
| EnvelopeFollower_On | 0.00 | 1.00 | 0.00 | % / Normalized |
| EnvelopeFollower_Attack | 0.00 | 0.03 | 0.01 | Seconds |
| EnvelopeFollower_Release | 0.00 | 0.40 | 0.20 | Seconds |
| EnvelopeFollower_AmountHz | -5000.00 | 5000.00 | 0.00 | Hz (Log) |
| EnvelopeFollower_AmountPitch | -24.00 | 24.00 | 0.00 | Linear |
| Delay_On | 0.00 | 1.00 | 0.00 | % / Normalized |
| Delay_SyncOn | 0.00 | 1.00 | 1.00 | % / Normalized |
| Delay_TimeSeconds | 0.01 | 8.00 | 0.25 | Seconds |
| Delay_SyncedTime | 0.00 | 17.00 | 9.00 | Seconds |
| Delay_Feedback | 0.00 | 1.50 | 0.00 | Linear |
| Global_ShifterMode | 0.00 | 2.00 | 0.00 | Linear |
| Global_Tone | 300.00 | 22000.00 | 22000.00 | Hz (Log) |
| Global_Wide | 0.00 | 1.00 | 0.00 | % / Normalized |
| Global_DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Spectral
- **XML Tag**: `Spectral`
- **Class**: `Spectral`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Freezer_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Freezer_FreezeOn | 0.00 | 1.00 | 0.00 | % / Normalized |
| Freezer_SyncIntervalUnits | 0.00 | 1.00 | 0.00 | Discrete/Enum |
| Freezer_SyncIntervalBeats | 0.00 | 21.00 | 6.00 | Discrete/Enum |
| Freezer_SyncIntervalSeconds | 0.02 | 10.00 | 0.50 | Discrete/Enum |
| Freezer_MainMode | 0.00 | 1.00 | 0.00 | % / Normalized |
| Freezer_RetriggerMode | 0.00 | 1.00 | 0.00 | % / Normalized |
| Freezer_FadeType | 0.00 | 1.00 | 0.00 | Discrete/Enum |
| Freezer_FadeIn | 0.00 | 10.00 | 0.00 | Linear |
| Freezer_CrossfadePercent | 0.00 | 1.00 | 0.00 | % / Normalized |
| Freezer_FadeOut | 0.02 | 10.00 | 0.04 | Linear |
| Freezer_Sensitivity | 0.00 | 1.00 | 0.50 | % / Normalized |
| Delay_On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Delay_TimeSeconds | 0.01 | 3.00 | 0.25 | Seconds |
| Delay_TimeUnit | 0.00 | 4.00 | 0.00 | Seconds |
| Delay_TimeSixteenths | 1.00 | 16.00 | 3.00 | Seconds |
| Delay_TimeDivisions | 0.00 | 21.00 | 15.00 | Seconds |
| Delay_Feedback | 0.00 | 1.00 | 0.00 | % / Normalized |
| Delay_Tilt | -2.00 | 2.00 | 0.00 | Linear |
| Delay_Spray | 0.00 | 0.40 | 0.00 | Linear |
| Delay_Mask | -1.00 | 1.00 | 0.00 | Linear |
| Delay_StereoSpread | 0.00 | 1.00 | 0.00 | % / Normalized |
| Delay_FrequencyShift | -400.00 | 400.00 | 0.00 | Hz (Log) |
| Delay_DryWet | 0.00 | 1.00 | 0.50 | % / Normalized |
| InputSendGain | 0.00 | 1.00 | 1.00 | dB |
| DryWet | 0.00 | 1.00 | 0.50 | % / Normalized |

---

## 📦 SpectrumAnalyzer
- **XML Tag**: `SpectrumAnalyzer`
- **Class**: `SpectrumAnalyzer`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |

---

## 📦 Transmute
- **XML Tag**: `Transmute`
- **Class**: `Transmute`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| MidiPitch_Transpose | -48.00 | 48.00 | 0.00 | Linear |
| MidiPitch_TransposeScaleDegrees | -28.00 | 28.00 | 0.00 | Linear |
| MidiPitch_Glide | 0.00 | 20.00 | 0.00 | Linear |
| PartialFrequencies_FrequencyHz | 8.20 | 2000.00 | 110.00 | Hz (Log) |
| PartialFrequencies_FrequencyNote | 0.00 | 96.00 | 45.00 | Hz (Log) |
| PartialFrequencies_Shift | -48.00 | 48.00 | 0.00 | Hz (Log) |
| PartialFrequencies_PartialStretch | -1.00 | 1.00 | 0.00 | Hz (Log) |
| PartialFrequencies_QuantizeToScaleOrTuning | 0.00 | 1.00 | 0.00 | Hz (Log) |
| DecayDamping_DecayTime | 0.00 | 20.00 | 0.22 | Seconds |
| DecayDamping_HighFreqDamp | 0.00 | 1.00 | 0.00 | Hz (Log) |
| DecayDamping_LowFreqDamp | 0.00 | 1.00 | 0.00 | Hz (Log) |
| Modulation_ModRate | 0.00 | 1.00 | 0.10 | % / Normalized |
| Modulation_PitchModAmount | 0.00 | 4.00 | 0.00 | Linear |
| Global_NumHarmonics | 1.00 | 256.00 | 256.00 | Linear |
| Global_Unison | 0.00 | 3.00 | 0.00 | Linear |
| Global_UnisonAmount | 0.00 | 1.00 | 0.10 | % / Normalized |
| Global_InputSend | -24.00 | 24.00 | 0.00 | Linear |
| Global_DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| Global_UseScale | 0.00 | 1.00 | 0.00 | % / Normalized |

---

## 📦 Tuner
- **XML Tag**: `Tuner`
- **Class**: `Tuner`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| TuningFreq | 410.00 | 480.00 | 440.00 | Hz (Log) |

---

## 📦 Utility
- **XML Tag**: `StereoGain`
- **Class**: `StereoGain`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| PhaseInvertL | 0.00 | 1.00 | 0.00 | % / Normalized |
| PhaseInvertR | 0.00 | 1.00 | 0.00 | % / Normalized |
| ChannelMode | 0.00 | 3.00 | 1.00 | Linear |
| StereoWidth | 0.00 | 4.00 | 1.00 | Linear |
| MidSideBalance | 0.00 | 2.00 | 1.00 | Linear |
| Mono | 0.00 | 1.00 | 0.00 | % / Normalized |
| BassMono | 0.00 | 1.00 | 0.00 | % / Normalized |
| BassMonoFrequency | 50.00 | 500.00 | 120.00 | Hz (Log) |
| Balance | -1.00 | 1.00 | 0.00 | Linear |
| Gain | 0.00 | 56.23 | 1.00 | dB |
| LegacyGain | -35.00 | 35.00 | 0.00 | dB |
| Mute | 0.00 | 1.00 | 0.00 | % / Normalized |
| DcFilter | 0.00 | 1.00 | 0.00 | % / Normalized |

---

## 📦 Vinyl Distortion
- **XML Tag**: `Vinyl`
- **Class**: `Vinyl`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Band2On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Gain2 | 0.00 | 1.00 | 0.00 | dB |
| BandFreq2 | 50.00 | 18000.00 | 684.00 | Hz (Log) |
| BandQ2 | 0.10 | 3.00 | 0.32 | Linear |
| Band1On | 0.00 | 1.00 | 1.00 | % / Normalized |
| Gain1 | 0.00 | 1.00 | 0.00 | dB |
| BandFreq1 | 50.00 | 18000.00 | 7500.00 | Hz (Log) |
| BandQ1 | 0.10 | 3.00 | 3.00 | Linear |
| Drive | 0.00 | 1.00 | 1.00 | % / Normalized |
| SoftHard | 0.00 | 1.00 | 0.00 | % / Normalized |
| NormalMono | 0.00 | 1.00 | 0.00 | % / Normalized |
| CracleDensity | 0.00 | 50.00 | 10.00 | Linear |
| CracleVolume | 0.00 | 1.00 | 0.00 | dB |

---

## 📦 Vocoder
- **XML Tag**: `Vocoder`
- **Class**: `Vocoder`

| Parameter | Min | Max | Default | Unit (Heuristic) |
| :--- | :--- | :--- | :--- | :--- |
| On | 0.00 | 1.00 | 1.00 | % / Normalized |
| LowFrequency | 20.00 | 2000.00 | 80.00 | Hz (Log) |
| HighFrequency | 200.00 | 18000.00 | 12000.00 | Hz (Log) |
| FormantShift | -36.00 | 36.00 | 0.00 | Linear |
| FilterBandWidth | 0.10 | 2.00 | 1.00 | Linear |
| Retro | 0.00 | 1.00 | 0.00 | % / Normalized |
| LevelGate | -60.00 | 12.00 | -60.00 | Linear |
| OutputGain | -24.00 | 24.00 | 0.00 | dB |
| EnvelopeRate | 1.00 | 1000.00 | 1.00 | Linear |
| EnvelopeRelease | 10.00 | 30000.00 | 150.00 | Hz (Log) |
| UvdThreshold | 0.00 | 1.00 | 0.50 | dB |
| UvdSlow | 0.00 | 1.00 | 0.00 | % / Normalized |
| UvdLevel | 0.00 | 1.00 | 0.00 | Linear |
| CarrierFlatten | 0.00 | 1.00 | 0.00 | % / Normalized |
| MonoStereo | 0.00 | 2.00 | 1.00 | Linear |
| DryWet | 0.00 | 1.00 | 1.00 | % / Normalized |
| ModulatorAmount | 0.00 | 2.00 | 1.00 | Linear |

---


**TOTAL PARAMETERS ANALYZED**: 930
