'''
Here we are trying to automatically split up a video into its individual frames and predict based 
on our google model.  Select video through our tkinter GUI
'''


import tensorflow.keras
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import cv2



ALPHA = .75
N_FRAMES = 5

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)


# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)



#global filename 
# defining open_file_chooser function
def open_file_chooser():
    filename = askopenfilename()
    child = tk.Tk()
    child.geometry("500x200")
    child.title("Video Classifer")
    label = tk.Label(child, fg="dark green")
    label.pack()
    label.config(text=str(filename))
    label2 = tk.Label(child, fg="dark blue",font=("Helvetica", 32))
    label2.pack()
    label2.config(text=str("Results:"))
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
    #image = Image.open(filename)

    #Array to hold every Nth frame of video
    
    #convert video to frames and resize using patricks thing

    #predict frames and store values into data array (returns array of arrays)

    #check confidence level of shot in hoop followed by shot through hoop

    for pic in frames:
        # Make sure to resize all images to 224, 224 otherwise they won't fit in the array
        new_pic = np.resize(pic, (224, 224,3))
        image_array = np.asarray(new_pic)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        print(prediction[0])
        print(prediction[0][0])

   
   
    #if statesments to replace results with actual guess
    label2.config(text=str("Results:"))



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















# --------------------------------------------------------------------------------

