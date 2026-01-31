from dataclasses import dataclass
from typing import List

@dataclass
class MacroMapping:
    """Represents a macro control mapping"""
    macro_index: int
    device_id: str
    param_path: List[str]
    min_val: float
    max_val: float
    label: str = ""
