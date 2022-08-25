from mpu6050 import mpu6050
import time, math
mpu = mpu6050(0x68)

while True:
    print("Temp : "+str(mpu.get_temp()))
    print()

    accel_data = mpu.get_accel_data()
    print("Acceleration: X:"+str(math.floor(accel_data['x']))+ ", Y:"+str(math.floor(accel_data['y'])) + ", Z:" +str(math.floor(accel_data['z']+12)))

    gyro_data = mpu.get_gyro_data()
    print("Gyroscope: X:"+str(math.floor(gyro_data['x']))+ ", Y:"+str(math.floor(gyro_data['y'])) + ", Z:" +str(math.floor(gyro_data['z'])))
    print("-------------------------------")
    time.sleep(1)