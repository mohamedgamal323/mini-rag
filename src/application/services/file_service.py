import os
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import Depends
import aiofiles
import logging
from fastapi import UploadFile
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from domain.enums import ProcessingEnum
from application.services.base_service import BaseService
from application.services.chunk_service import ChunkService
from application.services.project_service import ProjectService
from infrastructure.repositories.mongo_project_repository import MongoProjectRepository
from infrastructure.repositories.mongo_chunk_repository import MongoChunkRepository
from domain.models.chunk import Chunk
from application.dtos.response_signal import ResponseSignal
from helpers.config import get_settings


class FileService(BaseService):
    def __init__(self, project_repository: MongoProjectRepository = Depends(), 
                 chunk_service : ChunkService = Depends(),
                 project_service: ProjectService = Depends()):
        super().__init__()
        self.project_repository = project_repository
        self.chunk_service = chunk_service
        self.project_service = project_service
        self.app_settings = get_settings()
        self.logger = logging.getLogger('uvicorn.error')
        self.size_scale = 1024 * 1024  # Convert MB to bytes

    def validate_uploaded_file(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    async def upload_file(self, project_id: str, file: UploadFile):
        # Validate file properties
        is_valid, result_signal = self.validate_uploaded_file(file)
        if not is_valid:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": result_signal
                }
            )

        file_path, file_id = await self.generate_unique_filepath(
            orig_file_name=file.filename,
            project_id=project_id
        )

        try:
            async with aiofiles.open(file_path, "wb") as f:
                while chunk := await file.read(self.app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)
        except Exception as e:

            self.logger.error(f"Error while uploading file: {e}")

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
                }
            )

        return JSONResponse(
                content={
                    "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                    "file_id": file_id,
                }
            )

    async def process_file(
        self, project_id: str, file_id: str, chunk_size: int, overlap_size: int, do_reset: bool
    ) -> int:
        # Validate file properties (removed as file_id is not an UploadFile)

        # Validate project existence
        project = await self.project_repository.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID {project_id} not found")

        # Get project path and load file content
        project_path = os.path.join("assets/files", project_id)
        file_content = self.load_file_content(project_path, file_id)

        # Process file content into chunks
        chunks = self.process_file_content(file_content, chunk_size, overlap_size)
        chunk_objects = [
            Chunk(
                content=chunk.page_content,
                metadata=chunk.metadata,
                order=i + 1,
                project_id=project_id,
                file_id=file_id,
            )
            for i, chunk in enumerate(chunks)
        ]
        self.logger.info(f"Before checking do reset: {do_reset}")
        # Check if do_reset is True
        if do_reset:
            # Delete existing chunks for the project
            self.logger.info(f"Deleting existing chunks for file_id: {file_id}")
            await self.chunk_service.delete_chunks_by_file_id(file_id=file_id)

        # Insert chunks into the database
        return await self.chunk_service.insert_chunks(chunk_objects)
    
    def load_file_content(self, project_path: str, file_id: str) -> list:
        file_ext = os.path.splitext(file_id)[-1]
        file_path = os.path.join(project_path, file_id)

        if file_ext == ProcessingEnum.TXT.value:
            loader = TextLoader(file_path, encoding="utf-8")
        elif file_ext == ProcessingEnum.PDF.value:
            loader = PyMuPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {file_ext}")

        return loader.load()
    
    def process_file_content(self, file_content: list, chunk_size: int = 100, overlap_size: int = 20) -> list:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [rec.page_content for rec in file_content]
        file_content_metadata = [rec.metadata for rec in file_content]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks
    
    async def generate_unique_filepath(self, orig_file_name: str, project_id: str):

        random_key = self.generate_random_string()
        project_path = await self.project_service.get_project_path(project_id=project_id)

        cleaned_file_name = self.get_clean_file_name(
            orig_file_name=orig_file_name
        )

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name
    
    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name