% clear all;clc;close all;

% open('withAmp.mat');
% open('withoutAmp.mat');
% VarName1 = xlsread('./Suspended Mic Testing/15000.xlsx');

% test1 = load ('withAmp.mat');
% test1 = test1.unnamed;
% test2 = load ('withoutAmp.mat');
% test2 = test2.unnamed;

test1 = Rx_Signal;

fs = 44.1e3; % Sampling frequency
ts = 1/fs; % Sampling period
N = length(test1); % Number of points 
t = (0:1:(N-1))*ts; 

y = test1;

% plot our signal: time-domain
figure;
plot(t, y, 'r'); % t : x- axis, y: y -axis
xlabel('Time (s)');
ylabel('Signal y');
grid on; 

% Plot the spectrum: frequency domain
figure; 
FreqAxis_Hz = (-N/2:1:(N/2-1))*fs/N; 
fft_y = fftshift(fft(y));
plot(FreqAxis_Hz, 20*log10(abs(fft_y)));
grid on; 
xlabel('Frequency (Hz)');
ylabel('Magnitude of spectrum of y');
title('MAX4466 Microphone - With Amp');

% pks = findpeaks(real(20*log(fft_y)),'MinPeakDistance',25)

%%
y = test2;

% plot our signal: time-domain
figure;
plot(t, y, 'r'); % t : x- axis, y: y -axis
xlabel('Time (s)');
ylabel('Signal y');
grid on;

% Plot the spectrum: frequency domain
figure; 
FreqAxis_Hz = (-N/2:1:(N/2-1))*fs/N; 
fft_y = fftshift(fft(y));
plot(FreqAxis_Hz, 20*log10(abs(fft_y)));
grid on; 
xlabel('Frequency (Hz)');
ylabel('Magnitude of spectrum of y');
title('MAX9814 Microphone - No Amp');

%%

[y,Fs] = audioread('recordedAudio.wave');
sound(y,Fs)

t = 0:seconds(1/Fs):seconds(info.Duration);
t = t(1:end-1);

plot(t,y)
xlabel('Time')
ylabel('Audio Signal')