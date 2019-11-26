import video_preprocessor as vpp
from multiprocessing import Process, Queue
import os
import time
import cv2
import model_sim    # Used to simulate true/false values returned from model ## REMOVE THIS CALL FOR PRODUCTION USE
import tensorflow
from tensorflow import keras
import numpy as np
from PIL import Image


 


def main():
    
    ALPHA = .75
    N_FRAMES = 1

    # Load the model
    model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)
    
    # Create Queue for resource (in this case Image) sharing
    q = Queue()


    # In PRODUCTION, add filename from UI as argument
    # Create Process for preprocessing of images
    pipeline = Process(target=vpp.run_file, args=(q, 'make10.mp4'))

    # start video preprocessing
    pipeline.start()

    # In production, this is where work will be done
    # For now, just lists the files in the directory as they come in

    iterations = 0
    current_frame = 1
    new_images = []

    # Set up flags for 2-Flag decision system
    shot_made = False
    shot_attempted = False
    in_hoop = False
    in_frame = False

    # Initialize array for ??Storing Normalized Images??
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    # check for new images four times a second for 10 seconds
    while iterations < 20:
        
        """  #the number of frames to keep
        min_val_to_keep = current_frame - 20 """
        
        frame = q.get()
        print("get")
        if frame is not None:
            new_images.append(frame)
        else: 
            exit()
        if len(new_images) > 0:
            for img in new_images:
                image = Image.fromarray(img)
                image = image.resize((224,224))  
                image_array = np.asarray(image)

                # Normalize the image
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1            
                # This is where processing would occur.  Here however we simply get a random boolean back from model_sim testing module
                # For implementation, replace the model_sim with the actual model calls
                if model_sim.ballInFrame(img):
                    if not shot_attempted:
                        print("Shot attempted")
                    in_frame = True
                    shot_attempted = True
                    if model.predict(img):
                        if in_hoop:
                            shot_made = True
                            break
                        else:
                            in_hoop = True
                    else: 
                        in_hoop = False
                else: 
                    in_frame = False
                        
                if shot_attempted and not in_frame:
                    print("Shot missed")
                    shot_attempted = False
                    
                if shot_made:
                    print("Shot made")
                    in_hoop = False
                    shot_made = False
                    shot_attempted = False
                
                current_frame += 1
        new_images = []
        
        #Remove the frames that are too old to keep
        """ files = os.listdir()
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.jpg':
                framenum = int(filename)
                if framenum < min_val_to_keep:
                    os.remove(file) """
        time.sleep(0.1)
        iterations += 1  
    
    
        
    # close video preprocessing
    pipeline.join()
    
    # close Queue
    while not q.empty():
        q.get()
    q.close()

    # clean up directory afterwards
    files = os.listdir('.')
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg':
            os.remove(file)
        
if __name__ == '__main__':
    main()
