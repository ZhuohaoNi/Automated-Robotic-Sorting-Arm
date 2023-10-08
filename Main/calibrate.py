# Process signals if "calibrate" pressed on web
import time
from Arm import Shoulder, Elbow, Wrist, Base
import json


class calibrate_run:
    def run_calibrate():
        # Initialize the servo motors
        shoulder = Shoulder(65)
        elbow = Elbow(90)
        wrist = Wrist(90)
        time.sleep(1)
        base = Base(90)

        # Set the servo angles to 90 degrees
        time.sleep(1)
        shoulder.set_angle_conv(65)
        elbow.set_angle_conv(125)
        wrist.set_angle_conv(90)
        
        time.sleep(3)
        # save "calibrate" to file, as a signal for other processes
        capture = "calibrate"
        with open('capture.json', 'w') as f:
            json.dump(capture, f)