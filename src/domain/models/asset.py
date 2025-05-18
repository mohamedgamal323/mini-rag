from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from domain.enums.asset_type_enum import AssetType
from pymongo import ASCENDING, DESCENDING

class Asset(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Use str instead of ObjectId
    asset_id: str = Field(...)
    asset_name: str = Field(...)
    project_id: str = Field(...)
    type: AssetType = Field(...)
    source: str = Field(...)  # filename for files, URL for links, etc.
    content: Optional[bytes] = None  # For files, can be None for other types
    processed: bool = False
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        allow_population_by_field_name = True  # Allow alias usage

    @staticmethod
    def get_indexes():
        return [
            {"keys": [("project_id", ASCENDING), ("asset_id", ASCENDING)]},  # Composite index for project_id and asset_id
            {"keys": [("uploaded_at", DESCENDING)]},  # Index for sorting by upload date
            {"keys": [("type", ASCENDING)]},  # Index for filtering by asset type
        ]