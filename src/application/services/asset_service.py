from fastapi import UploadFile, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
from domain.enums.asset_type_enum import AssetType
from domain.models.asset import Asset
from domain.enums.llm_provider_enum import LLMProviderEnum
from infrastructure.repositories.mongo_asset_repository import MongoAssetRepository
from infrastructure.repositories.mongo_chunk_repository import MongoChunkRepository
from application.dtos.asset_dto import CreateAssetDTO
from application.dtos.process_request_dto import ProcessAllRequestDTO
from .asset_handlers.file_asset_handler import FileAssetHandler
from domain.enums.asset_type_enum import AssetType
from domain.models.chunk import Chunk
from application.services.base_service import BaseService
from application.services.llm_providers.llm_provider_factory import LLMProviderFactory
from application.services.vector_db_providers.vector_db_factory import VectorDBFactory
from domain.enums.vector_db_provider_enum import VectorDBProviderEnum
import logging 
import re   

class AssetService(BaseService):
    def __init__(
        self,
        asset_repository: MongoAssetRepository = Depends(),
        chunk_repository: MongoChunkRepository = Depends()
    ):
        self.asset_repository = asset_repository
        self.chunk_repository = chunk_repository
        self.logger = logging.getLogger('uvicorn.error')

    async def upload_file_asset(self, project_id: str, file: UploadFile):
        logging.info("Before reading file content")
        content = await file.read()
        logging.info("After reading file content")
        asset = Asset(
            asset_id=self.generate_random_string() + self.get_clean_asset_name(file.filename),  # You may want to generate a unique ID
            asset_name=self.get_clean_asset_name(file.filename),
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
            self.logger.info(f"Chunks generated: {len(chunks)}")
            self.logger.info(f"Chunks: {chunks[0]}")
            if chunks:
                # 1. Batch save chunk into MongoDB
                chunk_objects = [
                    Chunk(
                        content=chunk["content"],
                        metadata=chunk["metadata"],
                        order=chunk["chunk_order"],
                        project_id=project_id,
                        asset_id=asset_id,
                    )
                    for i, chunk in enumerate(chunks)
                ]
                await self.chunk_repository.insert_many_chunks(chunk_objects)

                # 2. Batch embed chunk texts
                llm = LLMProviderFactory.create(LLMProviderEnum.OPENAI)
                chunk_texts = [chunk["content"] for chunk in chunks]
                embeddings = await llm.batch_embed(chunk_texts)

                # 3. Push embeddings and metadata to VectorDB
                vector_db = VectorDBFactory.create(VectorDBProviderEnum.QDRANT)
                vector_points = [
                    {
                        "chunk_id": chunk["chunk_id"],
                        "asset_id": chunk["asset_id"],
                        "project_id": project_id,
                        "order": chunk.get("chunk_order", idx),
                        "embedding": embeddings[idx],
                    }
                    for idx, chunk in enumerate(chunks)
                ]
                vector_db.add_embeddings("chunks", vector_points)

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
    
    def get_clean_asset_name(self, orig_asset_name: str):

        # remove any special characters, except underscore and .
        cleaned_asset_name = re.sub(r'[^\w.]', '', orig_asset_name.strip())

        # replace spaces with underscore
        cleaned_asset_name = cleaned_asset_name.replace(" ", "_")

        return cleaned_asset_name