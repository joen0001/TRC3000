from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()
sleep(5)
camera.capture('/home/pi/TRC3000/images/image.jpg')
camera.stop_preview()
