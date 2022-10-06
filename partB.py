from picamera import PiCamera
import time
from time import sleep
import RPi.GPIO as GPIO
import smbus
from Kalman import KalmanAngle
import sys, math
from hx711 import HX711

# File to Initialise all modules
# Runs servo movement and corresponding camera
# Look at parallel running of IMU code

# Servo Setup
GPIO.setwarnings(False)
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
kalmanX = KalmanAngle()
kalmanY = KalmanAngle()
RestrictPitch = True
radToDeg = 57.2957786
kalAngleX = 0
kalAngleY = 0
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
# Camera Setup
image = 0
camera = PiCamera()

def Initialisation():
    # Servo Startup
    pwm.start(2.5)
    sleep(0.5)
    pwm.ChangeDutyCycle(0)
    # Load Cell Setup
    hx.reset()
    hx.tare()
    print("Servo Set to position 0\nTare done. Ready for flask")
    # IMU Setup
    MPU_Init()

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

def MPU_Init():
	#write to sample rate register
    bus.write_byte_data(DeviceAddress, SMPLRT_DIV, 7)

	#Write to power management register
    bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)

	#Write to Configuration register
	#Setting DLPF (last three bit of 0X1A to 6 i.e '110' It removes the noise due to vibration.) https://ulrichbuschbaum.wordpress.com/2015/01/18/using-the-mpu6050s-dlpf/
    bus.write_byte_data(DeviceAddress, CONFIG, int('0000110',2))

	#Write to Gyro configuration register
    bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)

	#Write to interrupt enable register
    bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)
    accX = read_raw_data(ACCEL_XOUT_H)
    accY = read_raw_data(ACCEL_YOUT_H)
    accZ = read_raw_data(ACCEL_ZOUT_H)
    if (RestrictPitch):
        roll = math.atan2(accY,accZ) * radToDeg
        pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
    else:
        roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
        pitch = math.atan2(-accX,accZ) * radToDeg
    kalmanX.setAngle(roll)
    kalmanY.setAngle(pitch)


def read_raw_data(addr):
        #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(DeviceAddress, addr)
        low = bus.read_byte_data(DeviceAddress, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

def IMU_Reading(timer):
    try:
        accX = read_raw_data(ACCEL_XOUT_H)
        accY = read_raw_data(ACCEL_YOUT_H)
        accZ = read_raw_data(ACCEL_ZOUT_H)

	    #Read Gyroscope raw value
        gyroX = read_raw_data(GYRO_XOUT_H)
        gyroY = read_raw_data(GYRO_YOUT_H)
        gyroZ = read_raw_data(GYRO_ZOUT_H)

        dt = time.time() - timer
        timer = time.time()

        if (RestrictPitch):
            roll = math.atan2(accY,accZ) * radToDeg
            pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
        else:
            roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
            pitch = math.atan2(-accX,accZ) * radToDeg
        gyroXRate = gyroX/131
        gyroYRate = gyroY/131
        gyroXAngle = roll
        gyroYAngle = pitch
        compAngleX = roll
        compAngleY = pitch 

        if (RestrictPitch):

            if((roll < -90 and kalAngleX >90) or (roll > 90 and kalAngleX < -90)):
                kalmanX.setAngle(roll)
                complAngleX = roll
                kalAngleX   = roll
                gyroXAngle  = roll
            else:
                kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

            if(abs(kalAngleX)>90):
                gyroYRate  = -gyroYRate
                kalAngleY  = kalmanY.getAngle(pitch,gyroYRate,dt)
        else:
            if((pitch < -90 and kalAngleY >90) or (pitch > 90 and kalAngleY < -90)):
                kalmanY.setAngle(pitch)
                complAngleY = pitch
                kalAngleY   = pitch
                gyroYAngle  = pitch
            else:
                kalAngleY = kalmanY.getAngle(pitch,gyroYRate,dt)

            if(abs(kalAngleY)>90):
                gyroXRate  = -gyroXRate
                kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)
        print('1')
		#angle = (rate of change of angle) * change in time
        gyroXAngle = gyroXRate * dt
        gyroYAngle = gyroYAngle * dt
        print('2')
		#compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
        compAngleX = 0.93 * (compAngleX + gyroXRate * dt) + 0.07 * roll
        compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch
        print('3')
        if ((gyroXAngle < -180) or (gyroXAngle > 180)):
            gyroXAngle = kalAngleX
        if ((gyroYAngle < -180) or (gyroYAngle > 180)):
            gyroYAngle = kalAngleY
        print('4')
        A_x = accX/16384.0
        A_y = accX/16384.0
        A_z = accX/16384.0
        print('5')
        return kalAngleX-180,kalAngleY,gyroZ,A_x,A_y,A_z
    except Exception as exc:
        flag += 1

def CameraCapture(image):
    name = "/home/pi/TRC3000/images/pic"+str(image)+".jpg"
    camera.capture(name)

# Body Loop
try:
    bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
    DeviceAddress = 0x68
    timer = time.time()
    Initialisation()
    input = input("Enter Y when sample has been loaded")
    while input != 'Y':
        input = input("Enter Y when sample has been loaded\n")
    print("Sample weighs: "+str(MeasureWeight())+"g")
    print("Starting Process")
    i = 0

    max_G_x = 0
    max_G_y = 0
    max_R_z = 0
    max_A_x = 0
    max_A_y = 0
    max_A_z = 0

    while i < 2:
        G_x,G_y,R_z,A_x,A_y,A_z = IMU_Reading(timer)
        print('fin')
        if max_G_x < G_x:
            max_G_x = G_x
        if max_G_y < G_y:
            max_G_y = G_y
        if max_R_z < R_z:
            max_R_z = R_z   
        if max_A_x < A_x:
            max_A_x = A_x
        if max_A_y < A_y:
            max_A_y = A_y
        if max_A_z < A_z:
            max_A_z = A_z

        if angle % 30 == 0:
            SetAngle(angle)
        
        if angle == 180:
            angle = 0
            i += 1
        angle += 3
        sleep(0.1)
    
    print('Maximum Tilt in X: ' + str(max_G_x))
    print('Maximum Tilt in Y: ' + str(max_G_y))
    print('Maximum Rotation Acceleration in Z axis: ' + str(max_R_z))
    print('Maximum Acceleration in X: ' + str(max_A_x))
    print('Maximum Acceleration in Y: ' + str(max_A_y))
    print('Maximum Acceleration in Z: ' + str(max_A_z))
except:
    print('Process Stopped: Interrupted')