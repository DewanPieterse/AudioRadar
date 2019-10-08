## Audio Radar Simulation and Real World

# Author:       Dewan Pieterse
# Supervisor:   Dr. Y. Abdul Gaffar
# Date:         June 2019

## Define constants and parameters

## Import relevant packages

import numpy as np
import math
from scipy import signal
import matplotlib.pyplot as plt
from waveGenerator import pulseGenerator, pulseTrainGenerator, waveGenerator
from rect import rect

# Radar parameters
# Parameters for editing

fc = 10e3                          # Center Frequency [Hz]
B = 4e3
T = 100/B                          # Pulse length in [s]
UnambigRange = 10                  # Unambiguous Range [m] (0.5 - 10)
RangeResolution = 0.5              # Range Resolution [m]  (0.05 - 2)
NumPulses = 35                     # Number of pulses      (typically 32)

c = 343                            # speed of sound [m/s]

PRI = (2 * UnambigRange) / c       # Pulse Repetition Interval [s]

# B = (2 * RangeResolution) / c;      # Bandwidth [Hz] 
PulseCompressionGain = T * B       # Pulse Compression needs to be higher than 100 to ensure 13dB between sidelobe and mainlobe. 

# Fixed parameters

fs = 44.1e3                        # Sampling rate by soundcard [Hz]
ts = 1/fs                          # Sampling period [s]
# R_max = c * PRI / 2;                # Maximum range of target to simulate
PRF = 1/PRI                        # Hz
t_max = PRI*NumPulses              # Maximum time to simulate 
K = B/T                            # Chirp rate
t  = (0:ts:(t_max-ts))             # Time vector (in seconds)
# NumSamplesInPRI = round(PRI*fs);

# Target parameters for when Rx is simulated
# R_target = 3;                       # Target range                                                      ONLY USED WHEN SIMULATING RX
# Vel_target = 0.00;                  # Target radial velocity in m/s                                     ONLY USED WHEN SIMULATING RX
# td = 2 * R_target / c;              # Time taken for signal to travel to target and back to the radar   ONLY USED WHEN SIMULATING RX

## Calculate and display radar parameters

# lamda = c/fc;
# BlindRange_m = c*T/2/PulseCompressionGain;
# UnambiguousRange_m = c*PRI/2;
# RangeResolution_m = c/(2*B);
# UnambiguousVelocity_cms = PRF/2*lamda/2*100;
# 

## Generate the transmit pulse

# Generate Transmit signal 

Tx_Signal = zeros(1, size(t,2));

for Count_PulseNum = 1: NumPulses
    tdn = PRI * (Count_PulseNum - 1);
    Tx_Signal = Tx_Signal +  cos(2*pi*(fc*(t - T/2 - tdn) + 0.5 * K * (t - T/2 - tdn)**2) ) * rect( (t - T/2 - tdn)/T );
end

figure; plot(t, Tx_Signal);
xlabel('Time (s)');
ylabel('Transmit Signal'); 

# soundsc(Tx_Signal, fs, 24); # 24 bit sound, sampled at 44.1 kHz

# Generate the transmit pulse 
NumSamplesTxPulse = ceil(T/ts);             # number of samples of the transmit pulse 
Tx_p = Tx_Signal(1: NumSamplesTxPulse);     # transmit pulse only

## Testing Chirp

t = 0: ts: T-ts;
y = (chirp(t, fc - B/2 - 1, t(end), fc + B/2 + 1));

soundsc(y,fs,24);

N = round(T/ts);
plot(t,y);
frequency = (-N/2: 1: (N/2-2)) * fs/N;
f = fftshift(fft(y));
figure(2);
plot(frequency, 20*log10(abs(f)));

## Generate the range line for multiple pulses, assuming a moving target
#  This is for simulation and a receive signal will be produced instead of
#  listened for.
 
# Generate the Received Signal

# Rx_Signal = zeros(1, size(t,2));
# 
# for Count_PulseNum = 1: NumPulses
#     tdn = 2*(R_target - Vel_target*PRI*(Count_PulseNum - 1))/c + PRI*(Count_PulseNum - 1); 
#     Rx_Signal = Rx_Signal +  1*(cos(2*pi*(fc*(t - T/2 - tdn) + 0.5*K*(t - T/2 - tdn).^2) ).* rect( (t - T/2 - tdn)/T ));  # received signal   
# end

## Record audio using microphone

recordLength = length(Tx_Signal);               # Set up the same time as transmitting signal
# recordSamples = (recordLength * ts);
recordSamples = NumPulses * PRI;

# soundsc(Tx_Signal, fs, 24); # 24 bit sound, sampled at 44.1 kHz

recordObject = audiorecorder(fs, 24, 1);        # Sampling freq, bits, mono or stereo (channels)

