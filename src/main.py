from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from controllers.file_controller import FileController
from controllers.project_controller import ProjectController
from controllers.chunk_controller import ChunkController

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.include_router(FileController().router, prefix="/api/v1")
    app.include_router(ProjectController().router, prefix="/api/v1")
    app.include_router(ChunkController().router, prefix="/api/v1")





