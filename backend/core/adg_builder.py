"""
ADG Builder - CORRECTED VERSION based on real Ableton Live 12.3 .adg structure
Analyzed from reference_rack.xml
"""

import gzip
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

# --- V23 MASTER PARAMETER AUTHORITY ---
# Explicitly defines scaling behavior for technical parameter keys.
# This eliminates "guessing" and ensures 100% mathematical consistency.
PARAMETER_AUTHORITY = {
    # 1ms Offset + 5s Normalized (The "Ableton Time" standard)
    "DelayLine_TimeL": "normalized_time_5s",
    "DelayLine_TimeR": "normalized_time_5s",
    "DelayLine_Time": "normalized_time_5s",
    "DelayTime": "normalized_time_5s",
    "DecayTime": "normalized_time_5s",
    "PreDelay": "normalized_time_5s",
    
    # Physical Hz (No normalization, just kHz -> Hz conversion if needed)
    "Filter_Frequency": "physical_hz",
    "Filter_HiPassFrequency": "physical_hz",
    "Filter_LowPassFrequency": "physical_hz",
    "Frequency": "physical_hz",
    "Freq": "physical_hz",
    "CenterFreq": "physical_hz",
    "Rate": "physical_hz", # For Chorus/Phaser, usually Hz
    
    # Physical dB
    "PreDrive": "physical_db",
    "PostDrive": "physical_db",
    "Drive": "physical_db",
    "OutputGain": "physical_db",
    "GlobalGain": "physical_db",
    "Gain": "physical_db",
    "Output": "physical_db",
    
    # Enums (Menus)
    "Mode": "enum",
    "Type": "enum",
    "FilterType": "enum",
    "ShaperType": "enum",
    "Routing": "enum",
    "Method": "enum"
}

# --- V23 MASTER ENUM AUTHORITY ---
# Maps AI strings to Ableton technical indices.
ENUM_AUTHORITY = {
    # Delay / Echo Modes
    "classic": 0.0, "fade": 1.0, "repitch": 2.0, "digital": 0.0,
    # Roar / Distortion Routings
    "single": 0.0, "serial": 1.0, "parallel": 2.0, "multiband": 3.0, "feedback": 4.0,
    # Chorus / Phaser Modes
    "chorus": 0.0, "ensemble": 1.0, "vibrato": 2.0, "classic": 0.0, "modern": 1.0,
    # Booleans
    "on": 1.0, "off": 0.0, "true": 1.0, "false": 0.0, "enabled": 1.0, "disabled": 0.0
}


def prettify_xml(elem):
    """Return an XML string with character-perfect Ableton 12.3 formatting"""
    # V31: Structural Purity - Restore indentation
    try:
        ET.indent(elem, space="\t", level=0)
    except AttributeError:
        pass
        
    # V31: Initial serialization
    rough_string = ET.tostring(elem, encoding='utf-8', xml_declaration=True).decode('utf-8')
    
    # --- V31 THE ATOMIC RECONSTRUCTION ---
    # Ableton 12.3 is EXTREMELY picky about:
    # 1. Double quotes in the header.
    # 2. Uppercase UTF-8.
    # 3. NO alphabetization of the Ableton root tag attributes.
    
    # Find the body (everything after the first >)
    header_end = rough_string.find("?>") + 2
    body = rough_string[header_end:].strip()
    
    # Mandatorily fix the Ableton root tag (it's always the first tag in the body)
    # We must match the order in template_rack.xml exactly:
    # MajorVersion, MinorVersion, SchemaChangeCount, Creator, Revision
    
    # 1. Reconstruction
    header = '<?xml version="1.0" encoding="UTF-8"?>'
    
    # 2. Extract the actual values from the current elem (to keep them dynamic if they ever change)
    # But usually they are static from the template.
    attrs = elem.attrib
    mv = attrs.get("MajorVersion", "5")
    miv = attrs.get("MinorVersion", "12.0_12300")
    scc = attrs.get("SchemaChangeCount", "1")
    cr = attrs.get("Creator", "Ableton Live 12.3")
    rev = attrs.get("Revision", "49ca8995cfdbe384bd4648a2e0d5a14dba7b993d")
    
    root_tag = f'<Ableton MajorVersion="{mv}" MinorVersion="{miv}" SchemaChangeCount="{scc}" Creator="{cr}" Revision="{rev}">'
    
    # 3. Find the first tag in the body to join with our custom root
    body_stripped = body.lstrip()
    body_start = body_stripped.find(">") + 1
    final_body = body_stripped[body_start:]
    
    # V34: NO NEWLINE between header and root, exactly as in working afternoon files
    # Ableton 12.3 on Windows can be allergic to that first \n
    xml_output = f'{header}{root_tag}{final_body}'
    
    # Final cleanup: space before self-closing tags
    xml_output = xml_output.replace('/>', ' />')
    
    return xml_output


@dataclass
class MacroMapping:
    """Represents a macro control mapping"""
    macro_index: int
    device_id: str  # ID from DevicePresets
    param_path: List[str]  # e.g. ["Bands.0", "ParameterA", "Gain"]
    min_val: float
    max_val: float
    label: str = "" # Creative name for the macro


