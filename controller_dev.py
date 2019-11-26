import video_preprocessor as vpp
from multiprocessing import Process, Queue, Event
import os
import time
import cv2
import model_sim    # Used to simulate true/false values returned from model ## REMOVE THIS CALL FOR PRODUCTION USE
import tensorflow
from tensorflow import keras
import numpy as np
from PIL import Image


 


def main():
    

    # Load the model
    model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)
    
    # Create Queue for resource (in this case Image) sharing
    q = Queue()

    # In PRODUCTION, add filename from UI as argument
    # Create Process for preprocessing of images
    pipeline = Process(target=vpp.run_file, args=(q, 'make10.mp4'))

    # start video preprocessing
    pipeline.start()
    
    time.sleep(2)
    

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
    finished = False

    # Initialize array for ??Storing Normalized Images??
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        
    # check for new images four times a second for 10 seconds
    while True:
        print(iterations)
        """  #the number of frames to keep
        min_val_to_keep = current_frame - 20 """
        
        try:
            frame = q.get(False)
        except:
            print("Queue is empty")
            break
        else:
            new_images.append(frame)
            
        if len(new_images) > 0:
            for img in new_images:
                
                # Normalize the image
                normalized_image_array = (img.astype(np.float32) / 127.0) - 1  
                
                # Load the image into the array
                data[0] = normalized_image_array 
                         
                # This is where processing would occur.  Here however we simply get a random boolean back from model_sim testing module
                # For implementation, replace the model_sim with the actual model call to davids model
                if model_sim.ballInFrame(img):
                    if not shot_attempted:
                        print("From Model -----------------------> Shot attempted")
                    in_frame = True
                    shot_attempted = True
                    if model.predict(data)[0][0] > 0.3:
                        if in_hoop:
                            shot_made = True                            
                        else:
                            print("I think a shot was made, let me double check")
                            in_hoop = True
                    else: 
                        if in_hoop:
                            print("Nevermind...")
                        in_hoop = False
                else: 
                    in_frame = False
                        
                if shot_attempted and not in_frame:
                    print("From Model -----------------------> Shot missed")
                    shot_attempted = False
                    finished = True
                    break
                    
                    
                if shot_made:
                    print("From Model -----------------------> Shot made")
                    in_hoop = False
                    shot_made = False
                    shot_attempted = False
                    finished = True
                    break
                current_frame += 1
            if finished:
                finished = False
                pass
        new_images = []
        
        #Remove the frames that are too old to keep
        """ files = os.listdir()
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.jpg':
                framenum = int(filename)
                if framenum < min_val_to_keep:
                    os.remove(file) """
        time.sleep(0.6)
        iterations += 1  
    
    
    
    # close Queue
    while not q.empty():
        q.get()
    q.close()
        
    # close video preprocessing
    pipeline.terminate()
    #pipeline.join()
    
    

    # clean up directory afterwards
    files = os.listdir('.')
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg':
            os.remove(file)
        
if __name__ == '__main__':
    main()
