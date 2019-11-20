import numpy as np    # for mathematical operations
import cv2     # for capturing videos
import math   # for mathematical operations
import os
from keras.preprocessing import image   # for preprocessing the images
import time



######### Images need to be 224 x 224 x 3 ###########

def run():
  cam = cv2.VideoCapture(0)
  shot_num=1
  print("Starting...")
  while shot_num < 10:
      success,image = cam.read()
      print ('Read a new frame: '), success
      # Our operations on the image come here
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      
      cv2.imwrite("miss%d_frame%d.jpg" % (shot_num, 0), gray)     # save frame as JPEG file


      # Display the resulting frame
      cv2.imshow('frame',gray)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      shot_num+=1
      time.sleep(1)
  # When everything done, release the capture
  cam.release()
  cv2.destroyAllWindows
