#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from rect import rect
import time

def waveGenerator(freq, duration):
    
    fs = 44100
    frequency = freq # Sampling frequency
    
    t = np.linspace(0, duration, fs * duration)  #  Produces a x second Audio-File
        
    y = np.sin(frequency * 2 * np.pi * t)  #  Has frequency of 440Hz
    
    name = str(frequency) + 'Hz.wave' 

    wavfile.write(name, fs, y)
    
    print('Successfully created ' + str(frequency) + 'Hz continuous wave file.')
    
    return name


def pulseTrainGenerator(frequency, duration, bandwidth, unambigRange, numPulses):
    
    fs = 44100
    T = duration
    t = np.linspace(0, duration, fs * duration)  #  Produces a x second Audio-File
    c = 343
    PRI = (2 * unambigRange) / c; # Pulse Repetition Interval [s]
    T = 100/bandwidth
    mu = bandwidth / T # Chirp Rate
    
    Tx_Signal = []

    for i in range(numPulses):
        
        tdn = PRI * i
        Tx_Signal = Tx_Signal.append(np.cos(2*np.pi *(frequency *(t -T/2 -tdn)+0.5*mu*(t-T/2-tdn)**2))*rect((t-T/2-tdn)/T))

    print (Tx_Signal)
    plot(t,Tx_Signal)
    name = 'Chirp ' + str(frequency) + 'Hz.wave' 

    wavfile.write(name, fs, Tx_Signal)
    
    print('Successfully created ' + str(frequency) + 'Hz pulsed wave file with a bandwidth of ' + str(bandwidth) + '.')
    print('Successfully created ' + str(numPulses) + ' pulses in second wave file.')
    
    return name


def pulseGenerator(frequency, bandwidth, duration):
    
    fs = 44100
    f0 = frequency - bandwidth/2 # Start frequency of chirp
    #f1 = frequency + bandwidth/2 # Stop frequency of chirp
    t = np.linspace(0, duration, duration*fs)
    #T = 100 / bandwidth
    mu = bandwidth / duration # Chirp Rate
    
    y = np.cos(2 * np.pi * (f0 * t + 0.5 * mu * t**2));
    
    name = 'Chirp ' + str(frequency) + 'Hz pulse.wave'
    wavfile.write(name, fs, y)
    
    print('Successfully created ' + str(frequency) + 'Hz pulsed wave file with a bandwidth of ' + str(bandwidth) + 'Hz.')
    
    return name
    
    
def chirp(numSamples, chirpLen_s, start_Hz, stop_Hz):

    times_s = np.linspace(0, chirpLen_s, numSamples) # Chirp times.
    k = (stop_Hz - start_Hz) / chirpLen_s # Chirp rate.
    sweepFreqs_Hz = (start_Hz + k/2. * times_s) * times_s
    chirp = np.sin(2 * np.pi * sweepFreqs_Hz)

    return chirp