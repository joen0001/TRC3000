from mpu6050 import mpu6050
import time
mpu = mpu6050(0x68)

while True:
    print("Temp : "+"{:.3f}".format(mpu.get_temp()))
    
    accel_data = mpu.get_accel_data()
    print("Acceleration: X:"+"{:.3f}".format(accel_data['x'])+ ", Y:"+"{:.3f}".format(accel_data['y']) + ", Z:" +"{:.3f}".format(accel_data['z']+12) )

    gyro_data = mpu.get_gyro_data()
    print("Gyroscope: X:"+"{:.3f}".format(gyro_data['x'])+ ", Y:"+"{:.3f}".format(gyro_data['y']) + ", Z:" +"{:.3f}".format(gyro_data['z']))
    print("-------------------------------")
    time.sleep(1)