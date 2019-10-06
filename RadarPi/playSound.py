import pygame, os

# from pydub import AudioSegment
# from pydub.playback import play

def playSound(fileName,volume):
    
    pygame.init() # Initialize pygame 
#     pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=88200)
    file = '/home/pi/Documents/RadarPi/static/' + fileName
#     time.sleep(1)
    sound = pygame.mixer.Sound(file) # Load the sounds
    sound.set_volume(volume)
    sound.play()
    
#     os.system(file)



#     song = AudioSegment.from_wav(file)
#     play(song)

# playSound('6000Hz.wave')