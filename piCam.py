from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()

i = 0
try:
    while True:
        sleep(2)
        name = "/home/pi/TRC3000/images/pic"+str(i)+".jpg"
        camera.capture(name)
        i += 1
except KeyboardInterrupt:
    print('Camera Stopped')
camera.stop_preview()