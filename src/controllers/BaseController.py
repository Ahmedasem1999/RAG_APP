from helpers.config import get_settings, Settings
import os
import random
import string

class BaseConltoller:
    def __init__(self):
        # Initialize the base controller
        self.app_settings = get_settings()
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print(f"Base path: {self.base_path}")
        
        self.file_paths = os.path.join(
            self.base_path,
            "assets/files"
            )
        
    def generate_random_string(self, length=10):
        """Generate a random string of fixed length."""
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(length))
    
