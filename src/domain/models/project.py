from pydantic import BaseModel, Field
from typing import Optional
from pymongo import ASCENDING

class Project(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Use str instead of ObjectId
    project_id: str = Field(..., min_length=1)

    class Config:
        allow_population_by_field_name = True  # Allow alias usage

    @staticmethod
    def get_indexes():
        return [
            {"keys": [("project_id", ASCENDING)], "options": {"unique": True}},
            {"keys": [("created_at", ASCENDING)]}
        ]