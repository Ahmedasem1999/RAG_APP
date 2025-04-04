from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import os
import aiofiles
from models import SignalResponces
import logging
from .schemes.data_scheme import DataScheme

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
    # print(f"File ID: {file_id}")
    # print(f"File path: {file_path}")


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


@data_router.post("/process/{project_id}")
async def process_file(project_id: str, DataScheme:DataScheme):
    file_id = DataScheme.file_id
    file_path = os.path.join(ProjectController().get_project_path(project_id=project_id), file_id)
    
    # print(f"File ID: {file_id}")
    # print(f"File path: {file_path}")

    file_extention = ProcessController(project_id).get_file_extension(file_name=file_id)
    # print(f"File extension: {file_extention}")

    if file_extention != ".pdf":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": SignalResponces.FILE_TYPE_NOT_SUPPORTED.value}
        )
    
    try:
        list_final_images = ProcessController(project_id).convert_pdf_to_images(file_path=file_path)
        # ProcessController(project_id).display_images(list_dict_final_images=list_final_images)
        print(f"List of images:",len(list_final_images))

        # text_content = ProcessController(project_id).extract_text_with_pytesseract(list_dict_final_images=list_final_images)
        # print(text_content)

    except Exception as e:
        # Log the error
        logger.error(f"Error processing file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": SignalResponces.FILE_UPLOAD_FAILED.value}
        )

    return file_id