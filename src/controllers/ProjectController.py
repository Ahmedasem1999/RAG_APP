from .BaseController import BaseConltoller
import os


class ProjectController(BaseConltoller):
    def __init__(self):
        super().__init__()
        
    def get_project_path(self, project_id: str):
        """
        Get the path for a specific project.
        """
        project_path = os.path.join(self.file_paths, project_id)
        
        # Check if the directory exists
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        
        return project_path
