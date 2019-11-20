import video_preprocessor as vpp
import threading
import os
import time

# Create preprocessing thread
pipeline = threading.Thread(target=vpp.run)

# start video preprocessing
pipeline.start()

# In production, this is where work will be done
# For now, just lists the files in the directory as they come in
iterations = 0
all_images = []
new_images = []
old_images = []
while iterations < 20:
    files = os.listdir('.')
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.jpg':
            if file not in old_images:
                new_images.append(file)
                all_images.append(file)
    """ for img in all_images:
        if img not in old_images:
            new_images.append(img) """
    old_images = all_images
    print(new_images)
    new_images = []
    time.sleep(0.5)
    iterations += 1  
pipeline.join()