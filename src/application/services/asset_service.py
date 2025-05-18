from fastapi import UploadFile, Depends
from fastapi.responses import JSONResponse

from typing import List, Optional
from domain.enums.asset_type_enum import AssetType
from domain.models.asset import Asset
from infrastructure.repositories.mongo_asset_repository import MongoAssetRepository
from infrastructure.repositories.mongo_chunk_repository import MongoChunkRepository
from application.dtos.asset_dto import CreateAssetDTO
from application.dtos.process_request_dto import ProcessAllRequestDTO
from .asset_handlers.file_asset_handler import FileAssetHandler
from domain.enums.asset_type_enum import AssetType
from domain.models.chunk import Chunk
from application.services.base_service import BaseService
import logging 

class AssetService(BaseService):
    def __init__(
        self,
        asset_repository: MongoAssetRepository = Depends(),
        chunk_repository: MongoChunkRepository = Depends()
    ):
        self.asset_repository = asset_repository
        self.chunk_repository = chunk_repository

    async def upload_file_asset(self, project_id: str, file: UploadFile):
        logging.info("Before reading file content")
        content = await file.read()
        logging.info("After reading file content")
        asset = Asset(
            asset_id=self.generate_random_string() + file.filename,  # You may want to generate a unique ID
            project_id=project_id,
            type=AssetType.FILE,
            source=file.filename,
            content=content,
            processed=False,
            metadata={"content_type": file.content_type, "size": len(content)},
        )
        asset = await self.asset_repository.create_asset(asset)
        return JSONResponse(
                    content={
                        "signal": "Success",
                        "asset_id": asset.asset_id,
                    }
                )

    async def process_asset(self, asset_id: str, project_id: str, process_all_request: Optional[ProcessAllRequestDTO] = None):
        asset = await self.asset_repository.get_asset(asset_id)
        if not asset or asset.processed:
            return None
        if asset.type == AssetType.FILE:
            file_handler = FileAssetHandler()
            chunks = file_handler.process(asset, process_all_request.chunk_size, process_all_request.overlap_size)
            if chunks:
            # Map the returned chunks to Chunk model before inserting into the repository
                chunk_objects = [
                    Chunk(
                        content=chunk,
                        metadata=asset.metadata,
                        order=chunk.chunk_order,
                        project_id=project_id,
                        asset_id=chunk.asset_id,
                    )
                    for i, chunk in enumerate(chunks)
                ]
                await self.chunk_repository.insert_many_chunks(chunk_objects)
                await self.asset_repository.mark_asset_processed(asset_id)
            return {"asset_id": asset_id, "chunks_count": len(chunks)}
        return None

    async def process_all_assets_for_project(self, project_id: str, process_all_request: ProcessAllRequestDTO):
        assets = await self.asset_repository.list_assets_by_project(project_id, AssetType.FILE)
        results = []
        for asset in assets:
            if not asset.processed:
                result = await self.process_asset(asset.asset_id, project_id, process_all_request)
                results.append(result)
        return results