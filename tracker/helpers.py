import cv2
import numpy as np


def convert_image_to_nump_array(uploaded_file):
    """since the ocr model expects either a file path or a numpy array
    the function converts the uploaded image of type TemporaryUploadedFile to 
    a numpy array"""
    # Reset pointer to start in case it was read before
    uploaded_file.seek(0)
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img
