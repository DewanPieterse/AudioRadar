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

    [numtaps, f1, f2] = 10001, (fc-(bandwidth/2)*1.02), (fc+(bandwidth/2)*1.02)
    coeffsBandPass = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
    y = (signal.convolve(audio, coeffsBandPass))
    # print('y\t',y.shape)
    # y = np.transpose(y)
    # print('y\t',y.shape)

    # Complex Downmixing of Transmit Pulse and Received Signal
    ts = 1/fs
    N = len(Tx_p)    
    N2 = len(y)

    time_tp = np.linspace(0,N*ts,N)
    tp = downMix(ts, bandwidth, fc, Tx_p, time_tp)          # Complex downmix and LPF Transmit Pulse

    time_rs = np.linspace(0,N2*ts,N2)
    r = downMix(ts, bandwidth, fc, y, time_rs)      # Complex downmix and LPF Received Signal

    RangeLine = matchedFilter(tp, r)

    peaks = signal.find_peaks(RangeLine,threshold=221,distance=1800)[0]
#     print((peaks))
    try:
        start = peaks[3]
        end = peaks[(3+numPulses)]
        RangeLine = RangeLine[start: end]
    except:
#         start = peaks[0]
#         end = peaks[(0+numPulses)]
        RangeLine = RangeLine#[start: end]

#     plt.plot(20*np.log10(RangeLine))
#     plt.ylabel('Frequency [Hz]')
#     plt.xlabel('Range [m]')
#     plt.title('Recieved Signal')
#     plt.savefig('/home/pi/Desktop/testing.png')
#     plt.clf()

    m = int(len(RangeLine)/numPulses)
    RangeLine = RangeLine[:int(m*numPulses)]

    Rx_Signal_Matrix = (np.reshape(RangeLine, (int(m), int(numPulses)))) # C-like index ordering # np.transpose
    Rx_Signal_Matrix_Window = hamming(Rx_Signal_Matrix)

    RangeDopplerMatrix = fftshift(fft(Rx_Signal_Matrix_Window, axis=0))#fftshift(fft(Rx_Signal_Matrix_Window,axis=1))
    matrix = 20*np.log10(np.abs((RangeDopplerMatrix)))

    # matrix[matrix < 172] = 160
    # matrix[matrix > 179] = 190

    plt.imshow(matrix, aspect='auto', extent = [0 , rangeU, numPulses , 0], cmap=plt.cm.get_cmap('seismic', 20))
    plt.colorbar()
#     plt.xlim(0,5.5)
    plt.ylabel('Number of Pulses')
    plt.xlabel('Range [m]')
    plt.title('Range Map')
    # plt.clim(-10,20)
    name = './static/assets/img/image5.png'
    plt.savefig(name)
    time.sleep(0.5)
    plt.clf()