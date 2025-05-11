from controllers.base_controller import BaseController
from fastapi import Depends
from application.services.project_service import ProjectService
from application.dtos.project_dto import CreateProjectDTO, ProjectResponseDTO
from infrastructure.repositories.mongo_project_repository import MongoProjectRepository

class ProjectController(BaseController):
    def __init__(self, db_client):
        super().__init__(prefix="/projects", tags=["projects"])
        self.db_client = db_client

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
def create_project_controller(db_client):
    project_controller = ProjectController(db_client)
    return project_controller.router