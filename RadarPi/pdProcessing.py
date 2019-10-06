#!/usr/bin/env python3

from scipy.io.wavfile import read
import math, time
import numpy as np
import scipy.signal as signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
from downMix import downMix
from matchedFilter import matchedFilter
from window import hamming

def pdProcessing(Tx_p, Rx_Signal, rangeU, numPulses=32, fc=8000, bandwidth=4000):
    
    c = 343
    lamda = c/fc
    PRI = (2 * rangeU) / c
    PRF = 1/PRI
    
    # read audio samples
    input_data = read(Rx_Signal)
    audio = input_data[1]
    fs = input_data[0]

    [numtaps, f1, f2] = 101, (fc-(bandwidth/2)*1.02), (fc+(bandwidth/2)*1.02)
    coeffsBandPass = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
    y = np.transpose(signal.convolve(audio, coeffsBandPass))
    y = np.transpose(y)

    # Complex Downmixing of Transmit Pulse and Received Signal
    ts = 1/fs
    N = len(Tx_p)    
    N2 = len(y)

    time_tp = np.linspace(0,N*ts,N)
    tp = downMix(ts, bandwidth, fc, Tx_p, time_tp)          # Complex downmix and LPF Transmit Pulse

    time_rs = np.linspace(0,N2*ts,N2)
    r = downMix(ts, bandwidth, fc, y, time_rs)      # Complex downmix and LPF Received Signal

    RangeLine = matchedFilter(tp, r)

    timeRL = np.arange(0.0, len(RangeLine)*ts, ts)
    RangeLineAxis = timeRL * c / 2
    
    m = int(len(RangeLine)/numPulses)
    RangeLine = RangeLine[:(m*numPulses)]

    Rx_Signal_Matrix = (np.reshape(RangeLine, (m, numPulses))) # C-like index ordering # np.transpose
    Rx_Signal_Matrix_Window = hamming(Rx_Signal_Matrix)

    NumCols_RxSignalMatrix = Rx_Signal_Matrix_Window.shape[1]
    t_new = np.arange(0.0, NumCols_RxSignalMatrix * ts, ts)
    RangeLineAxis_New = t_new * c / 2

    DopplerFreqAxis = np.arange(-PRF/2, PRF/2, PRF/N)      # Axis for Doppler Freq y
    VelocityAxis = DopplerFreqAxis * lamda / 2      # Axis for velocity y
    RangeLineAxis_New = t_new * c / 2               # Range Axis for x
    RangeDopplerMatrix = fftshift(fft(Rx_Signal_Matrix_Window,axis=1))
    matrix = 20*np.log10(np.abs(RangeDopplerMatrix))

    plt.imshow(matrix, aspect='auto', extent = [0 , rangeU, numPulses , 0], cmap='RdBu')
    time.sleep(1)
    plt.colorbar(extend='both')
    plt.xlabel('Range [m]')
    plt.title('Number of Pulses vs Range')
    name = './static/assets/img/image5.png'
    plt.savefig(name)
    time.sleep(0.5)
#     plt.show()
