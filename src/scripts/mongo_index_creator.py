import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Adjust the import path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from domain.models.project import Project
from domain.models.asset import Asset
from domain.models.chunk import Chunk
from domain.enums.database_enum import DataBaseEnum
from helpers.config import get_settings

def create_indexes_for_collection(collection, indexes):
    for index in indexes:
        keys = index["keys"]
        options = index.get("options", {})
        collection.create_index(keys, **options)

def main():
    settings = get_settings()
    mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    db_client = mongo_conn[settings.MONGODB_DATABASE]

    # Project indexes
    print("Creating indexes for 'project' collection...")
    create_indexes_for_collection(db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value], Project.get_indexes())

    # Asset indexes
    print("Creating indexes for 'asset' collection...")
    create_indexes_for_collection(db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value], Asset.get_indexes())

    # Chunk indexes
    print("Creating indexes for 'chunk' collection...")
    create_indexes_for_collection(db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value], Chunk.get_indexes())

    print("Indexes created successfully.")

if __name__ == "__main__":
    main()