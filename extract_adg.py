
import gzip
import sys
import os

try:
    filename = sys.argv[1]
    output = "debug_broken.xml"
    with gzip.open(filename, 'rb') as f:
        content = f.read()
    with open(output, 'wb') as f_out:
        f_out.write(content)
    print(f"SUCCESS: Extracted to {output}")
except Exception as e:
    print(f"ERROR: {e}")
