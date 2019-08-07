## Audio Radar Simulation and Real World - Continuous Wave

# Author:       Dewan Pieterse
# Supervisor:   Dr. Y. Abdul Gaffar
# Date:         June 2019

## Import relevant packages

import numpy as np
import math

## Define constants and parameters

pi = math.pi

# Radar parameters

fc = 10e3                          # Center Frequency [Hz]
T = 3                              # Pulse length in [s]
c = 343                            # speed of sound [m/s]
fs = 44.1e3                        # Sampling rate by soundcard [Hz]
ts = 1/fs                          # Sampling period [sc]
lamda = c/fc
t  = (0: ts: T)                    
t = np.arange(0, T, ts)

## Generate the transmit pulse

# Generate Transmit signal 

Tx_Signal = math.cos(2 * pi * fc * math.sin(2*pi*100 *t) );
spectrogram(Tx_Signal)

figure;
plot(t,Tx_Signal);
xlabel('time (in seconds)');
title('Signal versus Time');
zoom out; zoom out;

## Record the Received Signal

recordLength = length(Tx_Signal) * ts;          # Set up the same time as transmitting signal
recordObject = audiorecorder(fs, 24, 1);        # Sampling freq, bits, mono or stereo (channels)
record(recordObject, recordLength * 2);
pause(recordLength);
soundsc(Tx_Signal, fs, 24);                     # 24 bit sound, sampled at 44.1 kHz
pause(recordLength * 2);
stop(recordObject);

Rx_Signal = (getaudiodata(recordObject));      # Store recorded audio from object in double-precision array
Rx_Signal = bandpass(Rx_Signal, [(fc - 0.1*fc) (fc + 0.1*fc)], fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);
Rx_Signal = transpose(Rx_Signal);

## Plot Rx_Signal

time_s = 0: ts: (size(Rx_Signal, 2) - 1) * ts;

figure('Color','white');
plot(time_s,Rx_Signal);
title({'Received Signal', 'Continuous Wave'});
xlabel('Time [s]');
ylabel('Received Signal'); 
 
## Complex Downmixing of Transmit Pulse and Received Signal

# tp = downMix(ts, 0, fc, Tx_Signal, t);         # Complex downmix and LPF Transmit Pulse
# 
# time_rs = (0: 1: length(Rx_Signal)-1)*ts;
# 
# r = downMix(ts, 0, fc, Rx_Signal, time_rs);     # Complex downmix and LPF Received Signal


## Cut the received signal to transmitted signal's size

# [pks, locs] = findpeaks(abs(Rx_Signal), 'MinPeakHeight', 0.3);
# start = locs(4);
# last = locs(end);
# Rx_signal = Rx_Signal(1, start : ceil(last + (5 * T * ts)));

# averageNoise = max(abs(Rx_Signal(1, 100:1000)));
# index = find(Rx_Signal >= abs(averageNoise * 1.5), 10);
# startNumber = (index(1));
# Rx_Signal = Rx_Signal(1, startNumber: startNumber + (size(Tx_Signal,2)-1));         # Do this on matched filter signal

average = mean(abs(Rx_Signal(100:20000)));
[pks, locs] = findpeaks(Rx_Signal, 'MinPeakHeight',average*1e3);

Rx_Signal = Rx_Signal(locs(1):(locs(1)+size(Tx_Signal,2)-1));

# loc = 1;
# for i = length(Rx_Signal)
#    if  Rx_Signal(i) > Rx_Signal(i-1) * 10
#        loc = i;
#    end
# end

##

# 1. Zero pad the transmit pulse
# N3 = size(Tx_Signal, 2) - size(Rx_Signal, 2); 
# 
# Tx_Signal = [Tx_Signal zeros(1, abs(N3))];

ps = Tx_Signal.*Rx_Signal;

ps = lowpass(ps, (0.1*fc), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);

plot(time_s,ps);

## Plots

figure('Color','white');
subplot(2,1,1);
spectrogram(Rx_Signal);#xlim #Spectrogram do multiple ffts. look on website nfft
#meanfreq and medfreq
title('Spectrogram of Received Signal', 'fontsize', 12);
grid on;
colorbar;
colormap('jet');

subplot(2,1,2);
spectrogram(ps);
title('Spectrogram of Mixed Signal', 'fontsize', 12);
grid on;
colorbar;
colormap('jet');

# velocity = fd * lamda;

## Matched Filtering in the Frequency Domain to obtain Range Line

