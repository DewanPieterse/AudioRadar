close all;
clear all; 

f0 = 10; % start frequency of chirp
f1 = 50; % stop frequency of chirp
fs = 44.1e3; % Sampling frequency
ts = 1/fs; % Sampling period
PulseLength = 1;
mu = (f1 - f0)/PulseLength;
N = PulseLength*fs; % Number of points 
t = (0:1:(N-1))*ts; 

y = cos(2*pi*(f0*t + 0.5*mu*t.^2));

% plot our signal: time-domain
figure('Color','white');
plot(t, y,'Color',[0.8500, 0.3250, 0.0980],'LineWidth',1.5);
title(['Chirp Signal']);
xlabel('Time [s]');
ylabel('Amplitude');
grid on;

% Plot the spectrum: frequency domain
figure('Color','white'); 
FreqAxis_Hz = (-N/2:1:(N/2-1))*fs/N; 
fft_y = fftshift(fft(y));
plot(FreqAxis_Hz, 20*log10(abs(fft_y)),'Color',[0.8500, 0.3250, 0.0980],'LineWidth',1.5);
grid on; 
title('Magnitude of FFT');
ylabel('Magnitude |X(f)|');
xlabel('Frequency [Hz]');





