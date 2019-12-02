import tensorflow.keras
from PIL import Image
import numpy as np
import os
import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

BALL_THRESH = .9
NO_BALL_THRESH = .9
N_FRAMES = 1

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)



def open_file_chooser():
    filename = askopenfilename()
    child = tk.Tk()
    child.geometry("500x200")
    child.title("Video Classifer")
    label = tk.Label(child, fg="dark blue")
    label.pack()
    label.config(text=str(filename))
    
    # code goes here
    # Replace this with the path to your image
    frames = []
    # Opens the Video file
    cap= cv2.VideoCapture(filename)
    i=1
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i%N_FRAMES == 0:
            frames.append(frame)
            print("added")
        i+=1
 
    
    frames = np.array(frames)
    print(len(frames))
    cap.release()
    cv2.destroyAllWindows()


    #get video

    #Array to hold every Nth frame of video
    
    #convert video to frames and resize using patricks thing

    #predict frames and store values into data array (returns array of arrays)

    #check confidence level of shot in hoop followed by shot through hoop

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    index = 0
    in_frame = False
   
    for pic in frames:
        # convert image to cv2 format to RGB format
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        image= Image.fromarray(pic)
        # Make sure to resize all images to 224, 224 otherwise they won't fit in the array
        image = image.resize((224,224))

        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array
        prediction = model.predict(data)
        print("frame", index, 'P(ball) = ', prediction[0][0], 'P(no_ball) = ', prediction[0][1])

        if prediction[0][0] >= BALL_THRESH:
            print("There is a ball in frame " + str(index))
        if prediction[0][1] >= NO_BALL_THRESH:
            print("Ball left view on frame" + str(index))
            break # after the ball leaves the frame stop processing
        if prediction [0][0] < BALL_THRESH and prediction[0][1] < NO_BALL_THRESH: 
           print("Not super confident about frame " + str(index))
           
        index+=1


   


# creating an instance of Tk
root = tk.Tk()
root.geometry("300x100")
root.title("Video Classifer")


# Button : Open
open = tk.Button(root, text = "Open and Train", command = open_file_chooser)
open.pack()
label = tk.Label(root, fg="dark green")
label.pack()
label.config(text=str("Please choose a file."))

# Starting the Application
root.mainloop()