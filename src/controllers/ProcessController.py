from .BaseController import BaseConltoller
from .ProjectController import ProjectController
import os
import pypdfium2 as pdfium
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
from pytesseract import image_to_string 


class ProcessController(BaseConltoller):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)
        
    def get_file_extension(self, file_name: str):
        """
        Get the file extension of a given file name.
        """
        return os.path.splitext(file_name)[-1]

    def convert_pdf_to_images(self, file_path, scale=300/72):
    
        pdf_file = pdfium.PdfDocument(file_path)  
        page_indices = [i for i in range(len(pdf_file))]
        
        renderer = pdf_file.render(
            pdfium.PdfBitmap.to_pil,
            page_indices = page_indices, 
            scale = scale,
        )
        
        list_final_images = [] 
        
        for i, image in zip(page_indices, renderer):
            
            image_byte_array = BytesIO()
            image.save(image_byte_array, format='jpeg', optimize=True)
            image_byte_array = image_byte_array.getvalue()
            list_final_images.append(dict({i:image_byte_array}))
    
        return list_final_images
    
    def display_images(self ,list_dict_final_images:list):
        all_images = [list(data.values())[0] for data in list_dict_final_images]

        for index, image_bytes in enumerate(all_images):

            image = Image.open(BytesIO(image_bytes))
            figure = plt.figure(figsize = (image.width / 100, image.height / 100))

            plt.title(f"----- Page Number {index+1} -----")
            plt.imshow(image)
            plt.axis("off")
            plt.show()

    def extract_text_with_pytesseract(self, list_dict_final_images:list):
    
        image_list = [list(data.values())[0] for data in list_dict_final_images]
        image_content = []
        
        for index, image_bytes in enumerate(image_list):
            
            image = Image.open(BytesIO(image_bytes))
            raw_text = str(image_to_string(image))
            image_content.append(raw_text)
        
        return "\n".join(image_content)