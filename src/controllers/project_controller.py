from controllers.base_controller import BaseController
from fastapi import Depends
from application.services.project_service import ProjectService
from application.dtos.project_dto import CreateProjectDTO, ProjectResponseDTO
from infrastructure.repositories.mongo_project_repository import MongoProjectRepository

class ProjectController(BaseController):
    def __init__(self):
        super().__init__(prefix="/projects", tags=["projects"])

        @self.router.post("/", response_model=ProjectResponseDTO)
        async def create_project(dto: CreateProjectDTO, service: ProjectService = Depends()):
            return await service.create_project(dto)

        @self.router.get("/{project_id}", response_model=ProjectResponseDTO)
        async def get_project(project_id: str, service: ProjectService = Depends()):
            return await service.get_project(project_id)
