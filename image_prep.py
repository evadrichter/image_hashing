#importing modules
import os
import random
from PIL import Image

def crop_and_save(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        with Image.open(image_path) as img:
            width, height = img.size
            
            # generate random crop size
            crop_width = random.randint(int(width * 0.4), int(width * 0.8))
            crop_height = random.randint(int(height * 0.4), int(height * 0.8))
            
            #starting crop here
            left = random.randint(0, width - crop_width)
            top = random.randint(0, height - crop_height)
            right = left + crop_width
            bottom = top + crop_height
            
            # crop
            cropped_image = img.crop((left, top, right, bottom))
            
            # Save image
            cropped_image_path = os.path.join(folder_path, f"{os.path.splitext(image_file)[0]}_cropped{os.path.splitext(image_file)[1]}")
            cropped_image.save(cropped_image_path)


crop_and_save("C:/Users/evari/OneDrive/Old computer/Bilder/Old Computer/MlatzWerkstatt")