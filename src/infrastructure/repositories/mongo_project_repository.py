from bson.objectid import ObjectId
from fastapi import Depends
from infrastructure.repositories.db_client import get_db_client
from domain.models.project import Project
from domain.enums.database_enum import DataBaseEnum

class MongoProjectRepository:
    def __init__(self, db_client = Depends(get_db_client)):
        self.collection = db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    @staticmethod
    def to_mongo(project: Project) -> dict:
        return {
            "_id": ObjectId(project.id) if project.id else None,
            "project_id": project.project_id,
        }

    @staticmethod
    def from_mongo(data: dict) -> Project:
        return Project(
            id=str(data["_id"]) if "_id" in data else None,
            project_id=data["project_id"],
        )

    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project.id = str(result.inserted_id)
        return project

    async def get_project(self, project_id: str):
        result = await self.collection.find_one({"project_id": project_id})
        if result is None:
            return None
        # Convert _id to string before returning
        result["id"] = str(result["_id"])
        del result["_id"]
        return Project(**result)

    async def update_project(self, project_id: str, update_data: dict):
        result = await self.collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": update_data}
        )
        return result.modified_count

    async def delete_project(self, project_id: str):
        result = await self.collection.delete_one({"_id": ObjectId(project_id)})
        return result.deleted_count

    def create_indexes(self):
        for index in Project.get_indexes():
            self.collection.create_index(index["keys"], **index.get("options", {}))