from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    APP_NAME: str = "Mini-RAG App"
    APP_VERSION: str = "1.0.0"
    MONGODB_URL: str
    MONGODB_DATABASE: str
    PROJECTS_ROOT: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets/files")

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
