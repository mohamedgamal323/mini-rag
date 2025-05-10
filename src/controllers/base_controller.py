from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings

class BaseController:
    def __init__(self, prefix: str = "", tags: list[str] = None):
        self.router = APIRouter(prefix=prefix, tags=tags or [])
        self.app_settings = get_settings()
        self.base_dir = self.app_settings.PROJECTS_ROOT

        # Add a default route to retrieve application information
        @self.router.get("/")
        async def welcome(app_settings: Settings = Depends(get_settings)):
            return {
                "app_name": app_settings.APP_NAME,
                "app_version": app_settings.APP_VERSION,
            }