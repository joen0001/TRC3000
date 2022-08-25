from mpu6050 import mpu6050
import time
mpu = mpu6050(0x68)

while True:
    print("Temp : "+str(mpu.get_temp()))
    print()

    accel_data = mpu.get_accel_data()
    print("Acceleration: X:"+str(accel_data['x'])+ ", Y:"+str(accel_data['y']) + ", Z:" +str(accel_data['z']) )

    gyro_data = mpu.get_gyro_data()
    print("Gyroscope: X:"+str(gyro_data['x'])+ ", Y:"+str(gyro_data['y']) + ", Z:" +str(gyro_data['z']))
    print("-------------------------------")
    time.sleep(1)