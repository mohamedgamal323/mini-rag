from fastapi import APIRouter, HTTPException, UploadFile
from controllers.base_controller import BaseController
from application.services.file_service import FileService
from application.dtos.process_request_dto import ProcessRequestDTO

class FileController(BaseController):
    def __init__(self, db_client):
        super().__init__()
        self.router = APIRouter(prefix="/files", tags=["files"])

        # Initialize the service
        self.file_service = FileService(db_client)

        # Upload File Endpoint
        @self.router.post("/{project_id}/upload")
        async def upload_file(project_id: str, file: UploadFile):
            try:
                # Validate and upload the file using the service
                result = await self.file_service.upload_file(
                    project_id=project_id,
                    file=file
                )
                return result
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        # Process File Endpoint
        # This endpoint processes the file and returns the number of inserted chunks
        @self.router.post("/{project_id}/process")
        async def process_file(project_id: str, process_request: ProcessRequestDTO):
            try:
                # Process the file using the service
                result = await self.file_service.process_file(
                    project_id=project_id,
                    file_id=process_request.file_id,
                    chunk_size=process_request.chunk_size,
                    overlap_size=process_request.overlap_size,
                    do_reset=process_request.do_reset,
                )
                return {"signal": "PROCESSING_SUCCESS", "inserted_chunks": result}
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))