import numpy as np    # for mathematical operations
import cv2     # for capturing videos
import math   # for mathematical operations
import os
from keras.preprocessing import image   # for preprocessing the images
import time
from multiprocessing import Process, Queue
from PIL import Image


NUMBER_FRAMES = 40
FRAMES_PER_SEC = 5
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

def run_file(q, file):
  cam = cv2.VideoCapture(file)
  frame_num=1
  success = True
  while success == True:
      success,image = cam.read()
      #print("From vpp ----------> success = ", success)
      if success:
        print("vpp frame: %d" % frame_num)
        # Our operations on the image come here
        
        # convert image to cv2 format to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #img = cv2.resize(image, (448, 448), interpolation=cv2.INTER_AREA)
        
        image = Image.fromarray(image)
        image = image.resize((224,224))  
        image_array = np.asarray(image)
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #dimensions = (224, 224)
        
        
        # save frame as JPEG file
        #cv2.imwrite("%d.jpg" % (frame_num), gray)
        #cv2.imwrite("%d.jpg" % (frame_num), image) 
            
        # Add resulting frame to Queue for processing on controller
        q.put(image_array) 
        
        image = image.resize((448,448))  
        image_array = np.asarray(image)
        
        # Display the resulting frame
        cv2.imshow('frame', image_array)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
        """ if frame_num % 2 == 0:"""
        time.sleep(0.033) 

      frame_num+=1
      
  # When everything done, release the capture
  cam.release()
  cv2.destroyAllWindows()
