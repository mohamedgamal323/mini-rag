from pydantic import BaseModel, Field
from typing import Optional

class Chunk(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Use str instead of ObjectId
    chunk_id: str
    content: str

    class Config:
        allow_population_by_field_name = True  # Allow alias usage