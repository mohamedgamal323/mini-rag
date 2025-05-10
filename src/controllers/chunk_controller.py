from src.controllers.base_controller import BaseController
from fastapi import Depends
from src.application.services.chunk_service import ChunkService
from src.application.dtos.chunk_dto import CreateChunkDTO, ChunkResponseDTO
from src.infrastructure.repositories.mongo_chunk_repository import MongoChunkRepository

class ChunkController(BaseController):
    def __init__(self):
        super().__init__(prefix="/chunks", tags=["chunks"])

        # Dependency injection for the service
        def get_chunk_service() -> ChunkService:
            repository = MongoChunkRepository(db_client=self.db_client)
            return ChunkService(repository)

        @self.router.post("/", response_model=ChunkResponseDTO)
        def create_chunk(dto: CreateChunkDTO, service: ChunkService = Depends(get_chunk_service)):
            return service.create_chunk(dto)

        @self.router.get("/{chunk_id}", response_model=ChunkResponseDTO)
        def get_chunk(chunk_id: str, service: ChunkService = Depends(get_chunk_service)):
            return service.get_chunk(chunk_id)

# Instantiate the controller and expose its router
chunk_controller = ChunkController()
router = chunk_controller.router