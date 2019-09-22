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
#     print(audio)
#     print(input_data[0])
    
    [numtaps, f1, f2] = 101, (frequency-frequency*0.05), (frequency+frequency*0.05)
    coeffsBandPass = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
    y = signal.convolve(audio, coeffsBandPass)

    # Number of sample points
    N = len(y)
    # sample spacing
    T = 1.0 / 44100
    t = np.linspace(0.0, N*T, N)
    
    fig, (ax1, ax2) = plt.subplots(nrows=2)
    ax1.plot(t, y)
    Pxx, freqs, bins, im = ax2.specgram(y, NFFT=16384, Fs=44100, noverlap=1000)
    plt.ylim((f1+(frequency*0.04), f2-(frequency*0.04)))   # set the ylim to bottom, top
    # The `specgram` method returns 4 objects. They are:
    # - Pxx: the periodogram
    # - freqs: the frequency vector
    # - bins: the centers of the time bins
    # - im: the matplotlib.image.AxesImage instance representing the data in the plot
#     plt.show()
    
    
#     f,t,Sxx = signal.spectrogram(y, fs=44100, window='hamming', nperseg=512, noverlap=488, nfft=2048, scaling='spectrum', mode='magnitude')
#     plt.pcolormesh(t, np.fft.fftshift(f), np.fft.fftshift(Sxx, axes=0))
#     plt.ylabel('Frequency [Hz]')
#     plt.xlabel('Time [sec]')
#     plt.ylim(f1, f2)
#     plt.colorbar()
#     plt.show()

#     w = hamming(N)
#     ywf = fft(y*w)
#     ywf = fft(y)
#     xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
#     plt.semilogy(xf[1:int(N/2)], 2.0/N * np.abs(yf[1:int(N/2)]), '-b')
#     plt.semilogy(xf[1:int(N/2)], 2.0/N * np.abs(ywf[1:int(N/2)]), '-r')
#     plt.legend(['FFT', 'FFT w. window'])
    name = './static/assets/img/image5.png'
#     plt.grid()
    plt.savefig(name)
    plt.show()

cwProcessing('./static/recordedAudio.wave',11000)
