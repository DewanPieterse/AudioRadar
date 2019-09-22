#!/usr/bin/python3

import numpy as np
import scipy.signal as signal
import cmath

def window(RxSignalMatrix):

    # This function takes in a Matrix of the 
    # radar to perform windowing and FFT in slow time. The Matrix is also
    # corrected for the phase leakage experienced due to the sound card
    # introducing a phase delay in the transmitted signal.
    # It returns the matrix after going through a Hamming window and FFT.
    
    #  The FFT needs to be taken in the 'Slow Time' and this corresponds to the
    #  Pulse Repetition Frequency.
    
    n = RxSignalMatrix.shape[0]                           # RxSignalMatrix is a matrix nxm (NumPulses)
    m = RxSignalMatrix.shape[1]                           # We want to reproduce that but windowed.
    h = signal.hamming(n)
    Window = np.matlib.repmat(h, 1, m)
    
    phaseLeakageVector = np.angle(RxSignalMatri[ : , 1])     # First column of received matrix
    phaseLeakageMatrix = np.matlib.repmat(phaseLeakageVector, 1, m)  # Reproduce the phase leakage correction matrix
    
#     RangeMatrix_Windowed = RxSignalMatrix .* Window;        % Window with W
    

    RangeMatrix_Window_PhaseLeak = RxSignalMatrix .* np.conj(phaseLeakageMatrix) .* Window;
    
    RangeMatrix = fft(RangeMatrix_Window_PhaseLeak, [], 1); % FFT windowed/phaseLeakage funtion
    
#     RangeMatrix = fftshift(RangeMatrix_FFT, 1);             
#     FFT Shift result for display - Display not necessary now