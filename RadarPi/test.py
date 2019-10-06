#!/usr/bin/python3
import waveGenerator
import recordAudio
import cwProcessing
import pdProcessing
from playSound import playSound
# from flask import Flask, render_template, request
import matplotlib.pyplot as plt

from scipy.io.wavfile import read
import math
import numpy as np
import scipy.signal as signal
from scipy.fftpack import fft, fftshift
import matplotlib.pyplot as plt
from downMix import downMix
from matchedFilter import matchedFilter
from window import hamming

rangeU = 10
numPulses=32
fc=8000
bandwidth=4000

Tx_Signal, Tx_p = waveGenerator.pulseTrainGenerator(rangeU)
name = 'Chirp 8000Hz.wave'

duration = 32 * ((2 * rangeU) / 343) #PRI   
#             print(duration)
playSound(name)
Rx_Signal = recordAudio.recordAudio(duration)

c = 343
lamda = c/fc
PRI = (2 * rangeU) / c
PRF = 1/PRI
# read audio samples
input_data = read(Rx_Signal)
audio = input_data[1]
# print('audio\t',audio.shape)
fs = input_data[0]

[numtaps, f1, f2] = 101, (fc-(bandwidth/2)*1.02), (fc+(bandwidth/2)*1.02)
coeffsBandPass = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
y = np.transpose(signal.convolve(audio, coeffsBandPass))
# print('y\t',y.shape)
y = np.transpose(y)
# print('y\t',y.shape)

# Complex Downmixing of Transmit Pulse and Received Signal
ts = 1/fs
N = len(Tx_p)    
N2 = len(y)

time_tp = np.linspace(0,N*ts,N)
# print('timetp\t',time_tp.shape)
tp = downMix(ts, bandwidth, fc, Tx_p, time_tp)          # Complex downmix and LPF Transmit Pulse
# print('tp\t',tp.shape)

time_rs = np.linspace(0,N2*ts,N2)
# print('timers\t',time_rs.shape)
r = downMix(ts, bandwidth, fc, y, time_rs)      # Complex downmix and LPF Received Signal
# print('r\t',r.shape)

RangeLine = matchedFilter(tp, r)
# print('rangeline\t',RangeLine.shape)

timeRL = np.arange(0.0, len(RangeLine)*ts, ts)
# print('timeRL\t',timeRL.shape)
RangeLineAxis = timeRL * c / 2
# print('rangelineaxis\t',RangeLineAxis.shape)

# plt.plot(RangeLineAxis, 20*np.log10(RangeLine))
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Range [m]')
#     plt.title('Frequency vs Range')
#     name = './static/assets/img/image5.png'
#     plt.savefig(name)
# plt.show()

m = int(len(RangeLine)/numPulses)
RangeLine = RangeLine[:(m*numPulses)]

Rx_Signal_Matrix = (np.reshape(RangeLine, (m, numPulses))) # C-like index ordering # np.transpose
# print('RxSignalMatrix1\t',Rx_Signal_Matrix.shape)
Rx_Signal_Matrix_Window = hamming(Rx_Signal_Matrix)
# print('RxSignalMatrix2\t',Rx_Signal_Matrix.shape)

NumCols_RxSignalMatrix = Rx_Signal_Matrix_Window.shape[1]
t_new = np.arange(0.0, NumCols_RxSignalMatrix * ts, ts)
# print('t_new\t',t_new.shape)
RangeLineAxis_New = t_new * c / 2
# print('RangeLineAxis_New\t',RangeLineAxis_New.shape)

DopplerFreqAxis = np.arange(-PRF/2, PRF/2, PRF/N)      # Axis for Doppler Freq y
# print('DopplerFreqAxis\t',DopplerFreqAxis.shape)
#     DopplerFreqAxis = np.linspace(-N/2, 1, (N/2)) * PRF/N
#     print(DopplerFreqAxis.shape)
VelocityAxis = DopplerFreqAxis * lamda / 2      # Axis for velocity y
# print('VelocityAxis\t',VelocityAxis.shape)
RangeLineAxis_New = t_new * c / 2               # Range Axis for x
# print('RangeLineAxis_New\t',RangeLineAxis_New.shape)
RangeDopplerMatrix = fftshift(fft(Rx_Signal_Matrix_Window,axis=1))
# print('RangeDopplerMatrix\t',RangeDopplerMatrix.shape)
matrix = 20*np.log10(np.abs(RangeDopplerMatrix))

plt.imshow(20*np.log10(np.abs(matrix)), aspect='auto', extent = [0 , rangeU, numPulses , 0], cmap=plt.cm.get_cmap('RdBu', 20))
plt.colorbar(extend='both')
# plt.clim(-10,20)
plt.show()