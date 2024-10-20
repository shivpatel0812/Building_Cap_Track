from picamera2 import Picamera2, Preview
from time import sleep

camera = Picamera2()
camera.start_preview(Preview.QTGL)
camera.start()
sleep(10)
camera.close()
