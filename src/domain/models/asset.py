from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from domain.enums.asset_type_enum import AssetType

class Asset(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Use str instead of ObjectId
    asset_id: str = Field(...)
    project_id: str = Field(...)
    type: AssetType = Field(...)
    source: str = Field(...)  # filename for files, URL for links, etc.
    content: Optional[bytes] = None  # For files, can be None for other types
    processed: bool = False
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None