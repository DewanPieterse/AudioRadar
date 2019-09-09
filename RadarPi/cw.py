#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Audio Radar Simulation and Real World - Continuous Wave

# Author:       Dewan Pieterse
# Supervisor:   Dr. Y. Abdul Gaffar
# Date:         June 2019

## Import relevant packages

import numpy as np
import math
from scipy import signal
import matplotlib.pyplot as plt
from waveGenerator import pulseGenerator, pulseTrainGenerator, waveGenerator
from rect import rect

## Define constants and parameters

pi = np.pi

# Radar parameters

fc = 10e3                            # Center Frequency [Hz]
T = 3                               # Pulse length in [s]
c = 343                             # speed of sound [m/s]
fs = 44.1e3                         # Sampling rate by soundcard [Hz]
ts = 1/fs                           # Sampling period [sc]
lamda = c/fc                   
t = np.arange(0, T, ts)             # time array

# Generate Transmit signal 

#Tx_Signal = np.cos(2 * pi * fc * t)

fileName = waveGenerator(fc, T, 'cw')

# figure;
plt.plot(t,Tx_Signal);
plt.xlabel('time (in seconds)');
plt.title('Signal versus Time');

# Spectrogram
f, tspec, Sxx = signal.spectrogram(Tx_Signal, fs)
plt.pcolormesh(tspec, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

# Record the Received Signal

#recordAudio()

# recordLength = length(Tx_Signal) * ts;          # Set up the same time as transmitting signal
# recordObject = audiorecorder(fs, 24, 1);        # Sampling freq, bits, mono or stereo (channels)
# record(recordObject, recordLength * 2);
# pause(recordLength);
# soundsc(Tx_Signal, fs, 24);                     # 24 bit sound, sampled at 44.1 kHz
# pause(recordLength * 2);
# stop(recordObject);

# Rx_Signal = (getaudiodata(recordObject));      # Store recorded audio from object in double-precision array
# Rx_Signal = bandpass(Rx_Signal, [(fc - 0.1*fc) (fc + 0.1*fc)], fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);
# Rx_Signal = transpose(Rx_Signal);

# ## Plot Rx_Signal

# time_s = 0: ts: (size(Rx_Signal, 2) - 1) * ts;

# figure('Color','white');
# plot(time_s,Rx_Signal);
# title({'Received Signal', 'Continuous Wave'});
# xlabel('Time [s]');
# ylabel('Received Signal'); 
 
# ## Complex Downmixing of Transmit Pulse and Received Signal

# # tp = downMix(ts, 0, fc, Tx_Signal, t);         # Complex downmix and LPF Transmit Pulse
# # 
# # time_rs = (0: 1: length(Rx_Signal)-1)*ts;
# # 
# # r = downMix(ts, 0, fc, Rx_Signal, time_rs);     # Complex downmix and LPF Received Signal


# ## Cut the received signal to transmitted signal's size

# # [pks, locs] = findpeaks(abs(Rx_Signal), 'MinPeakHeight', 0.3);
# # start = locs(4);
# # last = locs(end);
# # Rx_signal = Rx_Signal(1, start : ceil(last + (5 * T * ts)));

# # averageNoise = max(abs(Rx_Signal(1, 100:1000)));
# # index = find(Rx_Signal >= abs(averageNoise * 1.5), 10);
# # startNumber = (index(1));
# # Rx_Signal = Rx_Signal(1, startNumber: startNumber + (size(Tx_Signal,2)-1));         # Do this on matched filter signal

# average = mean(abs(Rx_Signal(100:20000)));
# [pks, locs] = findpeaks(Rx_Signal, 'MinPeakHeight',average*1e3);

# Rx_Signal = Rx_Signal(locs(1):(locs(1)+size(Tx_Signal,2)-1));

# # loc = 1;
# # for i = length(Rx_Signal)
# #    if  Rx_Signal(i) > Rx_Signal(i-1) * 10
# #        loc = i;
# #    end
# # end

# ##

# # 1. Zero pad the transmit pulse
# # N3 = size(Tx_Signal, 2) - size(Rx_Signal, 2); 
# # 
# # Tx_Signal = [Tx_Signal zeros(1, abs(N3))];

# ps = Tx_Signal.*Rx_Signal;

# ps = lowpass(ps, (0.1*fc), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);

# plot(time_s,ps);

# ## Plots

# figure('Color','white');
# subplot(2,1,1);
# spectrogram(Rx_Signal);#xlim #Spectrogram do multiple ffts. look on website nfft
# #meanfreq and medfreq
# title('Spectrogram of Received Signal', 'fontsize', 12);
# grid on;
# colorbar;
# colormap('jet');

# subplot(2,1,2);
# spectrogram(ps);
# title('Spectrogram of Mixed Signal', 'fontsize', 12);
# grid on;
# colorbar;
# colormap('jet');

# # velocity = fd * lamda;

