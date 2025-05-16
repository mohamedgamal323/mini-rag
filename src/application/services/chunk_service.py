from fastapi import Depends
from application.dtos.chunk_dto import CreateChunkDTO, ChunkResponseDTO
from domain.models.chunk import Chunk
from infrastructure.repositories.mongo_chunk_repository import MongoChunkRepository

class ChunkService:
    def __init__(self, repository: MongoChunkRepository = Depends()):
        self.repository = repository

    def create_chunk(self, dto: CreateChunkDTO) -> ChunkResponseDTO:
        # Create a Chunk instance
        chunk = Chunk(chunk_id=dto.chunk_id, content=dto.content)

        # Save to the database
        mongo_data = self.repository.to_mongo(chunk)
        # Simulate saving to the database (replace with actual DB call)
        saved_data = mongo_data  # Replace with actual DB save logic

        # Convert to response DTO
        return ChunkResponseDTO(
            id=str(saved_data["_id"]),
            chunk_id=saved_data["chunk_id"],
            content=saved_data["content"],
        )

    def get_chunk(self, chunk_id: str) -> ChunkResponseDTO:
        # Simulate fetching from the database (replace with actual DB call)
        mongo_data = {
            "_id": "60f7c0f5b4d6c8b2f8e4d456",
            "chunk_id": chunk_id,
            "content": "Example content",
        }  # Replace with actual DB fetch logic

        # Convert MongoDB data to a Chunk instance
        chunk = self.repository.from_mongo(mongo_data)

        # Convert to response DTO
        return ChunkResponseDTO(
            id=chunk.id,
            chunk_id=chunk.chunk_id,
            content=chunk.content,
        )

    async def insert_chunks(self, chunks: list[Chunk]):
        # Insert chunks into the database
        return await self.repository.insert_many_chunks(chunks)

    async def delete_chunks_by_project_id(self, project_id: str):
        # Delete chunks for a specific project
        return await self.repository.delete_chunks_by_project_id(project_id)
    
    async def delete_chunks_by_file_id(self, file_id: str):
        # Delete chunks for a specific file
        return await self.repository.delete_chunks_by_file_id(file_id)