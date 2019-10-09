#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import os
#from scipy import signal
from scipy.io import wavfile
#from rect import rect
#import time

def waveGenerator(duration, frequency=8000):
    
    fs = 44100
    
    t = np.linspace(0, duration, fs * duration)  #  Produces a x second Audio-File
        
    y = np.int16(np.sin(frequency * 2 * np.pi * t) * 32767)
    
    # Path 
    path = "/home/pi/Documents/RadarPi"
  
    # Join various path components  
    name = (os.path.join(path, "static", (str(int(frequency)) + 'Hz.wave'))) 
    
#     name = '/home/pi/Documents/RadarPi/static/' + str(int(frequency)) + 'Hz.wave'
#     name = str(int(frequency)) + 'Hz.wave'
    
    #y = np.int8(y)
    
#     y = y.astype('int16') * 32767

    wavfile.write(name, fs, y)
    
#     print(y.dtype)
    
    #print('Successfully created ' + str(frequency) + 'Hz continuous wave file.')
    
    #return name


def pulseTrainGenerator(unambigRange, resolution=0.05, frequency=8000, bandwidth=4000, numPulses=32):
    
    fc = int(frequency)                # Center Frequency [Hz]
    B = int(bandwidth)                 # Bandwidth [Hz] 
    T = 100/B                          # Pulse length in [s]                       T < PRI/2
    UnambigRange = unambigRange        # Unambiguous Range [m] (0.5 - 10)
    #RangeResolution = 0.5              # Range Resolution [m]  (0.05 - 2)

    c = 343                            # speed of sound [m/s]
    PRI = (2 * UnambigRange) / c       # Pulse Repetition Interval [s]
    #PulseCompressionGain = T * B       # Pulse Compression needs to be higher than 100 to ensure 13dB between sidelobe and mainlobe.
#     B = c / (2 * resolution)
    fs = 44100                         # Sampling rate by soundcard [Hz]
    ts = 1/fs                          # Sampling period [s]
    #PRF = 1/PRI                        # Hz
    #t_max = PRI * numPulses            # Maximum time to simulate 
    #lamda = c/fc
    t  = np.arange(0,(PRI),ts)         # Time vector (in seconds)

    #K = B/T                            # Chirp rate

    # Generate Transmit pulse and signal
    y = pulseGenerator(T,fc,B)
#     print(len(t))
#     print(len(y))
    pulsePadded = np.pad(y, (0,int(len(t)-len(y))), 'constant')
    Tx_Signal = np.tile(pulsePadded, int(numPulses))
    Tx_p = np.pad(pulsePadded, (0, (len(Tx_Signal)-len(pulsePadded))), 'constant')
    
    name = '/home/pi/Documents/RadarPi/static/Chirp ' + str(int(frequency)) + 'Hz.wave' 

    wavfile.write(name, fs, Tx_Signal)
    
    return Tx_Signal, y


def pulseGenerator(duration, frequency=8000, bandwidth=2000):
    
    fs = 44100
    ts = 1/fs
    f0 = frequency - bandwidth/2 # Start frequency of chirp
    #f1 = frequency + bandwidth/2 # Stop frequency of chirp
    t = np.linspace(0, duration, int(duration // ts))
    #T = 100 / bandwidth
    mu = bandwidth / duration # Chirp Rate
    
    y = np.int16(np.cos(2 * np.pi * (f0 * t + 0.5 * mu * t**2)) * 32767)
    
#     name = './static/Chirp ' + str(frequency) + 'Hz pulse.wave'
#     wavfile.write(name, fs, y)
    
    return y

# pulseTrainGenerator(5, resolution=1, frequency=12000, bandwidth=3000, numPulses=16)