from .vector_db_provider import VectorDBProvider
from helpers.config import vector_db_config
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, Distance, VectorParams
import logging
class QdrantProvider(VectorDBProvider):
    def __init__(self):
        self.client = QdrantClient(
            host=vector_db_config.QDRANT_HOST,
            port=vector_db_config.QDRANT_PORT,
            api_key=vector_db_config.QDRANT_API_KEY 
        )
        self.logger = logging.getLogger('uvicorn.error')
        self.vector_size = vector_db_config.QDRANT_VECTOR_SIZE
        self.distance = vector_db_config.QDRANT_DISTANCE
        

    def add_embeddings(self, collection: str, embeddings: list[dict], batch_size: int = 100):
        is_collection_exist = self.client.collection_exists(collection_name=collection)
        self.logger.info(f"Collection '{collection}' exists: {is_collection_exist}")
        # If the collection does not exist, create it
        if not is_collection_exist:
            self.logger.info(f"Creating collection '{collection}'")
            self.create_collection(collection=collection)
        for i in range(0, len(embeddings), batch_size):
            batch = embeddings[i:i + batch_size]   
            points = [
                PointStruct(
                    id=chunk["chunk_id"],
                    vector=chunk["embedding"],
                    payload=chunk  # store all chunk info as payload
                )
                for chunk in batch
            ]
            self.client.upsert(collection_name=collection, points=points)

    def query(self, collection: str, embedding: list[float], top_k: int = 5) -> list[dict]:
        hits = self.client.search(
            collection_name=collection,
            query_vector=embedding,
            limit=top_k
        )
        return [hit.payload for hit in hits]

    def create_collection(self, collection: str):
        self.client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=self.vector_size, distance= models.Distance.DOT if self.distance == "Dot" else Distance.COSINE),
        )

    def delete_collection(self, collection: str):
        self.client.delete_collection(collection_name=collection)