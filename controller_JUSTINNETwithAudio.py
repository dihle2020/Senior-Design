import video_preprocessor as vpp
from multiprocessing import Process, Queue, Event
import os
import time
import cv2
import tensorflow
from tensorflow import keras
import numpy as np
from PIL import Image
from playsound import playsound
import random
#folder and files that are selected for the audio tracks
fileName = 'labeled_audio/'
positiveSoundLabeled =['pos_short','pos_med','pos_long']
neutralSoundLabeled =['net_short','net_med','net_long']
negativeSoundLabeled =['neg_short','neg_med','neg_long']



 #Shutterspeed : 1/320
 #Aperture: 4.5
 #Iso: 1250


#Decision logic to select the track being used
#makes count the number of makes for the three round session
#misses counts the number of missed for three round session
#shot tracks whether current shot is a make or missed
#1 being for made and 0 for missed
def trackSelector(makes, misses , shot):
    #plays background track
    clip = fileName + 'background.mp3'
    #print('playing background noise.')

    # all positive shots
    playsound(clip,False)
    if (makes == 1 and misses == 0 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        #plays clip
        playsound(clip,False)
        #returns the makes and miss to pass between functions
        return makes, misses
    elif (makes == 2 and misses == 0 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        return makes, misses
    elif( makes == 3 and misses == 0 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        #resets for depth of three decision treee
        makes = 0
        misses = 0
        return makes, misses

    #combination of middle of tree
    elif( makes == 1 and misses == 1 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        return makes, misses
    elif( makes == 1 and misses == 1 and shot == 0):
        clip = fileName +negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        return makes, misses
    elif (makes == 2 and misses == 1 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses
    elif (makes == 2 and misses == 1 and shot == 0):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses
    elif (makes ==1 and misses == 2 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses
    elif (makes == 1 and misses == 2 and shot == 0):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses
    # all negative sounds
    elif (makes == 0 and misses == 1 and shot == 1):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        return makes, misses
    elif (makes == 0 and misses == 2 and shot == 0):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        return makes, misses
    elif( makes == 0 and misses == 3 and shot == 0):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        #print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses


def main():
    
    loading_start = time.time()

    # Load the model
    ballinframe_model = tensorflow.keras.models.load_model('../rfc_frame_model/ball_in_frame_everything.h5', compile=False)
    shotmade_model = tensorflow.keras.models.load_model('../rfc_shot_model/binarymakemiss_jc.h5', compile=False)
    
    # Create Queue for resource (in this case Image) sharing
    q = Queue()

    # In PRODUCTION, add filename from UI as argument
    # Create Process for preprocessing of images
    pipeline = Process(target=vpp.run_file, args=(q,'../test_clips/happypath2.mp4'))

    # start video preprocessing
    pipeline.start()
        

    iterations = 0
    current_frame = 4
    new_images = []
    
    # Number of Frames to Skip
    skip_ballinframe = 1
    

    # Set up flags for 2-Flag decision system
    finished = False
    attempted = False
    in_frame = False
    
    #shot flags for audio
    makes = 0
    misses = 0
    
    counter = 0

    # Initialize array for ??Storing Normalized Images??
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    print("Controller Loading Duration -> %s seconds ---" % (time.time() - loading_start))

    # check for new images four times a second for 10 seconds
    while True:
        iteration_start = time.time()
        #print("controller: ", iterations)
        
        try:
            frame = q.get(True, 8)
        except:
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
                    if ballinframe_prediction[0] == 1.0 and counter == 0:
                        in_frame = True
                        attempted = True
                        finished = False
                        counter = 45
                        print("From controller ----------------------------------------------------------------------> Shot attempted")
                    if ballinframe_prediction[1] > 0.5:
                        in_frame = False
                        finished = True
                        if attempted:
                            print("From Controller -------------------------------------------------------------------------------> Shot Missed")
                            makes, misses = trackSelector(makes,misses,0)
                #print(counter)
                if counter > 0:
                    #print(attempted, finished)
                    if attempted and not finished:
                        shotmade_prediction = shotmade_model.predict(data)[0]
                        print(shotmade_prediction)
                        if shotmade_prediction[0] > 0.85:
                            finished = True
                            print("in hoop")
                            print("From Controller ----------------------------------------------------------------------------------> Shot Made")
                            makes, misses = trackSelector(makes,misses,1)
                            pass
                            
                if not counter == 0:
                    counter -= 1
                if finished:
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
    """ files = os.listdir('.')
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg':
            os.remove(file) """
        
if __name__ == '__main__':
    main()
