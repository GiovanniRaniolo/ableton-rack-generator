import xml.etree.ElementTree as ET
import os
from typing import List, Dict, Optional
from .chain import Chain
from .models import MacroMapping
from .serialization import prettify_xml, save_adg
from .constants import PARAMETER_AUTHORITY, SEMANTIC_MAP

class AudioEffectRack:
    """Main class for building an Audio Effect Rack - Orchestrator (Modular)"""
    
    def __init__(self, name: str = "Custom Rack", device_db=None):
        self.name = name
        self.device_db = device_db
        self.chains: List[Chain] = []
        self.macro_count = 8
        self.macro_mappings: List[MacroMapping] = []
        self.device_id_counter = 1
        self.preset_id_counter = 20
    
    def get_next_device_id(self) -> str:
        did = str(self.device_id_counter)
        self.device_id_counter += 1
        return did

    def get_next_preset_id(self) -> str:
        pid = str(self.preset_id_counter)
        self.preset_id_counter += 1
        return pid
    
    def add_chain(self, chain: Chain):
        self.chains.append(chain)
    
    def add_macro_mapping(self, mapping: MacroMapping):
        self.macro_mappings.append(mapping)
    
    def auto_map_macros(self, nlp_resp: dict = None):
        if not nlp_resp: return
        
        ai_mapping_plan = nlp_resp.get("macro_details", [])
        surgical_devices = nlp_resp.get("surgical_devices", [])
        
        for s_dev in surgical_devices:
            dev_name = s_dev.get("name", "").lower()
            params = s_dev.get("parameters", {})
            for chain in self.chains:
                for device in chain.devices:
                    d_norm = device.name.lower().replace(" ", "").replace("-", "").replace("_", "")
                    s_norm = dev_name.replace(" ", "").replace("-", "").replace("_", "")
                    if s_norm in d_norm or d_norm in s_norm:
                        for p_name, p_val in params.items():
                            device.set_initial_parameter(p_name, p_val)

        macro_idx = 0
        used_macros = set()
        if ai_mapping_plan:
            for plan_item in ai_mapping_plan:
                if macro_idx >= 16: break
                raw_target_dev = plan_item.get("target_device") or ""
                raw_target_param = plan_item.get("target_parameter") or ""
                target_dev_name = str(raw_target_dev).lower().replace(" ", "").replace("_", "").replace("-", "")
                target_param = str(raw_target_param).lower()
                
                if not target_dev_name or not target_param: continue
                
                local_found = False
                for chain in self.chains:
                    for device in chain.devices:
                        if local_found: break
                        d_name_norm = device.name.lower().replace(" ", "").replace("_", "").replace("-", "").replace("2", "").replace("new", "")
                        
                        if target_dev_name in d_name_norm or d_name_norm in target_dev_name:
                            suggestions = self.device_db.get_macro_suggestions(device.name)
                            best_param = None
                            best_path = []
                            min_v, max_v = 0.0, 1.0
                            
                            for sugg in suggestions:
                                if target_param in sugg['param_name'].lower() or sugg['param_name'].lower() in target_param:
                                    best_param = sugg['param_name']
                                    min_v, max_v = sugg['min'], sugg['max']
                                    break
                            
                            s_key = device.name.lower().replace(" ", "").replace("_", "").replace("-", "")
                            # Alias mapping
                            alias_map = {"autofilter": "autofilter2", "chorus": "chorus2", "autopan": "autopan2", "phaser": "phasernew", "redux": "redux2"}
                            for a_k, a_v in alias_map.items():
                                if a_k in s_key: s_key = a_v; break

                            device_semantic = {}
                            for k, v in SEMANTIC_MAP.items():
                                if k.lower().replace(" ", "").replace("_", "").replace("-", "") == s_key:
                                    device_semantic = v
                                    break
                            
                            for intent, real_param in device_semantic.items():
                                if intent.lower() == target_param or intent.lower() in target_param:
                                    best_param = real_param
                                    best_path = [] 
                                    break
                            
                            if best_param == target_param:
                                global_map = {"frequency": "Filter_Frequency", "cutoff": "Filter_Frequency", "freq": "Filter_Frequency", "resonance": "Filter_Resonance", "res": "Filter_Resonance", "drive": "DriveAmount", "output": "OutputGain", "gain": "OutputGain", "time": "DelayLine_TimeL", "feedback": "Feedback", "drywet": "DryWet"}
                                lookup = target_param.lower().strip()
                                for g_key, g_val in global_map.items():
                                     if g_key in lookup or lookup in g_key:
                                          best_param = g_val; break

                            if not best_param:
                                for p in device.device_info.get("parameters", []):
                                    if target_param == p["name"].lower() or target_param in p["name"].lower() or p["name"].lower() in target_param:
                                        best_param = p["name"]; best_path = []; break

                            # EQ8 special path logic
                            if best_param and device.xml_tag == "Eq8" and any(x in best_param for x in ["Freq", "Gain", "Q"]):
                                 best_path = ["Bands.0", "ParameterA"]
                                 if "Freq" in best_param: best_param = "Freq"
                                 elif "Gain" in best_param: best_param = "Gain"
                                 elif "Q" in best_param: best_param = "Q"

                            if not best_param: continue

                            t_macro_idx = plan_item.get("macro")
                            t_macro_idx = int(t_macro_idx) - 1 if t_macro_idx is not None else macro_idx
                            while t_macro_idx < 16 and t_macro_idx in used_macros and "macro" not in plan_item:
                                t_macro_idx += 1
                            
                            if t_macro_idx >= 16: break
                            used_macros.add(t_macro_idx)

                            full_path = tuple(best_path + [best_param])
                            if full_path in device.mappings:
                                found_match = True; break

                            macro_label = plan_item.get("name") or plan_item.get("label") or best_param
                            min_v = plan_item.get("min", min_v)
                            max_v = plan_item.get("max", max_v)
                            
                            matched_p = next((p for p in device.device_info.get("parameters", []) if p["name"] == best_param), None)
                            if matched_p:
                                p_max = matched_p.get("max", 1.0)
                                p_min = matched_p.get("min", 0.0)
                                auth_type = PARAMETER_AUTHORITY.get(best_param)
                                
                                if auth_type == "normalized_time_5s" or (any(x in best_param for x in ["TimeL", "TimeR", "Time", "DecayTime"]) and "Rate" not in best_param and p_max <= 60.0):
                                    p_max_ms = p_max * 1000.0
                                    def to_ms(v, pm):
                                        if v is None: return 1.0
                                        return v * 1000.0 if (v < pm and v != 1.0) else v
                                    rm_min = to_ms(min_v, p_max); rm_max = to_ms(max_v, p_max)
                                    min_v = max(0.0, (rm_min - 1.0) / p_max_ms); max_v = max(0.0, (rm_max - 1.0) / p_max_ms)
                                elif auth_type == "physical_hz" or ("Freq" in best_param and p_max > 100):
                                    if 0 < min_v < 200.0: min_v *= 1000.0; max_v *= 1000.0
                                elif (0.0 <= min_v <= 1.0) and (0.0 <= max_v <= 1.0) and (p_max - p_min > 1.1):
                                    min_v = p_min + (p_max - p_min) * min_v; max_v = p_min + (p_max - p_min) * max_v

                            if min_v == max_v and min_v is not None:
                                 max_v = min_v + (0.0001 if (matched_p and matched_p.get("max", 1.0) <= 60.0) else 1.0)

                            mapping = MacroMapping(macro_index=t_macro_idx, device_id="0", param_path=best_path + [best_param], min_val=min_v, max_val=max_v, label=macro_label)
                            device.add_mapping(best_path + [best_param], mapping)
                            self.add_macro_mapping(mapping)
                            if "macro" not in plan_item: macro_idx = t_macro_idx + 1
                            local_found = True; break 
                    if local_found: break

        if ai_mapping_plan and len(ai_mapping_plan) > 0: return

        if macro_idx < 16:
            for chain in self.chains:
                for device in chain.devices:
                    suggestions = self.device_db.get_macro_suggestions(device.name)
                    for suggestion in suggestions:
                        while macro_idx < 16 and macro_idx in used_macros: macro_idx += 1
                        if macro_idx >= 8: break
                        p_name = suggestion['param_name']; p_path = []
                        if tuple(p_path + [p_name]) in device.mappings: continue
                        if device.xml_tag == "Eq8" and any(x in p_name for x in ["Freq", "Gain", "Q"]):
                             p_path = ["Bands.0", "ParameterA"]; p_name = p_name.replace("1 ", "").replace(" A", "")
                        mapping = MacroMapping(macro_index=macro_idx, device_id="0", param_path=p_path + [p_name], min_val=suggestion['min'], max_val=suggestion['max'], label=p_name)
                        device.add_mapping(mapping.param_path, mapping); self.add_macro_mapping(mapping); macro_idx += 1

    def to_xml(self) -> ET.Element:
        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "template_rack.xml")
        tree = ET.parse(template_path)
        root = tree.getroot()
        gp = root.find("GroupDevicePreset")
        rack = gp.find("Device/AudioEffectGroupDevice")
        num_macros = rack.find("NumVisibleMacroControls")
        if num_macros is not None: num_macros.set("Value", str(self.macro_count))
        branches_elem = rack.find("Branches")
        if branches_elem is not None:
            for child in list(branches_elem): branches_elem.remove(child)
        bp_list = gp.find("BranchPresets")
        if bp_list is None: bp_list = ET.SubElement(gp, "BranchPresets")
        else:
            for child in list(bp_list): bp_list.remove(child)
        self.device_id_counter = 1; self.preset_id_counter = 20
        for i, chain in enumerate(self.chains):
            bp_list.append(chain.to_branch_preset_xml(branch_id=i, device_db=self))
        for i in range(16):
            dn = rack.find(f"MacroDisplayNames.{i}")
            if dn is not None:
                val = f"Macro {i+1}"
                for m in self.macro_mappings:
                    if m.macro_index == i: val = m.label if m.label else m.param_path[-1]; break
                dn.set("Value", val)
        return root

    def save(self, filepath: str):
        xml_tree = self.to_xml()
        xml_string = prettify_xml(xml_tree)
        save_adg(xml_string, filepath)
