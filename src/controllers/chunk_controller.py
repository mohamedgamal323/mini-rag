from controllers.base_controller import BaseController
from fastapi import Depends
from application.services.chunk_service import ChunkService
from application.dtos.chunk_dto import CreateChunkDTO, ChunkResponseDTO
from infrastructure.repositories.mongo_chunk_repository import MongoChunkRepository

class ChunkController(BaseController):
    def __init__(self):
        super().__init__(prefix="/chunks", tags=["chunks"])

        @self.router.post("/", response_model=ChunkResponseDTO)
        def create_chunk(dto: CreateChunkDTO, service: ChunkService = Depends()):
            return service.create_chunk(dto)

        @self.router.get("/{chunk_id}", response_model=ChunkResponseDTO)
        def get_chunk(chunk_id: str, service: ChunkService = Depends()):
            return service.get_chunk(chunk_id)
