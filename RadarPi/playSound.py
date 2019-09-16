import pygame

def playSound(fileName):
    
    pygame.init() # Initialize pygame 
#     pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=88200)
    file = '/home/pi/Documents/RadarPi/static/' + fileName

    sound = pygame.mixer.Sound(file) # Load the sounds
    sound.play()

# playSound('6000Hz.wave')