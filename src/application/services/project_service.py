import os
from helpers.config import get_settings
from domain.models.project import Project
from application.dtos.project_dto import CreateProjectDTO, ProjectResponseDTO
from infrastructure.repositories.mongo_project_repository import MongoProjectRepository

class ProjectService:
    def __init__(self, repository: MongoProjectRepository):
        self.repository = repository
        self.settings = get_settings()

    async def create_project(self, dto: CreateProjectDTO) -> ProjectResponseDTO:
        # Validate and create a project
        project = Project(project_id=dto.project_id)
        saved_project = await self.repository.create_project(project)
        return ProjectResponseDTO(id=saved_project.id, project_id=saved_project.project_id)

    async def get_project(self, project_id: str) -> ProjectResponseDTO:
        # Retrieve project from the repository
        project = await self.repository.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")
        return ProjectResponseDTO(id=project.id, project_id=project.project_id)

    async def get_project_path(self, project_id: str) -> str:
        # Ensure the project exists
        await self.get_project(project_id)

        # Construct the project path
        project_path = os.path.join(self.settings.PROJECTS_ROOT, project_id)
        os.makedirs(project_path, exist_ok=True)
        return project_path