# recordblocking(recordObject, 2);    # Records audio for same time as transmitting signal
record(recordObject, recordSamples*8);
pause(1.5);
soundsc(Tx_Signal, fs, 24); # 24 bit sound, sampled at 44.1 kHz
pause(recordSamples + 0.5);
stop(recordObject);
pause(0.5);
play(recordObject);

Rx_Signal = (getaudiodata(recordObject))'      # Store recorded audio from object in double-precision array
Rx_Signal = highpass(Rx_Signal, (fc/2), fs,'ImpulseResponse','fir','Steepness',0.8);
plot(Rx_Signal);

## Just some tests to see if the bandpass filter in matlab works - It does
figure;plot(Rx_Signal);
figure;
N = length(Rx_Signal);
rxfft = fftshift(fft(Rx_Signal));
ffttime = (-N/2:1:(N/2-1))*fs/N; 
plot(ffttime, rxfft);
# 
# 
# Rx_Signal1 = bandpass(Rx_Signal, [(fc - B/2) (fc + B/2)], fs,'ImpulseResponse','fir','Steepness',0.8);
# figure;
# N = length(Rx_Signal1);
# rxfft1 = fftshift(fft(Rx_Signal1));
# ffttime1 = (-N/2:1:(N/2-1))*fs/N; 
# plot(ffttime1, rxfft1);

## Bandpass Filter on received signal

# filterCoefficients = [-0.0385061425231694;
#                       0.0203869018338601;
#                       0.0113981054825192;
#                       0.00913082525901292;
#                       0.109155438611511;
#                       0.0527275092744292;
#                       -0.222624280377525;
#                       -0.161123944895586;
#                       0.257658550220670;
#                       0.257658550220670;
#                       -0.161123944895586;
#                       -0.222624280377525;
#                       0.0527275092744292;
#                       0.109155438611511;
#                       0.00913082525901292;
#                       0.0113981054825192;
#                       0.0203869018338601;
#                       -0.0385061425231694]';
    
# Rx_Signal = filter(filterCoefficients, 1, Rx_Signal);

Rx_Signal = bandpass(Rx_Signal, [(fc - B/2) (fc + B/2)], fs,'ImpulseResponse','fir','Steepness',0.8);

## Exercise 6: Do matched filtering first and then reshaping

# Matched filter in frequency domain

# Perform complex down-mixing on the transmit pulse
# b = [ -0.001905049334911;
#       -0.006629787329332;
#       0.007066797068609;
#       0.026155865376474;
#       -0.014229857484611;
#       -0.078377748412724;
#       0.020814383984572;
#       0.308023347098905;
#       0.476507451532680;
#       0.308023347098905;
#       0.020814383984572;
#       -0.078377748412724;
#       -0.014229857484611;
#       0.026155865376474;
#       0.007066797068609;
#       -0.006629787329332;
#       -0.001905049334911]';

# I channel
time_tp = (0:1:(NumSamplesTxPulse-1)) * ts;
I_tp = Tx_p .* cos(2*pi*fc*time_tp); 
# I_tp_LPF = filter(b, 1, I_tp);
I_tp_LPF = lowpass(I_tp, (fc + B/2), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.8);

## Test matlab low pass filter - works same as with coefficients
# figure;
# plot(I_tp)
# figure;
# plot(I_tp_LPF)
# 
# I_tp_LPF1 = lowpass(I_tp, (fc + B/2), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.8);
# figure;
# plot(I_tp_LPF1);

##

# Q channel
Q_tp = Tx_p .* -sin(2 * pi * fc * time_tp);
# Q_tp_LPFold = filter(b, 1, Q_tp);
Q_tp_LPF = lowpass(Q_tp, (fc + B/2), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.8);

# figure;
# plot(Q_tp)
# figure;
# plot(Q_tp_LPFold)
# figure;
# plot(Q_tp_LPF);


##
# Complex output signal
Complex_tp_bb = I_tp_LPF + 1i*Q_tp_LPF;

tp = Complex_tp_bb; 


# Perform complex down-mixing on the received signal

# I channel
I_Rx = Rx_Signal .* cos(2 * pi * fc * t); 
# I_Rx_LPF = filter(b, 1, I_Rx);
I_Rx_LPF = lowpass(I_Rx, (fc + B/2), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.8);

# Q channel
Q_Rx = Rx_Signal .* -sin(2 * pi * fc * t);
# Q_Rx_LPF = filter(b, 1, Q_Rx);
Q_Rx_LPF = lowpass(Q_Rx, (fc + B/2), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.8);

# Complex output signal
r = I_Rx_LPF + 1i*Q_Rx_LPF;


# Perform  matched filtering in the frequency domain

# 1. Zero pad the transmit pulse
N1 = size(tp, 2);
N2 = size(r, 2);
N3 = N2 - N1;

tp_ZP = [tp zeros(1, N3)];

