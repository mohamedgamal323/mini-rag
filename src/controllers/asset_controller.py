from fastapi import APIRouter, UploadFile, File, Depends
from application.services.asset_service import AssetService
from application.dtos.process_request_dto import ProcessAllRequestDTO
import logging
class AssetController:
    def __init__(self):
        self.router = APIRouter(prefix="/assets", tags=["Assets"])


        @self.router.post("/{project_id}/upload")
        async def upload_file_asset(
            project_id: str,
            file: UploadFile,
            asset_service: AssetService = Depends(),
        ):
            logging.info("Before sending file to service")
            return await asset_service.upload_file_asset(project_id, file)

        @self.router.post("/{project_id}/process_all")
        async def process_all_assets(
            project_id: str,
            process_all_request: ProcessAllRequestDTO,
            asset_service: AssetService = Depends(),
        ):
            return await asset_service.process_all_assets_for_project(project_id,process_all_request )