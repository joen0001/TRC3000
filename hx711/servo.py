from gpiozero import Servo
from time import sleep

servo = Servo(17)
val = -1
increament  = 0.1
try:
    while True:
        servo.value = val
        sleep(increament)
        val = val + increament
        if val > 1:
            val = -1
except KeyboardInterrupt:
    print('Stopped')