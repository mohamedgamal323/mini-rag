from bson.objectid import ObjectId
from src.domain.models.project import Project
from src.domain.enums.database_enum import DataBaseEnum

class MongoProjectRepository:
    def __init__(self, db_client):
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
        result = await self.collection.find_one({"_id": ObjectId(project_id)})
        if result is None:
            return None
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