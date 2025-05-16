from helpers.config import get_settings
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

def get_db_client() -> AsyncIOMotorClient:
    """
    Dependency to get the database client.
    This function is used in FastAPI routes to provide the database client.
    """
    settings = get_settings()
    mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    db_client = mongo_conn[settings.MONGODB_DATABASE]
    try:
        yield db_client
    finally:
        mongo_conn.close()