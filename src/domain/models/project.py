from pydantic import BaseModel, Field
from typing import Optional

class Project(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Use str instead of ObjectId
    project_id: str = Field(..., min_length=1)

    class Config:
        allow_population_by_field_name = True  # Allow alias usage