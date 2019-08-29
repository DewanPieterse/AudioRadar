
fs = 44.1e3; % Sampling frequency
ts = 1/fs; % Sampling period
N = length(test); % Number of points 
t = (0:1:(N-1))*ts; 

y = VarName1;

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

y = test;

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