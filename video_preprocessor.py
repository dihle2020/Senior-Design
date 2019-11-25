import numpy as np    # for mathematical operations
import cv2     # for capturing videos
import math   # for mathematical operations
import os
from keras.preprocessing import image   # for preprocessing the images
import time
from multiprocessing import Process, Queue

NUMBER_FRAMES = 40
FRAMES_PER_SEC = 20
SLEEP_TIME = 1 / FRAMES_PER_SEC

######### Images need to be 224 x 224 x 3 ###########

def run_webcam(q):
  cam = cv2.VideoCapture(0)
  frame_num=1
  while frame_num < NUMBER_FRAMES:
      success,image = cam.read()
      if success:
      
        # Our operations on the image come here
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dimensions = (224, 224)
        gray = cv2.resize(gray, dimensions, interpolation=cv2.INTER_AREA)
        
        # save frame as JPEG file
        cv2.imwrite("%d.jpg" % (frame_num), gray)
        
        # Add resulting frame to Queue for processing on controller
        q.put(gray)     

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      
      frame_num+=1
      time.sleep(SLEEP_TIME)
  # When everything done, release the capture
  cam.release()
  cv2.destroyAllWindows

def run_file(q):
  cam = cv2.VideoCapture('make10.mp4')
  frame_num=1
  success = True
  while success == True:
      success,image = cam.read()
      if success:
        #print("frame: %d" % frame_num)
        # Our operations on the image come here
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dimensions = (224, 224)
        gray = cv2.resize(gray, dimensions, interpolation=cv2.INTER_AREA)
        
        # save frame as JPEG file
        cv2.imwrite("%d.jpg" % (frame_num), gray) 
            
        # Add resulting frame to Queue for processing on controller
        q.put(gray) 

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      frame_num+=1
      time.sleep(SLEEP_TIME)
      
  # When everything done, release the capture
  cam.release()
  cv2.destroyAllWindows
