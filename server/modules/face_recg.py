
import cv2 #For Image processing 
import numpy as np #For converting Images to Numerical array 
import os #To handle directories 
from PIL import Image #Pillow lib for handling images 



def face_train():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    Face_ID = 0 
    pev_person_name = ""
    y_ID = []
    x_train = []

    Face_Images = os.path.dirname(os.path.realpath(__file__)) + "/img copy" #Tell the program where we have saved the face images 
    print (Face_Images)

    for root, dirs, files in os.walk(Face_Images): #go to the face image directory 
        for file in files: #check every directory in it 
                if file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png"): #for image files ending with jpeg,jpg or png 
                    path = os.path.join(root, file)
                    person_name = os.path.basename(root)
                    print(path, person_name)

                
                    if pev_person_name!=person_name: #Check if the name of person has changed 
                        Face_ID=Face_ID+1 #If yes increment the ID count 
                        pev_person_name = person_name

			
                Gery_Image = Image.open(path).convert("L") # convert the image to greysclae using Pillow
                Crop_Image = Gery_Image.resize( (800,800) , Image.ANTIALIAS) #Crop the Grey Image to 550*550 (Make sure your face is in the center in all image)
                Final_Image = np.array(Crop_Image, "uint8")
                #print(Numpy_Image)
                faces = face_cascade.detectMultiScale(Final_Image, scaleFactor=1.5, minNeighbors=5) #Detect The face in all sample image 
                print (Face_ID,faces)

                for (x,y,w,h) in faces:
                    roi = Final_Image[y:y+h, x:x+w] #crop the Region of Interest (ROI)
                    x_train.append(roi)
                    y_ID.append(Face_ID)

    recognizer.train(x_train, np.array(y_ID)) #Create a Matrix of Training data 
    recognizer.save("face-trainner.yml") #Save the matrix as YML file 

face_train()


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