from pydantic_settings import BaseSettings
from pydantic import BaseSettings as PydanticBaseSettings
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

def get_settings():
    return Settings()

class LLMConfig(PydanticBaseSettings):
    openai_api_key: str
    openai_generation_model: str = "gpt-3.5-turbo"
    openai_embedding_model: str = "text-embedding-ada-002"

    cohere_api_key: str
    cohere_generation_model: str = "command"
    cohere_embedding_model: str = "embed-english-v3.0"

    class Config:
        env_file = ".env"

llm_config = LLMConfig()
