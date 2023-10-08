import sys
import threading
import traceback
from jetson_utils import videoSource, videoOutput, cudaFromNumpy, saveImageRGBA
import torch
import cv2
import time
import numpy as np
class Stream(threading.Thread):
    """
    Thread for streaming video and applying DNN inference
    """
    def __init__(self, args):
        super().__init__()
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', '/home/nvidia/P2_L2B_G8/Main/best.pt')
        self.args = args
        self.cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")
        self.output = videoOutput(args.output, argv=sys.argv)
        self.frames = 0

    def process(self):
        # Read the next frame from the video file
        ret, frame = self.cap.read()

        if (ret is not True):
            print("capture failed")
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform object detection on the current frame using the YOLOv5 model
        results = self.model(frame)

        # # Display the results
        # frame_conv = cv2.cvtColor(results.render()[0], cv2.COLOR_RGB2BGR)
        # cv2.imshow("Object detection", frame_conv)

        cuda_mem = cudaFromNumpy(results.render()[0])
        self.output.Render(cuda_mem)


        if self.frames % 25 == 0 or self.frames < 15:
            print(f"captured {self.frames} frames from /dev/video0 => {self.args.output} ({cuda_mem.width} x {cuda_mem.height})")
            saveImageRGBA("test1.jpg", cuda_mem)
        #     print(results.pandas.xyxy[0])
   
        self.frames += 1
        
    def run(self):
        # Run the stream processing thread's main loop.
        while True:
            try:
                self.process()
            except:
                traceback.print_exc()
                
    @staticmethod
    def usage():
        return videoSource.Usage() +videoOutput.Usage() 
