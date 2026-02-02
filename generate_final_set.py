import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from core.builder.rack import AudioEffectRack, MacroMapping
from core.builder.chain import Chain
from core.builder.device import AbletonDevice
from core.device_mapper import DeviceDatabase

def create_rack(name, chains_def, db):
    print(f"Generating: {name}...")
    rack = AudioEffectRack(name, device_db=db)
    
    for c_idx, c_def in enumerate(chains_def):
        chain = Chain(c_def['name'])
        for d_def in c_def['devices']:
            dev = AbletonDevice(d_def['name'], db)
            if 'params' in d_def:
                for p_k, p_v in d_def['params'].items():
                    dev.set_initial_parameter(p_k, float(p_v))
            
            # Map specific parameters if requested
            if 'mappings' in d_def:
                for map_def in d_def['mappings']:
                    # map_def: {macro_idx, param_name, min, max, label}
                    m = MacroMapping(
                        macro_index=map_def['idx'],
                        device_id="0",
                        param_path=[map_def['param']],
                        min_val=map_def['min'],
                        max_val=map_def['max'],
                        label=map_def['label']
                    )
                    dev.add_mapping([map_def['param']], m)
                    rack.add_macro_mapping(m)
            
            chain.add_device(dev)
        rack.add_chain(chain)
        
    filename = f"{name.replace(' ', '_')}_V64.adg"
    rack.save(filename)
    print(f"  -> Saved {filename}")

def generate_all():
    print("--- 🏭 FINAL PRODUCTION RUN (V64) 🏭 ---")
    db = DeviceDatabase()

    # 1. DRUMS (Parallel Compression)
    # Uses parallel chains for New York compression style
    drums_def = [
        {'name': 'Dry', 'devices': [{'name': 'Utility', 'params': {'Gain': 0.0}}]},
        {'name': 'Smash', 'devices': [
            {'name': 'Compressor', 'params': {'Ratio': 8.0, 'Threshold': -20.0}, 
             'mappings': [{'idx': 0, 'param': 'Threshold', 'min': 0.0, 'max': -40.0, 'label': 'Smash Amt'}]},
            {'name': 'Saturator', 'params': {'Drive': 10.0},
             'mappings': [{'idx': 1, 'param': 'Drive', 'min': 0.0, 'max': 20.0, 'label': 'Grit'}]}
        ]}
    ]
    create_rack("Live Set - Drums", drums_def, db)

    # 2. BASS (Monofication & Drive)
    bass_def = [
        {'name': 'Main', 'devices': [
            {'name': 'Utility', 'params': {'BassMono': 1.0, 'BassMonoFreq': 120.0},
             'mappings': [{'idx': 0, 'param': 'BassMonoFreq', 'min': 50.0, 'max': 200.0, 'label': 'Mono Focus'}]},
            {'name': 'Overdrive', 'params': {'Drive': 0.5},
             'mappings': [{'idx': 1, 'param': 'Drive', 'min': 0.0, 'max': 1.0, 'label': 'Drive'}]},
            {'name': 'EQ Eight', 'params': {}}
        ]}
    ]
    create_rack("Live Set - Bass", bass_def, db)

    # 3. SYNTH (Space & Modulation)
    synth_def = [
        {'name': 'Main', 'devices': [
            {'name': 'Chorus', 'params': {'Amount': 0.5},
             'mappings': [{'idx': 0, 'param': 'Amount', 'min': 0.0, 'max': 1.0, 'label': 'Width'}]},
            {'name': 'Auto Filter', 'params': {'Frequency': 2000.0, 'Resonance': 0.3},
             'mappings': [{'idx': 1, 'param': 'Frequency', 'min': 200.0, 'max': 15000.0, 'label': 'Cutoff'},
                          {'idx': 2, 'param': 'Resonance', 'min': 0.0, 'max': 0.8, 'label': 'Reso'}]}
        ]}
    ]
    create_rack("Live Set - Synth", synth_def, db)

    # 4. KEYBOARDS (Vintage Warmth)
    keys_def = [
        {'name': 'Main', 'devices': [
            {'name': 'Vinyl Distortion', 'params': {'Drive': 0.2},
             'mappings': [{'idx': 0, 'param': 'Drive', 'min': 0.0, 'max': 1.0, 'label': 'Dust'}]},
            {'name': 'Phaser', 'params': {'Amount': 0.4},
             'mappings': [{'idx': 1, 'param': 'Amount', 'min': 0.0, 'max': 1.0, 'label': 'Phase'}]}
        ]}
    ]
    create_rack("Live Set - Keyboards", keys_def, db)

    # 5. VOCALS (Parallel Clarity & Verb)
    vocals_def = [
        {'name': 'Dry', 'devices': [{'name': 'Utility', 'params': {}}]},
        {'name': 'Air', 'devices': [
            {'name': 'EQ Eight', 'params': {}}, # High shelf implicit
            {'name': 'Reverb', 'params': {'DryWet': 1.0, 'DecayTime': 2.0},
             'mappings': [{'idx': 0, 'param': 'DecayTime', 'min': 0.5, 'max': 5.0, 'label': 'Space'}]}
        ]}
    ]
    create_rack("Live Set - Vocals", vocals_def, db)

    # 6. PERCUSSION (Industrial Wash - The Benchmark)
    perc_def = [
        {'name': 'Dry', 'devices': [{'name': 'Utility', 'params': {}}]},
        {'name': 'Wash', 'devices': [
            {'name': 'Hybrid Reverb', 'params': {'DryWet': 1.0}},
            {'name': 'Saturator', 'params': {'Drive': 5.0}},
            {'name': 'Auto Filter', 'params': {'Frequency': 500.0},
             'mappings': [{'idx': 0, 'param': 'Frequency', 'min': 100.0, 'max': 5000.0, 'label': 'Wash Tone'}]}
        ]}
    ]
    create_rack("Live Set - Percussion", perc_def, db)

if __name__ == "__main__":
    generate_all()
