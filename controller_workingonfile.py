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
from playsound import playsound


 #Shutterspeed : 1/100
 #Aperture: 4.5
 #Iso: 1600


def main():
    
    loading_start = time.time()

    # Load the model
    ballinframe_model = tensorflow.keras.models.load_model('keras_model_ballinframe.h5', compile=False)
    shotmade_model = tensorflow.keras.models.load_model('thomas_model3.h5', compile=False)
    
    # Create Queue for resource (in this case Image) sharing
    q = Queue()

    # In PRODUCTION, add filename from UI as argument
    # Create Process for preprocessing of images
    pipeline = Process(target=vpp.run_file, args=(q, 'stitch_test5.mp4'))

    # start video preprocessing
    pipeline.start()
        

    iterations = 0
    current_frame = 4
    new_images = []
    
    # Number of Frames to Skip
    skip_ballinframe = 2
    

    # Set up flags for 2-Flag decision system
    above_rim = False
    in_hoop = False
    below_hoop = False
    finished = False
    attempted = False
    in_frame = False
    
    counter = 0

    # Initialize array for ??Storing Normalized Images??
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    print("Controller Loading Duration -> %s seconds ---" % (time.time() - loading_start))

    # check for new images four times a second for 10 seconds
    while True:
        iteration_start = time.time()
        #print("controller: ", iterations)
        
        try:
            frame = q.get(True, 5)
        except:
            if attempted:
                print("From Controller -------------------------------------------------------------------------------> Shot Missed")
                playsound('boo.mp3')
            print("Queue is empty")
            break
        else:
            new_images.append(frame)
            
        if len(new_images) > 0:
            for img in new_images:
                #print(current_frame)
                # Normalize the image
                normalized_image_array = (img.astype(np.float32) / 127.0) - 1  
                
                # Load the image into the array
                data[0] = normalized_image_array 
                         
                # Obtain Ball-In-Frame prediction
                if current_frame % skip_ballinframe == 0:
                    ballinframe_prediction = ballinframe_model.predict(data)[0]
                    #print(ballinframe_prediction)
                    if ballinframe_prediction[0] > 0.95 and counter == 0:
                        in_frame = True
                        attempted = True
                        finished = False
                        counter = 50
                        print("From controller ----------------------------------------------------------------------> Shot attempted")
                if ballinframe_prediction[1] > 0.6:
                    in_frame = False
                    finished = True
                    if attempted:
                        print("From Controller -------------------------------------------------------------------------------> Shot Missed")
                        playsound('boo.mp3')
                ##print(counter)
                if counter > 0:
                    #print(attempted, finished)
                    if attempted and not finished:
                        shotmade_prediction = shotmade_model.predict(data)[0]
                        #print(shotmade_prediction)
                        if shotmade_prediction[2] > 0.5 and not above_rim:
                            above_rim = True
                            pass
                        if shotmade_prediction[0] > 0.5 and above_rim and not in_hoop:
                            in_hoop = True
                            finished = True
                            print("From Controller ----------------------------------------------------------------------------------> Shot Made")
                            playsound('Ding Sound Effect.mp3')
                            pass
                        if shotmade_prediction[1] > 0.5 and above_rim and in_hoop and not below_hoop:
                            below_hoop = True
                            finished = True
                            print("From Controller ----------------------------------------------------------------------------------> Shot Made")
                            playsound('Ding Sound Effect.mp3')
                if not counter == 0:
                    counter -= 1
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
        #print("Controller Iteration Duration -> %s seconds ---" % (time.time() - iteration_start))
        iterations += 1  
    
    
    print("Controller Execution Duration -> %s seconds ---" % (time.time() - loading_start))
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
