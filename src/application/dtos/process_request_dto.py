from pydantic import BaseModel

class ProcessRequestDTO(BaseModel):
    file_id: str
    chunk_size: int
    overlap_size: int
    do_reset: bool