#!/usr/bin/env python3
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from downMix import downMix
from matchedFilter import matchedFilter
from window import window


def pdProcessing(Tx_Signal, Tx_p, Rx_Signal, rangeU, numPulses=32, fc=8000, bandwidth=4000):
    
    # read audio samples
    input_data = read(Rx_Signal)
    audio = input_data[1]
    fs = input_data[0]
    
    [numtaps, f1, f2] = 101, (fc-(bandwidth/2)*1.02), (fc+(bandwidth/2)*1.02)
    coeffsBandPass = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
    y = signal.convolve(audio, coeffsBandPass)
    

    # Complex Downmixing of Transmit Pulse and Received Signal
    ts = 1/fs
    N = len(Tx_p)
    
    time_tp = np.linspace(0.0, N*ts, N)
    tp = downMix(ts, bandwidth, fc, Tx_p, time_tp)          # Complex downmix and LPF Transmit Pulse

    time_rs = np.linspace(0.0, ts, len(Rx_Signal)*ts)
    r = downMix(ts, bandwidth, fc, Rx_Signal, time_rs)      # Complex downmix and LPF Received Signal
    
    
    RangeLine = matchedFilter(tp, r)
    
    timeRL = np.linspace(0.0, ts, len(RangeLine)*ts)
    RangeLineAxis = timeRL * 343 / 2
    
#     plt.plot(RangeLineAxis, RangeLine)
#     plt.ylabel('Frequency [Hz]')
#     plt.xlabel('Range [m]')
#     plt.title('Frequency vs Range')
#     name = './static/assets/img/image5.png'
#     plt.savefig(name)
#     plt.show()
    
    
    Rx_Signal_Matrix = np.reshape(RangeLine, (len(RangeLine)/numPulses, numPulses)) # C-like index ordering
    Rx_Signal_Matrix = window(Rx_Signal_Matrix)
    
    
    