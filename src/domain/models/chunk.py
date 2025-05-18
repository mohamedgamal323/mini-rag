from pydantic import BaseModel, Field
from typing import Optional
from pymongo import ASCENDING
from datetime import datetime

class Chunk(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Use str instead of ObjectId
    metadata: Optional[dict] = Field(None, alias="chunk_metadata")
    content: str
    file_id: str
    asset_id: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), alias="created_at")
    project_id: str
    order: int

    class Config:
        allow_population_by_field_name = True  # Allow alias usage

    @staticmethod
    def get_indexes():
        return [
            {"keys": [("project_id", ASCENDING), ("file_id", ASCENDING)]},
            {"keys": [("chunk_order", ASCENDING)]},
            {"keys": [("created_at", ASCENDING)], "options": {"expireAfterSeconds": 3600}}
        ]