from .BaseController import BaseConltoller
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import SignalResponces
import os
import re
class DataController(BaseConltoller):
    def __init__(self):
        super().__init__()
        self.size_scale = 10485760  

    def validate_uploaded_file(self, file: UploadFile):
        # print(f"File type: {file.content_type}")
        # print(f"File size: {file.size}")
        # print(f"Allowed types: {self.app_settings.File_Allowed_Types}")

        if file.content_type not in self.app_settings.File_Allowed_Types:
            return False, SignalResponces.FILE_TYPE_INVALID.value
        
        if file.size > self.app_settings.File_Max_Size * self.size_scale:
            return False, SignalResponces.FILE_SIZE_EXCEEDED.value
        
        return True, SignalResponces.FILE_UPLOAD_SUCCESS.value

    def generate_unique_file_path(self, original_file_name: str, project_id: str):
        """Generate a unique file name by appending a random string to the original file name."""
        random_string = self.generate_random_string()
        file_path = ProjectController().get_project_path(project_id=project_id)
        clean_file_name = self.get_clean_file_name(original_file_name)
        new_file_path = os.path.join(file_path, f"{random_string}_{clean_file_name}")

        # Ensure the file name is unique
        while os.path.exists(new_file_path):
            random_string = self.generate_random_string()
            new_file_path = os.path.join(file_path, f"{random_string}_{clean_file_name}")
        
        return new_file_path, random_string + "_" + clean_file_name

    def get_clean_file_name(self, file_name: str):
        """Remove special characters from the file name."""
        # Remove special characters and replace spaces with underscores
        clean_file_name = re.sub(r'[^\w.]', ' ', file_name.strip())
        clean_file_name = clean_file_name.replace(' ', '_')
        
        return clean_file_name
