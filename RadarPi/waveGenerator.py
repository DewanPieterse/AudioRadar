#!/usr/bin/env python3

import numpy as np
from scipy.io import wavfile

def waveGenerator(freq, duration, mode, bandwidth):
    fs = 44100
    frequency = freq # Sampling frequency
    
    t = np.linspace(0, duration, fs * duration)  #  Produces a 5 second Audio-File
    
    if mode == 'cw':
        
        y = np.sin(frequency * 2 * np.pi * t)  #  Has frequency of 440Hz
        
        name = str(frequency) + 'Hz.wave' 

        wavfile.write(name, fs, y)
        
        print('Successfully created ' + str(frequency) + 'Hz continuous wave file.')
        

    elif mode == 'pulse':
        
        Tx_Signal = zeros(1, size(t,2));

         for count = 1: NumPulses
             tdn = PRI * (count - 1);
             Tx_Signal = Tx_Signal +  cos(2*pi*(fc*(t - T/2 - tdn) + 0.5*K*(t - T/2 - tdn).^2) ).* rect( (t - T/2 - tdn)/T );  % received signal 
         end
         
         
        
        f0 = frequency - bandwidth/2 # Start frequency of chirp
        f1 = frequency + bandwidth/2 # Stop frequency of chirp
        
        mu = bandwidth / duration # Chirp Rate
        
        y = np.cos(2 * np.pi * (f0 * t + 0.5 * mu * t**2));
        
        name = 'Chirp ' + str(frequency) + 'Hz.wave' 

        wavfile.write(name, fs, y)
        
        print('Successfully created ' + str(frequency) + 'Hz pulsed wave file with a bandwidth of ' + str(bandwidth) + '.')
        
    else:
        
        print('You have to specify the mode, either \'cw\' or \'pulse\'.')