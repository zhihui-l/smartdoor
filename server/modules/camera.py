from picamera import PiCamera
from time import sleep
import os
import hashlib


camera = PiCamera()

camera.start_preview()
# sleep(10)
for i in range (1,101):
    camera.capture("img/jeffery/" + str(i) + ".jpg")
 
hashlib.md5("whatever your string is".encode('utf8')).hexdigest()

camera.stop_preview()