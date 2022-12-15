"""
self defined image convertion utilities 
"""
from PIL import Image
import io
import base64
import numpy as np
import cv2

def imgc_pil2cv(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def imgc_cv2pil(cv_img):
    return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))


def imgc_pil2base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def imgc_cv2base64(cv_img):
    return imgc_pil2base64(imgc_cv2pil(cv_img))

def imgc_base642pil(base64_str):
    try:
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64_str, "utf-8"))))
    except:
        img = Image.new('RGB', (800, 800), (255,255,255))
    return img


def imgc_base642cv(base64_str):
    return imgc_pil2cv(imgc_base642pil(base64_str))

def imgc_base642url(base64_str):
    return 'data:image/jpeg;base64,' + base64_str

def imgc_base642bytesio(base64_str):
    temp_io = io.BytesIO()
    imgc_base642pil(base64_str).save(temp_io, format='JPEG')
    temp_io.seek(0)
    return temp_io

