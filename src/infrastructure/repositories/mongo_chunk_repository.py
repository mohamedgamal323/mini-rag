from bson.objectid import ObjectId
from pymongo import InsertOne
from src.domain.models.chunk import Chunk
from src.domain.enums.database_enum import DataBaseEnum

class MongoChunkRepository:
    def __init__(self, db_client):
        self.collection = db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk: Chunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk.id = str(result.inserted_id)
        return chunk

    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if result is None:
            return None
        return Chunk(**result)

    async def insert_many_chunks(self, chunks: list[Chunk], batch_size: int = 100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]
            await self.collection.bulk_write(operations)
        return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count

    @staticmethod
    def to_mongo(chunk: Chunk) -> dict:
        return {
            "_id": ObjectId(chunk.id) if chunk.id else None,
            "chunk_id": chunk.chunk_id,
            "content": chunk.content,
        }

    @staticmethod
    def from_mongo(data: dict) -> Chunk:
        return Chunk(
            id=str(data["_id"]) if "_id" in data else None,
            chunk_id=data["chunk_id"],
            content=data["content"],
        )