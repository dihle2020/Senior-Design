import cv2     # for capturing videos
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
import os
import pandas as pd
from keras.preprocessing import image   # for preprocessing the images
import numpy as np    # for mathematical operations
from keras.utils import np_utils
from skimage.transform import resize   # for resizing images

shot_num=1
while shot_num < 11:
    count = 0
    vidcap = cv2.VideoCapture('Shot Data\miss%d.mp4' % shot_num)

    success,image = vidcap.read()
    count = 0
    success = True
    while success:
      cv2.imwrite("miss%d_frame%d.jpg" % (shot_num, count), image)     # save frame as JPEG file
      success,image = vidcap.read()
      print ('Read a new frame: '), success
      count += 1

    shot_num+=1

shot_num=1
while shot_num < 11:
    count = 0
    vidcap = cv2.VideoCapture('Shot Data\make%d.mp4' % shot_num)

    success,image = vidcap.read()
    count = 0
    success = True
    while success:
      cv2.imwrite("make%d_frame%d.jpg" % (shot_num, count), image)     # save frame as JPEG file
      success,image = vidcap.read()
      print ('Read a new frame: '), success
      count += 1

    shot_num+=1

