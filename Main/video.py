# code that runs and displays object detection, if recieve signals from flaskapp,
# capture a frame, save to a image file.
import torch
import cv2
import time
import json
from jetson_utils import cudaFromNumpy, saveImageRGBA

# Load the pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')
# Open the webcam using OpenCV
cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")

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

    # check if button is pressed on website (check content of capture.json)
    with open("capture.json", 'r') as f:
        capture = json.load(f)
        if (capture == "calibrate"):
            # write detection to file
            data = results.pandas().xyxy[0].to_json(orient="records")
            data = json.loads(data)

            # capture frame and save to local
            # convert numpy array (from opencv) to cudaiamge, then save as file.jpg
            cuda_mem = cudaFromNumpy(results.render()[0])
            saveImageRGBA("detection.jpg", cuda_mem)
            
            # write detetion data to file
            with open("detection.json", "w") as f2:
                json.dump(data, f2)

            # reset capture signal in capture.json
            with open("capture.json", "w") as f:
                json.dump("nope", f)
