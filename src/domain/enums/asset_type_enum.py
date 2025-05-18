from enum import Enum

class AssetType(str, Enum):
    FILE = "file"
    # Future: URL = "url"
    # Future: API = "api"