import Arm
import time
from adafruit_servokit import ServoKit
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
import busio

if __name__ == "__main__":

    while True:
        i2c_bus = busio.I2C(SCL, SDA)
        pca = PCA9685(i2c_bus)
        pca.frequency = 1526
        pca.channels[11].duty_cycle = 0xffff
    # kit = ServoKit(channels=16)
    # mag = kit.servo[11]
    #     mag.angle = 0

    #     print("start")
    #     pwm = adafruit_pca9685.PCA9685()
    #     pwm.set_pwm(6, 0, 4095)