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
        
        # V59: Self-Correcting Signal Flow
        # Physically reorder devices based on musical hierarchy
        self._reorder_signal_chain()
        
        # V58: Validate signal chain order before mapping
        self._validate_signal_chain()
        
        ai_mapping_plan = nlp_resp.get("macro_details", [])
        surgical_devices = nlp_resp.get("surgical_devices", [])
        
        configured_instances = set()
        for s_dev in surgical_devices:
            dev_name = str(s_dev.get("name", "")).lower()
            params = s_dev.get("parameters", {})
            s_norm = dev_name.replace(" ", "").replace("-", "").replace("_", "")
            
            for chain in self.chains:
                for device in chain.devices:
                    if device in configured_instances: continue
                    d_norm = device.name.lower().replace(" ", "").replace("-", "").replace("_", "")
                    if s_norm in d_norm or d_norm in s_norm:
                        # Found matching UNCONFIGURED instance
                        for p_name, p_val in params.items():
                            device.set_initial_parameter(p_name, p_val)
                        configured_instances.add(device)
                        break

        macro_idx = 0
        used_macros = set()
        global_mapped_paths = set()  # Track (macro_idx, full_path) - same param on same macro
        global_param_paths = set()   # Track full_path only - same param on ANY macro (cross-macro dedup)
        
        # V56: Reorder macro plan for device adjacency
        if ai_mapping_plan:
            ai_mapping_plan = self._reorder_macro_plan(ai_mapping_plan)
        
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
                            # RESOLVE PARAMETER (same as before)
                            suggestions = self.device_db.get_macro_suggestions(device.name)
                            best_param = None
                            best_path = []
                            min_v, max_v = 0.0, 1.0
                            
                            for sugg in suggestions:
                                if target_param in sugg['param_name'].lower() or sugg['param_name'].lower() in target_param:
                                    best_param = sugg['param_name']; min_v, max_v = sugg['min'], sugg['max']; break
                            
                            s_key = device.name.lower().replace(" ", "").replace("_", "").replace("-", "")
                            alias_map = {"autofilter": "autofilter2", "chorus": "chorus2", "autopan": "autopan2", "phaser": "phasernew", "redux": "redux2"}
                            for a_k, a_v in alias_map.items():
                                if a_k in s_key: s_key = a_v; break

                            device_semantic = {}
                            for k, v in SEMANTIC_MAP.items():
                                if k.lower().replace(" ", "").replace("_", "").replace("-", "") == s_key:
                                    device_semantic = v; break
                            
                            for intent, real_param in device_semantic.items():
                                if intent.lower() == target_param or intent.lower() in target_param:
                                    best_param = real_param; best_path = []; break
                            
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

                            if best_param and device.xml_tag == "Eq8" and any(x in best_param for x in ["Freq", "Gain", "Q"]):
                                 best_path = ["Bands.0", "ParameterA"]
                                 if "Freq" in best_param: best_param = "Freq"
                                 elif "Gain" in best_param: best_param = "Gain"
                                 elif "Q" in best_param: best_param = "Q"

                            if not best_param: continue

                            # MULTI-INSTANCE DETECTION: Track (DeviceID, Param) globally to allow round-robin
                            full_leaf_path = tuple(best_path + [best_param])
                            global_instance_param_key = (device.device_id, full_leaf_path)
                            
                            if global_instance_param_key in global_param_paths:
                                # This SPECIFIC parameter on this SPECIFIC device instance is already busy.
                                # Continue to the NEXT device in the chain (multiplicity support)
                                continue

                            # SLOT SELECTION
                            t_macro_idx = plan_item.get("macro")
                            if t_macro_idx is not None:
                                t_macro_idx = int(t_macro_idx) - 1
                            else:
                                while macro_idx < 16 and macro_idx in used_macros: macro_idx += 1
                                t_macro_idx = macro_idx
                            
                            if t_macro_idx >= 16: break
                            used_macros.add(t_macro_idx)
                            
                            global_key = (t_macro_idx, global_instance_param_key)
                            if global_key in global_mapped_paths:
                                # Already mapped this exact instance param on this macro - skip
                                local_found = True; break
                            
                            global_mapped_paths.add(global_key)
                            global_param_paths.add(global_instance_param_key)

                            macro_label = plan_item.get("name") or plan_item.get("label") or best_param
                            
                            # EXPANSION LOGIC (V36.2): If AI provides point value without range, expand to full context
                            ai_min = plan_item.get("min")
                            ai_max = plan_item.get("max")
                            
                            if ai_min is not None and ai_max is None:
                                 # AI gave target but no top. If it's a Sweep param, use Full Range
                                 if any(x in best_param for x in ["Freq", "Frequency", "Cutoff", "DryWet", "Amount", "Gain", "Feedback", "Width", "Stereo", "Spread"]):
                                      min_v, max_v = 0.0, 1.0 # Will be scaled below
                                 else:
                                      min_v, max_v = ai_min, ai_min + 0.1
                            elif ai_min is not None and ai_max is not None:
                                min_v, max_v = ai_min, ai_max
                            # else: keep suggestion values
                            
                            # --- MACRO RANGE POLISH & SAFETY (V36.9 - THE DEFINITIVE FIX) ---
                            
                            # 1. ULTRA-FUZZY PARAMETER MATCHER
                            best_param_clean = str(best_param).lower().replace(" ", "").replace("_", "").replace("-", "")
                            matched_p = None
                            for p in device.device_info.get("parameters", []):
                                p_name_raw = str(p["name"])
                                p_clean = p_name_raw.lower().replace(" ", "").replace("_", "").replace("-", "")
                                if p_clean == best_param_clean or p_clean in best_param_clean or best_param_clean in p_clean:
                                    matched_p = p; break

                            # Audibility flags (MUST be set before nudge logic)
                            is_gain = any(x in best_param for x in ["Gain", "Threshold", "Volume", "OutputGain"])
                            is_linear_amp = PARAMETER_AUTHORITY.get(best_param) == "linear_amplitude"
                            is_stereo_width = PARAMETER_AUTHORITY.get(best_param) == "stereo_width_linear"
                            is_freq = any(x in best_param for x in ["Freq", "Frequency", "Cutoff"])
                            is_width = any(x in best_param for x in ["Width", "Stereo", "Spread"])
                            is_feedback = "Feedback" in best_param
                            is_drywet = any(x in best_param for x in ["DryWet", "Mix", "Amount"])

                            # 2. INTERPRET RANGE (MetaData or Fallback Authority)
                            if matched_p:
                                min_v, max_v = self._interpret_parameter_range(best_param, min_v, max_v, matched_p)
                            else:
                                # FALLBACK AUTHORITY (If device metadata is missing)
                                print(f"[FALLBACK] Using heuristic ranges for {best_param}")
                                if is_gain: min_v, max_v = -30.0, 0.0
                                elif is_freq: min_v, max_v = 400.0, 8000.0
                                elif is_drywet: min_v, max_v = 0.0, 100.0
                                elif is_feedback: min_v, max_v = 0.0, 70.0
                            
                            # 3. STATIC RANGE NUDGE (Force Movement)
                            if (min_v == max_v or abs(max_v - min_v) < 0.0001) and min_v is not None:
                                p_min, p_max = (matched_p.get("min", 0.0), matched_p.get("max", 1.0)) if matched_p else (min_v, min_v + 10.0)
                                if p_min < -1000.0: p_min = -70.0 # Safe range for math
                                
                                p_range = p_max - p_min
                                nudge = p_range * 0.20 if p_range > 0 else 1.0 # 20% escursivity
                                
                                # Escapology from Silence (-inf)
                                if is_gain and min_v < -70.0:
                                    max_v = -18.0 # Jump to highly audible level
                                    min_v = -1e9 # Restore -inf / silence
                                elif is_width and min_v >= (p_max * 0.9): 
                                    # V55: Cap width nudge at 200% (2.0), not 400%
                                    safe_w_max = min(p_max, 2.0) if is_stereo_width else p_max
                                    min_v = safe_w_max * 0.5; max_v = safe_w_max
                                elif abs(min_v - p_min) < p_range * 0.1:
                                    max_v = min_v + nudge
                                elif abs(min_v - p_max) < p_range * 0.1:
                                    min_v = max_v - nudge
                                else:
                                    min_v = min_v - (nudge/2); max_v = max_v + (nudge/2)

                            # 4. FINAL QUALITY POLISH (Audibility & Safety)
                            if is_gain and not is_linear_amp and abs(max_v - min_v) < 6.0:
                                # Increase gain escursivity to at least 15dB (only for actual dB params)
                                if max_v >= min_v: max_v = min_v + 15.0
                                else: min_v = max_v + 15.0
                            elif is_linear_amp and abs(max_v - min_v) < 0.1:
                                # V55: For linear amplitude, nudge by ±3dB equivalent
                                min_v = max(p_min, min_v * 0.5)   # ≈ -6dB
                                max_v = min(p_max, max_v * 2.0)   # ≈ +6dB
                                if max_v < 0.1: max_v = 2.0       # Safety: if near silence, jump to 0dB
                            
                            if is_feedback:
                                min_v = min(min_v, 95.0); max_v = min(max_v, 95.0)

                            # --- MACRO MOVEMENT INSURANCE (V37.5 - THE FINAL STAND) ---
                            # This runs AFTER all scaling and interpretation to guarantee movement.
                            
                            # Final hardware clamp (Pre-insurance)
                            if matched_p:
                                p_min, p_max = matched_p.get("min", 0.0), matched_p.get("max", 1.0)
                                min_v = max(p_min, min(p_max, min_v))
                                max_v = max(p_min, min(p_max, max_v))
                            
                            # ABSOLUTE MOVEMENT INSURANCE: If still static or functionally static
                            if (min_v == max_v or abs(max_v - min_v) < 0.0001) and min_v is not None:
                                print(f"[INSURANCE] Param {best_param} is static at {min_v}. Forcing range.")
                                if matched_p:
                                    p_min, p_max = matched_p.get("min", 0.0), matched_p.get("max", 1.0)
                                    p_range = p_max - p_min
                                    if p_range > 0:
                                        nudge = p_range * 0.20 # Force 20% escursivity
                                        
                                        # If at bottom, move UP. If at top, move DOWN. Else move UP.
                                        if abs(min_v - p_min) < p_range * 0.1:
                                            max_v = min_v + nudge
                                        elif abs(min_v - p_max) < p_range * 0.1:
                                            min_v = max_v - nudge
                                        else:
                                            # Center: split the nudge
                                            min_v = min_v - (nudge/2); max_v = max_v + (nudge/2)
                                        
                                        # Re-clamp after nudge
                                        min_v = max(p_min, min(p_max, min_v))
                                        max_v = max(p_min, min(p_max, max_v))
                                        
                                        # Final check for Discrete params (like Transpose): Ensure nudges are integers
                                        if "Transpose" in best_param or p_range < 25.0:
                                            if abs(max_v - min_v) < 1.0:
                                                if max_v < p_max: max_v += 1.0
                                                elif min_v > p_min: min_v -= 1.0
                                else:
                                    max_v = min_v + 1.0 # Blind fallback

                            # 5. SPECIAL CASE: "On" parameter logic (The Toggle Trap)
                            # If it's a binary "On" parameter, ensure it's expressive (usually 64 -> 127)
                            if any(x in best_param for x in ["On", "Enable", "Active"]) and "Frequency" not in best_param:
                                if min_v == max_v:
                                    min_v, max_v = 64.0, 127.0

                            mapping = MacroMapping(
                                macro_index=t_macro_idx, 
                                device_id=device.device_id, 
                                param_path=best_path + [best_param], 
                                min_val=min_v, 
                                max_val=max_v, 
                                label=macro_label
                            )
                            device.add_mapping(best_path + [best_param], mapping)
                            self.add_macro_mapping(mapping)
                            if "macro" not in plan_item: macro_idx = t_macro_idx + 1
                            local_found = True; break 
                    if local_found: break

        if macro_idx < 16:
            for chain in self.chains:
                for device in chain.devices:
                    suggestions = self.device_db.get_macro_suggestions(device.name)
                    for suggestion in suggestions:
                        while macro_idx < 16 and macro_idx in used_macros: macro_idx += 1
                        if macro_idx >= 8: break
                        p_name = suggestion['param_name']; p_path = []
                        
                        # Check if already mapped in this device
                        if tuple(p_path + [p_name]) in device.mappings: continue
                        
                        # GLOBAL DUPLICATE CHECK: Prevent same parameter name across devices
                        already_mapped = False
                        for existing_mapping in self.macro_mappings:
                            if existing_mapping.param_path[-1] == p_name:
                                already_mapped = True
                                break
                        if already_mapped: continue
                        
                        if device.xml_tag == "Eq8" and any(x in p_name for x in ["Freq", "Gain", "Q"]):
                             p_path = ["Bands.0", "ParameterA"]; p_name = p_name.replace("1 ", "").replace(" A", "")
                        mapping = MacroMapping(
                            macro_index=macro_idx, 
                            device_id=device.device_id, 
                            param_path=p_path + [p_name], 
                            min_val=suggestion['min'], 
                            max_val=suggestion['max'], 
                            label=p_name
                        )
                        device.add_mapping(mapping.param_path, mapping); self.add_macro_mapping(mapping); macro_idx += 1

    def _reorder_macro_plan(self, plan: list) -> list:
        """
        V57: Cluster-based macro reorder for device adjacency.
        
        Algorithm:
        1. Group items by macro number (atomic units)
        2. Assign each macro group a "primary device" (most params)
        3. Build device clusters: group macros by primary device
        4. Order clusters using the AI's original first-appearance order
        5. Within each cluster, put single-device macros first, multi-device bridges last
        6. Reassign sequential macro numbers
        
        This ensures all macros touching the same device are adjacent.
        """
        if not plan or len(plan) <= 1:
            return plan
        
        # 1. Group items by macro number
        macro_groups = {}
        group_order = []
        for item in plan:
            m = item.get("macro", 0)
            if m not in macro_groups:
                macro_groups[m] = []
                group_order.append(m)
            macro_groups[m].append(item)
        
        if len(macro_groups) <= 1:
            return plan
        
        # 2. For each group, compute primary device (most params) and all devices
        def norm_dev(name):
            return str(name).lower().replace(" ", "").replace("-", "").replace("_", "")
        
        group_info = {}
        for m, items in macro_groups.items():
            dev_counts = {}
            for item in items:
                dev = norm_dev(item.get("target_device", ""))
                if dev:
                    dev_counts[dev] = dev_counts.get(dev, 0) + 1
            
            # Primary = device with most params in this group
            primary = max(dev_counts, key=dev_counts.get) if dev_counts else ""
            all_devs = set(dev_counts.keys())
            group_info[m] = {
                "primary": primary,
                "all_devs": all_devs,
                "is_multi": len(all_devs) > 1,
                "original_pos": group_order.index(m)
            }
        
        # 3. Build device clusters: group macros by primary device
        # Preserve original order of first appearance for each device
        device_first_pos = {}
        for m in group_order:
            primary = group_info[m]["primary"]
            if primary not in device_first_pos:
                device_first_pos[primary] = group_info[m]["original_pos"]
        
        clusters = {}
        for m in group_order:
            primary = group_info[m]["primary"]
            if primary not in clusters:
                clusters[primary] = []
            clusters[primary].append(m)
        
        # 4. Order clusters by first appearance of their primary device
        sorted_cluster_keys = sorted(clusters.keys(), key=lambda d: device_first_pos[d])
        
        # 5. Within each cluster: single-device macros first, multi-device last
        # Multi-device macros at end of cluster act as "bridges" to next cluster
        sorted_macros = []
        for device_key in sorted_cluster_keys:
            cluster_macros = clusters[device_key]
            # Sort: single-device first (by original position), multi-device last
            singles = [m for m in cluster_macros if not group_info[m]["is_multi"]]
            multis = [m for m in cluster_macros if group_info[m]["is_multi"]]
            # Sort each sub-list by original position
            singles.sort(key=lambda m: group_info[m]["original_pos"])
            multis.sort(key=lambda m: group_info[m]["original_pos"])
            sorted_macros.extend(singles)
            sorted_macros.extend(multis)
        
        # 6. Rebuild plan with new sequential macro numbers
        new_plan = []
        for new_num, old_macro in enumerate(sorted_macros, start=1):
            for item in macro_groups[old_macro]:
                new_item = dict(item)
                new_item["macro"] = new_num
                new_plan.append(new_item)
        
        return new_plan


    def _interpret_parameter_range(self, param_name: str, min_v: float, max_v: float, p_meta: dict) -> tuple:
        """
        UNIVERSAL PARAMETER INTERPRETER (V55/59)
        Heuristically determines the correct scaling for any Ableton parameter.
        """
        import math
        p_max = p_meta.get("max", 1.0)
        p_min = p_meta.get("min", 0.0)
        auth_type = PARAMETER_AUTHORITY.get(param_name)
        
        # V59: SAFETY VALVES
        # Clamp Feedback to 0.90 to prevent runaway oscillation
        if any(x in param_name.lower() for x in ["feedback", "feedback_amount"]):
            p_max = min(p_max, 0.90)
            max_v = min(max_v, 0.90)
            min_v = min(min_v, 0.90)
            
        # Clamp Dry/Wet for time-based FX to 0.85 to preserve dry signal
        if any(x in param_name.lower() for x in ["drywet", "dry_wet", "mix"]):
            p_max = min(p_max, 0.85)
            max_v = min(max_v, 0.85)
            min_v = min(min_v, 0.85)
            
        # 0. V55: LINEAR AMPLITUDE CONVERTER (dB -> linear)
        # For params like Utility Gain (0-56.2) and Roar OutputGain (0-3.98)
        # AI sends dB values (e.g. -6, +12), we convert to linear amplitude.
        if auth_type == "linear_amplitude":
            def db_to_linear(db_val):
                """Convert dB to linear amplitude. 0dB=1.0, -6dB≈0.5, +6dB≈2.0"""
                if db_val <= -70.0: return 0.0  # Silence
                return 10.0 ** (db_val / 20.0)
            
            # If AI sent values that look like dB (negative or small positive numbers)
            # convert them. If they're already in linear range (0-56), pass through.
            if min_v < 0 or (0 <= min_v <= 1.1 and 0 <= max_v <= 1.1 and p_max > 2.0):
                # AI sent 0-1 normalized OR dB values
                if 0 <= min_v <= 1.1 and 0 <= max_v <= 1.1:
                    # 0-1 projection: map to safe linear range
                    # 0.0 -> p_min, 1.0 -> safe_max (capped at ~+12dB = 3.98)
                    safe_max = min(p_max, 4.0)  # Cap at +12dB equivalent
                    target_min = p_min + (safe_max - p_min) * min_v
                    target_max = p_min + (safe_max - p_min) * max_v
                    return target_min, target_max
                else:
                    # AI sent dB values directly (e.g. -6, +12)
                    lin_min = db_to_linear(min_v)
                    lin_max = db_to_linear(max_v)
                    # Clamp to hardware
                    lin_min = max(p_min, min(p_max, lin_min))
                    lin_max = max(p_min, min(p_max, lin_max))
                    return lin_min, lin_max
            else:
                # Values already in linear amplitude range, just clamp
                return max(p_min, min(p_max, min_v)), max(p_min, min(p_max, max_v))
        
        # 0b. V55: STEREO WIDTH LINEAR (0-4 where 1.0=100%)
        if auth_type == "stereo_width_linear":
            if 0 <= min_v <= 1.1 and 0 <= max_v <= 1.1:
                # 0-1 projection: map 0->0%, 0.5->100%, 1.0->200%
                safe_max = min(p_max, 2.5)  # Cap at 250%
                target_min = safe_max * min_v
                target_max = safe_max * max_v
                return target_min, target_max
            elif max_v > 4.0:
                # AI sent percentage (e.g. 100, 200) — convert to 0-4 scale
                return min(p_max, min_v / 100.0), min(p_max, max_v / 100.0)
            else:
                # Already in correct 0-4 scale
                return max(p_min, min(p_max, min_v)), max(p_min, min(p_max, max_v))

        # 1. AI 0.0-1.0 PROJECTOR (The Universal Scaler)
        if (0.0 <= min_v <= 1.1) and (0.0 <= max_v <= 1.1) and (p_max - p_min > 0.0):
             # V58 FIX: Handle -inf (effectively) to prevent NaN math
             safe_p_min = p_min
             if p_min < -1000.0: safe_p_min = -70.0 # Clamp -inf to -70dB for scaling math
             
             safe_p_range = p_max - safe_p_min
             target_min = safe_p_min + (safe_p_range * min_v)
             target_max = safe_p_min + (safe_p_range * max_v)
             
             # Restore -inf if min_v was 0.0 and p_min was very low
             if min_v == 0.0 and p_min < -1000.0: target_min = p_min
             if max_v == 0.0 and p_min < -1000.0: target_max = p_min

             # DISCRETE QUANTIZER: If it's a discrete param, round to nearest integer step
             if auth_type == "discrete" or (p_max - p_min < 20.0 and p_max == int(p_max) and p_min == int(p_min)):
                  target_min = round(target_min)
                  target_max = round(target_max)
             elif auth_type == "boolean":
                  target_min = 1.0 if target_min >= 0.5 else 0.0
                  target_max = 1.0 if target_max >= 0.5 else 0.0

             return target_min, target_max

        # 2. HEURISTIC TIME NORMALIZER (ms/s)
        if auth_type == "normalized_time_5s" or (any(x in param_name for x in ["Time", "DecayTime"]) and "Rate" not in param_name and p_max <= 65.0):
            p_max_ms = p_max * 1000.0
            def to_ms(v, pm):
                if v is None: return 1.0
                return v * 1000.0 if (v < pm and v != 1.0) else v
            rm_min = to_ms(min_v, p_max); rm_max = to_ms(max_v, p_max)
            return max(0.0, (rm_min - 1.0) / p_max_ms), max(0.0, (rm_max - 1.0) / p_max_ms)

        # 3. HEURISTIC HZ DETECTOR
        if auth_type == "hz_physical" or ("Freq" in param_name and p_max > 200):
            # If AI sent kHz (e.g. 15.2), convert to Hz. 
            # V48 FIX: Lowered threshold to 18.0 to prevent 40Hz -> 40kHz conversion.
            if 0 < min_v < 18.0: min_v *= 1000.0
            if 0 < max_v < 18.0: max_v *= 1000.0
            return min_v, max_v

        # 4. HEURISTIC DB/PERCENTAGE DETECTOR
        if auth_type in ["db_physical", "percentage"] or any(x in param_name for x in ["Threshold", "Volume", "Amount", "DryWet", "Mix", "Feedback"]):
             # If already projection-handled, we skip. Otherwise, ensure it's clamped.
             pass  # Fall through to universal safety clamp

        # V57: UNIVERSAL SAFETY CLAMP
        # Final safety net: if AI values exceed device bounds, fix them.
        # Case 1: Values way above device max (AI sent percentage for a 0-1 param)
        if p_max <= 1.1 and (min_v > 1.5 or max_v > 1.5):
            # AI likely sent 0-100 for a 0-1 param → project to 0-1
            min_v = min_v / 100.0
            max_v = max_v / 100.0
        
        # Case 2: Values exceed device bounds → clamp
        result_min = max(p_min, min(p_max, min_v))
        result_max = max(p_min, min(p_max, max_v))
        
        # Ensure min < max
        if result_min > result_max:
            result_min, result_max = result_max, result_min
        
        return result_min, result_max


    def _validate_signal_chain(self):
        """
        V58/59: Quality control check for signal chain order.
        Iterates through all chains and flags common musical flow inversions.
        """
        for chain in self.chains:
            prev_pos = -1
            prev_name = ""
            for device in chain.devices:
                d_name = device.name.lower()
                # Find best match in hierarchy
                current_pos = -1
                for h_name, pos in SIGNAL_CHAIN_HIERARCHY.items():
                    if h_name in d_name:
                        current_pos = pos
                        break
                
                if current_pos != -1 and prev_pos != -1:
                    if current_pos < prev_pos:
                        print(f"  [DESIGN WARNING]: Signal flow inversion detected in '{chain.name}': "
                              f"'{d_name}' (Hierarchy {current_pos}) placed after '{prev_name}' (Hierarchy {prev_pos}).")
                
                if current_pos != -1:
                    prev_pos = current_pos
                    prev_name = d_name

    def _reorder_signal_chain(self):
        """
        V59: Self-Correcting Signal Flow.
        Physically reorders devices in each chain based on SIGNAL_CHAIN_HIERARCHY.
        """
        for chain in self.chains:
            # Only reorder if there are multiple devices
            if len(chain.devices) > 1:
                def get_rank(device):
                    # V59: More robust stripping for sorting (e.g. utility2 -> utility)
                    d_name = device.name.lower()
                    clean = "".join([c for c in d_name if not c.isdigit()]).strip().replace("_", " ").replace("-", " ")
                    for h_name, pos in SIGNAL_CHAIN_HIERARCHY.items():
                        if h_name in clean:
                            return pos
                    return 5 # Neutral position if not found
                
                # Sort stable to preserve original AI order within same rank
                chain.devices.sort(key=get_rank)
                print(f"  [AUTO-FIX]: Signal chain in '{chain.name}' reordered for optimal musical flow.")

    def _check_gain_compensation(self):
        """
        V58: Quality control check for gain compensation.
        Warns if a macro controls 'Drive' but not 'Output Gain' on the same device.
        """
        macro_map = {}
        for mapping in self.macro_mappings:
            m = mapping.macro_index
            if m not in macro_map: macro_map[m] = []
            macro_map[m].append(mapping)
            
        for m, mappings in macro_map.items():
            # For each macro, find devices it controls
            dev_params = {}
            for map_item in mappings:
                # V59: Accurate device resolution for gain compensation check
                target_dev = "Unknown"
                for chain in self.chains:
                    for dev in chain.devices:
                        if dev.device_id == map_item.device_id:
                            target_dev = dev.name.lower()
                            break
                
                param = map_item.param_path[-1].lower()
                if target_dev not in dev_params: dev_params[target_dev] = []
                dev_params[target_dev].append(param)
            
            for dev, params in dev_params.items():
                has_drive = any(p in params for p in ["drive", "driveamount", "inputgain", "gain"])
                has_output = any(p in params for p in ["output", "outputgain", "makup", "volume"])
                
                # Specifically targeting distortion devices
                if has_drive and not has_output:
                    if any(d in dev for d in ["saturator", "roar", "pedal", "overdrive", "distort"]):
                        print(f"  [DESIGN WARNING]: Macro {m+1} controls 'Drive' on '{dev}' but lacks gain compensation. "
                              f"Mapping an inverse 'Output Gain' is recommended.")

    def to_xml(self) -> ET.Element:
        template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "template_rack.xml")
        tree = ET.parse(template_path)
        root = tree.getroot()
        gp = root.find("GroupDevicePreset")
        rack = gp.find("Device/AudioEffectGroupDevice")
        
        # MAPPING RESTORATION (V64): Enable 16 Modulation Sources (Macros)
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
