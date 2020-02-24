from playsound import playsound
import random

#folder and files that are selected for the audio tracks
fileName = 'labeled_audio/'
positiveSoundLabeled =['pos_short','pos_med','pos_long']
neutralSoundLabeled =['net_short','net_med','net_long']
negativeSoundLabeled =['neg_short','neg_med','neg_long']


#Decision logic to select the track being used
#makes count the number of 
def trackSelector(makes, misses , shot):
    #plays background track
    clip = fileName + 'background.mp3'
    print('playing background noise.')
    print(makes)
    print(misses)
    print(shot)

    # all positive shots
    playsound(clip,False)
    if (makes == 1 and misses == 0 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        #plays clip
        playsound(clip,False)
        #returns the makes and miss to pass between functions
        return makes, misses
    elif (makes == 2 and misses == 0 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        return makes, misses
    elif( makes == 3 and misses == 0 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        #resets for depth of three decision treee
        makes = 0
        misses = 0
        return makes, misses

    #combination of middle of tree
    elif( makes == 1 and misses == 1 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        return makes, misses
    elif( makes == 1 and misses == 1 and shot == 0):
        clip = fileName +negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        return makes, misses
    elif (makes == 2 and misses == 1 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses
    elif (makes == 2 and misses == 1 and shot == 0):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses
    elif (makes ==1 and misses == 2 and shot == 1):
        clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses
    elif (makes == 1 and misses == 2 and shot == 0):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses
    # all negative sounds
    elif (makes == 0 and misses == 1 and shot == 1):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        return makes, misses
    elif (makes == 0 and misses == 2 and shot == 0):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        return makes, misses
    elif( makes == 0 and misses == 3 and shot == 0):
        clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(2,4))+'.mp3'
        print(clip)
        playsound(clip,False)
        makes = 0
        misses = 0
        return makes, misses




def main():
    makes = 0
    misses = 0
    while(True):
        shot = input("a for make, l for miss")
        if(shot == 'a'):
            makes, misses = trackSelector(makes+1,misses,1)
        else:
            makes, misses = trackSelector(makes,misses+1,0)
        

if __name__ == '__main__':
    main()