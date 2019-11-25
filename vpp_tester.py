import video_preprocessor as vpp
import threading
import os
import time

# Create preprocessing thread
pipeline = threading.Thread(target=vpp.run_file)

# start video preprocessing
pipeline.start()

# In production, this is where work will be done
# For now, just lists the files in the directory as they come in

iterations = 0
current_frame = 1
all_images = []
new_images = []
old_images = []

# check for new images four times a second for 10 seconds
while iterations < 35:
    
    #the number of frames to keep
    min_val_to_keep = current_frame - 20
    
    files = os.listdir('.')
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg':
            if file not in old_images:
                new_images.append(file)
                all_images.append(file)
    old_images = all_images
    if len(new_images) > 0:
        for img in new_images:
            ## This is where processing would occur.  Here however we simply print the name of the frame
            print(img)
            current_frame += 1
    new_images = []
    
    #Remove the frames that are too old to keep
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg':
            framenum = int(filename)
            if framenum < min_val_to_keep:
                os.remove(file)
    time.sleep(0.33)
    iterations += 1  
    
# close video preprocessing
pipeline.join()

# clean up directory afterwards
files = os.listdir('.')
for file in files:
    filename, file_extension = os.path.splitext(file)
    if file_extension == '.jpg':
        os.remove(file)