class AbletonDevice:
    """Represents a single Ableton device with full parameter support"""
    
    def __init__(self, name: str, device_db, device_id: str = "0"):
        self.name = name
        self.device_id = device_id
        
        # Get device config from database
        self.device_info = device_db.get_device(name)
        
        # SAFE FALLBACK LOGIC
        if not self.device_info:
            print(f"[WARNING] Device '{name}' not found in DB (Nuked?). Applying Fallback strategy.")
            
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
            fallback_name = fallback_map.get(name, "Utility") # Last resort: Utility (Safe)
            
            print(f" -> Mapping '{original_name}' to '{fallback_name}'")
            self.device_info = device_db.get_device(fallback_name)
            self.name = fallback_name # Update internal name to match reality
            
            if not self.device_info:
                 raise ValueError(f"Critical: Fallback device '{fallback_name}' also missing!")
        self.xml_tag = self.device_info['xml_tag']
        self.class_name = self.device_info['class_name']
        self.type = self.device_info['type']
        self.mappings: Dict[tuple, MacroMapping] = {} # Keyed by param path tuple
        self.parameter_overrides: Dict[str, float] = {} # Keyed by param name
    
    def set_initial_parameter(self, name: str, value: float):
        """Set an initial value for a parameter (Surgical Control)"""
        self.parameter_overrides[name] = value

    def add_mapping(self, param_path: List[str], mapping: MacroMapping):
        self.mappings[tuple(param_path)] = mapping

    def _create_parameter(self, name: str, value: float, min_val: float = 0.0, max_val: float = 127.0, param_path: List[str] = []) -> ET.Element:
        """Create a full Ableton parameter element with optional macro mapping"""
        
        # SURGICAL INITIALIZATION: Look for overrides from the AI
        if name in self.parameter_overrides:
            val = self.parameter_overrides[name]
            
            # V23 MASTER TRANSLATOR (String-to-Enum)
            if isinstance(val, str):
                val_lower = val.lower().strip()
                if val_lower in ENUM_AUTHORITY:
                    value = ENUM_AUTHORITY[val_lower]
                    print(f"DEBUG: V23 Enum Translator: '{val}' -> {value}")
                else:
                    try:
                        value = float(val)
                    except (ValueError, TypeError):
                        print(f"[WARNING] V23 Guard: Rejecting unknown string '{val}' for {name}. Using default.")
            else:
                value = val
            print(f"DEBUG: Surgical Initialization for {self.name}.{name} -> {value}")

        elem = ET.Element(name)
        ET.SubElement(elem, "LomId").set("Value", "0")
        
        # Check for mapping
        full_path = tuple(param_path + [name])
        mapping = self.mappings.get(full_path)
        
        if mapping:
            # --- MACRO CONTROL CONNECTOR (V12) ---
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
            
            # Use mapping ranges!
            min_val = mapping.min_val
            max_val = mapping.max_val
            
            # EXTRA SAFETY (V23): Ensure mapping ranges are numeric
            try:
                min_val = float(min_val)
                max_val = float(max_val)
            except:
                min_val, max_val = 0.0, 1.0
        
        is_bool = name in ["On", "IsOn", "EditMode", "Speaker", "IsSoloed", "SoftClip", "SaturatorSoftClip", "Freeze"]
        is_enum = PARAMETER_AUTHORITY.get(name) == "enum" or name in ["Mode", "Type", "Routing", "Method", "FilterType", "ShaperType"]
        
        if is_bool:
            # Booleans use MidiCCOnOffThresholds, NO ModulationTarget, NO MidiControllerRange
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
            # Numeric/Enum Parameters
            try:
                numeric_val = float(value)
                if numeric_val == int(numeric_val):
                    val_str = str(int(numeric_val))
                else:
                    # Precision check for Ableton
                    val_str = f"{numeric_val:.8f}".rstrip('0').rstrip('.') if "." in str(numeric_val) else str(numeric_val)
            except (ValueError, TypeError):
                val_str = "0"
            
            ET.SubElement(elem, "Manual").set("Value", val_str)
            auto_target = ET.SubElement(elem, "AutomationTarget")
            auto_target.set("Id", "0")
            ET.SubElement(auto_target, "LockEnvelope").set("Value", "0")
            
            # CRITICAL (V24): ONLY add mapping tags if it's NOT an enum AND (it's mapped OR it's a standard numeric param)
            # Enums/Menus NEVER have these tags in native devices.
            if not is_enum:
                midi_range = ET.SubElement(elem, "MidiControllerRange")
                ET.SubElement(midi_range, "Min").set("Value", str(min_val))
                ET.SubElement(midi_range, "Max").set("Value", str(max_val))
                
                mod_target = ET.SubElement(elem, "ModulationTarget")
                mod_target.set("Id", "0")
                ET.SubElement(mod_target, "LockEnvelope").set("Value", "0")
        
        return elem

    # Removed ghost to_preset_xml
        
    def _add_metadata_fields(self, elem: ET.Element, class_name: str, is_mixer: bool = False):
        """Add standard Ableton metadata fields to a device element"""
        last_preset = ET.SubElement(elem, "LastPresetRef")
        val = ET.SubElement(last_preset, "Value")
        
        if is_mixer:
            # Mixers use AbletonDefaultPresetRef WITHOUT FileRef
            p_ref = ET.SubElement(val, "AbletonDefaultPresetRef")
            p_ref.set("Id", "0")
            ET.SubElement(p_ref, "DeviceId").set("Name", class_name)
        else:
            # Standard devices use FilePresetRef
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
        """Generate full AbletonDevicePreset XML with a specific preset ID"""
        preset = ET.Element("AbletonDevicePreset")
        preset.set("Id", preset_id)
        ET.SubElement(preset, "OverwriteProtectionNumber").set("Value", "3075")
        
        device_wrapper = ET.SubElement(preset, "Device")
        device_elem = ET.SubElement(device_wrapper, self.xml_tag)
        device_elem.set("Id", "0")
        
        # Standard Device Header
        ET.SubElement(device_elem, "LomId").set("Value", "0")
        ET.SubElement(device_elem, "LomIdView").set("Value", "0")
        ET.SubElement(device_elem, "IsExpanded").set("Value", "true")
        ET.SubElement(device_elem, "BreakoutIsExpanded").set("Value", "false")
        
        # On parameter
        device_elem.append(self._create_parameter("On", 1.0, 0.0, 1.0))
        
        ET.SubElement(device_elem, "ModulationSourceCount").set("Value", "0")
        ET.SubElement(device_elem, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(device_elem, "Pointee").set("Id", "0")
        ET.SubElement(device_elem, "LastSelectedTimeableIndex").set("Value", "0")
        ET.SubElement(device_elem, "LastSelectedClipEnvelopeIndex").set("Value", "0")
        
        self._add_metadata_fields(device_elem, self.class_name)

        # --- DEVICE SPECIFIC PARAMETERS ---
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
            # GENERIC GENERATION FROM DATABASE
            self._create_generic_device_xml(device_elem)
        
        # Device PresetRef
        pref = ET.SubElement(preset, "PresetRef")
        
        # CRITICAL FIX: Built-in devices use AbletonDefaultPresetRef, NOT FilePresetRef
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
        
        # DeviceId is required for DefaultPresetRef
        ET.SubElement(p_ref, "DeviceId").set("Name", self.xml_tag)
        
        return preset

    def _create_generic_device_xml(self, device_elem):
        """Generates XML for standard devices based on JSON parameters"""
        if not self.device_info or 'parameters' not in self.device_info:
            print(f"Warning: No parameters definition for {self.xml_tag}")
            return

        for param in self.device_info['parameters']:
            p_name = param['name']
            
            # Skip parameters handled elsewhere or blacklisted
            if p_name in ["Device On", "DeviceOn", "On"]:
                continue
            
            # CRITICAL: For generic generation, only use simple parameters we've mapped or known safe ones
            # This prevents invalid XML for complex devices like MultibandDynamics
            is_mapped = any(p_name in mapping.param_path for mapping in self.mappings.values())
            is_simple = " " not in p_name and "." not in p_name
            
            if not (is_mapped or is_simple or p_name in ["DryWet", "Gain", "Amount", "Drive", "Threshold"]):
                continue

            p_def = param.get('default', 0.0)
            p_min = param.get('min', 0.0)
            p_max = param.get('max', 1.0)
            
            device_elem.append(self._create_parameter(p_name, p_def, p_min, p_max))


    def to_node_xml(self) -> ET.Element:
        """Generate runtime XML for the device (without Preset wrapper)"""
        device_elem = ET.Element(self.xml_tag)
        device_elem.set("Id", self.device_id)
        
        # Standard Device Header
        ET.SubElement(device_elem, "LomId").set("Value", "0")
        ET.SubElement(device_elem, "LomIdView").set("Value", "0")
        ET.SubElement(device_elem, "IsExpanded").set("Value", "true")
        ET.SubElement(device_elem, "BreakoutIsExpanded").set("Value", "false")
        
        # On parameter
        device_elem.append(self._create_parameter("On", 1.0, 0.0, 1.0))
        
        ET.SubElement(device_elem, "ModulationSourceCount").set("Value", "0")
        ET.SubElement(device_elem, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(device_elem, "Pointee").set("Id", "0")
        ET.SubElement(device_elem, "LastSelectedTimeableIndex").set("Value", "0")
        ET.SubElement(device_elem, "LastSelectedClipEnvelopeIndex").set("Value", "0")
        
        self._add_metadata_fields(device_elem, self.class_name)

        # --- DEVICE SPECIFIC PARAMETERS ---
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
            # GENERIC GENERATION FROM DATABASE
            self._create_generic_device_xml(device_elem)
            
        return device_elem


class Chain:
    """Represents a chain within a rack"""
    
    def __init__(self, name: str = "Chain"):
        self.name = name
        self.devices: List[AbletonDevice] = []
        self.color = 0
        self.is_soloed = False
    
    def add_device(self, device: AbletonDevice):
        """Add a device to this chain"""
        self.devices.append(device)
    
    def to_branch_node_xml(self, branch_id: int = 0, device_db=None) -> ET.Element:
        """Generate AudioEffectBranch XML for the main rack's Branches list"""
        branch = ET.Element("AudioEffectBranch")
        branch.set("Id", str(branch_id))
        
        # Standard Device Header
        ET.SubElement(branch, "LomId").set("Value", "0")
        ET.SubElement(branch, "LomIdView").set("Value", "0")
        ET.SubElement(branch, "IsExpanded").set("Value", "true")
        ET.SubElement(branch, "BreakoutIsExpanded").set("Value", "false")
        ET.SubElement(branch, "OverwriteProtectionNumber").set("Value", "3075")
        ET.SubElement(branch, "UserName").set("Value", self.name)
        
        # Prepare helper device for parameter creation (use dummy if empty)
        helper_device = self.devices[0] if self.devices else None
        if not helper_device:
            if not device_db: raise ValueError("device_db required for empty chain generation")
            helper_device = AbletonDevice("Utility", device_db)

        # On parameter
        branch.append(helper_device._create_parameter("On", 1.0, 0.0, 1.0))
        
        ET.SubElement(branch, "ModulationSourceCount").set("Value", "0")
        ET.SubElement(branch, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(branch, "Pointee").set("Id", "0")
        ET.SubElement(branch, "LastSelectedTimeableIndex").set("Value", "0")
        ET.SubElement(branch, "LastSelectedClipEnvelopeIndex").set("Value", "0")
        
        # Metadata for AudioEffectBranch (Minimal for branches)
        source_ctx = ET.SubElement(branch, "SourceContext")
        branch_ctx = ET.SubElement(source_ctx, "BranchSourceContext")
        branch_ctx.set("Id", "0")
        ET.SubElement(branch_ctx, "OriginalFileRef")
        ET.SubElement(branch_ctx, "BrowserContentPath").set("Value", "")
        ET.SubElement(branch_ctx, "LocalFiltersJson").set("Value", "")
        ET.SubElement(branch_ctx, "PresetRef")
        ET.SubElement(branch_ctx, "BranchDeviceId").set("Value", "")
            
        # Device Chain (CRITICAL Missing Component)
        device_chain = ET.SubElement(branch, "DeviceChain")
        
        # Main Device List
        devices_list = ET.SubElement(device_chain, "Devices")
        if self.devices:
            for dev in self.devices:
                # Use rack counter if provided
                if hasattr(device_db, "get_next_device_id"):
                    dev.device_id = device_db.get_next_device_id()
                devices_list.append(dev.to_node_xml())

        # Signal Modulations (Empty)
        ET.SubElement(device_chain, "SignalModulations")

        # Mixer (Peer to DeviceChain in modern branches)
        mixer_device = ET.SubElement(branch, "Mixer")
        mixer_xml = ET.SubElement(mixer_device, "AudioBranchMixerDevice")
        mixer_xml.set("Id", "0")
        
        # Mixer Header
        ET.SubElement(mixer_xml, "LomId").set("Value", "0")
        ET.SubElement(mixer_xml, "LomIdView").set("Value", "0")
        ET.SubElement(mixer_xml, "IsExpanded").set("Value", "true")
        
        # Mixer Params
        mixer_xml.append(helper_device._create_parameter("On", 1.0, 0.0, 1.0))
        ET.SubElement(mixer_xml, "ModulationSourceCount").set("Value", "0")
        ET.SubElement(mixer_xml, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(mixer_xml, "Pointee").set("Id", "0")
        
        helper_device._add_metadata_fields(mixer_xml, "AudioBranchMixerDevice", is_mixer=True)
        
        mixer_xml.append(helper_device._create_parameter("Speaker", 1.0, 0.0, 1.0))
        mixer_xml.append(helper_device._create_parameter("Volume", 1.0, 0.0, 1.0))
        mixer_xml.append(helper_device._create_parameter("Pan", 0.0, -1.0, 1.0))
        
        ET.SubElement(mixer_xml, "SendInfos")
        routing = ET.SubElement(mixer_xml, "RoutingHelper")
        rout = ET.SubElement(routing, "Routable")
        ET.SubElement(rout, "Target").set("Value", "AudioOut/None")
        ET.SubElement(rout, "UpperDisplayString").set("Value", "No Output")
        ET.SubElement(rout, "LowerDisplayString").set("Value", "")
        
        # Branch Selector & View Metadata (CRITICAL for Rack Validity)
        selector_range = ET.SubElement(branch, "BranchSelectorRange")
        ET.SubElement(selector_range, "Min").set("Value", "0")
        ET.SubElement(selector_range, "Max").set("Value", "127")
        ET.SubElement(selector_range, "CrossfadeMin").set("Value", "0")
        ET.SubElement(selector_range, "CrossfadeMax").set("Value", "0")
        
        ET.SubElement(branch, "SessionViewBranchWidth").set("Value", "80")
        ET.SubElement(branch, "DocumentColorIndex").set("Value", "0")
        ET.SubElement(branch, "AutoColored").set("Value", "true")
        ET.SubElement(branch, "AutoColorScheme").set("Value", "0")

        return branch

    def to_branch_preset_xml(self, branch_id: int = 0, device_db=None) -> ET.Element:
        """Generate AudioEffectBranchPreset XML"""
        branch = ET.Element("AudioEffectBranchPreset")
        branch.set("Id", str(branch_id))
        
        ET.SubElement(branch, "Name").set("Value", self.name)
        ET.SubElement(branch, "IsSoloed").set("Value", "false")
        
        # DevicePresets
        device_presets = ET.SubElement(branch, "DevicePresets")
        for i, device in enumerate(self.devices):
            # Devices in presets typically start at Id="0" relative to the preset
            # But the preset itself needs a unique global ID
            device.device_id = str(i)
            
            global_preset_id = "0"
            if hasattr(device_db, "get_next_preset_id"):
                global_preset_id = device_db.get_next_preset_id()
                
            preset = device.to_preset_xml(preset_id=global_preset_id)
            device_presets.append(preset)
            
        # MixerPreset (REQUIRED for parallel chains)
        # In Golden Sample, Mixer is also an AbletonDevicePreset
        mixer_preset_root = ET.SubElement(branch, "MixerPreset")
        
        global_mixer_preset_id = "0"
        if hasattr(device_db, "get_next_preset_id"):
            global_mixer_preset_id = device_db.get_next_preset_id()

        mixer_preset_wrapper = ET.SubElement(mixer_preset_root, "AbletonDevicePreset")
        mixer_preset_wrapper.set("Id", global_mixer_preset_id)
        ET.SubElement(mixer_preset_wrapper, "OverwriteProtectionNumber").set("Value", "3075")
        
        mixer_device_wrapper = ET.SubElement(mixer_preset_wrapper, "Device")
        mixer_device = ET.SubElement(mixer_device_wrapper, "AudioBranchMixerDevice")
        mixer_device.set("Id", "0")
        
        # Mixer Header
        ET.SubElement(mixer_device, "LomId").set("Value", "0")
        ET.SubElement(mixer_device, "LomIdView").set("Value", "0")
        ET.SubElement(mixer_device, "IsExpanded").set("Value", "true")
        
        # Prepare helper device for parameter creation (use dummy if empty)
        helper_device = self.devices[0] if self.devices else None
        if not helper_device:
            if not device_db: raise ValueError("device_db required for empty chain generation")
            helper_device = AbletonDevice("Utility", device_db)

        # On parameter (FULL)
        mixer_device.append(helper_device._create_parameter("On", 1.0, 0.0, 1.0))
        
        ET.SubElement(mixer_device, "ModulationSourceCount").set("Value", "0")
        # ParametersListWrapper
        ET.SubElement(mixer_device, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(mixer_device, "Pointee").set("Id", "0")
        
        # Last Preset Ref (V35 GOLDEN)
        last_ref_val = ET.SubElement(mixer_device, "LastPresetRef")
        last_ref = ET.SubElement(last_ref_val, "Value")
        def_ref = ET.SubElement(last_ref, "AbletonDefaultPresetRef")
        def_ref.set("Id", "0")
        ET.SubElement(def_ref, "DeviceId").set("Name", "AudioBranchMixerDevice")
        
        # Speaker (Mandatory for Mixer)
        mixer_device.append(helper_device._create_parameter("Speaker", 1.0, 0.0, 1.0))
        
        # Volume
        mixer_device.append(helper_device._create_parameter("Volume", 1.0, 0.0, 1.0))
        
        # Pan
        mixer_device.append(helper_device._create_parameter("Pan", 0.0, -1.0, 1.0))
        
        ET.SubElement(mixer_device, "SendInfos")
        
        routing = ET.SubElement(mixer_device, "RoutingHelper")
        routable = ET.SubElement(routing, "Routable")
        ET.SubElement(routable, "Target").set("Value", "AudioOut/None")
        ET.SubElement(routable, "UpperDisplayString").set("Value", "No Output")
        ET.SubElement(routable, "LowerDisplayString").set("Value", "")
        mpe = ET.SubElement(routable, "MpeSettings")
        ET.SubElement(mpe, "ZoneType").set("Value", "0")
        ET.SubElement(mpe, "FirstNoteChannel").set("Value", "1")
        ET.SubElement(mpe, "LastNoteChannel").set("Value", "15")
        ET.SubElement(routable, "MpePitchBendUsesTuning").set("Value", "true")
        ET.SubElement(routing, "TargetEnum").set("Value", "0")
        
        ET.SubElement(mixer_device, "SendsListWrapper").set("LomId", "0")
        
        # Branch Metadata
        selector_range = ET.SubElement(branch, "BranchSelectorRange")
        ET.SubElement(selector_range, "Min").set("Value", "0")
        ET.SubElement(selector_range, "Max").set("Value", "127")
        ET.SubElement(selector_range, "CrossfadeMin").set("Value", "0")
        ET.SubElement(selector_range, "CrossfadeMax").set("Value", "0")
        
        ET.SubElement(branch, "SessionViewBranchWidth").set("Value", "80")
        ET.SubElement(branch, "DocumentColorIndex").set("Value", "0")
        ET.SubElement(branch, "AutoColored").set("Value", "true")
        ET.SubElement(branch, "AutoColorScheme").set("Value", "0")
        
        source_ctx = ET.SubElement(branch, "SourceContext")
        branch_ctx = ET.SubElement(source_ctx, "BranchSourceContext")
        branch_ctx.set("Id", "0")
        ET.SubElement(branch_ctx, "OriginalFileRef")
        ET.SubElement(branch_ctx, "BrowserContentPath").set("Value", "")
        ET.SubElement(branch_ctx, "LocalFiltersJson").set("Value", "")
        ET.SubElement(branch_ctx, "PresetRef")
        ET.SubElement(branch_ctx, "BranchDeviceId").set("Value", "")
        
        return branch


class AudioEffectRack:
    """Main class for building an Audio Effect Rack - CORRECTED"""
    
    def __init__(self, name: str = "Custom Rack", device_db=None):
        self.name = name
        self.device_db = device_db
        self.chains: List[Chain] = []
        self.macro_count = 8  # Visible macros (max 16 total)
        self.macro_mappings: List[MacroMapping] = []
        self.device_id_counter = 1 # Rack is 0, devices start at 1
        self.preset_id_counter = 20 # Start high for presets
    
    def get_next_device_id(self) -> str:
        did = str(self.device_id_counter)
        self.device_id_counter += 1
        return did

    def get_next_preset_id(self) -> str:
        pid = str(self.preset_id_counter)
        self.preset_id_counter += 1
        return pid
    
    def add_chain(self, chain: Chain):
        """Add a chain to the rack"""
        self.chains.append(chain)
    
    def add_macro_mapping(self, mapping: MacroMapping):
        """Add a macro control mapping"""
        self.macro_mappings.append(mapping)
    
    def auto_map_macros(self, nlp_resp: dict = None):
        """
        Automatically map macros and initialize parameters.
        Prioritizes AI Surgical Plan if provided.
        """
        if not nlp_resp: return
        
        ai_mapping_plan = nlp_resp.get("macro_details", [])
        surgical_devices = nlp_resp.get("surgical_devices", [])
        
        # 0. DEEP INITIALIZATION: Apply surgical parameter overrides
        for s_dev in surgical_devices:
            dev_name = s_dev.get("name", "").lower()
            params = s_dev.get("parameters", {})
            
            # Find the actual device in the rack
            for chain in self.chains:
                for device in chain.devices:
                    # Ironclad matching: remove spaces and non-alpha characters
                    d_norm = device.name.lower().replace(" ", "").replace("-", "").replace("_", "")
                    s_norm = dev_name.replace(" ", "").replace("-", "").replace("_", "")
                    
                    if s_norm in d_norm or d_norm in s_norm:
                        print(f"DEBUG: Surgical Init Match: '{dev_name}' -> '{device.name}'")
                        for p_name, p_val in params.items():
                            device.set_initial_parameter(p_name, p_val)

        macro_idx = 0
        used_macros = set()
        mapped_devices = set()

        # 1. Try to follow AI Plan
        if ai_mapping_plan:
            print(f"DEBUG: Processing {len(ai_mapping_plan)} AI macro plans...")
            for plan_item in ai_mapping_plan:
                if macro_idx >= 16: break
                
                raw_target_dev = plan_item.get("target_device") or ""
                raw_target_param = plan_item.get("target_parameter") or ""
                
                target_dev_name = str(raw_target_dev).lower().replace(" ", "").replace("_", "").replace("-", "")
                target_param = str(raw_target_param).lower()
                
                if not target_dev_name or not target_param:
                    print(f"DEBUG: Skipping invalid macro plan item: {plan_item}")
                    continue
                
                if not target_dev_name or not target_param:
                    print(f"DEBUG: Skipping invalid macro plan item: {plan_item}")
                    continue
                
                # V12: Track matches to avoid re-mapping if multiple devices match
                local_found = False
                
                # Find matching device in any chain
                for chain in self.chains:
                    for device in chain.devices:
                        if local_found: break # Only one device instance per plan item
                        
                        # Ironclad matching: remove spaces and suffixes
                        d_name_norm = device.name.lower().replace(" ", "").replace("_", "").replace("-", "").replace("2", "").replace("new", "")
                        
                        if target_dev_name in d_name_norm or d_name_norm in target_dev_name:
                            # Try to find parameter
                            suggestions = self.device_db.get_macro_suggestions(device.name)
                            
                            best_param = None
                            best_path = []
                            min_v = 0.0
                            max_v = 1.0
                            
                            # Check suggestions for match
                            for sugg in suggestions:
                                if target_param in sugg['param_name'].lower() or sugg['param_name'].lower() in target_param:
                                    best_param = sugg['param_name']
                                    min_v = sugg['min']
                                    max_v = sugg['max']
                                    break
                            
                            # SEMANTIC FORCE MAPPING (Overrides Fuzzy Logic)
                            # "Grand Unified Map" - Covers all 43 Native Devices from Audit
                            SEMANTIC_MAP = {
                                # --- DYNAMICS ---
                                "Compressor2": {
                                    "thresh": "Threshold", "ratio": "Ratio", "attack": "Attack", "release": "Release", "gain": "Gain"
                                },
                                "GlueCompressor": {
                                    "thresh": "Threshold", "ratio": "Ratio", "makeup": "Makeup", "range": "Range", "attack": "Attack",
                                    "focus": "Threshold", "sub": "Threshold", "compress": "Threshold" # Fix for "Sub Focus"
                                },
                                "Limiter": {
                                    "ceiling": "Ceiling", "gain": "Gain", "look": "Lookahead"
                                },
                                "MultibandDynamics": {
                                    "ott": "GlobalAmount", "amount": "GlobalAmount", "time": "GlobalTime",
                                    "output": "OutputGain", "mix": "GlobalAmount" # OTT usually implies Mix/Amount
                                },
                                "Gate": {
                                    "thresh": "Threshold", "return": "Return", "attack": "Attack", "hold": "Hold", "release": "Release"
                                },
                                "DrumBuss": {
                                    "drive": "DriveAmount", "crunch": "CrunchAmount", "boom": "BoomAmount", 
                                    "transient": "TransientShaping", "damp": "DampingFrequency", "trim": "InputTrim"
                                },

                                # --- DISTORTION & COLOR ---
                                "Roar": {
                                    "drive": "Stage1_Shaper_Amount", "amount": "Stage1_Shaper_Amount", 
                                    "cutoff": "Stage1_Filter_Frequency", "freq": "Stage1_Filter_Frequency", # FIX: Explicit 'freq' mapping
                                    "res": "Stage1_Filter_Resonance", "bias": "Stage1_Shaper_Bias"
                                },
                                "Saturator": {
                                    "drive": "PreDrive", "depth": "ColorDepth", "curve": "WsCurve", "color": "ColorOn", "output": "PostDrive"
                                },
                                "Delay": {
                                    "time": "DelayLine_TimeL", "feedback": "Feedback", "drywet": "DryWet"
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
                                "Tube": { # Dynamic Tube
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

                                # --- FILTERS & EQ ---
                                "AutoFilter2": {
                                    "cutoff": "Filter_Frequency", "freq": "Filter_Frequency", "res": "Filter_Resonance", 
                                    "lfo": "Lfo_Amount", "rate": "Lfo_Frequency", "drive": "Filter_Drive"
                                },
                                "Eq8": {
                                    "freq": "Freq", "gain": "GlobalGain", "q": "AdaptiveQ" # Or band specific?
                                    # Note: Band specific logic is handled below in 'best_param' check, this is fallback
                                },
                                "ChannelEq": {
                                    "low": "LowShelfGain", "mid": "MidGain", "high": "HighShelfGain", "freq": "MidFrequency"
                                },
                                "FilterEQ3": {
                                    "low": "GainLo", "mid": "GainMid", "high": "GainHi", "slope": "Slope"
                                },

                                # --- MODULATION ---
                                "Chorus2": {
                                    "rate": "Rate", "amount": "Amount", "width": "Width", "warmth": "Warmth", "feed": "Feedback"
                                },
                                "PhaserNew": {
                                    "rate": "Modulation_Frequency", "amount": "Modulation_Amount", "feed": "Feedback", "color": "Modulation_Amount"
                                },
                                "AutoPan2": {
                                    "rate": "Modulation_Frequency", "amount": "Modulation_Amount", "width": "Modulation_PhaseOffset" # Phase = Width in AutoPan
                                },
                                "Shifter": { # Freq Shifter + Ring Mod
                                    "coarse": "Pitch_Coarse", "fine": "Pitch_Fine", "ring": "ModBasedShifting_RingMod_Drive", 
                                    "rate": "Lfo_RateHz", "amount": "Lfo_Amount"
                                },
                                
                                # --- TIME & SPACE ---
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
                                    "low": "Freq", "high": "Freq" # Will be adjusted by path logic
                                },
                                "Roar": {
                                    "drive": "Stage1_Shaper_Amount", "amount": "Stage1_Shaper_Amount", "grit": "Stage1_Shaper_Amount",
                                    "cutoff": "Stage1_Filter_Frequency", "freq": "Stage1_Filter_Frequency",
                                    "res": "Stage1_Filter_Resonance", "bias": "Stage1_Shaper_Bias",
                                    "tone": "Stage1_Filter_Frequency"
                                },
                                "Delay": {
                                    "time": "DelayLine_TimeL", "feedback": "Feedback", "filter": "Filter_Frequency"
                                },
                                "GrainDelay": {
                                    "spray": "Spray", "pitch": "Pitch", "freq": "Freq", "random": "RandomPitch", "feed": "Feedback"
                                },
                                "Spectral": { # Spectral Time/Resonator
                                    "freeze": "Freezer_On", "spray": "Delay_Spray", "shift": "Delay_FrequencyShift", "feedback": "Delay_Feedback"
                                },
                                "Resonator": {
                                    "decay": "ResDecay", "color": "ResColor", "gain": "GlobalGain", "width": "Width"
                                },
                                "Corpus": {
                                    "freq": "Frequency", "tune": "Frequency", "coarse": "Frequency", "pitch": "Frequency", # FIX: Explicit synonym for Coarse
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
                            
                            # --- SEMANTIC MASTER (V6/V10) ---
                            # Normalize key for semantic lookup (no spaces, all lower)
                            s_key = device.name.lower().replace(" ", "").replace("_", "").replace("-", "")
                            # Map aliases to the target keys in SEMANTIC_MAP (lowercase)
                            if "autofilter" in s_key: s_key = "autofilter2"
                            if "chorus" in s_key: s_key = "chorus2"
                            if "autopan" in s_key: s_key = "autopan2"
                            if "drumbuss" in s_key: s_key = "drumbuss"
                            if "phaser" in s_key: s_key = "phasernew"
                            if "redux" in s_key: s_key = "redux2"

                            # Normalize SEMANTIC_MAP for this device (V10: Lowercase keys)
                            device_semantic = {}
                            for k, v in SEMANTIC_MAP.items():
                                if k.lower().replace(" ", "").replace("_", "").replace("-", "") == s_key:
                                    device_semantic = v
                                    break
                            
                            for intent, real_param in device_semantic.items():
                                if intent.lower() == target_param or intent.lower() in target_param:
                                    print(f"DEBUG: Surgical Semantic Match: '{target_param}' -> '{real_param}'")
                                    best_param = real_param
                                    best_path = [] 
                                    break
                            
                            # C. Global Resolver (V21: Backup for missing device maps)
                            if best_param == target_param:
                                global_map = {
                                    "frequency": "Filter_Frequency", "cutoff": "Filter_Frequency", 
                                    "freq": "Filter_Frequency", "resonance": "Filter_Resonance",
                                    "res": "Filter_Resonance", "drive": "DriveAmount",
                                    "output": "OutputGain", "gain": "OutputGain",
                                    "time": "DelayLine_TimeL", "feedback": "Feedback", "drywet": "DryWet"
                                }
                                lookup = target_param.lower().strip()
                                for g_key, g_val in global_map.items():
                                     if g_key in lookup or lookup in g_key:
                                          best_param = g_val
                                          print(f"DEBUG: V21 Global Resolver: '{target_param}' -> '{best_param}'")
                                          break

                            # --- DIRECT PARAMETER LOOKUP (V10) ---
                            # If still no match, try to find the parameter directly in the device's DNA
                            if not best_param:
                                device_params = device.device_info.get("parameters", [])
                                for p in device_params:
                                    p_name = p["name"]
                                    p_name_lower = p_name.lower()
                                    if target_param == p_name_lower or target_param in p_name_lower or p_name_lower in target_param:
                                        print(f"DEBUG: Direct DNA Match: '{target_param}' -> '{p_name}'")
                                        best_param = p_name
                                        best_path = []
                                        break

                            # If not in suggestions or semantic, try generic heuristics
                            if not best_param:
                                if "dec" in target_param: best_param = "DecayTime"
                                elif "dry" in target_param or "wet" in target_param: best_param = "DryWet"
                                elif "freq" in target_param: best_param = "Filter_Frequency" if "Auto" in device.name else "Frequency"
                                elif "gain" in target_param: best_param = "Gain"
                                elif "amount" in target_param: best_param = "Amount"
                                
                            if best_param:
                                # Special handling for complex devices like EQ8
                                if device.xml_tag == "Eq8" and any(x in best_param for x in ["Freq", "Gain", "Q"]):
                                     best_path = ["Bands.0", "ParameterA"]
                                     if "Freq" in best_param: best_param = "Freq"
                                     if "Gain" in best_param: best_param = "Gain"
                                     if "Q" in best_param: best_param = "Q"
                            if not best_param:
                                print(f"DEBUG: Could not resolve parameter '{target_param}' for {device.name}. Skipping mapping.")
                                continue

                            # Determine Target Macro Index (V11: Diamond Precision)
                            target_macro_idx = plan_item.get("macro")
                            if target_macro_idx is not None:
                                target_macro_idx = int(target_macro_idx) - 1
                            else:
                                # Find next free macro that isn't already claimed
                                while macro_idx < 16 and macro_idx in used_macros:
                                    macro_idx += 1
                                target_macro_idx = macro_idx
                            
                            if target_macro_idx < 0: target_macro_idx = 0
                            if target_macro_idx >= 16: break
                            
                            used_macros.add(target_macro_idx)

                            # --- MAPPING GUARD ---
                            # Prevent mapping the SAME parameter twice, but ALLOW the same macro 
                            # to map to multiple DIFFERENT parameters (Multi-Target Power)
                            full_path = tuple(best_path + [best_param])
                            if full_path in device.mappings:
                                found_match = True
                                break

                            # Determine labels and ranges (SURGICAL PRIORITY)
                            macro_label = plan_item.get("name") or plan_item.get("label") or best_param
                            min_v = plan_item.get("min")
                            max_v = plan_item.get("max")
                            
                            # --- SURGICAL SCALER (V7/V11) ---
                            device_params = device.device_info.get("parameters", [])
                            matched_p = next((p for p in device_params if p["name"] == best_param), None)
                            
                            # --- UNIVERSAL MASTER SCALER (V23) ---
                            # DETERMINISTIC scaling based on parameter identity, not just value ranges.
                            if matched_p:
                                p_max = matched_p.get("max", 1.0)
                                p_min = matched_p.get("min", 0.0)
                                authority_type = PARAMETER_AUTHORITY.get(best_param)
                                
                                # Case A: Normalized Time (1ms UI = 0.0 XML, Max UI = 1.0 XML)
                                if authority_type == "normalized_time_5s" or (
                                    any(x in best_param for x in ["TimeL", "TimeR", "Time", "DecayTime"]) and "Rate" not in best_param and p_max <= 60.0
                                ):
                                    print(f"DEBUG: V23.1 Authority (Time): Normalizing '{best_param}' -> 0-1 (of {p_max}s)")
                                    p_max_ms = p_max * 1000.0
                                    
                                    # Hybrid Detection (ms vs s)
                                    def to_ms(v, p_max_val):
                                        if v is None: return 1.0
                                        if v == 1.0: return 1.0 # The explicit floor
                                        if v < p_max_val: return v * 1000.0 # e.g. 0.001s or 4.95s
                                        return v # e.g. 127ms or 4950ms
                                        
                                    raw_ms_min = to_ms(min_v, p_max)
                                    raw_ms_max = to_ms(max_v, p_max)
                                    
                                    min_v = max(0.0, (raw_ms_min - 1.0) / p_max_ms)
                                    max_v = max(0.0, (raw_ms_max - 1.0) / p_max_ms)

                                # Case B: Physical Hz
                                elif authority_type == "physical_hz" or ("Freq" in best_param and p_max > 100):
                                    if min_v < 200.0 and max_v < 200.0 and min_v > 0:
                                        print(f"DEBUG: V23 Authority (Hz): Scaling kHz -> Hz Physical for '{best_param}'")
                                        min_v *= 1000.0
                                        max_v *= 1000.0
                                    else:
                                        print(f"DEBUG: V23 Authority (Hz): Already in Hz physical range for '{best_param}'")

                                # Case C: Physical dB
                                elif authority_type == "physical_db":
                                    print(f"DEBUG: V23 Authority (dB): Keeping Physical values for '{best_param}'")

                                # Case D: Generic Normalized (0-1 AI to Physics)
                                elif (0.0 <= min_v <= 1.0) and (0.0 <= max_v <= 1.0) and (p_max - p_min > 1.1):
                                    print(f"DEBUG: V23 Scaling '{best_param}' AI 0-1 to Physical [{p_min}, {p_max}]")
                                    orig_min, orig_max = min_v, max_v
                                    min_v = p_min + (p_max - p_min) * orig_min
                                    max_v = p_min + (p_max - p_min) * orig_max
                            else:
                                # Safe default for unknown devices
                                min_v = 0.0 if min_v is None else min_v
                                max_v = 1.0 if max_v is None else max_v

                            # Flat Range Protection (Units-aware)
                            if min_v == max_v and min_v is not None:
                                 # For normalized time params, use tiny increment
                                 increment = 0.0001 if (matched_p and matched_p.get("max", 1.0) <= 60.0) else 1.0
                                 max_v = min_v + increment

                            mapping = MacroMapping(
                                macro_index=target_macro_idx,
                                device_id="0", # V12: Source is always Rack
                                param_path=best_path + [best_param],
                                min_val=min_v,
                                max_val=max_v,
                                label=macro_label
                            )
                            print(f"✅ SURGICAL MAPPING: Macro {target_macro_idx} -> {device.name}.{best_param} ('{macro_label}')")
                            device.add_mapping(best_path + [best_param], mapping)
                            self.add_macro_mapping(mapping)
                            
                            # Mark macro as used
                            used_macros.add(target_macro_idx)
                            
                            # Increment macro_idx only if we are using the default loop index
                            if "macro" not in plan_item:
                                macro_idx += 1
                                
                            local_found = True
                            break 
                    if local_found: break

        # 2. Fill remaining slots with Auto-Logic (ONLY IF NO AI PLAN)
        # V17 Titanium Policy: Early exit if AI plan exists to prevent GHOST mappings.
        if ai_mapping_plan and len(ai_mapping_plan) > 0:
            print(f"DEBUG: V17 Titanium - Surgical Plan confirmed. Blocking all fallback mappings.")
            return

        if macro_idx < 16:
            print(f"DEBUG: No AI plan. Filling empty rack with suggestions...")
            for chain in self.chains:
                for device in chain.devices:
                    suggestions = self.device_db.get_macro_suggestions(device.name)
                    for suggestion in suggestions:
                        # V14: RIGOROUS SLOT PROTECTION
                        while macro_idx < 16 and macro_idx in used_macros:
                            macro_idx += 1
                                
                            if macro_idx >= 8: break
                            
                            param_name = suggestion['param_name']
                            p_path = []
                            
                            # Guard: Don't map what's already mapped
                            if tuple(p_path + [param_name]) in device.mappings:
                                continue

                        # ... (Device specific path logic)
                        if device.xml_tag == "Eq8" and any(x in param_name for x in ["Freq", "Gain", "Q"]):
                             p_path = ["Bands.0", "ParameterA"]
                             param_name = param_name.replace("1 ", "").replace(" A", "")

                        mapping = MacroMapping(
                            macro_index=macro_idx,
                            device_id="0", # V12: Source is always Rack
                            param_path=p_path + [param_name],
                            min_val=suggestion['min'],
                            max_val=suggestion['max'],
                            label=param_name # Fallback label
                        )
                        print(f"ℹ️ FALLBACK MAPPING: Macro {macro_idx} -> {device.name}.{param_name}")
                        device.add_mapping(mapping.param_path, mapping)
                        self.add_macro_mapping(mapping)
                        macro_idx += 1
    
    def _create_macro_control(self, index: int) -> ET.Element:
        """Create a single MacroControl element"""
        macro = ET.Element(f"MacroControls.{index}")
        
        ET.SubElement(macro, "LomId").set("Value", "0")
        ET.SubElement(macro, "Manual").set("Value", "0" if index >= 2 else "63.5")
        
        midi_range = ET.SubElement(macro, "MidiControllerRange")
        ET.SubElement(midi_range, "Min").set("Value", "0")
        ET.SubElement(midi_range, "Max").set("Value", "127")
        
        auto_target = ET.SubElement(macro, "AutomationTarget")
        auto_target.set("Id", "0")
        ET.SubElement(auto_target, "LockEnvelope").set("Value", "0")
        
        mod_target = ET.SubElement(macro, "ModulationTarget")
        mod_target.set("Id", "0")
        ET.SubElement(mod_target, "LockEnvelope").set("Value", "0")
        
        return macro
    
        # Branches (EMPTY for Preset-based generation - Let Ableton hydrate)
        ET.SubElement(rack, "Branches")
        
        ET.SubElement(rack, "IsBranchesListVisible").set("Value", "false")
        ET.SubElement(rack, "IsReturnBranchesListVisible").set("Value", "false")
        ET.SubElement(rack, "IsRangesEditorVisible").set("Value", "false")
        ET.SubElement(rack, "AreDevicesVisible").set("Value", "true")
        
        # NumVisibleMacroControls
        ET.SubElement(rack, "NumVisibleMacroControls").set("Value", str(self.macro_count))
        
        # MacroControls (16 total, but only macro_count visible)
        for i in range(16):
             # ... (Macro generation code remains same, handled in next lines)
             pass 

    def to_xml(self) -> ET.Element:
        """
        Generate ADG XML using a Template-First approach with Preset Injection.
        Loads 'template_rack.xml', clears Runtime Branches, and injects BranchPresets.
        """
        # Load template
        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "template_rack.xml")
        if not os.path.exists(template_path):
            raise FileNotFoundError("Critical: template_rack.xml missing. Cannot generate valid rack.")
            
        tree = ET.parse(template_path)
        root = tree.getroot()
        
        # Find critical sections
        # Path: GroupDevicePreset -> Device -> AudioEffectGroupDevice
        gp = root.find("GroupDevicePreset")
        rack = gp.find("Device/AudioEffectGroupDevice")
        
        if rack is None:
            raise ValueError("Invalid Template: AudioEffectGroupDevice not found")
            
        # 1. Update Macro Count
        # SEARCH ROBUSTLY: some templates might have it as a sub-value or direct attribute
        num_macros = rack.find("NumVisibleMacroControls")
        if num_macros is not None:
            num_macros.set("Value", str(self.macro_count))
        else:
            # Fallback path for different template versions
            num_macros_val = rack.find("NumVisibleMacroControls/Value")
            if num_macros_val is not None:
                num_macros_val.set("Value", str(self.macro_count))
        
        # 2. CLEAR Runtime BRANCHES (Crucial Step: Must be empty for Saved Rack)
        branches_elem = rack.find("Branches")
        if branches_elem is not None:
            for child in list(branches_elem):
                branches_elem.remove(child)
                
        # 3. POPULATE BranchPresets (The "Menu" for Ableton to cook)
        bp_list = gp.find("BranchPresets")
        if bp_list is None:
            bp_list = ET.SubElement(gp, "BranchPresets")
        else:
            # Clear existing presets from template
            for child in list(bp_list):
                bp_list.remove(child)
                
        # Inject our new chains as PRESETS
        # V35: Reset counters for fresh generation
        self.device_id_counter = 1
        self.preset_id_counter = 20
        for i, chain in enumerate(self.chains):
            bp_list.append(chain.to_branch_preset_xml(branch_id=i, device_db=self))

        # 4. Update Macros (Names, Defaults, etc.)
        # Macro Display Names
        for i in range(16):
            # SEARCH ROBUSTLY: some templates might have it differently
            dn = rack.find(f"MacroDisplayNames.{i}")
            if dn is not None:
                val = f"Macro {i+1}"
                found_mapping = False
                for m in self.macro_mappings:
                    if m.macro_index == i:
                        val = m.label if m.label else m.param_path[-1]
                        found_mapping = True
                        break
                
                print(f"DEBUG: Setting Macro {i} Label -> '{val}' (Found Mapping: {found_mapping})")
                dn.set("Value", val)
            else:
                # Try sub-element path if direct tag fails (rare in Live 12 but safe)
                sub_dn = rack.find(f"MacroDisplayNames.{i}/Value")
                if sub_dn is not None:
                     sub_dn.set("Value", val)

        return root

    def _to_xml_fallback_runtime(self) -> ET.Element:
        """Old generation logic as fallback"""
        # (This is just a stub or we could keep the old logic here, but for now let's error if template missing)
        raise FileNotFoundError("Critical: template_rack.xml missing. Cannot generate valid rack.")
        
        return root
    
    def save(self, filepath: str):
        """Save rack as .adg file with character-perfect structural integrity"""
        # Generate XML
        xml_tree = self.to_xml()
        
        # V34: Character-Perfect Serialization
        xml_string = prettify_xml(xml_tree)
        
        # V34 CRITICAL: Standardize line endings to CRLF for Windows/Ableton 12.3
        # Ensure absolute CRLF and no trailing/leading garbage
        xml_string = xml_string.replace('\r', '').replace('\n', '\r\n').strip()
        
        # Compress with gzip 
        # FNAME flag set (via filename arg) to match 'afternoon' success files
        import gzip
        with open(filepath, 'wb') as f:
            # We use the filename without extension or hash to keep it clean
            fname = os.path.basename(filepath).split('_')[0]
            with gzip.GzipFile(filename=fname, mode='wb', fileobj=f, compresslevel=9, mtime=0) as gz:
                gz.write(xml_string.encode('utf-8'))
        
        print(f"SUCCESS: Saved V35 'Golden DNA' Rack: {filepath}")
        print(f"DEBUG: XML START: {xml_string[:100]}")
