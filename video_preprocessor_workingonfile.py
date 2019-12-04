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
  loading_start = time.time()
  cam = cv2.VideoCapture(1)
  frame_num=1
  success = True
  send_frame = 0
  time.sleep(6)
  print("VPP Loading Duration -> %s seconds ---" % (time.time() - loading_start))
  print("FPS: ", cam.get(cv2.CAP_PROP_FPS))
  while success:
    reading_start = time.time()
    success,image = cam.read()
    if success:
        # Our operations on the image come here
        
        # convert image to cv2 format to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        image = Image.fromarray(image)
        image = image.resize((224,224))  
        image_array = np.asarray(image)
            
        # Add resulting frame to Queue for processing on controller
        q.put(image_array) 
        
        image = image.resize((896,896))
        image_array = np.asarray(image)
        # Display the resulting frame
        cv2.imshow('frame', image_array)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

    frame_num+=1
    #print("VPP Iteration Duration -> %s seconds ---" % (time.time() - reading_start))
      
  # When everything done, release the capture
  cam.release()
  cv2.destroyAllWindows()
  print("VPP Execution Duration -> %s seconds ---" % (time.time() - loading_start))

def run_file(q, file):
  cam = cv2.VideoCapture(file)
  frame_num=1
  time.sleep(1)
  success = True
  while success == True:
      success,image = cam.read()
      if success:
        # Our operations on the image come here
        
        # convert image to cv2 format to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        image = Image.fromarray(image)
        image = image.resize((224,224))  
        image_array = np.asarray(image)
            
        # Add resulting frame to Queue for processing on controller
        q.put(image_array) 
        
        # Display the resulting frame
        cv2.imshow('frame', image_array)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
        time.sleep(0.033) 

      frame_num+=1
      
  # When everything done, release the capture
  cam.release()
  cv2.destroyAllWindows()
