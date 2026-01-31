import xml.etree.ElementTree as ET
import os
import gzip

def prettify_xml(elem):
    """Return an XML string with character-perfect Ableton 12.3 formatting"""
    # Header and root are hardcoded to match confirmed working files
    header = '<?xml version="1.0" encoding="UTF-8"?>'
    
    # Extract root tag and body manually
    # NOTE: In V35.2, we must ensure 'Ableton' root tag is formatted EXACTLY
    # because ET.tostring alphabetizes attributes which causes load failure.
    
    raw_xml = ET.tostring(elem, encoding='utf-8').decode('utf-8')
    
    # 1. Identify the first child of the root node (GroupDevicePreset)
    start_pos = raw_xml.find('<GroupDevicePreset')
    final_body = raw_xml[start_pos:]
    
    # 2. Reconstruct the root tag with character-perfect attribute order
    # Analyzing golden sample: <Ableton MajorVersion="5" MinorVersion="12.0_12300" SchemaChangeCount="1" Creator="Ableton Live 12.3" Revision="49ca8995cfdbe384bd4648a2e0d5a14dba7b993d">
    root_tag = '<Ableton MajorVersion="5" MinorVersion="12.0_12300" SchemaChangeCount="1" Creator="Ableton Live 12.3" Revision="49ca8995cfdbe384bd4648a2e0d5a14dba7b993d">'
    
    # 3. Concatenate without ANY newline after header
    # V35/36: NO NEWLINE between header and root
    xml_output = f'{header}{root_tag}{final_body}'
    
    # 4. Final character cleanup: space before self-closing tags
    xml_output = xml_output.replace('/>', ' />')
    
    return xml_output

def save_adg(xml_string: str, filepath: str):
    """Save rack as .adg file with character-perfect structural integrity"""
    # Standardize line endings to CRLF for Windows/Ableton 12.3
    xml_string = xml_string.replace('\r', '').replace('\n', '\r\n').strip()
    
    # Compress with gzip 
    # FNAME flag set (via filename arg) to match 'afternoon' success files
    with open(filepath, 'wb') as f:
        # We use the filename without extension or hash to keep it clean
        fname = os.path.basename(filepath).split('_')[0]
        with gzip.GzipFile(filename=fname, mode='wb', fileobj=f, compresslevel=9, mtime=0) as gz:
            gz.write(xml_string.encode('utf-8'))
    
    print(f"SUCCESS: Saved V35 'Golden DNA' Rack (Modular): {filepath}")
