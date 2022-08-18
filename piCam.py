from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()

i = 0
try:
    while True:
        sleep(5)
        name = "/home/pi/TRC3000/images/pic{}".format(str(i))
        camera.capture(name)
        i += 1
except KeyboardInterrupt:
    print('Camera Stopped')
camera.stop_preview()