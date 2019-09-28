#!/usr/bin/env python3

from scipy.io.wavfile import read
import math
import numpy as np
import scipy.signal as signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
from downMix import downMix
from matchedFilter import matchedFilter
from window import hamming

def pdProcessing(Tx_Signal, Tx_p, Rx_Signal, rangeU, numPulses=32, fc=8000, bandwidth=4000):
    
    c = 343
    lamda = c/fc
    PRI = (2 * rangeU) / c
    PRF = 1/PRI
    # read audio samples
    input_data = read(Rx_Signal)
    audio = input_data[1]
    fs = input_data[0]
    
#     plt.plot(audio)
#     plt.show()
    
    [numtaps, f1, f2] = 101, (fc-(bandwidth/2)*1.02), (fc+(bandwidth/2)*1.02)
    coeffsBandPass = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
    y = signal.convolve(audio, coeffsBandPass)
    

    # Complex Downmixing of Transmit Pulse and Received Signal
    ts = 1/fs
    N = len(Tx_p)    
    N2 = len(y)
    
    time_tp = np.linspace(0,N*ts,N)
    tp = downMix(ts, bandwidth, fc, Tx_p, time_tp)          # Complex downmix and LPF Transmit Pulse

    time_rs = np.linspace(0,N2*ts,N2)
    r = downMix(ts, bandwidth, fc, y, time_rs)      # Complex downmix and LPF Received Signal
    
    
    RangeLine = matchedFilter(tp, r)
    
    timeRL = np.linspace(0.0, ts, len(RangeLine)*ts)
    RangeLineAxis = timeRL * c / 2
    
#     plt.plot(RangeLineAxis, RangeLine)
#     plt.ylabel('Frequency [Hz]')
#     plt.xlabel('Range [m]')
#     plt.title('Frequency vs Range')
#     name = './static/assets/img/image5.png'
#     plt.savefig(name)
#     plt.show()
    
    m = int(len(RangeLine)/numPulses)
    RangeLine = RangeLine[:(m*numPulses)]

    Rx_Signal_Matrix = np.transpose(np.reshape(RangeLine, (m, numPulses))) # C-like index ordering
    Rx_Signal_Matrix_Window = hamming(Rx_Signal_Matrix)
    
    NumCols_RxSignalMatrix = Rx_Signal_Matrix_Window.shape[1]
    t_new = np.linspace(0.0, ts, NumCols_RxSignalMatrix * ts)
    RangeLineAxis_New = t_new * c / 2
    
    DopplerFreqAxis = np.arange(-PRF/2, PRF/2, PRF/N)      # Axis for Doppler Freq y
#     DopplerFreqAxis = np.linspace(-N/2, 1, (N/2)) * PRF/N
#     print(DopplerFreqAxis.shape)
    VelocityAxis = DopplerFreqAxis * lamda / 2      # Axis for velocity y
    RangeLineAxis_New = t_new * c / 2               # Range Axis for x

    RangeDopplerMatrix = fftshift(fft(Rx_Signal_Matrix_Window,axis=1))
    
    matrix = 20*np.log10(np.abs(RangeDopplerMatrix))
    
    plt.figure(figsize=(10,2))
    
    plt.matshow(matrix, aspect='auto',cmap='RdBu')
    plt.ylabel('Velocity [m/s]')
    
    plt.colorbar()
    plt.xlabel('Range [m]')
    plt.title('Velocity vs Range')
    name = './static/assets/img/image5.png'
    plt.savefig(name)
#     plt.show()
