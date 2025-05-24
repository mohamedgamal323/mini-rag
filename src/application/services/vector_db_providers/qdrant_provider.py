from .vector_db_provider import VectorDBProvider
from helpers.config import llm_config
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams

class QdrantProvider(VectorDBProvider):
    def __init__(self):
        self.client = QdrantClient(
            host=llm_config.QDRANT_HOST,
            api_key=llm_config.QDRANT_API_KEY 
        )

    async def add_embeddings(self, collection: str, embeddings: list[dict]):
        points = [
            PointStruct(
                id=chunk["chunk_id"],
                vector=chunk["embedding"],
                payload=chunk  # store all chunk info as payload
            )
            for chunk in embeddings
        ]
        self.client.upsert(collection_name=collection, points=points)

    async def query(self, collection: str, embedding: list[float], top_k: int = 5) -> list[dict]:
        hits = self.client.search(
            collection_name=collection,
            query_vector=embedding,
            limit=top_k
        )
        return [hit.payload for hit in hits]

    async def create_collection(self, collection: str, vector_size: int = 768, distance: str = "Cosine"):
        self.client.recreate_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance[distance])
        )

    async def delete_collection(self, collection: str):
        self.client.delete_collection(collection_name=collection)