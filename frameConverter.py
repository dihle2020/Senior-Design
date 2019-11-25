

import tensorflow.keras
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2
import os

ADDRESS = 'C:/Users/Thoma/Videos/shot detection'

i=0
for filename in os.listdir(ADDRESS):
    if filename.endswith(".mp4")and filename.startswith('r'): 
        print(filename)
        cap= cv2.VideoCapture(ADDRESS + '/'+(filename))
        f=0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            pic = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image= Image.fromarray(pic)
            # Make sure to resize all images to 224, 224 otherwise they won't fit in the array
            image = image.resize((224,224))
            if(f==0):
                print('MissedFrames/r'+ str(i)+'-'+str(f)+'.jpg')
            image.save('MissedFrames/r'+ str(i)+'-'+str(f)+'.jpg')
            f+=1
        cap.release()
        print('added folder')
    i+=1
 