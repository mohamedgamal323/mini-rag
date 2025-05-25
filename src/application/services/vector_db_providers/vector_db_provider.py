from abc import ABC, abstractmethod

class VectorDBProvider(ABC):
    @abstractmethod
    def add_embeddings(self, collection: str, embeddings: list[dict], batch_size: int = 100):
        pass

    @abstractmethod
    def query(self, collection: str, embedding: list[float], top_k: int = 5) -> list[dict]:
        pass

    @abstractmethod
    def create_collection(self, collection: str, **kwargs):
        pass

    @abstractmethod
    def delete_collection(self, collection: str):
        pass