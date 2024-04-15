import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import imagehash
import cv2



def ahash(image, hash_size=8):
    #convert image into grayscale for easier computation
    image = ImageOps.grayscale(image) 
    #resize image down to 9x8 aspect ratio: 
    image = image.resize((hash_size, hash_size), Image.Resampling.LANCZOS)
    pixels = np.array(image)
    avg = pixels.mean()
    diff = pixels > avg
    return ''.join(['1' if val else '0' for val in diff.flatten()])

def dhash(image, hash_size=8):
    image = ImageOps.grayscale(image)
    image = image.resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = np.array(image)
    diff = pixels[:, 1:] > pixels[:, :-1]
    return ''.join(['1' if val else '0' for val in diff.flatten()])


def phash(image, hash_size=8):
#try this for now
    image = ImageOps.grayscale(image)
    image = image.resize((32, 32), Image.Resampling.LANCZOS)
    pixels = np.array(image, dtype=np.float32)
    # need opencv
    dct = cv2.dct(pixels)
    dct_low_freq = dct[:hash_size, :hash_size]
    median = np.median(dct_low_freq)
    diff = dct_low_freq >= median
    return ''.join(['1' if val else '0' for val in diff.flatten()])

def hamming_distance(hash1, hash2):
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

def load_image(image_file):
    return Image.open(image_file)

def main():
    
    with open( "app/style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    st.title("Image Hashing App")
    st.write("Upload two images to check the how the two hashing algorithms compare. Also check with similar images, like screenshots or cropped images. ")
    hashing_option = st.radio("Choose the hashing method:", ["Simple hash", "Perceptual hash", "Difference hash"])
    if hashing_option == "Simple hash":
            st.write("Performing a simple hash: ")
            st.write("The average hash (ahash), or a simple hash simplifies an image by resizing it to a small, uniform size, converting it to grayscale, and then computing the average pixel value. Each pixel's value is then compared to this average, assigning a 1 if it's above the average or 0 if below, forming a binary hash.")
            st.write("This is a fast method and is good at identifying images with minor differences. ")

    elif hashing_option == "Perceptual hash":
            st.write("Performing a perceptual hash: ")
            st.write("Perceptual Hash (phash) also starts by resizing and converting the image to grayscale but then applies a Discrete Cosine Transform (DCT) to focus on the image's frequency patterns. Only the most significant components of the DCT (representing the image's 'essence') are kept to construct the hash. This makes pHash more sensitive to image content rather than details and is better at identifying images that are perceptually similar rather than pixel-by-pixel identical.")

    elif hashing_option == "Difference hash":
            st.write("Performing a difference hash: ")
            st.write("Difference Hash (dhash) creates a hash reflecting the image's texture and gradient patterns. This method is particularly effective for detecting images with similar content despite variations in brightness or contrast. The Transform (DCT) is used to focus on the image's frequency patterns. Only the most significant components of the DCT (representing the image's 'essence') are kept to construct the hash. ")

    # Creating two columns for the file uploaders:
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        image_file1 = st.file_uploader("Upload image 1", type=["png", "jpg", "jpeg"], key="file_uploader1")

    with col2:
        image_file2 = st.file_uploader("Upload image 2", type=["png", "jpg", "jpeg"], key="file_uploader2")

    if image_file1 and image_file2 and hashing_option:
        image1 = load_image(image_file1)
        image2 = load_image(image_file2)
        with col3:

            st.image(image1, caption="Uploaded Image 1", use_column_width=False, width=250)
        
        with col4:
            st.image(image2, caption="Uploaded Image 2", use_column_width=False, width=250)

        if hashing_option == "Simple hash":
            st.write("Performing a simple hash: ")
            hash1 = ahash(image1)
            hash2 = ahash(image2)
        elif hashing_option == "Perceptual hash":
            st.write("Performing a perceptual hash: ")
            hash1 = phash(image1)
            hash2 = phash(image2)
        elif hashing_option == "Difference hash":
            st.write("Performing a difference hash: ")
            hash1 = dhash(image1)
            hash2 = dhash(image2)


        distance = hamming_distance(hash1, hash2)
        similarity = "similar" if distance <= 5 else "not similar"
        st.write(f"The images are {similarity} (Hamming distance: {distance}).")

if __name__ == "__main__":
    main()
