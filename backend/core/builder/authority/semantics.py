from .specialized import SPECIALIZED_MAP
from .standard import STANDARD_MAP

# Unified aggregator (V37)
# Merges all atomic maps into a single source of truth
SEMANTIC_MAP = {**STANDARD_MAP, **SPECIALIZED_MAP}
