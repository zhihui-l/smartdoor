import cv2
import numpy as np 
import os
from PIL import Image 


face_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)) + '/../lib/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
print(os.path.dirname(os.path.realpath(__file__)) + '/../lib/haarcascade_frontalface_default.xml')
MODEL_DIR = '/var/SMARTDOOR_MODEL.yml'

HAVE_MODEL = False

if os.path.exists(MODEL_DIR):
    recognizer.read(MODEL_DIR)
    HAVE_MODEL = True


def detect_face(img_original):

    img = np.copy(img_original)
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_position = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    faces = []
    for (x, y, w, h) in faces_position:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        faces.append(gray[y:y+h, x:x+w])
    
    return img, faces, faces_position, HAVE_MODEL


def recg_face(face):
    return recognizer.predict(face)


def label_face(img, face_position, id, confidence):
    cv2.putText(img, 
        str(id) + ': ' + str(confidence) + '%' 
    , (face_position[0],face_position[1]), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 10)
    return img

def train_face(id, face):
    global HAVE_MODEL
    recognizer.update([face], np.array([id]))
    recognizer.save(MODEL_DIR)
    HAVE_MODEL = True
    print('tt', id)

def retrain_face(ids, faces):
    global HAVE_MODEL
    recognizer.train(faces, np.array(ids))
    recognizer.save(MODEL_DIR)
    HAVE_MODEL = True