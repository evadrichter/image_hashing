import os
from PIL import Image
import pandas as pd
import imagehash
import matplotlib.pyplot as plt

# path
folder_path = r"C:\Users\evari\OneDrive\Old computer\Bilder\Old Computer\MlatzWerkstatt"

data = []

#  list iwth cropped images
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

# Process each file
for file in files:
    if "_cropped" in file:
        continue
    
    base_name = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    cropped_file = base_name + "_cropped" + extension
    
    if cropped_file in files:
        # Compute the hash values and Hamming distances
        original_path = os.path.join(folder_path, file)
        cropped_path = os.path.join(folder_path, cropped_file)
        
        original_image = Image.open(original_path)
        cropped_image = Image.open(cropped_path)
        
        # Compute hashes
        ahash_distance = imagehash.average_hash(original_image) - imagehash.average_hash(cropped_image)
        phash_distance = imagehash.phash(original_image) - imagehash.phash(cropped_image)
        dhash_distance = imagehash.dhash(original_image) - imagehash.dhash(cropped_image)
        crop_distance = imagehash.crop_resistant_hash(original_image) - imagehash.crop_resistant_hash(cropped_image)
        
        # Append the results to the data list
        data.append([file, cropped_file, ahash_distance, phash_distance, dhash_distance, crop_distance])

# Create a df from the collected data
df = pd.DataFrame(data, columns=['Name of Image', 'Name of Cropped Image', 'ahash_h_distance', 'phash_h_distance', 'dhash_h_distance', 'crop_resistant_h_distance'])



# aHash
plt.figure(figsize=(5, 5)) 
plt.hist(df['ahash_h_distance'], bins=10, color='lightblue')
plt.title('Simple hash hamming distance (ahash)')
plt.xlabel('Hamming Distance')
plt.ylabel('Frequency')
plt.xlim(0, 50)
plt.show() 

# pHash
plt.figure(figsize=(5, 5)) 
plt.hist(df['phash_h_distance'], bins=10, color='lightgreen')
plt.title('Perceptual hash hamming distance (phash)')
plt.xlabel('Hamming Distance')
plt.ylabel('Frequency')
plt.xlim(0, 50)
plt.show()  

# dHash
plt.figure(figsize=(5, 5))  
plt.hist(df['dhash_h_distance'], bins=10, color='salmon')
plt.title('Difference hash hamming distance (dhash)')
plt.xlabel('Hamming Distance')
plt.ylabel('Frequency')
plt.xlim(0, 50)
plt.show()  

# Crop-resistant hashing
plt.figure(figsize=(5, 5)) 
plt.hist(df['crop_resistant_h_distance'], bins=10, color='pink')
plt.title('Crop-resistant hamming distances')
plt.xlabel('Hamming Distance')
plt.ylabel('Frequency')
plt.xlim(0, 50)
plt.show() 
