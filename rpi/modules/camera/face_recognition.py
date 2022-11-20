#Program to Detect the Face and Recognise the Person based on the data from face-trainner.yml

import cv2 #For Image processing 
import numpy as np #For converting Images to Numerical array 
import os #To handle directories 
from PIL import Image #Pillow lib for handling images 



def face_recg(img, userList):

    recg_id = []

    face_cascade = cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__))+'/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(os.path.dirname(os.path.realpath(__file__))+"/face-trainner.yml")


    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert Video frame to Greyscale
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) #Recog. faces
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w] #Convert Face to greyscale 
        id_, conf = recognizer.predict(roi_gray) #recognize the Face 
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        if conf >= 30:
            font = cv2.FONT_HERSHEY_SIMPLEX #Font style for the name 
            name = userList[id_] #Get the name from the List using ID number 
            recg_id.append(id_)
            cv2.putText(img, name, (x,y), font, 1, (0,0,255), 2)
    if len(recg_id): return True, recg_id, img
    return False, recg_id, img

    


labels = ["jerry", "kevin", "jeffery"] 

cap = cv2.VideoCapture(0) #Get vidoe feed from the Camera

while True:
    ret, img = cap.read() # Break video into frames 
    a, b,c = face_recg(img, labels)
    print(a,b)
    cv2.imwrite('Preview.jpg', c)
    

# When everything done, release the captur