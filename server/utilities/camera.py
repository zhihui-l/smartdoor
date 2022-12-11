from picamera import PiCamera
from io import BytesIO
from PIL import Image

class Camera:
    camera = None

    def __init__(self):
        self.camera = PiCamera()
        self.camera.start_preview()

    def __del__(self):
        self.camera.stop_preview()

    def get(self):
        stream = BytesIO()
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        image = Image.open(stream).resize( (800,800) , Image.ANTIALIAS)
        return image

