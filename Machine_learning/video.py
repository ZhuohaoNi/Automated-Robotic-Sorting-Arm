import torch
# from flask import Flask, render_template, Response
import cv2
import time
import sys
sys.path.insert(0, '/home/nvidia/P2_L2B_G8/Arm Control Code/')
import time
from Arm import Shoulder, Elbow, Wrist



class calibrate_run:
    capture = False
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


sys.path.insert(0, '/home/nvidia/P2_L2B_G8/Arm Control Code/')
# from calibrate import capture

# Load the pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', '/home/nvidia/P2_L2B_G8/Machine Learning/best.pt')

# Open the webcam using OpenCV
cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")
past = time.time()

# Loop over each frame in the video file
while cap.isOpened():
    # Read the next frame from the video file
    ret, frame = cap.read()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Perform object detection on the current frame using the YOLOv5 model
        results = model(frame)

        # Draw bounding boxes around the detected objects
        results.render()

        # Display the results
        cv2.imshow('Object Detection', cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR))

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

    if (calibrate_run.capture is True):
        print("capture")
        print(results.pandas().xyxy[0])
        calibrate_run.capture = False

# Release the video file and output video file
cap.release()
# out.release()

# Close all windows
cv2.destroyAllWindows()