import cv2
import streamlit as st
from PIL import Image
import numpy as np

def decode_barcode(image):
    detector = cv2.barcode_BarcodeDetector()
    retval, decoded_info, decoded_type, corners = detector.detectAndDecode(image)
    if retval:
        return decoded_info[0]  # Връща първия намерен баркод
    else:
        return None

st.title("Barcode Scanner with OpenCV")

uploaded_file = st.file_uploader("Upload an image with a barcode")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    image_np = np.array(image)
    decoded = decode_barcode(image_np)
    if decoded:
        st.success(f"Decoded barcode: {decoded}")
    else:
        st.error("Barcode not detected")
