from domain.enums.vector_db_provider_enum import VectorDBProviderEnum
from .qdrant_provider import QdrantProvider
# from .faiss_provider import FaissProvider

class VectorDBFactory:
    @staticmethod
    def create(provider: VectorDBProviderEnum):
        if provider == VectorDBProviderEnum.QDRANT:
            return QdrantProvider()
        # elif provider == VectorDBProviderEnum.FAISS:
        #     return FaissProvider()
        else:
            raise ValueError(f"Unsupported Vector DB provider: {provider}")