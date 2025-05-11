from pydantic import BaseModel, Field
from typing import Optional

class Chunk(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Use str instead of ObjectId
    metadata: Optional[dict] = Field(None, alias="chunk_metadata")
    content: str
    file_id: str
    project_id: str
    order: int

    class Config:
        allow_population_by_field_name = True  # Allow alias usage