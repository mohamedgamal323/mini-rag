from enum import Enum

class VectorDBProviderEnum(str, Enum):
    QDRANT = "qdrant"
    FAISS = "faiss"
    PINECONE = "pinecone"
    # Add more as needed