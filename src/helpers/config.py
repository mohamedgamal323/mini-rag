from pydantic_settings import BaseSettings
from pydantic import Extra
import os

class Settings(BaseSettings):
    APP_NAME: str = "Mini-RAG App"
    APP_VERSION: str = "1.0.0"
    FILE_ALLOWED_TYPES: list[str] = ["text/plain", "application/pdf"]
    FILE_DEFAULT_CHUNK_SIZE: int = 1024 * 1024  # 1 MB
    FILE_MAX_SIZE: int = 10 * 1024 * 1024  # 10 MB
    MONGODB_URL: str
    MONGODB_DATABASE: str
    PROJECTS_ROOT: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets/files")

    class Config:
        env_file = ".env"
        extra = Extra.allow

def get_settings():
    return Settings()

class LLMConfig(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_GENERATION_MODEL: str = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"

    COHERE_API_KEY: str
    COHERE_GENERATION_MODEL: str = "command"
    COHERE_EMBEDDING_MODEL: str = "embed-english-v3.0"

    class Config:
        env_file = ".env"
        extra = Extra.allow

llm_config = LLMConfig()

class VectorDBConfig(BaseSettings):
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str = ""
    QDRANT_VECTOR_SIZE: int = 768
    QDRANT_DISTANCE: str = "Cosine"

    class Config:
        env_file = ".env"
        extra = Extra.allow

vector_db_config = VectorDBConfig()
