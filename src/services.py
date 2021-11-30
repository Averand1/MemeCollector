from typing import List
import os
import random 
import fastapi
import time as _time

def get_image_filenames(director_name: str) -> List[str]:
    return os.listdir(director_name)

def select_random_image(directory_name: str) -> str:
    images = get_image_filenames(directory_name)
    random_image = random.choice(images)
    path = f"{directory_name}/{random_image}"
    return path
    
def _is_image(filename: str) -> bool:
    valid_extensions  = (".png", ".jpg", "jpeg", ".gif")
    return filename.endswith(valid_extensions)

def upload_image(directory_name: str, image: fastapi.UploadFile):
    if _is_image(image.filename):
        timestr = _time.strftime("%Y_%m_%d_%H_%M_%S")
        image_name = timestr + image.filename.replace(" ", "-")
        with open(f"{directory_name}/{image_name}", "wb+") as image_file_upload:
            image_file_upload.write(image.file.read())
            
            
        return f"{directory_name}/{image_name}"
    
    return None