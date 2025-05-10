from src.controllers.base_controller import BaseController
from fastapi import Depends
from src.application.services.project_service import ProjectService
from src.application.dtos.project_dto import CreateProjectDTO, ProjectResponseDTO
from src.infrastructure.repositories.mongo_project_repository import MongoProjectRepository

class ProjectController(BaseController):
    def __init__(self):
        super().__init__(prefix="/projects", tags=["projects"])

        # Dependency injection for the service
        def get_project_service() -> ProjectService:
            repository = MongoProjectRepository(db_client=self.db_client)
            return ProjectService(repository)

        @self.router.post("/", response_model=ProjectResponseDTO)
        def create_project(dto: CreateProjectDTO, service: ProjectService = Depends(get_project_service)):
            return service.create_project(dto)

        @self.router.get("/{project_id}", response_model=ProjectResponseDTO)
        def get_project(project_id: str, service: ProjectService = Depends(get_project_service)):
            return service.get_project(project_id)

# Instantiate the controller and expose its router
project_controller = ProjectController()
router = project_controller.router