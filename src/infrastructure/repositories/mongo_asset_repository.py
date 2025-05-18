from fastapi import Depends
from infrastructure.repositories.db_client import get_db_client
from domain.models.asset import Asset
from domain.enums.asset_type_enum import AssetType

class MongoAssetRepository:
    def __init__(self, db_client=Depends(get_db_client)):
        self.collection = db_client["assets"]

    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = str(result.inserted_id)
        return asset

    async def get_asset(self, asset_id: str):
        result = await self.collection.find_one({"asset_id": asset_id})
        if result is None:
            return None
        result["id"] = str(result["_id"])
        del result["_id"]
        return Asset(**result)

    async def list_assets_by_project(self, project_id: str, asset_type: AssetType = None):
        query = {"project_id": project_id}
        if asset_type:
            query["type"] = asset_type
        cursor = self.collection.find(query)
        assets = []
        async for doc in cursor:
            doc.pop("_id", None)  # Remove the _id field
            assets.append(Asset(**doc))
        return assets

    async def mark_asset_processed(self, asset_id: str):
        await self.collection.update_one({"asset_id": asset_id}, {"$set": {"processed": True}})