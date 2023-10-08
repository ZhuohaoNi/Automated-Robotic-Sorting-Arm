import time
from Arm import Shoulder, Elbow, Wrist
import json
import capture.json


class calibrate_run:
    def run_calibrate():
        # Initialize the servo motors
        shoulder = Shoulder(0)
        elbow = Elbow(90)
        wrist = Wrist(90)

        # Set the servo angles to 90 degrees
        shoulder.set_angle_conv(90)
        elbow.set_angle_conv(90)
        wrist.set_angle_conv(90)
        capture = True
        with open('capture.json', 'w') as f:
            json.dump(capture, f)