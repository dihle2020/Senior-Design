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
    ballinframe_model = tensorflow.keras.models.load_model('keras_model_ballinframe.h5', compile=False)
    shotmade_model = tensorflow.keras.models.load_model('keras_model_shotmade.h5', compile=False)
    
    # Create Queue for resource (in this case Image) sharing
    q = Queue()

    # In PRODUCTION, add filename from UI as argument
    # Create Process for preprocessing of images
    pipeline = Process(target=vpp.run_file, args=(q, 'missmakemake_3.mp4'))

    # start video preprocessing
    pipeline.start()
    
    time.sleep(0.5)
    

    iterations = 0
    current_frame = 1
    new_images = []

    # Set up flags for 2-Flag decision system
    above_rim = False
    in_hoop = False
    below_hoop = False
    finished = False
    shot_made = False
    attempted = False
    in_frame = False
    
    counter = 0

    # Initialize array for ??Storing Normalized Images??
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        
    # check for new images four times a second for 10 seconds
    while True:
        print("------------------------------------------------------")
        print("controller: ", iterations)
        """  #the number of frames to keep
        min_val_to_keep = current_frame - 20 """
        
        try:
            frame = q.get(True, 5)
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
                         
                # Obtain Ball-In-Frame prediction
                ballinframe_prediction = ballinframe_model.predict(data)[0]
                
                print("In frame?: ", ballinframe_prediction)
                if ballinframe_prediction[0] > 0.6 and counter == 0:
                    in_frame = True
                    #if not finished:
                    attempted = True
                    counter = 50
                    print("From controller ----------------------------------------------------------------------> Shot attempted")
                if ballinframe_prediction[1] > 0.5:
                    in_frame = False
                    finished = True
                    if attempted:
                        print("From Controller -------------------------------------------------------------------------------> Shot Missed")
                print(counter)
                if counter > 0:
                    if attempted and not finished:
                        print("Above Rim: ", above_rim) 
                        print("In hoop: ", in_hoop)
                        print("Below Hoop: ", below_hoop)
                        shotmade_prediction = shotmade_model.predict(data)[0]
                        print(shotmade_prediction)
                        if shotmade_prediction[2] > 0.9 and not above_rim:
                            print("above rim")
                            above_rim = True
                            pass
                        if shotmade_prediction[0] > 0.5 and above_rim and not in_hoop:
                            print("in hoop")
                            in_hoop = True
                            pass
                        if shotmade_prediction[1] > 0.9 and above_rim and in_hoop and not below_hoop:
                            below_hoop = True
                            finished = True
                            shot_made = True
                            print("From Controller ----------------------------------------------------------------------------------> Shot Made")
                if not counter == 0:
                    counter -= 1
                """ if ballinframe_prediction[0] > 0.7:
                    if not finished and not attempted:
                        attempted = True
                        print("From controller -------------> Shot attempted")    
                else:
                    print("From Controller ------------- > not in frame")
                    if attempted and not shot_made:
                        print("From Controller ----------------> Shot Missed")
                        finished = True
                        attempted = False
                    if attempted:
                        print("From Controller ---------------> Ball has left screen")
                        print("Shot made: ", shot_made) """
                """ if attempted and not finished:
                    print("Above Rim: ", above_rim)
                    print("In hoop: ", in_hoop)
                    print("Below Hoop: ", below_hoop)
                    shotmade_prediction = shotmade_model.predict(data)[0]
                    print(shotmade_prediction)
                    if shotmade_prediction[2] > 0.9 and not above_rim:
                        print("above rim")
                        above_rim = True
                        pass
                    if shotmade_prediction[0] > 0.9 and above_rim and not in_hoop:
                        print("in hoop")
                        in_hoop = True
                        pass
                    if shotmade_prediction[1] > 0.9 and above_rim and in_hoop and not below_hoop:
                        below_hoop = True
                        finished = True
                        shot_made = True
                        print("From Controller ----------------> Shot Made") """
                if finished:
                    above_rim = False
                    in_hoop = False
                    below_hoop = False
                    attempted = False
                    if not in_frame:
                        finished = False
                    pass
                
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
        #time.sleep(0.4)
        iterations += 1  
    
    
    
    # close Queue
    while not q.empty():
        q.get()
    q.close()
        
    # close video preprocessing
    pipeline.terminate()
    
    

    # clean up directory afterwards
    files = os.listdir('.')
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg':
            os.remove(file)
        
if __name__ == '__main__':
    main()
