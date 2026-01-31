import xml.etree.ElementTree as ET
from typing import List, Optional
from .device import AbletonDevice

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
        
        ET.SubElement(branch, "LomId").set("Value", "0")
        ET.SubElement(branch, "LomIdView").set("Value", "0")
        ET.SubElement(branch, "IsExpanded").set("Value", "true")
        ET.SubElement(branch, "BreakoutIsExpanded").set("Value", "false")
        ET.SubElement(branch, "OverwriteProtectionNumber").set("Value", "3075")
        ET.SubElement(branch, "UserName").set("Value", self.name)
        
        helper_device = self.devices[0] if self.devices else None
        if not helper_device:
            if not device_db: raise ValueError("device_db required for empty chain generation")
            helper_device = AbletonDevice("Utility", device_db)

        branch.append(helper_device._create_parameter("On", 1.0, 0.0, 1.0))
        
        ET.SubElement(branch, "ModulationSourceCount").set("Value", "0")
        ET.SubElement(branch, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(branch, "Pointee").set("Id", "0")
        ET.SubElement(branch, "LastSelectedTimeableIndex").set("Value", "0")
        ET.SubElement(branch, "LastSelectedClipEnvelopeIndex").set("Value", "0")
        
        source_ctx = ET.SubElement(branch, "SourceContext")
        branch_ctx = ET.SubElement(source_ctx, "BranchSourceContext")
        branch_ctx.set("Id", "0")
        ET.SubElement(branch_ctx, "OriginalFileRef")
        ET.SubElement(branch_ctx, "BrowserContentPath").set("Value", "")
        ET.SubElement(branch_ctx, "LocalFiltersJson").set("Value", "")
        ET.SubElement(branch_ctx, "PresetRef")
        ET.SubElement(branch_ctx, "BranchDeviceId").set("Value", "")
            
        device_chain = ET.SubElement(branch, "DeviceChain")
        devices_list = ET.SubElement(device_chain, "Devices")
        if self.devices:
            for dev in self.devices:
                if hasattr(device_db, "get_next_device_id"):
                    dev.device_id = device_db.get_next_device_id()
                devices_list.append(dev.to_node_xml())

        ET.SubElement(device_chain, "SignalModulations")

        mixer_device = ET.SubElement(branch, "Mixer")
        mixer_xml = ET.SubElement(mixer_device, "AudioBranchMixerDevice")
        mixer_xml.set("Id", "0")
        
        ET.SubElement(mixer_xml, "LomId").set("Value", "0")
        ET.SubElement(mixer_xml, "LomIdView").set("Value", "0")
        ET.SubElement(mixer_xml, "IsExpanded").set("Value", "true")
        
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
        branch = ET.Element("AudioEffectBranchPreset")
        branch.set("Id", str(branch_id))
        ET.SubElement(branch, "Name").set("Value", self.name)
        ET.SubElement(branch, "IsSoloed").set("Value", "false")
        
        device_presets = ET.SubElement(branch, "DevicePresets")
        for i, device in enumerate(self.devices):
            device.device_id = str(i)
            global_preset_id = "0"
            if hasattr(device_db, "get_next_preset_id"):
                global_preset_id = device_db.get_next_preset_id()
            device_presets.append(device.to_preset_xml(preset_id=global_preset_id))
            
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
        
        ET.SubElement(mixer_device, "LomId").set("Value", "0")
        ET.SubElement(mixer_device, "LomIdView").set("Value", "0")
        ET.SubElement(mixer_device, "IsExpanded").set("Value", "true")
        
        helper_device = self.devices[0] if self.devices else None
        if not helper_device:
            if not device_db: raise ValueError("device_db required for empty chain generation")
            helper_device = AbletonDevice("Utility", device_db)

        mixer_device.append(helper_device._create_parameter("On", 1.0, 0.0, 1.0))
        ET.SubElement(mixer_device, "ModulationSourceCount").set("Value", "0")
        ET.SubElement(mixer_device, "ParametersListWrapper").set("LomId", "0")
        ET.SubElement(mixer_device, "Pointee").set("Id", "0")
        
        last_ref_val = ET.SubElement(mixer_device, "LastPresetRef")
        last_ref = ET.SubElement(last_ref_val, "Value")
        def_ref = ET.SubElement(last_ref, "AbletonDefaultPresetRef")
        def_ref.set("Id", "0")
        ET.SubElement(def_ref, "DeviceId").set("Name", "AudioBranchMixerDevice")
        
        mixer_device.append(helper_device._create_parameter("Speaker", 1.0, 0.0, 1.0))
        mixer_device.append(helper_device._create_parameter("Volume", 1.0, 0.0, 1.0))
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
