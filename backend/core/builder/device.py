import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from .constants import PARAMETER_AUTHORITY, ENUM_AUTHORITY
from .models import MacroMapping

class AbletonDevice:
    """Represents a single Ableton device with full parameter support"""
    
    def __init__(self, name: str, device_db, device_id: str = "0"):
        self.name = name
        self.device_id = device_id
        
        # Get device config from database
        self.device_info = device_db.get_device(name)
        
        # SAFE FALLBACK LOGIC
        if not self.device_info:
            print(f"[WARNING] Device '{name}' not found in DB. Applying Fallback strategy.")
            
            fallback_map = {
                "Echo": "Delay",
                "Spectral": "Reverb", 
                "SpectralTime": "Delay",
                "SpectralResonator": "Reverb",
                "Corpus": "Resonator",
                "Amp": "Overdrive",
                "Cabinet": "Overdrive"
            }
            
            original_name = name
            fallback_name = fallback_map.get(name, "Utility")
            
            print(f" -> Mapping '{original_name}' to '{fallback_name}'")
            self.device_info = device_db.get_device(fallback_name)
            self.name = fallback_name
            
            if not self.device_info:
                 raise ValueError(f"Critical: Fallback device '{fallback_name}' also missing!")
                 
        self.xml_tag = self.device_info['xml_tag']
        self.class_name = self.device_info['class_name']
        self.type = self.device_info['type']
        self.mappings: Dict[tuple, MacroMapping] = {}
        self.parameter_overrides: Dict[str, float] = {}
    
    def set_initial_parameter(self, name: str, value: float):
        """Set an initial value for a parameter (Surgical Control)"""
        self.parameter_overrides[name] = value

    def add_mapping(self, param_path: List[str], mapping: MacroMapping):
        self.mappings[tuple(param_path)] = mapping

    def _create_parameter(self, name: str, value: float, min_val: float = 0.0, max_val: float = 127.0, param_path: List[str] = []) -> ET.Element:
        """Create a full Ableton parameter element with optional macro mapping"""
        if name in self.parameter_overrides:
            val = self.parameter_overrides[name]
            if isinstance(val, str):
                val_lower = val.lower().strip()
                if val_lower in ENUM_AUTHORITY:
                    value = ENUM_AUTHORITY[val_lower]
                else:
                    try:
                        value = float(val)
                    except:
                        pass
            else:
                value = val

        elem = ET.Element(name)
        ET.SubElement(elem, "LomId").set("Value", "0")
        
        full_path = tuple(param_path + [name])
        mapping = self.mappings.get(full_path)
        
        if mapping:
            connector = ET.SubElement(elem, "MacroControlConnector")
            connector.set("Id", "0")
            ET.SubElement(connector, "SourceDeviceId").set("Value", "0")
            ET.SubElement(connector, "SourceEnum").set("Value", str(mapping.macro_index))
            
            key_midi = ET.SubElement(elem, "KeyMidi")
            ET.SubElement(key_midi, "PersistentKeyString").set("Value", "")
            ET.SubElement(key_midi, "IsNote").set("Value", "false")
            ET.SubElement(key_midi, "Channel").set("Value", "16")
            ET.SubElement(key_midi, "NoteOrController").set("Value", str(mapping.macro_index))
            ET.SubElement(key_midi, "LowerRangeNote").set("Value", "-1")
            ET.SubElement(key_midi, "UpperRangeNote").set("Value", "-1")
            ET.SubElement(key_midi, "ControllerMapMode").set("Value", "0")
            
            min_val = mapping.min_val
            max_val = mapping.max_val
        
        is_bool = name in ["On", "IsOn", "EditMode", "Speaker", "IsSoloed", "SoftClip", "SaturatorSoftClip", "Freeze"]
        is_enum = PARAMETER_AUTHORITY.get(name) == "enum" or name in ["Mode", "Type", "Routing", "Method", "FilterType", "ShaperType"]
        
        if is_bool:
            try:
                if isinstance(value, str):
                    val_str = "true" if value.lower() in ["true", "on", "1", "1.0"] else "false"
                else:
                    val_str = "true" if float(value) > 0.5 else "false"
            except:
                val_str = "false"
            
            ET.SubElement(elem, "Manual").set("Value", val_str)
            auto_target = ET.SubElement(elem, "AutomationTarget")
            auto_target.set("Id", "0")
            ET.SubElement(auto_target, "LockEnvelope").set("Value", "0")
            
            midi_thresh = ET.SubElement(elem, "MidiCCOnOffThresholds")
            ET.SubElement(midi_thresh, "Min").set("Value", "64")
            ET.SubElement(midi_thresh, "Max").set("Value", "127")
        else:
            try:
                numeric_val = float(value)
                if numeric_val == int(numeric_val):
                    val_str = str(int(numeric_val))
                else:
                    val_str = f"{numeric_val:.8f}".rstrip('0').rstrip('.') if "." in str(numeric_val) else str(numeric_val)
            except:
                val_str = "0"
            
            ET.SubElement(elem, "Manual").set("Value", val_str)
            auto_target = ET.SubElement(elem, "AutomationTarget")
            auto_target.set("Id", "0")
            ET.SubElement(auto_target, "LockEnvelope").set("Value", "0")
            
            if not is_enum:
                midi_range = ET.SubElement(elem, "MidiControllerRange")
                ET.SubElement(midi_range, "Min").set("Value", str(min_val))
                ET.SubElement(midi_range, "Max").set("Value", str(max_val))
                
                mod_target = ET.SubElement(elem, "ModulationTarget")
                mod_target.set("Id", "0")
                ET.SubElement(mod_target, "LockEnvelope").set("Value", "0")
        
        return elem

    def _add_metadata_fields(self, elem: ET.Element, class_name: str, is_mixer: bool = False):
        last_preset = ET.SubElement(elem, "LastPresetRef")
        val = ET.SubElement(last_preset, "Value")
        
        if is_mixer:
            p_ref = ET.SubElement(val, "AbletonDefaultPresetRef")
            p_ref.set("Id", "0")
            ET.SubElement(p_ref, "DeviceId").set("Name", class_name)
        else:
            p_ref = ET.SubElement(val, "FilePresetRef")
            p_ref.set("Id", "0")
            file_ref = ET.SubElement(p_ref, "FileRef")
            ET.SubElement(file_ref, "RelativePathType").set("Value", "0")
            ET.SubElement(file_ref, "RelativePath").set("Value", "")
            ET.SubElement(file_ref, "Path").set("Value", "")
            ET.SubElement(file_ref, "Type").set("Value", "1")
            ET.SubElement(file_ref, "LivePackName").set("Value", "")
            ET.SubElement(file_ref, "LivePackId").set("Value", "")
            ET.SubElement(file_ref, "OriginalFileSize").set("Value", "0")
            ET.SubElement(file_ref, "OriginalCrc").set("Value", "0")
            ET.SubElement(file_ref, "SourceHint").set("Value", "")
        
        ET.SubElement(elem, "LockedScripts")
        ET.SubElement(elem, "IsFolded").set("Value", "false")
        ET.SubElement(elem, "ShouldShowPresetName").set("Value", "true" if not is_mixer else "false")
        ET.SubElement(elem, "UserName").set("Value", "")
        ET.SubElement(elem, "Annotation").set("Value", "")
        
        source_ctx = ET.SubElement(elem, "SourceContext")
        ET.SubElement(source_ctx, "Value")
        
        ET.SubElement(elem, "MpePitchBendUsesTuning").set("Value", "true")
        ET.SubElement(elem, "ViewData").set("Value", "{}")
        ET.SubElement(elem, "OverwriteProtectionNumber").set("Value", "3075")

    def to_preset_xml(self, preset_id: str = "0") -> ET.Element:
        preset = ET.Element("AbletonDevicePreset")
        preset.set("Id", preset_id)
        ET.SubElement(preset, "OverwriteProtectionNumber").set("Value", "3075")
        
        device_wrapper = ET.SubElement(preset, "Device")
        device_elem = ET.SubElement(device_wrapper, self.xml_tag)
        device_elem.set("Id", "0")
        
        ET.SubElement(device_elem, "LomId").set("Value", "0")
        ET.SubElement(device_elem, "LomIdView").set("Value", "0")
        ET.SubElement(device_elem, "IsExpanded").set("Value", "true")
        ET.SubElement(device_elem, "BreakoutIsExpanded").set("Value", "false")
        
        device_elem.append(self._create_parameter("On", 1.0, 0.0, 1.0))
        ET.SubElement(device_elem, "ModulationSourceCount").set("Value", "0")
        ET.SubElement(device_elem, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(device_elem, "Pointee").set("Id", "0")
        ET.SubElement(device_elem, "LastSelectedTimeableIndex").set("Value", "0")
        ET.SubElement(device_elem, "LastSelectedClipEnvelopeIndex").set("Value", "0")
        
        self._add_metadata_fields(device_elem, self.class_name)

        if self.xml_tag == "Eq8":
            ET.SubElement(device_elem, "Precision").set("Value", "0")
            ET.SubElement(device_elem, "Mode").set("Value", "0")
            ET.SubElement(device_elem, "EditMode").set("Value", "false")
            ET.SubElement(device_elem, "SelectedBand").set("Value", "0")
            device_elem.append(self._create_parameter("GlobalGain", 0.0, -12.0, 12.0))
            device_elem.append(self._create_parameter("Scale", 1.0, -2.0, 2.0))
            for i in range(8):
                band = ET.SubElement(device_elem, f"Bands.{i}")
                for side in ["ParameterA", "ParameterB"]:
                    p_side = ET.SubElement(band, side)
                    p_path = [f"Bands.{i}", side]
                    p_side.append(self._create_parameter("IsOn", 1.0, 0, 1, p_path))
                    p_side.append(self._create_parameter("Mode", 3, 0, 7, p_path))
                    p_side.append(self._create_parameter("Freq", 100 * (i+1), 10, 22000, p_path))
                    p_side.append(self._create_parameter("Gain", 0.0, -15, 15, p_path))
                    p_side.append(self._create_parameter("Q", 0.707, 0.1, 18, p_path))
        else:
            self._create_generic_device_xml(device_elem)
        
        pref = ET.SubElement(preset, "PresetRef")
        p_ref = ET.SubElement(pref, "AbletonDefaultPresetRef")
        p_ref.set("Id", "0")
        
        file_ref2 = ET.SubElement(p_ref, "FileRef")
        ET.SubElement(file_ref2, "RelativePathType").set("Value", "0")
        ET.SubElement(file_ref2, "RelativePath").set("Value", "")
        ET.SubElement(file_ref2, "Path").set("Value", "")
        ET.SubElement(file_ref2, "Type").set("Value", "1")
        ET.SubElement(file_ref2, "LivePackName").set("Value", "")
        ET.SubElement(file_ref2, "LivePackId").set("Value", "")
        ET.SubElement(file_ref2, "OriginalFileSize").set("Value", "0")
        ET.SubElement(file_ref2, "OriginalCrc").set("Value", "0")
        ET.SubElement(file_ref2, "SourceHint").set("Value", "")
        ET.SubElement(p_ref, "DeviceId").set("Name", self.xml_tag)
        
        return preset

    def _create_generic_device_xml(self, device_elem):
        if not self.device_info or 'parameters' not in self.device_info:
            return
        for param in self.device_info['parameters']:
            p_name = param['name']
            if p_name in ["Device On", "DeviceOn", "On"]:
                continue
            is_mapped = any(p_name in mapping.param_path for mapping in self.mappings.values())
            is_simple = " " not in p_name and "." not in p_name
            if not (is_mapped or is_simple or p_name in ["DryWet", "Gain", "Amount", "Drive", "Threshold"]):
                continue
            p_def = param.get('default', 0.0)
            p_min = param.get('min', 0.0)
            p_max = param.get('max', 1.0)
            device_elem.append(self._create_parameter(p_name, p_def, p_min, p_max))

    def to_node_xml(self) -> ET.Element:
        device_elem = ET.Element(self.xml_tag)
        device_elem.set("Id", self.device_id)
        ET.SubElement(device_elem, "LomId").set("Value", "0")
        ET.SubElement(device_elem, "LomIdView").set("Value", "0")
        ET.SubElement(device_elem, "IsExpanded").set("Value", "true")
        ET.SubElement(device_elem, "BreakoutIsExpanded").set("Value", "false")
        device_elem.append(self._create_parameter("On", 1.0, 0.0, 1.0))
        ET.SubElement(device_elem, "ModulationSourceCount").set("Value", "0")
        ET.SubElement(device_elem, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(device_elem, "Pointee").set("Id", "0")
        ET.SubElement(device_elem, "LastSelectedTimeableIndex").set("Value", "0")
        ET.SubElement(device_elem, "LastSelectedClipEnvelopeIndex").set("Value", "0")
        self._add_metadata_fields(device_elem, self.class_name)
        if self.xml_tag == "Eq8":
            ET.SubElement(device_elem, "Precision").set("Value", "0")
            ET.SubElement(device_elem, "Mode").set("Value", "0")
            ET.SubElement(device_elem, "EditMode").set("Value", "false")
            ET.SubElement(device_elem, "SelectedBand").set("Value", "0")
            device_elem.append(self._create_parameter("GlobalGain", 0.0, -12.0, 12.0))
            device_elem.append(self._create_parameter("Scale", 1.0, -2.0, 2.0))
            
            for i in range(8):
                band = ET.SubElement(device_elem, f"Bands.{i}")
                for side in ["ParameterA", "ParameterB"]:
                    p_side = ET.SubElement(band, side)
                    p_path = [f"Bands.{i}", side]
                    p_side.append(self._create_parameter("IsOn", 1.0, 0, 1, p_path))
                    p_side.append(self._create_parameter("Mode", 3, 0, 7, p_path))
                    p_side.append(self._create_parameter("Freq", 100 * (i+1), 10, 22000, p_path))
                    p_side.append(self._create_parameter("Gain", 0.0, -15, 15, p_path))
                    p_side.append(self._create_parameter("Q", 0.707, 0.1, 18, p_path))
        else:
            self._create_generic_device_xml(device_elem)
        return device_elem
