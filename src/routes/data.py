from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import os
import aiofiles
from models import SignalResponces
import logging

# Initialize logging
logger = logging.getLogger('uvicorn_error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1" ,"Data"],
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)): 

    data_controller = DataController()

    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": result_signal}
        )

    # Save the file to the project directory
    # project_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_file_path(
        original_file_name=file.filename,
        project_id=project_id
    )
    print(f"File ID: {file_id}")
    print(f"File path: {file_path}")


    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.File_Chunk_Size):
                await f.write(chunk)
    except Exception as e:
        # Log the error
        logger.error(f"Error saving file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": SignalResponces.FILE_UPLOAD_FAILED.value}
        )

    return JSONResponse(
        content={"message": SignalResponces.FILE_UPLOAD_SUCCESS.value,
                 "file_id": file_id
                },
    )        