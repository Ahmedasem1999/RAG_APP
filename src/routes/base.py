from fastapi import FastAPI,  APIRouter, Depends
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["Base"],
)

@base_router.get("/")
async def welcome_message(app_settings: Settings = Depends(get_settings)):

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    if app_name and app_version:
        return f"Hello {app_name} version {app_version}!"
    else:
        # Fallback message if environment variables are not set
        return "Welcome to the FastAPI application!"