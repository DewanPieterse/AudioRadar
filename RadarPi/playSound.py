from pygame import mixer

def playSound(fileName):
    
    mixer.init() # Initialize pygame mixer
    file = '/home/pi/Documents/RadarPi/' + fileName

    sound = mixer.Sound(file) # Load the sounds
    sound.play()
