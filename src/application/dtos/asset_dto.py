from pydantic import BaseModel
from typing import Optional, Dict, Any
from domain.enums.asset_type_enum import AssetType

class CreateAssetDTO(BaseModel):
    project_id: str
    type: AssetType
    source: str
    content: Optional[bytes] = None
    metadata: Optional[Dict[str, Any]] = None

class AssetResponseDTO(BaseModel):
    id: str
    asset_id: str
    project_id: str
    type: AssetType
    source: str
    processed: bool
    metadata: Optional[Dict[str, Any]] = None