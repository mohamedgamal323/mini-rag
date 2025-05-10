from pydantic import BaseModel

class CreateChunkDTO(BaseModel):
    chunk_id: str
    content: str

class ChunkResponseDTO(BaseModel):
    id: str
    chunk_id: str
    content: str