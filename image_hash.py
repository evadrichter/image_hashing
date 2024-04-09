import streamlit as st
from PIL import Image, ImageOps
import numpy as np

def ahash(image, hash_size=8):
    image = ImageOps.grayscale(image)
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

def hamming_distance(hash1, hash2):
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

def load_image(image_file):
    return Image.open(image_file)

def main():

    st.title("Image Hashing App")
    st.write("Upload two images to check the how the two hashing algorithms compare. Also check with similar images, like screenshots or cropped images. ")
    hashing_option = st.radio("Choose the hashing method:", ["Simple hash", "Difference hash"])
    if hashing_option == "Simple hash":
            st.write("Performing a simple hash: ")

    elif hashing_option == "Perceptual hash":
            st.write("Performing a difference hash: ")

    # Creating two columns for the file uploaders:
    col1, col2 = st.columns(2)

    with col1:
        image_file1 = st.file_uploader("Upload image 1", type=["png", "jpg", "jpeg"], key="file_uploader1")

    with col2:
        image_file2 = st.file_uploader("Upload image 2", type=["png", "jpg", "jpeg"], key="file_uploader2")

    if image_file1 and image_file2 and hashing_option:
        image1 = load_image(image_file1)
        image2 = load_image(image_file2)


        st.image(image1, caption="Uploaded Image 1", use_column_width=False, width=250)
        st.image(image2, caption="Uploaded Image 2", use_column_width=False, width=250)

        if hashing_option == "Simple hash":
            st.write("Performing a simple hash: ")
            hash1 = ahash(image1)
            hash2 = ahash(image2)
        elif hashing_option == "Perceptual hash":
            st.write("Performing a perceptual hash: ")
            hash1 = dhash(image1)
            hash2 = dhash(image2)

        distance = hamming_distance(hash1, hash2)
        similarity = "similar" if distance <= 5 else "not similar"
        st.write(f"The images are {similarity} (Hamming distance: {distance}).")

if __name__ == "__main__":
    main()
