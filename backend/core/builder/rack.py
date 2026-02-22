import xml.etree.ElementTree as ET
import os
from typing import List, Dict, Optional
from .chain import Chain
from .device import AbletonDevice
from .models import MacroMapping
from .serialization import prettify_xml, save_adg
from .authority import PARAMETER_AUTHORITY, SEMANTIC_MAP, SIGNAL_CHAIN_HIERARCHY

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
    
    def create_device(self, name: str) -> AbletonDevice:
        """Create a device with a unique ID managed by this rack"""
        did = self.get_next_device_id()
        return AbletonDevice(name, self.device_db, device_id=did)

    def add_macro_mapping(self, mapping: MacroMapping):
        self.macro_mappings.append(mapping)
    
    def auto_map_macros(self, nlp_resp: dict = None):
        if not nlp_resp: return
        
        # 1. Physical Signal Flow Self-Correction
        self._reorder_signal_chain()
        self._validate_signal_chain()
        
        # 2. Configure Surgical Initial States
        surgical_devices = nlp_resp.get("surgical_devices", [])
        configured_instances = set()
        for s_dev in surgical_devices:
            dev_name = str(s_dev.get("name", "")).lower().replace(" ", "").replace("-", "").replace("_", "")
            params = s_dev.get("parameters", {})
            for chain in self.chains:
                for device in chain.devices:
                    if device in configured_instances: continue
                    d_norm = device.name.lower().replace(" ", "").replace("-", "").replace("_", "")
                    if dev_name in d_norm or d_norm in dev_name:
                        for p_name, p_val in params.items():
                            device.set_initial_parameter(p_name, p_val)
                        configured_instances.add(device)
                        break

        # 3. Resolve & Cluster Macro Details (The Brain)
        ai_mapping_plan = nlp_resp.get("macro_details", [])
        if ai_mapping_plan:
            # Cluster-based Adjacency Polish
            ai_mapping_plan = self._reorder_macro_plan(ai_mapping_plan)
            # Apply mappings via Semantic Clustering Engine
            self._apply_semantic_clustering(ai_mapping_plan)
        
        # 4. Final Quality Check
        self._check_gain_compensation()

    def _apply_semantic_clustering(self, plan: List[dict]):
        """
        V61: ENHANCED CLUSTERING ENGINE
        Primary: Group by AI-suggested Index (if provided).
        Secondary: Group by Name (Semantic Clustering).
        """
        candidates = []
        seen_instance_params = set()
        
        # Phase 1: Resolution
        for item in plan:
            raw_target_dev = str(item.get("target_device") or "").lower().replace(" ", "").replace("_", "").replace("-", "")
            target_param = str(item.get("target_parameter") or "").lower()
            if not raw_target_dev or not target_param: continue

            resolved = False
            for chain in self.chains:
                for device in chain.devices:
                    d_norm = device.name.lower().replace(" ", "").replace("-", "").replace("_", "").replace("2", "").replace("new", "").replace("repeat", "repeat")
                    if raw_target_dev in d_norm or d_norm in raw_target_dev:
                        best_p, best_path, min_v, max_v = self._resolve_parameter_for_device(device, target_param)
                        if not best_p: continue
                        
                        inst_key = (device.device_id, tuple(best_path + [best_p]))
                        if inst_key in seen_instance_params: 
                            resolved = True; break
                        
                        candidates.append({
                            "device": device, "param": best_p, "path": best_path,
                            "min": item.get("min", min_v), "max": item.get("max", max_v),
                            "name": item.get("name") or item.get("label") or best_p,
                            "ai_idx": item.get("macro"), "inst_key": inst_key
                        })
                        seen_instance_params.add(inst_key)
                        resolved = True; break
                if resolved: break
            
            if not resolved:
                all_device_names = [d.name for chain in self.chains for d in chain.devices]
                print(f"  [DEBUG] Failed to resolve: {item.get('target_device')} -> {target_param}")

        # Phase 2: Multi-Pass Clustering
        # Pass A: Group by explicit macro index (if AI specified one)
        # Pass B: Group by name similarity (Semantic)
        final_macros: Dict[int, List[dict]] = {}
        semantic_groups: Dict[str, List[dict]] = {}
        
        unassigned = []
        for c in candidates:
            if c["ai_idx"] is not None:
                idx = int(c["ai_idx"]) - 1
                if idx not in final_macros: final_macros[idx] = []
                final_macros[idx].append(c)
            else:
                unassigned.append(c)
        
        # Semantic grouping for unassigned
        for c in unassigned:
            k = c["name"].lower().strip()
            # If this name already exists in an indexed macro, join it!
            matched_idx = None
            for idx, group in final_macros.items():
                if any(k in g["name"].lower() for g in group):
                    matched_idx = idx; break
            
            if matched_idx is not None:
                final_macros[matched_idx].append(c)
            else:
                if k not in semantic_groups: semantic_groups[k] = []
                semantic_groups[k].append(c)

        # Phase 3: Physical Mapping
        used_indices = set(final_macros.keys())
        macro_ptr = 0
        
        # A. Map explicit groups
        all_groups = []
        for idx in sorted(final_macros.keys()):
            all_groups.append((idx, final_macros[idx]))
        
        # B. Map semantic groups to first available
        for name_key in semantic_groups:
            while macro_ptr < 16 and macro_ptr in used_indices: macro_ptr += 1
            if macro_ptr >= 16: break
            all_groups.append((macro_ptr, semantic_groups[name_key]))
            used_indices.add(macro_ptr)
            macro_ptr += 1

        for m_idx, group in all_groups:
            if m_idx >= 16: continue
            macro_label = group[0]["name"]
            for c in group:
                dev = c["device"]; p_name = c["param"]; p_path = c["path"]
                p_meta = next((p for p in dev.device_info.get("parameters", []) if p["name"].lower() == p_name.lower()), None)
                min_val, max_val = self._interpret_parameter_range(p_name, c["min"], c["max"], p_meta)
                
                mapping = MacroMapping(macro_index=m_idx, device_id=dev.device_id, param_path=p_path + [p_name], min_val=min_val, max_val=max_val, label=macro_label)
                dev.add_mapping(mapping.param_path, mapping); self.add_macro_mapping(mapping)
                
                # Auto-Inverse Gain
                if any(x in p_name.lower() for x in ["drive", "driveamount", "threshold", "inputgain"]):
                    if any(x in dev.name.lower() for x in ["saturator", "roar", "pedal", "overdrive", "tube", "amp"]):
                        gain_p = next((p["name"] for p in dev.device_info.get("parameters", []) if any(x in p["name"].lower() for x in ["outputgain", "volume", "makeup", "gain"])), None)
                        if gain_p and tuple([gain_p]) not in dev.mappings:
                            g_min, g_max = 0.0, -12.0
                            dm = self.device_db.get_macro_suggestions(dev.name)
                            for s in dm:
                                if gain_p in s['param_name']: g_min, g_max = s['max'], s['min']; break
                            comp = MacroMapping(macro_index=m_idx, device_id=dev.device_id, param_path=[gain_p], min_val=g_min, max_val=g_max, label=macro_label)
                            dev.add_mapping([gain_p], comp); self.add_macro_mapping(comp)

    def _resolve_parameter_for_device(self, device: AbletonDevice, target_param: str):
        """Helper to find the best parameter path and default range for a target intent."""
        best_param = None
        best_path = []
        min_v, max_v = 0.0, 1.0
        
        # 1. Suggestion DB
        suggestions = self.device_db.get_macro_suggestions(device.name)
        for sugg in suggestions:
            if target_param in sugg['param_name'].lower() or sugg['param_name'].lower() in target_param:
                best_param = sugg['param_name']; min_v, max_v = sugg['min'], sugg['max']; break
        
        # 2. Semantic Map
        s_key = device.name.lower().replace(" ", "").replace("_", "").replace("-", "")
        alias_map = {
            "autofilter": "autofilter2", 
            "chorus": "chorus2", 
            "autopan": "autopan2", 
            "phaser": "phasernew", 
            "redux": "redux2", 
            "beatrepeat": "BeatRepeat", 
            "spectralresonator": "SpectralResonator", 
            "spectraltime": "Spectral",
            "spectral": "Spectral",
            "hybridreverb": "Hybrid",
            "hybrid": "Hybrid",
            "roar": "Roar",
            "phaserflanger": "PhaserNew", 
            "chorusensemble": "Chorus2",
            "chorus-ensemble": "Chorus2",
            "filterdelay": "FilterDelay"
        }
        for a_k, a_v in alias_map.items():
            if a_k in s_key: s_key = a_v; break
        
        device_semantic = {}
        for k, v in SEMANTIC_MAP.items():
            if k.lower().replace(" ", "").replace("_", "").replace("-", "") == s_key:
                device_semantic = v; break

        target_norm = target_param.lower().replace(" ", "").replace("/", "").replace("_", "").replace("-", "")
        for intent, real_param in device_semantic.items():
            intent_norm = intent.lower().replace(" ", "").replace("/", "").replace("_", "").replace("-", "")
            if intent_norm == target_norm or intent_norm in target_norm:
                best_param = real_param; best_path = []; break
        
        # 3. Global Authority
        if not best_param or best_param == target_param:
            global_map = {"frequency": "Filter_Frequency", "cutoff": "Filter_Frequency", "freq": "Filter_Frequency", "resonance": "Filter_Resonance", "res": "Filter_Resonance", "drive": "DriveAmount", "output": "OutputGain", "gain": "OutputGain", "time": "DelayLine_TimeL", "feedback": "Feedback", "drywet": "DryWet"}
            lookup = target_param.lower().strip()
            for g_key, g_val in global_map.items():
                 if g_key in lookup or lookup in g_key:
                      best_param = g_val; break
        
        # 4. Device Metadata Fuzzy Match (Enhanced V63)
        if not best_param:
            t_norm = target_param.lower().replace("_", "").replace(" ", "").replace("-", "")
            for p in device.device_info.get("parameters", []):
                p_name = p["name"]
                p_norm = p_name.lower().replace("_", "").replace(" ", "").replace("-", "")
                if t_norm == p_norm or t_norm in p_norm or p_norm in t_norm:
                    best_param = p_name; best_path = []; break

        return best_param, best_path, min_v, max_v

    def _reorder_macro_plan(self, plan: list) -> list:
        """Preserved from V57: Cluster-based macro reorder for device adjacency."""
        if not plan or len(plan) <= 1: return plan
        macro_groups = {}; group_order = []
        for item in plan:
            m = item.get("macro", 0)
            if m not in macro_groups: macro_groups[m] = []; group_order.append(m)
            macro_groups[m].append(item)
        if len(macro_groups) <= 1: return plan
        def norm_dev(name): return str(name).lower().replace(" ", "").replace("-", "").replace("_", "")
        group_info = {}
        for m, items in macro_groups.items():
            dev_counts = {}
            for item in items:
                dev = norm_dev(item.get("target_device", ""))
                if dev: dev_counts[dev] = dev_counts.get(dev, 0) + 1
            primary = max(dev_counts, key=dev_counts.get) if dev_counts else ""
            all_devs = set(dev_counts.keys())
            group_info[m] = {"primary": primary, "all_devs": all_devs, "is_multi": len(all_devs) > 1, "original_pos": group_order.index(m)}
        device_first_pos = {}
        for m in group_order:
            primary = group_info[m]["primary"]
            if primary not in device_first_pos: device_first_pos[primary] = group_info[m]["original_pos"]
        clusters = {}
        for m in group_order:
            primary = group_info[m]["primary"]
            if primary not in clusters: clusters[primary] = []
            clusters[primary].append(m)
        sorted_cluster_keys = sorted(clusters.keys(), key=lambda d: device_first_pos[d])
        sorted_macros = []
        for d_key in sorted_cluster_keys:
            c_macros = clusters[d_key]
            singles = sorted([m for m in c_macros if not group_info[m]["is_multi"]], key=lambda m: group_info[m]["original_pos"])
            multis = sorted([m for m in c_macros if group_info[m]["is_multi"]], key=lambda m: group_info[m]["original_pos"])
            sorted_macros.extend(singles + multis)
        new_plan = []
        for new_num, old_macro in enumerate(sorted_macros, start=1):
            for item in macro_groups[old_macro]:
                new_item = dict(item); new_item["macro"] = new_num; new_plan.append(new_item)
        return new_plan

    def _interpret_parameter_range(self, param_name: str, min_v: float, max_v: float, p_meta: dict) -> tuple:
        """Preserved from V55/59: Universal Parameter Interpreter."""
        if not p_meta: return min_v, max_v
        p_max = p_meta.get("max", 1.0); p_min = p_meta.get("min", 0.0)
        auth_type = PARAMETER_AUTHORITY.get(param_name)
        if any(x in param_name.lower() for x in ["feedback", "feedback_amount"]): p_max = min(p_max, 0.90); max_v = min(max_v, 0.90); min_v = min(min_v, 0.90)
        if any(x in param_name.lower() for x in ["drywet", "dry_wet", "mix"]): p_max = min(p_max, 0.85); max_v = min(max_v, 0.85); min_v = min(min_v, 0.85)
        if auth_type == "linear_amplitude":
            def db_to_linear(db_val):
                if db_val <= -70.0: return 0.0
                return 10.0 ** (db_val / 20.0)
            if min_v < 0 or (0 <= min_v <= 1.1 and 0 <= max_v <= 1.1 and p_max > 2.0):
                if 0 <= min_v <= 1.1: safe_max = min(p_max, 4.0); target_min = p_min + (safe_max - p_min) * min_v; target_max = p_min + (safe_max - p_min) * max_v; return target_min, target_max
                else: lin_min = db_to_linear(min_v); lin_max = db_to_linear(max_v); return max(p_min, min(p_max, lin_min)), max(p_min, min(p_max, lin_max))
            return max(p_min, min(p_max, min_v)), max(p_min, min(p_max, max_v))
        if auth_type == "stereo_width_linear":
            if 0 <= min_v <= 1.1: safe_max = min(p_max, 2.5); return safe_max * min_v, safe_max * max_v
            if max_v > 4.0: return min(p_max, min_v / 100.0), min(p_max, max_v / 100.0)
            return max(p_min, min(p_max, min_v)), max(p_min, min(p_max, max_v))
        if (0.0 <= min_v <= 1.1) and (0.0 <= max_v <= 1.1) and (p_max - p_min > 0.0):
             safe_p_min = max(p_min, -70.0) if p_min < -1000.0 else p_min
             safe_p_range = p_max - safe_p_min
             t_min = safe_p_min + (safe_p_range * min_v); t_max = safe_p_min + (safe_p_range * max_v)
             if min_v == 0.0 and p_min < -1000.0: t_min = p_min
             if auth_type == "discrete" or (p_max - p_min < 20.0 and p_max == int(p_max)): return round(t_min), round(t_max)
             if auth_type == "boolean": return (1.0 if t_min >= 0.5 else 0.0), (1.0 if t_max >= 0.5 else 0.0)
             return t_min, t_max
        if auth_type == "hz_physical" or ("Freq" in param_name and p_max > 200):
            if 0 < min_v < 18.0: min_v *= 1000.0
            if 0 < max_v < 18.0: max_v *= 1000.0
        return max(p_min, min(p_max, min_v)), max(p_min, min(p_max, max_v))

    def _validate_signal_chain(self):
        """Preserved from V58/59: Quality control check for signal chain order."""
        for chain in self.chains:
            prev_pos = -1; prev_name = ""
            for device in chain.devices:
                d_name = device.name.lower(); current_pos = -1
                for h_name, pos in SIGNAL_CHAIN_HIERARCHY.items():
                    if h_name in d_name: current_pos = pos; break
                if current_pos != -1 and prev_pos != -1 and current_pos < prev_pos:
                    print(f"  [DESIGN WARNING]: Signal flow inversion in '{chain.name}': '{d_name}' after '{prev_name}'.")
                if current_pos != -1: prev_pos = current_pos; prev_name = d_name

    def _reorder_signal_chain(self):
        """Preserved from V59: Self-Correcting Signal Flow."""
        for chain in self.chains:
            if len(chain.devices) > 1:
                def get_rank(device):
                    d_name = device.name.lower()
                    clean = "".join([c for c in d_name if not c.isdigit()]).strip().replace("_", " ").replace("-", " ")
                    for h_name, pos in SIGNAL_CHAIN_HIERARCHY.items():
                        if h_name in clean: return pos
                    return 5
                chain.devices.sort(key=get_rank)
                print(f"  [AUTO-FIX]: Signal chain in '{chain.name}' reordered for optimal musical flow.")

    def _check_gain_compensation(self):
        """Preserved from V58: Quality control check for gain compensation."""
        macro_map = {}
        for mapping in self.macro_mappings:
            m = mapping.macro_index
            if m not in macro_map: macro_map[m] = []
            macro_map[m].append(mapping)
        for m, mappings in macro_map.items():
            dev_params = {}
            for map_item in mappings:
                target_dev = "Unknown"
                for chain in self.chains:
                    for dev in chain.devices:
                        if dev.device_id == map_item.device_id: target_dev = dev.name.lower(); break
                param = map_item.param_path[-1].lower()
                if target_dev not in dev_params: dev_params[target_dev] = []
                dev_params[target_dev].append(param)
            for dev, params in dev_params.items():
                has_drive = any(p in params for p in ["drive", "driveamount", "inputgain", "gain"])
                has_output = any(p in params for p in ["output", "outputgain", "makup", "volume"])
                if has_drive and not has_output and any(d in dev for d in ["saturator", "roar", "pedal", "overdrive", "distort"]):
                    print(f"  [DESIGN WARNING]: Macro {m+1} on '{dev}' lacks gain compensation.")

    def to_xml(self) -> ET.Element:
        """Preserved XML logic."""
        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "template_rack.xml")
        tree = ET.parse(template_path); root = tree.getroot()
        gp = root.find("GroupDevicePreset"); rack = gp.find("Device/AudioEffectGroupDevice")
        mod_count = rack.find("ModulationSourceCount")
        if mod_count is not None: mod_count.set("Value", "16")
        num_macros = rack.find("NumVisibleMacroControls")
        if num_macros is not None: num_macros.set("Value", str(self.macro_count))
        branches_elem = rack.find("Branches")
        if branches_elem is not None:
            for child in list(branches_elem): branches_elem.remove(child)
        bp_list = gp.find("BranchPresets")
        if bp_list is None: bp_list = ET.SubElement(gp, "BranchPresets")
        else:
            for child in list(bp_list): bp_list.remove(child)
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
