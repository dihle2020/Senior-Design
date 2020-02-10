from playsound import playsound
import random

fileName = 'labeled_audio/'
positiveSoundLabeled =['pos_short','pos_med','pos_long']
neutralSoundLabeled =['net_short','net_med','net_long']
negativeSoundLabeled =['neg_short','neg_med','neg_long']

def AudioHomeTree(tree):
    if tree == '1':
        PostiveAndNegative()
    else:
        PostiveAndNeutral()


def PostiveAndNegative():
    keepGoing = True
    while(keepGoing):
        shot = input('a: for made. and l: for miss. e: end session: ')
        if(shot == 'a'):
            clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(1,8))+'.mp3'
            print(clip)
            playsound(clip)
            shot = input('a: for made. and l: for miss.: ')
            if(shot == 'a'):
                clip = fileName + positiveSoundLabeled[1] + '_' + str(random.randint(1,4))+'.mp3'
                print(clip)
                playsound(clip)
                shot = input('a: for made. and l: for miss.: ')
                if(shot == 'a'):
                    clip = fileName + positiveSoundLabeled[2] + '_' + str(random.randint(1,1))+'.mp3'
                    print(clip)
                    playsound(clip)
                else:
                    clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
            else:
                clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
                print(clip)
                playsound(clip)
                shot = input('a: for made. and l: for miss.: ')
                if(shot == 'a'):
                    clip = fileName + positiveSoundLabeled[1] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
                else:
                    clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
        
        elif(shot == 'e'):
            keepGoing = False
            print("ending session")
        else:
            clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
            print(clip)
            playsound(clip)
            shot = input('a: for made. and l: for miss.: ')
            if(shot == 'a'):
                clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(1,8))+'.mp3'
                print(clip)
                playsound(clip)
                shot = input('a: for made. and l: for miss.: ')
                if(shot == 'a'):
                    clip = fileName + positiveSoundLabeled[1] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
                else:
                    clip = fileName + negativeSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
            else:
                clip = fileName + negativeSoundLabeled[1] + '_' + str(random.randint(1,2))+'.mp3'
                print(clip)
                playsound(clip)
                shot = input('a: for made. and l: for miss.: ')
                if(shot == 'a'):
                    clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(1,8))+'.mp3'
                    print(clip)
                    playsound(clip)
                else:
                    clip = fileName + negativeSoundLabeled[2] + '_' + str(random.randint(1,2))+'.mp3'
                    print(clip)
                    playsound(clip)
 

def PostiveAndNeutral():
    keepGoing = True
    while(keepGoing):
        shot = input('a: for made. and l: for miss. e: end session: ')
        if(shot == 'a'):
            clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(1,8))+'.mp3'
            print(clip)
            playsound(clip)
            shot = input('a: for made. and l: for miss.: ')
            if(shot == 'a'):
                clip = fileName + positiveSoundLabeled[1] + '_' + str(random.randint(1,4))+'.mp3'
                print(clip)
                playsound(clip)
                shot = input('a: for made. and l: for miss.: ')
                if(shot == 'a'):
                    clip = fileName + positiveSoundLabeled[2] + '_' + str(random.randint(1,1))+'.mp3'
                    print(clip)
                    playsound(clip)
                else:
                    clip = fileName + neutralSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
            else:
                clip = fileName + neutralSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
                print(clip)
                playsound(clip)
                shot = input('a: for made. and l: for miss.: ')
                if(shot == 'a'):
                    clip = fileName + positiveSoundLabeled[1] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
                else:
                    clip = fileName + neutralSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
        
        elif(shot == 'e'):
            keepGoing = False
            print("ending session")
        else:
            clip = fileName + neutralSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
            print(clip)
            playsound(clip)
            shot = input('a: for made. and l: for miss.: ')
            if(shot == 'a'):
                clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(1,8))+'.mp3'
                print(clip)
                playsound(clip)
                shot = input('a: for made. and l: for miss.: ')
                if(shot == 'a'):
                    clip = fileName + positiveSoundLabeled[1] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
                else:
                    clip = fileName + neutralSoundLabeled[0] + '_' + str(random.randint(1,4))+'.mp3'
                    print(clip)
                    playsound(clip)
            else:
                clip = fileName + neutralSoundLabeled[1] + '_' + str(random.randint(1,2))+'.mp3'
                print(clip)
                playsound(clip)
                shot = input('a: for made. and l: for miss.: ')
                if(shot == 'a'):
                    clip = fileName + positiveSoundLabeled[0] + '_' + str(random.randint(1,8))+'.mp3'
                    print(clip)
                    playsound(clip)
                else:
                    clip = fileName + neutralSoundLabeled[2] + '_' + str(random.randint(1,2))+'.mp3'
                    print(clip)
                    playsound(clip)

def main():
    print("1. Positive and Negative Sounds")
    print("2. Postivie and Neurtral Sounds")
    tree = input("Enter which tree you want: ")
    AudioHomeTree(tree)

if __name__ == '__main__':
    main()