#Thomas McDonald
#Data Augmentor
# sources:  https://towardsdatascience.com/image-augmentation-examples-in-python-d552c26f2873
#           https://www.kaggle.com/chris471/basic-brightness-augmentation
#           https://www.wouterbulten.nl/blog/tech/data-augmentation-using-tensorflow-data-dataset/
from PIL import Image
import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2
import os
from os import path 

# Folder of images to be augmented
ADDRESS = './throughNet'
ADDRESS_FLIPPED = ADDRESS + '-flipped'
ADDRESS_SHIFT_LEFT = ADDRESS + '-shift_left'
ADDRESS_SHIFT_RIGHT = ADDRESS + '-shift_right'
ADDRESS_NOISE = ADDRESS + '-noise'
ADDRESS_BRIGHT = ADDRESS + '-bright'
ADDRESS_COLORS = ADDRESS + '-colors'

# Height and width of images
HEIGHT = 224
WIDTH = 224



try: 
    os.mkdir(ADDRESS_FLIPPED)
except OSError:
    print("couldnt create folder")
try: 
    os.mkdir(ADDRESS_NOISE)
except OSError:
    print("couldnt create folder")
try: 
    os.mkdir(ADDRESS_BRIGHT)
except OSError:
    print("couldnt create folder")
try: 
    os.mkdir(ADDRESS_COLORS)
except OSError:
    print("couldnt create folder")

for filename in os.listdir(ADDRESS):
    if filename.endswith(".jpg"):
        print(filename)
        img = Image.open(ADDRESS + '/' + filename)
        img = np.array(img)

        # Flipping images with Numpy
        if(not path.exists(ADDRESS_FLIPPED+ '/' + filename)):
            flipped_img = np.fliplr(img)
            flipped_img = Image.fromarray(flipped_img)
            flipped_img.save(ADDRESS_FLIPPED+ '/' + filename)
        
        # Decided to not use this since we were shifting the camera angle manually
        """# Shifting Left
        if(not path.exists(ADDRESS_SHIFT_LEFT+ '/' + filename)):
            left_img = img
            for i in range(HEIGHT, 1, -1):
                for j in range(WIDTH):
                    if (i < HEIGHT-20):
                        left_img[j][i] = img[j][i-20]
                    elif (i < HEIGHT-1):
                        left_img[j][i] = 0
            left_img = Image.fromarray(left_img)
            left_img.save(ADDRESS_SHIFT_LEFT+ '/' + filename)"""
        # ADDING NOISE
        if(not path.exists(ADDRESS_NOISE+ '/' + filename)):
            noise_img = img
            noise = np.random.randint(5, size = (HEIGHT, WIDTH,1), dtype = 'uint8')
            for i in range(WIDTH):
                for j in range(HEIGHT):
                    for k in range(1):
                        if (noise_img[i][j][k] != 255):
                            noise_img[i][j][k]+= noise[i][j][k]
            noise_img = Image.fromarray(noise_img)
            noise_img.save(ADDRESS_NOISE+ '/' + filename)

        #Adding Brightness
        if(not path.exists(ADDRESS_BRIGHT+ '/' + filename)):
            factor=0.5
            hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV) #convert to hsv
            hsv = np.array(hsv, dtype=np.float64)
            hsv[:, :, 2] = hsv[:, :, 2] * (factor + np.random.uniform()) #scale channel V uniformly
            hsv[:, :, 2][hsv[:, :, 2] > 255] = 255 #reset out of range values
            bright_img = cv2.cvtColor(np.array(hsv, dtype=np.uint8), cv2.COLOR_HSV2RGB)
            bright_img = Image.fromarray(bright_img)
            bright_img.save(ADDRESS_BRIGHT+ '/' + filename)

        #Adding random hues, brightness, contrast, and saturations.
        if(not path.exists(ADDRESS_COLORS+ '/' + filename)):
            colored_img = tf.image.random_hue(img, .08)
            colored_img = tf.image.random_saturation(colored_img, 0.6, 1.6)
            colored_img = tf.image.random_brightness(colored_img, 0.05)
            colored_img = tf.image.random_contrast(colored_img, 0.7, 1.3)
            colored_img = colored_img.numpy()
            colored_img = Image.fromarray(colored_img)
            colored_img.save(ADDRESS_COLORS+ '/' + filename)
        
                    