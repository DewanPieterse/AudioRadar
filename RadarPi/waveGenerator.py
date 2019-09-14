#!/usr/bin/env python3

import numpy as np
#import matplotlib.pyplot as plt
#from scipy import signal
from scipy.io import wavfile
#from rect import rect
#import time

def waveGenerator(duration, frequency=10000):
    
    fs = 44100
    
    t = np.linspace(0, duration, fs * duration)  #  Produces a x second Audio-File
        
    y = np.sin(frequency * 2 * np.pi * t)  #  Has frequency of 440Hz
    
    name = str(frequency) + 'Hz.wave' 

    wavfile.write(name, fs, y)
    
    print('Successfully created ' + str(frequency) + 'Hz continuous wave file.')
    
    return name


def pulseTrainGenerator(resolution, unambigRange=10, frequency=8000, bandwidth=1000, numPulses=32):
    
    fc = int(frequency)                # Center Frequency [Hz]
    B = int(bandwidth)                 # Bandwidth [Hz] 
    T = 100/B                          # Pulse length in [s]                       T < PRI/2
    UnambigRange = unambigRange        # Unambiguous Range [m] (0.5 - 10)
    #RangeResolution = 0.5              # Range Resolution [m]  (0.05 - 2)

    c = 343                            # speed of sound [m/s]
    PRI = (2 * UnambigRange) / c       # Pulse Repetition Interval [s]
    #PulseCompressionGain = T * B       # Pulse Compression needs to be higher than 100 to ensure 13dB between sidelobe and mainlobe. 
    fs = 44100                         # Sampling rate by soundcard [Hz]
    ts = 1/fs                          # Sampling period [s]
    #PRF = 1/PRI                        # Hz
    #t_max = PRI * numPulses            # Maximum time to simulate 
    #lamda = c/fc
    t  = np.arange(0,(PRI),ts)    # Time vector (in seconds)

    #K = B/T                            # Chirp rate

    # Generate Transmit pulse and signal
    y = pulseGenerator(fc,B,T)
    pulsePadded = np.pad(y, (0,(len(t)-len(y))), 'constant')
    Tx_Signal = np.tile(pulsePadded, numPulses)
    Tx_p = np.pad(pulsePadded, (0, (len(Tx_Signal)-len(pulsePadded))), 'constant')    
    
    name = 'Chirp ' + str(frequency) + 'Hz.wave' 

    wavfile.write(name, fs, Tx_Signal)
    
    #print('Successfully created ' + str(frequency) + 'Hz pulsed wave file with a bandwidth of ' + str(bandwidth) + '.')
    #print('Successfully created ' + str(numPulses) + ' pulses in second wave file.')
    
    return Tx_Signal, Tx_p


def pulseGenerator(frequency, bandwidth, duration):
    
    fs = 44100
    ts = 1/fs
    f0 = frequency - bandwidth/2 # Start frequency of chirp
    #f1 = frequency + bandwidth/2 # Stop frequency of chirp
    t = np.linspace(0, duration, int(duration // ts))
    #T = 100 / bandwidth
    mu = bandwidth / duration # Chirp Rate
    
    y = np.cos(2 * np.pi * (f0 * t + 0.5 * mu * t**2));
    
    name = 'Chirp ' + str(frequency) + 'Hz pulse.wave'
    wavfile.write(name, fs, y)
        
    #f, t, Sxx = signal.spectrogram(y, fs)
    #plt.pcolormesh(t, f, Sxx)
    #plt.ylabel('Frequency [Hz]')
    #plt.xlabel('Time [sec]')
    #plt.show()
    
    return y
