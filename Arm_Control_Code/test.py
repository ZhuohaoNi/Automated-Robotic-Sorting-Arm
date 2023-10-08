import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels = 16)
servo1 = kit.servo[0]
servo2 = kit.servo[1]
servo3 = kit.servo[2]
servo4 = kit.servo[3]


servo1.angle = 166.15
servo2.angle = 45*1.04348
servo3.angle = 64.8
servo4.angle = 70



# for i in range (0, 12):

#     servo1.angle = 120 - i * 10
#     servo2.angle = 60 + i * 10
# #     servo3.angle = i
# #     servo4.angle = i
# #     print(servo1.angle)

#     time.sleep(0.05)


# for i in range (0, 12):

#     servo1.angle = 120 - i * 10
#     servo2.angle = 60 + i * 10
#     servo3.angle = i
#     servo4.angle = i
#     print(servo1.angle)

    # time.sleep(0.05)
    
