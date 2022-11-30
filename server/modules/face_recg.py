import cv2 #For Image processing 
import numpy as np #For converting Images to Numerical array 
import os #To handle directories 
from PIL import Image #Pillow lib for handling images 
from db import DB_DIR, getImagesByUser, getUser

MODEL_FILENAME = DB_DIR + '/face_recg_model.xml'

face_cascade = cv2.CascadeClassifier(os.path.realpath(__file__)) + '/haarcascade_frontalface_default.xml')




def face_train(user_face_dict):
    global face_cascade, MODEL_FILENAME
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    y_ID = []
    x_train = []

    for id, faceList in user_face_dict.items():
        for face in faceList:        
            Gery_Image = face.convert("L") # convert the image to greysclae using Pillow
            Crop_Image = Gery_Image.resize( (800,800) , Image.ANTIALIAS) #Crop the Grey Image to 550*550 (Make sure your face is in the center in all image)
            Final_Image = np.array(Crop_Image, "uint8")
            faces = face_cascade.detectMultiScale(Final_Image, scaleFactor=1.5, minNeighbors=5) #Detect The face in all sample image 
            print (id,faces)

            for (x,y,w,h) in faces:
                roi = Final_Image[y:y+h, x:x+w] #crop the Region of Interest (ROI)
                x_train.append(roi)
                y_ID.append(Face_ID)

    recognizer.train(x_train, np.array(y_ID)) #Create a Matrix of Training data 
    recognizer.save(MODEL_FILENAME)


def face_recg(img):
    global face_cascade, MODEL_FILENAME

    userList = list(map(lambda a:a[2], getUser(ActiveOnly = False)))

    recg_id = []
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_FILENAME)


    gray  = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2GRAY) #convert Video frame to Greyscale
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
    
    img = Image.fromarray(img)
    if len(recg_id): return True, recg_id, img
    return False, recg_id, img

