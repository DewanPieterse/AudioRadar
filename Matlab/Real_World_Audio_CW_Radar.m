%% Audio Radar Simulation and Real World - Continuous Wave

% Author:       Dewan Pieterse
% Supervisor:   Dr. Y. Abdul Gaffar
% Date:         June 2019

%% Clear variables and command window
clear all; close all; clc;

%% Define constants and parameters

% Radar parameters

fc = 8e3;                           % Center Frequency [Hz]
T = 5;                              % Pulse length in [s]
c = 343;                            % speed of sound [m/s]
fs = 44.1e3;                        % Sampling rate by soundcard [Hz]
ts = 1/fs;                          % Sampling period [sc]
lamda = c/fc;
t  = (0: ts: T);                    % Time vector (in seconds)

%% Generate the transmit pulse

% Generate Transmit signal 

Tx_Signal = cos(2 * pi * fc*t );
spectrogram(Tx_Signal)

figure;
plot(t,Tx_Signal);
xlabel('time (in seconds)');
title('Signal versus Time');
zoom out; zoom out;

%% Record the Received Signal

recordLength = length(Tx_Signal) * ts;          % Set up the same time as transmitting signal
recordObject = audiorecorder(fs, 24, 1);        % Sampling freq, bits, mono or stereo (channels)
record(recordObject, recordLength * 2);
pause(recordLength);
soundsc(Tx_Signal, fs, 24);                     % 24 bit sound, sampled at 44.1 kHz
pause(recordLength * 2);
stop(recordObject);

Rx_Signal = (getaudiodata(recordObject));      % Store recorded audio from object in double-precision array
Rx_Signal = bandpass(Rx_Signal, [(fc - 0.1*fc) (fc + 0.1*fc)], fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);
Rx_Signal = transpose(Rx_Signal);

%% Plot Rx_Signal

time_s = 0: ts: (size(Rx_Signal, 2) - 1) * ts;

figure('Color','white');
plot(time_s,Rx_Signal);
title({'Received Signal', 'Continuous Wave'});
xlabel('Time [s]');
ylabel('Received Signal'); 
 
%% Complex Downmixing of Transmit Pulse and Received Signal

% tp = downMix(ts, 0, fc, Tx_Signal, t);         % Complex downmix and LPF Transmit Pulse
% 
% time_rs = (0: 1: length(Rx_Signal)-1)*ts;
% 
% r = downMix(ts, 0, fc, Rx_Signal, time_rs);     % Complex downmix and LPF Received Signal


%% Cut the received signal to transmitted signal's size

% [pks, locs] = findpeaks(abs(Rx_Signal), 'MinPeakHeight', 0.3);
% start = locs(4);
% last = locs(end);
% Rx_signal = Rx_Signal(1, start : ceil(last + (5 * T * ts)));

% averageNoise = max(abs(Rx_Signal(1, 100:1000)));
% index = find(Rx_Signal >= abs(averageNoise * 1.5), 10);
% startNumber = (index(1));
% Rx_Signal = Rx_Signal(1, startNumber: startNumber + (size(Tx_Signal,2)-1));         % Do this on matched filter signal

average = mean(abs(Rx_Signal(100:20000)));
[pks, locs] = findpeaks(Rx_Signal, 'MinPeakHeight',average*1e3);

Rx_Signal = Rx_Signal(locs(1):(locs(1)+size(Tx_Signal,2)-1));

% loc = 1;
% for i = length(Rx_Signal)
%    if  Rx_Signal(i) > Rx_Signal(i-1) * 10
%        loc = i;
%    end
% end

%%

% 1. Zero pad the transmit pulse
% N3 = size(Tx_Signal, 2) - size(Rx_Signal, 2); 
% 
% Tx_Signal = [Tx_Signal zeros(1, abs(N3))];

ps = Tx_Signal.*Rx_Signal;

ps = lowpass(ps, (0.1*fc), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);

plot(time_s,ps);

%% Plots

figure('Color','white');
subplot(2,1,1);
spectrogram(Rx_Signal);%xlim %Spectrogram do multiple ffts. look on website nfft
%meanfreq and medfreq
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

% velocity = fd * lamda;
