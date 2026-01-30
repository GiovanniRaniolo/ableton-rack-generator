"""
ADG Builder - CORRECTED VERSION based on real Ableton Live 12.3 .adg structure
Analyzed from reference_rack.xml
"""

import gzip
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict, Optional
from dataclasses import dataclass


def prettify_xml(elem):
    """Return a pretty-printed XML string matching Ableton's exact lexical style"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    # Ableton uses tabs
    xml_str = reparsed.toprettyxml(indent="\t")
    
    # Ableton's lexical style:
    # 1. Space before self-closing tag: <Tag />
    # 2. UTF-8 header
    # 3. Newlines between every tag (toprettyxml does mostly this)
    
    if xml_str.startswith('<?xml version="1.0" ?>'):
        xml_str = xml_str.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>', 1)
    
    # Add space before self-closing tags: "/>" -> " />"
    # But only if not already there
    import re
    xml_str = re.sub(r'([^ ])/>', r'\1 />', xml_str)
    
    return xml_str


@dataclass
class MacroMapping:
    """Represents a macro control mapping"""
    macro_index: int
    device_id: str  # ID from DevicePresets
    param_path: List[str]  # e.g. ["Bands.0", "ParameterA", "Gain"]
    min_val: float
    max_val: float


class AbletonDevice:
    """Represents a single Ableton device with full parameter support"""
    
    def __init__(self, name: str, device_db, device_id: str = "0"):
        self.name = name
        self.device_id = device_id
        
        # Get device config from database
        self.device_info = device_db.get_device(name)
        if not self.device_info:
            raise ValueError(f"Device '{name}' not found in database")
        
        self.xml_tag = self.device_info['xml_tag']
        self.class_name = self.device_info['class_name']
        self.type = self.device_info['type']
        self.mappings: Dict[tuple, MacroMapping] = {} # Keyed by param path tuple
    
    def add_mapping(self, param_path: List[str], mapping: MacroMapping):
        self.mappings[tuple(param_path)] = mapping

    def _create_parameter(self, name: str, value: float, min_val: float = 0.0, max_val: float = 127.0, param_path: List[str] = []) -> ET.Element:
        """Create a full Ableton parameter element with optional macro mapping"""
        elem = ET.Element(name)
        ET.SubElement(elem, "LomId").set("Value", "0")
        
        # Check for mapping
        full_path = tuple(param_path + [name])
        mapping = self.mappings.get(full_path)
        
        if mapping:
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
        
        is_bool = name in ["On", "IsOn", "EditMode", "Speaker", "IsSoloed", "SoftClip", "SaturatorSoftClip"]
        
        if is_bool:
            val_str = "true" if value > 0.5 else "false"
        else:
            # Ableton prefers "0" over "0.0" for integer values
            if value == int(value):
                val_str = str(int(value))
            else:
                val_str = str(value)
            
        ET.SubElement(elem, "Manual").set("Value", val_str)
        
        # Automation target always present
        auto_target = ET.SubElement(elem, "AutomationTarget")
        auto_target.set("Id", "0")
        ET.SubElement(auto_target, "LockEnvelope").set("Value", "0")
        
        if is_bool:
            # Booleans use MidiCCOnOffThresholds, NO ModulationTarget, NO MidiControllerRange
            midi_thresh = ET.SubElement(elem, "MidiCCOnOffThresholds")
            ET.SubElement(midi_thresh, "Min").set("Value", "64")
            ET.SubElement(midi_thresh, "Max").set("Value", "127")
        else:
            # Reals/Ints use MidiControllerRange and ModulationTarget
            midi_range = ET.SubElement(elem, "MidiControllerRange")
            ET.SubElement(midi_range, "Min").set("Value", str(min_val))
            ET.SubElement(midi_range, "Max").set("Value", str(max_val))
            
            mod_target = ET.SubElement(elem, "ModulationTarget")
            mod_target.set("Id", "0")
            ET.SubElement(mod_target, "LockEnvelope").set("Value", "0")
        
        return elem

    def to_preset_xml(self) -> ET.Element:
        """Generate full AbletonDevicePreset XML"""
        preset = ET.Element("AbletonDevicePreset")
        preset.set("Id", self.device_id)
        
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

    def to_preset_xml(self) -> ET.Element:
        """Generate full AbletonDevicePreset XML"""
        preset = ET.Element("AbletonDevicePreset")
        preset.set("Id", "0")
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
        
        # Metadata for AudioEffectBranch
        helper_device._add_metadata_fields(branch, "AudioEffectBranch", is_mixer=True)
            
        # Device Chain (CRITICAL Missing Component)
        device_chain = ET.SubElement(branch, "DeviceChain")
        
        # Mixer
        mixer_device = ET.SubElement(device_chain, "Mixer")
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
        
        # Main Device List
        devices_list = ET.SubElement(device_chain, "Devices")
        if self.devices:
            for dev in self.devices:
                devices_list.append(dev.to_node_xml())

        # Signal Modulators (Empty)
        ET.SubElement(device_chain, "SignalModulations")

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
        
        source_ctx = ET.SubElement(branch, "SourceContext")
        branch_ctx = ET.SubElement(source_ctx, "BranchSourceContext")
        branch_ctx.set("Id", "0")
        ET.SubElement(branch_ctx, "OriginalFileRef")
        ET.SubElement(branch_ctx, "BrowserContentPath").set("Value", "")
        ET.SubElement(branch_ctx, "LocalFiltersJson").set("Value", "")
        ET.SubElement(branch_ctx, "PresetRef")
        ET.SubElement(branch_ctx, "BranchDeviceId").set("Value", "")

        return branch

    def to_branch_preset_xml(self, branch_id: int = 0, device_db=None) -> ET.Element:
        """Generate AudioEffectBranchPreset XML"""
        branch = ET.Element("AudioEffectBranchPreset")
        branch.set("Id", str(branch_id))
        
        ET.SubElement(branch, "Name").set("Value", self.name)
        ET.SubElement(branch, "IsSoloed").set("Value", "false")
        
        # DevicePresets
        device_presets = ET.SubElement(branch, "DevicePresets")
        for idx, device in enumerate(self.devices):
            preset = device.to_preset_xml()
            preset.set("Id", str(idx))
            device_presets.append(preset)
            
        # MixerPreset (REQUIRED for parallel chains)
        mixer_preset = ET.SubElement(branch, "MixerPreset")
        
        mixer_preset_wrapper = ET.SubElement(mixer_preset, "AbletonDevicePreset")
        mixer_preset_wrapper.set("Id", "0")
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
        ET.SubElement(mixer_device, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(mixer_device, "Pointee").set("Id", "0")
        ET.SubElement(mixer_device, "LastSelectedTimeableIndex").set("Value", "0")
        ET.SubElement(mixer_device, "LastSelectedClipEnvelopeIndex").set("Value", "0")
        
        # Mixer Metadata
        helper_device._add_metadata_fields(mixer_device, "AudioBranchMixerDevice", is_mixer=True)
        
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
    
    def add_chain(self, chain: Chain):
        """Add a chain to the rack"""
        self.chains.append(chain)
    
    def add_macro_mapping(self, mapping: MacroMapping):
        """Add a macro control mapping"""
        self.macro_mappings.append(mapping)
    
    def auto_map_macros(self, ai_mapping_plan: list = None):
        """
        Automatically map macros to parameters.
        Prioritizes AI Mapping Plan if provided, otherwise falls back to database suggestions.
        """
        macro_idx = 0
        mapped_devices = set()

        # 1. Try to follow AI Plan
        if ai_mapping_plan:
            print(f"DEBUG: Processing {len(ai_mapping_plan)} AI macro plans...")
            for plan_item in ai_mapping_plan:
                if macro_idx >= 16: break
                
                target_dev_name = plan_item.get("target_device", "").lower()
                target_param = plan_item.get("target_parameter", "").lower()
                
                # Find matching device in any chain
                found_match = False
                for chain in self.chains:
                    for device in chain.devices:
                        # Fuzzy match device name (e.g. "Reverb" in "Reverb2")
                        if target_dev_name in device.name.lower() or device.name.lower() in target_dev_name:
                            # Try to find parameter
                            # Note: This is tricky without a full parameter map. 
                            # We will try to map to 'known' params first via fuzzy search on suggestions
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
                            
                            # If not in suggestions, try generic mapping if it's a common param
                            if not best_param:
                                # Fallback: simple heuristic for standard params
                                if "dec" in target_param: best_param = "DecayTime"
                                elif "dry" in target_param or "wet" in target_param: best_param = "DryWet"
                                elif "freq" in target_param: best_param = "Frequency"
                                elif "gain" in target_param: best_param = "Gain"
                                elif "amount" in target_param: best_param = "Amount"
                                
                            if best_param:
                                # Special handling for complex devices like EQ8
                                if device.xml_tag == "Eq8":
                                     if any(x in best_param for x in ["Freq", "Gain", "Q"]):
                                         best_path = ["Bands.0", "ParameterA"]
                                         if "Freq" in best_param: best_param = "Freq"
                                         if "Gain" in best_param: best_param = "Gain"
                                         if "Q" in best_param: best_param = "Q"
                            
                                mapping = MacroMapping(
                                    macro_index=macro_idx,
                                    device_id=device.device_id,
                                    param_path=best_path + [best_param],
                                    min_val=min_v,
                                    max_val=max_v
                                )
                                device.add_mapping(mapping.param_path, mapping)
                                self.add_macro_mapping(mapping)
                                macro_idx += 1
                                found_match = True
                                break # Done with this plan item
                    if found_match: break

        # 2. Fill remaining slots with Auto-Logic (Fallback)
        if macro_idx < 8:
            for chain_idx, chain in enumerate(self.chains):
                for device_idx, device in enumerate(chain.devices):
                    suggestions = self.device_db.get_macro_suggestions(device.name)
                    
                    for suggestion in suggestions:
                        if macro_idx >= 8: break # Only auto-fill up to 8
                        
                        # Verify we haven't already mapped this exact param (naive check)
                        # Ideally we check self.macro_mappings but let's just populate
                        
                        param_name = suggestion['param_name']
                        p_path = []
                        
                        # Handle nested paths for specific devices
                        if device.xml_tag == "Eq8":
                            # EQ Eight uses Bands.0, Bands.1, etc.
                            if any(x in param_name for x in ["Freq", "Gain", "Q"]):
                                 p_path = ["Bands.0", "ParameterA"]
                                 # If the param_name was "1 Frequency A", use "Freq"
                                 if "Freq" in param_name: param_name = "Freq"
                                 if "Gain" in param_name: param_name = "Gain"
                                 if "Q" in param_name: param_name = "Q"
                                 
                        elif device.xml_tag == "MultibandDynamics":
                            # Handle specific band mappings if suggested
                            if "Mid" in param_name:
                                 p_path = ["SideChainAndSplitter", "SplitMidHigh"] # Simplified
                            elif "Low" in param_name:
                                 pass # Top level often works for OutputGain
                            
                            # Fix for OutputGain which is often mapped
                            if param_name == "OutputGain":
                                 p_path = []
                        
                        mapping = MacroMapping(
                            macro_index=macro_idx,
                            device_id=device.device_id,
                            param_path=p_path + [param_name],
                            min_val=suggestion['min'],
                            max_val=suggestion['max']
                        )
                        
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
        num_macros = rack.find("NumVisibleMacroControls/Value")
        if num_macros: num_macros.set("Value", str(self.macro_count))
        
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
        for i, chain in enumerate(self.chains):
            bp_list.append(chain.to_branch_preset_xml(branch_id=i, device_db=self.device_db))

        # 4. Update Macros (Names, Defaults, etc.)
        # Macro Display Names
        for i in range(16):
            dn = rack.find(f"MacroDisplayNames.{i}")
            if dn:
                val = f"Macro {i+1}"
                for m in self.macro_mappings:
                    if m.macro_index == i:
                        val = m.param_path[-1] 
                        break
                dn.set("Value", val)

        return root

    def _to_xml_fallback_runtime(self) -> ET.Element:
        """Old generation logic as fallback"""
        # (This is just a stub or we could keep the old logic here, but for now let's error if template missing)
        raise FileNotFoundError("Critical: template_rack.xml missing. Cannot generate valid rack.")
        
        return root
    
    def save(self, filepath: str):
        """Save rack as .adg file"""
        # Generate XML
        xml_tree = self.to_xml()
        
        # Pretty print with tabs
        xml_string = prettify_xml(xml_tree)
        
        # Standardize line endings to standard CRLF (\r\n)
        xml_string = xml_string.replace('\r\r\n', '\n').replace('\r\n', '\n').replace('\n', '\r\n')
        
        # If the user's system produces \r\r\n upon saving or something, we should be aware.
        # But for now, let's use the most standard Windows line endings.
        
        # Compress with gzip (mtime=0 for deterministic output)
        import gzip
        with gzip.GzipFile(filepath, 'wb', compresslevel=9, mtime=0) as f:
            f.write(xml_string.encode('utf-8'))
        
        print(f"SUCCESS: Saved: {filepath}")
