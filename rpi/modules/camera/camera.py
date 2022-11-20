from picamera import PiCamera
from time import sleep
import os

# img_path = 'home/zl826/smartdoor/rpi/modules/camera/img/kevin'

# try:
#     os.mkdir(img_path)
# except OSError as error:
#     print(error)
    
camera = PiCamera()

camera.start_preview()
# sleep(10)
for i in range (1,101):
    camera.capture("img/jeffery/" + str(i) + ".jpg")
 
camera.stop_preview()