import video_preprocessor as vpp
from multiprocessing import Process, Queue
import os
import time
import cv2
import model_sim    # Used to simulate true/false values returned from model ## REMOVE THIS CALL FOR PRODUCTION USE

def main():
    # Create Queue for resource (in this case Image) sharing
    q = Queue()


    # In PRODUCTION, add filename from UI as argument
    # Create Process for preprocessing of images
    pipeline = Process(target=vpp.run_file, args=(q,))

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

    # check for new images four times a second for 10 seconds
    while iterations < 10:
        
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
                
                               
                # This is where processing would occur.  Here however we simply get a random boolean back from model_sim testing module
                # For implementation, replace the model_sim with the actual model calls
                if model_sim.ballInFrame(img):
                    if not shot_attempted:
                        print("Shot attempted")
                    in_frame = True
                    shot_attempted = True
                    if model_sim.ballInHoop(img):
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
        time.sleep(0.05)
        iterations += 1  
    
    # close Queue
    q.close()
        
    # close video preprocessing
    pipeline.join()

    # clean up directory afterwards
    files = os.listdir('.')
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg':
            os.remove(file)
        
if __name__ == '__main__':
    main()
    exit()