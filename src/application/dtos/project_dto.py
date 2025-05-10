from pydantic import BaseModel

class CreateProjectDTO(BaseModel):
    project_id: str

class ProjectResponseDTO(BaseModel):
    id: str
    project_id: str