from fastapi import FastAPI,  APIRouter
import os


base_router = APIRouter(
    prefix="/api/v1",
    tags=["Base"],
)

@base_router.get("/")
async def welcome_message():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    if app_name and app_version:
        return f"Welcome to {app_name} version {app_version}!"
    else:
        # Fallback message if environment variables are not set
        return "Welcome to the FastAPI application!"