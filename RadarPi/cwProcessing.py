#!/usr/bin/python3

from scipy.io.wavfile import read
from scipy.fftpack import fft
from scipy.signal import hamming
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import time

def cwProcessing(Rx_Signal, frequency=8000):
    
    # read audio samples
    input_data = read(Rx_Signal)
    audio = input_data[1]
    fs = input_data[0]
    
    numtaps = 10001
    
    # Bandpass filter
#     [numtaps1, f1, f2] = 1001, (frequency-frequency*0.075), (frequency+frequency*0.075)
#     coeffsBandPass = signal.firwin(numtaps1, [f1, f2], fs=fs, window = "hamming")
#     y_BP = signal.convolve( coeffsBandPass,audio)
# #     y_BP = signal.lfilter(numtaps1,1,audio)
#     
#     # Notch filter
#     [numtaps, f1, f2] = 1001, (frequency-30), (frequency+30)
#     coeffsNotch = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
#     y = signal.convolve(audio, coeffsNotch)
# #     y = signal.lfilter(numtaps,1,y_BP)
# 
#     [numtaps, f] = 1001, (frequency-frequency*0.075)
#     coeffsHigh = signal.firwin(numtaps, f, pass_zero=False, fs=fs)#, window = "hamming")
#     y = signal.convolve(y, coeffsHigh)
# 
#     [numtaps, f] = 1001, (frequency+frequency*0.075)
#     coeffsLow = signal.firwin(numtaps, f, fs=fs)#, window = "hamming")
#     y = signal.convolve(y, coeffsLow)
#     
#     [f1,f2] = (frequency-10), (frequency+10)
#     coeffsStop = signal.firwin(numtaps, [f1, f2], fs=fs)
#     y = signal.convolve(y, coeffsStop)

    f = (frequency-frequency*0.075)
    coeffsHigh = signal.firwin(numtaps, f, pass_zero=False, fs=fs, window = "hamming")
    y = signal.convolve(audio, coeffsHigh)

    f = (frequency+frequency*0.075)
    coeffsLow = signal.firwin(numtaps, f, fs=fs, window = "hamming")
    y = signal.convolve(y, coeffsLow)

    [f1,f2] = (frequency-20), (frequency+20)
    coeffsStop = signal.firwin(numtaps, [f1, f2], fs=fs, window ='hamming')
    y = signal.convolve(y, coeffsStop)

#     nyq = 0.5 * fs
#     low = f1 / nyq
#     high = f2 / nyq
#     b, a = signal.butter(101, [low, high], btype='band')
#     output_signal = signal.filtfilt(b, a, audio)

    # Number of sample points
    N = len(y)
    T = 1.0 / 44100
    t = np.linspace(0.0, N*T, N)
    
#     f, t, Sxx = signal.spectrogram(y, fs=fs)   
#     dBS = 20 * np.log10(Sxx)  # convert to dB
#     plt.pcolormesh(t, f, dBS)
    
    Pxx, freqs, bins, im = plt.specgram(y, NFFT=16384, Fs=fs,noverlap=8092)#     plt.pcolormesh(Pxx)
    plt.ylim((f1+(frequency*0.05), f2-(frequency*0.05)))   # set the ylim to bottom, top
    
#     Pxx[Pxx < 25] = -50
# # matrix[matrix > 179] = 190
#     plt.xlim(0, bins[-1])
    plt.title('Spectrogram %i Hz' %frequency)
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.colorbar()

    name = './static/assets/img/image5.png'
    plt.savefig(name)
    time.sleep(0.5)
    plt.clf()

# cwProcessing('./static/recordedAudio.wave',8000)