# RangeLine = matchedFilter(tp, r);
# 
# # Cut off the excess signal to just capture the peaks
# 
# [pks, locs] = findpeaks(abs(RangeLine), 'MinPeakDistance', (PRI/2) * ts, 'MinPeakHeight', 40);
# start = locs(4);
# last = locs(end);
# RangeLine = RangeLine(1, start : ceil(last + (5 * T * ts)));
# 
# 
# # averageNoise = max(abs(Rx_Signal(1, 100:1000)));
# # index = find(Rx_Signal >= abs(averageNoise * 1.5), 10);
# # startNumber = (index(4));
# # Rx_Signal = Rx_Signal(1, startNumber: startNumber + (size(Tx_Signal,2)-1));         # Do this on matched filter signal
# 
# timeRl = (0: 1: length(RangeLine) - 1) * ts;
# RangeLineAxis = timeRl * c / 2; 
# 
# figure('Color','white'); 
# plot(RangeLineAxis, dB(RangeLine));
# xlabel('Range [m]', 'fontsize', 12);
# ylabel('Matched Filter Output', 'fontsize', 12);
# title('Matched Filter Output', 'fontsize', 12);
# grid on; 
# 
# ## Reshape to a matrix: Range Line per transmitted pulse 
# 
# # NewNumPulses = NumPulses - 3;
# 
# if mod((length(RangeLine)/NumPulses), 1) ~= 0
#     temp = floor(length(RangeLine)/NumPulses) * NumPulses;
#     RangeLine = RangeLine(1: temp);
# end
#  
# RxSignalMatrix = transpose(reshape(RangeLine,  (size(RangeLine,2)/NumPulses), NumPulses));
# # RxSignalMatrix = transpose(reshape(RangeLine,  size(Rx_Signal,2)/NumPulses, NumPulses));
# 
# NumCols_RxSignalMatrix = size(RxSignalMatrix, 2);
# t_new = (0:1:(NumCols_RxSignalMatrix-1)) * ts;
# RangeLineAxis_New = t_new * c / 2;
# 
# # figure('Color','white'); 
# # imagesc( RangeLineAxis_New_m,1:NumPulses, 20*log10(abs(RxSignalMatrix)));
# # xlabel('Range (m)', 'fontsize', 12);
# # ylabel('Number of pulses', 'fontsize', 12); 
# # title('Simulated Range Line', 'fontsize', 12);
# # grid on;
# # colorbar;
# # colormap('jet');
# 
# 
# ## Window the Received signal and apply FFT in slow time
# 
# RangeMatrix = window(RxSignalMatrix);
# 
# figure('Color','white');
# imagesc( RangeLineAxis_New, 1: NumPulses, dB(RangeMatrix));
# xlabel('Range [m]', 'fontsize', 12);
# ylabel('Number of Pulses', 'fontsize', 12); 
# title('Simulated Range Line - Windowed Old', 'fontsize', 12);
# grid on;
# colorbar;
# colormap('jet');
# 
# ## Generate new Range Doppler Map with Windowing (Hamming) function
# 
# DopplerFreqAxis = (-N/2: 1: (N/2 - 1)) * PRF/N;  # Axis for Doppler Freq y
# VelocityAxis = DopplerFreqAxis * lamda / 2;       # Axis for velocity y
# RangeLineAxis_New = t_new*c/2;                # Range Axis for x
# 
# RangeDopplerMatrix = fftshift(fft(RxSignalMatrix, [], 1),1);
# 
# # figure('Color','white');                                                          # With Transpose
# # # imagesc( RangeLineAxis_New_m,1:NumPulses, 20*log10(abs(RangeDopplerMatrix')));              
# # imagesc( RangeLineAxis_New,1:NumPulses, 20*log10(abs(RangeMatrix')));
# # xlabel('Range [m]', 'fontsize', 12);
# # ylabel('Number of pulses', 'fontsize', 12); 
# # title('Simulated Range Line - Windowed New', 'fontsize', 12);
# # grid on;
# # colorbar;
# # colormap('jet');
# 
# figure('Color','white');
# # imagesc(RangeLineAxis_New_m, DopplerFreqAxis, 20*log10(abs(RangeDopplerMatrix))); 
# imagesc(RangeLineAxis_New, DopplerFreqAxis, 20*log10(abs(RangeMatrix))); 
# xlabel('Range [m]', 'fontsize', 12);
# ylabel('Doppler Frequency [Hz]', 'fontsize', 12); 
# title('Range-Doppler Map - Windowed', 'fontsize', 12);
# grid on;
# colorbar;
# colormap('jet');
# 
# figure('Color','white');
# spectrogram(Tx_p,128,120,128,1e3,'yaxis');
# title('Spectrogram - Windowed', 'fontsize', 12);
# grid on;
# colorbar;
# colormap('jet');
# 
# figure('Color','white');
# # imagesc(RangeLineAxis_New_m, VelocityAxis, 20*log10(abs(RangeDopplerMatrix))); 
# imagesc(RangeLineAxis_New, VelocityAxis, 20*log10(abs(RangeMatrix))); 
# xlabel('Range [m]', 'fontsize', 12);
# ylabel('Velocity [m/s]', 'fontsize', 12); 
# title('Range-Velocity Map - Windowed', 'fontsize', 12);
# grid on;
# colorbar;
# colormap('jet');
# axis xy
