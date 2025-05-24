from abc import ABC, abstractmethod

class VectorDBProvider(ABC):
    @abstractmethod
    async def add_embeddings(self, collection: str, embeddings: list[dict]):
        pass

    @abstractmethod
    async def query(self, collection: str, embedding: list[float], top_k: int = 5) -> list[dict]:
        pass

    @abstractmethod
    async def create_collection(self, collection: str, **kwargs):
        pass

    @abstractmethod
    async def delete_collection(self, collection: str):
        pass