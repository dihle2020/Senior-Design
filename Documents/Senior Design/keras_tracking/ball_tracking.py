import cv2     # for capturing videos
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
import os
import pandas as pd
from keras.preprocessing import image   # for preprocessing the images
from keras.applications.vgg16 import preprocess_input
import numpy as np    # for mathematical operations
from keras.utils import np_utils
from skimage.transform import resize   # for resizing images



data = pd.read_csv('frame_data.csv')     # reading the csv file
print(data.head())      # printing first five rows of the file

directory="C:/Users/David/Documents/Senior Design/keras_tracking/shot_images/all_shots/made/"

Makes = [ ]     # creating an empty array
for img_name in os.listdir(directory):
    print(img_name)
    img = plt.imread(directory + img_name)
    Makes.append(img)  # storing each image of the made basket samples
    
Makes = np.array(Makes)    # converting list to array

# We now have an array Makes that contains all of the 425 images from made basket clips
print("NOW ADDING THE MISSES -------------------------------------------------")
directory="C:/Users/David/Documents/Senior Design/keras_tracking/shot_images/all_shots/missed/"

Misses = [ ]     # creating an empty array
for img_name in os.listdir(directory):
    print(img_name)
    img = plt.imread(directory + img_name)
    Misses.append(img)  # storing each image of the made basket samples
    
Misses = np.array(Misses)    # converting list to array


y = data.ball_thru_hoop
dummy_y = np_utils.to_categorical(y)    # one hot encoding Classes

# -------------------- resize our made basket images  to fit VGG16 pretrained model (224 X 224 X 3)---------

image = []
for i in range(0,Makes.shape[0]):
    a = resize(Makes[i], preserve_range=True, output_shape=(224,224)).astype(int)      # reshaping to 224*224*3
    image.append(a)

for j in range(0,Misses.shape[0]):
    a = resize(Misses[j], preserve_range=True, output_shape=(224,224)).astype(int)      # reshaping to 224*224*3
    image.append(a)

final_pics = np.array(image)
print("done!")


print("Preprocessing input data for VGG16 algorithm")
final_pics = preprocess_input(final_pics, mode='tf')      # preprocessing the input data

print(final_pics.shape)
print(dummy_y.shape)

from sklearn.model_selection import train_test_split
Makes_train, Makes_valid, y_train, y_valid = train_test_split(final_pics, dummy_y, test_size=0.3, random_state=42)    # preparing the validation set







#------------------------------------BUILDING THE MODEL ----------------------
from keras.models import Sequential
from keras.applications.vgg16 import VGG16
from keras.layers import Dense, InputLayer, Dropout

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))    # include_top=False to remove the top layer

Makes_train = base_model.predict(Makes_train)
Makes_valid = base_model.predict(Makes_valid)
Makes_train.shape, Makes_valid.shape

print(Makes_train.shape)
print(Makes_valid.shape)


Makes_train = Makes_train.reshape(574, 7*7*512)      # converting to 1-D
Makes_valid = Makes_valid.reshape(246, 7*7*512)

train = Makes_train/Makes_train.max()      # centering the data
Makes_valid = Makes_valid/Makes_train.max()


# i. Building the model
model = Sequential()
model.add(InputLayer((7*7*512,)))    # input layer
model.add(Dense(units=1024, activation='sigmoid')) # hidden layer
model.add(Dense(2, activation='softmax'))    # output layer

model.summary()

# ii. Compiling the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# iii. Training the model
model.fit(train, y_train, epochs=10, validation_data=(Makes_valid, y_valid))


#------------------------ TESTING THE DATA ----------------------
directory="C:/Users/David/Documents/Senior Design/keras_tracking/shot_images/test_shots/"


test = pd.read_csv('test_shot.csv')

test_image = []
for img_name in os.listdir(directory):
    img = plt.imread(directory + img_name)
    test_image.append(img)
test_img = np.array(test_image)

test_image = []
for i in range(0,test_img.shape[0]):
    a = resize(test_img[i], preserve_range=True, output_shape=(224,224)).astype(int)
    test_image.append(a)
test_image = np.array(test_image)
print(test_image.shape)
# preprocessing the images
test_image = preprocess_input(test_image, mode='tf')

# extracting features from the images using pretrained model
test_image = base_model.predict(test_image)

# converting the images to 1-D form
test_image = test_image.reshape(69, 7*7*512)

# zero centered images
test_image = test_image/test_image.max()

predictions = model.predict_classes(test_image)

print("The number of frames after made basket", predictions[predictions==1].shape[0], "frames")
print("Number of frames not through basket", predictions[predictions==0].shape[0], "frames")