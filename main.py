from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from mpu6050 import mpu6050
import sys
from hx711 import HX711

# File to Initialise all modules
# Runs servo movement and corresponding camera
# Look at parallel running of IMU code

input = 'N'
# Servo Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm=GPIO.PWM(11, 50)
angle = 0
# Load Cell Setup
referenceUnit = 210.05
hx = HX711(29, 31)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
weight = 0
# IMU Setup
mpu = mpu6050(0x68)
# Camera Setup
image = 0
camera = PiCamera()

def Initialisation():
    # Servo Startup
    pwm.start(2.5)
    sleep(0.5)
    pwm.ChangeDutyCycle(0)
    GPIO.setwarnings(False)
    # Load Cell Setup
    hx.reset()
    hx.tare()
    print("Tare done. Ready for flask")

def SetAngle(angle):
	duty = angle/18 + 2.5
	GPIO.output(11, True)
	pwm.ChangeDutyCycle(duty)
	sleep(0.5)
	GPIO.output(11, False)
	pwm.ChangeDutyCycle(0)

def MeasureWeight():
    val = hx.get_weight(5)
    hx.power_down()
    hx.power_up()
    return val-60

def PrintIMU():
    print("Temp : "+"{:.3f}".format(mpu.get_temp()))
    
    accel_data = mpu.get_accel_data()
    print("Acceleration: X:"+"{:.3f}".format(accel_data['x'])+ ", Y:"+"{:.3f}".format(accel_data['y']) + ", Z:" +"{:.3f}".format(accel_data['z']+12) )

    gyro_data = mpu.get_gyro_data()
    print("Gyroscope: X:"+"{:.3f}".format(gyro_data['x'])+ ", Y:"+"{:.3f}".format(gyro_data['y']) + ", Z:" +"{:.3f}".format(gyro_data['z']))

def CheckIMU():
    gyro_data = mpu.get_gyro_data()
    accel_data = mpu.get_gyro_data()
    if accel_data['x'] or accel_data['y'] or accel_data['z'] >= 1000:
        return 1
    if gyro_data['x'] or gyro_data['y'] or gyro_data['z'] >= 1000:
        return 1
    else:
        return 0

def CameraCapture():
    name = "/home/pi/TRC3000/images/pic"+str(image)+".jpg"
    camera.capture(name)

# Body
try:
    #Initialisation()
    #while input != 'Y':
    #    input = input("Enter Y when sample has been loaded")
    print("Sample weighs: " + MeasureWeight() + "g")
    print("Starting Process")
    while True:
        #if CheckIMU() == 1:
        #    print("Process Stopped: Excessive movement has been detected")
        #    break
        if angle % 30 == 0:
            SetAngle(angle)
            CameraCapture()
        if angle == 180:
            angle = 0
        angle += 3
        sleep(0.1)
except:
    print('Process Stopped')