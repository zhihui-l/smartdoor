
import cv2
from time import time, sleep

def camera(queue_photo_from_camera):
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, img = cap.read()
            if queue_photo_from_camera.qsize() < 2:
                queue_photo_from_camera.put(img)
    except KeyboardInterrupt:
        del cap    
