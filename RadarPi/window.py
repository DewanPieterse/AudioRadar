#!/usr/bin/python3

import numpy as np
import scipy.signal as signal
import cmath
from scipy.fftpack import fft

def hamming(RxSignalMatrix):

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
    Window = np.transpose(np.matlib.repmat(h, m, 1))
#     print(n,m)
#     print(RxSignalMatrix.shape,Window.shape)
    
    phaseLeakageVector = np.angle(RxSignalMatrix[ : , 1])     # First column of received matrix
#     print(phaseLeakageVector.shape)
    phaseLeakageMatrix = np.transpose(np.matlib.repmat(phaseLeakageVector, m, 1))  # Reproduce the phase leakage correction matrix
#     print(phaseLeakageMatrix.shape)
    
#     RangeMatrix_Windowed = RxSignalMatrix .* Window;        % Window with W
    

    RangeMatrix_Window_PhaseLeak = RxSignalMatrix * Window * np.conj(phaseLeakageMatrix)
    
    RangeMatrix = fft(RangeMatrix_Window_PhaseLeak, axis=0) # FFT windowed/phaseLeakage funtion FAST TIME
    
#     RangeMatrix = fftshift(RangeMatrix_FFT, 1);             
#     FFT Shift result for display - Display not necessary now

    return RangeMatrix 