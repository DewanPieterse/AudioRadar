#!/usr/bin/python3

from scipy.io.wavfile import read
from scipy.fftpack import fft
from scipy.signal import hamming
import numpy as np
import matplotlib.pyplot as plt

def cwProcessing(Rx_Signal):
    
    # read audio samples
    input_data = read(Rx_Signal)
    audio = input_data[1]
#     print(audio)
#     print(input_data[0])

    # Number of sample points
    N = len(audio)
    # sample spacing
    T = 1.0 / 44100
    x = np.linspace(0.0, N*T, N)
    y = audio
    yf = fft(y)

    w = hamming(N)
    ywf = fft(y*w)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    image = './static/assets/img/image5.png'
    plt.semilogy(xf[1:int(N/2)], 2.0/N * np.abs(yf[1:int(N/2)]), '-b')
    plt.semilogy(xf[1:int(N/2)], 2.0/N * np.abs(ywf[1:int(N/2)]), '-r')
    plt.legend(['FFT', 'FFT w. window'])
    plt.grid()
    plt.savefig(image)
#     plt.show()

    
