#!/usr/bin/python3

from scipy.io.wavfile import read
from scipy.fftpack import fft
from scipy.signal import hamming
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

def cwProcessing(Rx_Signal, frequency=8000):
    
    # read audio samples
    input_data = read(Rx_Signal)
    audio = input_data[1]
    fs = input_data[0]
    
    [numtaps, f1, f2] = 101, (frequency-frequency*0.05), (frequency+frequency*0.05)
    coeffsBandPass = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
    y = signal.convolve(audio, coeffsBandPass)

    # Number of sample points
    N = len(y)
    T = 1.0 / 44100
    t = np.linspace(0.0, N*T, N)
    
    Pxx, freqs, bins, im = plt.specgram(y, NFFT=16384, Fs=44100, noverlap=1000)
    plt.ylim((f1+(frequency*0.04), f2-(frequency*0.04)))   # set the ylim to bottom, top
    plt.xlim(0, bins[-1])
    plt.title('Spectrogram')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')

    name = './static/assets/img/image5.png'
    plt.savefig(name)

# cwProcessing('./static/recordedAudio.wave',10000)