# 2. Find FFT_conj_tp_ZP

FFT_conj_tp_ZP = conj(fft(tp_ZP));

# 3. Find FFT_r

FFT_r = fft(r);

# 4. Compute the matched filter output
RangeLine = ifft( FFT_conj_tp_ZP.*FFT_r);

figure; 
RangeLineAxis_m = t * c / 2; 
plot(RangeLineAxis_m, 20 * log10(abs(RangeLine)));
xlabel('Range [m]');
ylabel('Matched Filter output');
grid on; 


# Reshape to a matrix: Range Line per transmitted pulse

rows = ceil(size(RangeLine, 2) / NumPulses);
cols = NumPulses;
reshapeSize = rows * cols;
reshapeSizeDiff = size(RangeLine, 2) - reshapeSize;
# if reshapeSizeDiff > 0
#     RangeLine = [];
# end
RangeLine = resample(RangeLine, (reshapeSize), (size(RangeLine, 2)));

RxSignalMatrix = reshape(RangeLine, rows, cols);
RxSignalMatrix = transpose(RxSignalMatrix);

figure; 
NumCols_RxSignalMatrix = size(RxSignalMatrix, 2);
t_new = (0: 1: (NumCols_RxSignalMatrix - 1)) * ts;
RangeLineAxis_New_m = t_new * c / 2;

imagesc( RangeLineAxis_New_m,1:NumPulses, 20*log10(abs(RxSignalMatrix)));
xlabel('Range (m)', 'fontsize', 12);
ylabel('Number of pulses', 'fontsize', 12); 
title('Simulated range line', 'fontsize', 12);
grid on;
colorbar;
colormap('jet');


## Window the Received signal

n = size(RxSignalMatrix, 1);# RxSignalMatrix is a matrix nxm (NumPulses)
m = size(RxSignalMatrix, 2);# We want to reproduce that but windowed.
h = hamming(n);
W = repmat(h, 1, m);

## Generate new Range Doppler Map with Windowing (Hamming) function
#  The FFT needs to be taken in the 'Slow Time' and this corresponds to the
#    Pulse Repetition Frequency.

N = n;                  # Numer of Pulses
#fs = PRF;               # Sampling frequency

DopplerFreqAxis = (-N/2: 1: (N/2 - 1)) * PRF/N;  # Axis for Doppler Freq y
VelocityAxis = DopplerFreqAxis * lamda/2;       # Axis for velocity y
RangeLineAxis_New_m = t_new*c/2;                # Range Axis for x

RangeDopplerMatrix_Windowed = RxSignalMatrix .* W;          # Window with W
RangeDopplerMatrix_FFT = fft(RangeDopplerMatrix_Windowed);  # FFT windowed funtion
RangeDopplerMatrix = fftshift(RangeDopplerMatrix_FFT);      # FFT Shift result for display


# Displaying Range Doppler Map - Windowed using the Hamming Function
#   (Raised cosine).

figure;
imagesc(RangeLineAxis_New_m, DopplerFreqAxis, 20*log10(abs(RangeDopplerMatrix)));
xlabel('Range [m]');
ylabel('Doppler Frequency [Hz]');
title('Windowed Range-Doppler Map');
colorbar;
colormap('jet');
grid on;


# Plotting the velocity of objects instead of the Doppler Frequency

figure;
imagesc(RangeLineAxis_New_m, VelocityAxis, 20*log10(abs(RangeDopplerMatrix))); 
xlabel('Range [m]');
ylabel('Velocity [m/s]');
title('Windowed Range-Velocity Map');
colorbar;
colormap('jet');
grid on;
axis xy;                                # Used to flip vertically

## Generate the Range Doppler Map (Unwindowed)
# 
#     # apply FFT in the slow-time dimension to generate the Range-Doppler
#     # map
#     N = NumPulses;
#     #fs = PRF; 
#     DopplerFreq_Hz = (-N/2:1:(N/2-1))*PRF/N; 
# 
#     RangeDopplerMatrix = fftshift(fft(RxSignalMatrix, [], 1),1);
#     figure;
#     imagesc(RangeLineAxis_New_m, DopplerFreq_Hz, 20*log10(abs(RangeDopplerMatrix))); 
#     grid on;
#     colorbar;
#     colormap('jet');
#     xlabel('Range (m)');
#     ylabel('Doppler Frequency (Hz)');
#     title('Range-Doppler map'); 
# 
#     VelocityAxis = DopplerFreq_Hz*lamda/2; 
#     figure;
#     imagesc(RangeLineAxis_New_m, VelocityAxis, 20*log10(abs(RangeDopplerMatrix))); 
#     grid on;
#     colorbar;
#     colormap('jet');
#     xlabel('Range (m)');
#     ylabel('Velocity (m/s)');
#     title('Range-Velocity map'); 
#     axis xy

  
