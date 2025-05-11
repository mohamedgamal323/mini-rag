from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from controllers.file_controller import FileController
from controllers.project_controller import ProjectController
from controllers.chunk_controller import ChunkController

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    # Initialize controllers with the database client
    app.file_processing_controller = FileController(app.db_client)
    app.project_controller = ProjectController(app.db_client)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()

# Include routers from controllers
app.include_router(app.file_processing_controller.router, prefix="/api/v1")
app.include_router(app.project_controller.router, prefix="/api/v1")
app.include_router(app.chunk_controller.router, prefix="/api/v1")


