%% Audio Radar Simulation and Real World

% Author:       Dewan Pieterse
% Supervisor:   Dr. Y. Abdul Gaffar
% Date:         June 2019

%% Clear variables and command window
clear all; close all; clc;

%% Define constants and parameters

% Radar parameters

fc = 10e3;                           % Center Frequency [Hz]
B = 4e3;                            % Bandwidth [Hz] 
T = 100/B;                          % Pulse length in [s]                       T < PRI/2
UnambigRange = 10;                   % Unambiguous Range [m] (0.5 - 10)
RangeResolution = 0.5;              % Range Resolution [m]  (0.05 - 2)
NumPulses = 35;                     % Number of pulses      (typically 32)

c = 343;                            % speed of sound [m/s]
PRI = (2 * UnambigRange) / c;       % Pulse Repetition Interval [s]
PulseCompressionGain = T * B;       % Pulse Compression needs to be higher than 100 to ensure 13dB between sidelobe and mainlobe. 
fs = 44.1e3;                        % Sampling rate by soundcard [Hz]
ts = 1/fs;                          % Sampling period [sc]
PRF = 1/PRI;                        % Hz
t_max = PRI * NumPulses;            % Maximum time to simulate 
lamda = c/fc;
t  = (0:ts:(t_max-ts));             % Time vector (in seconds)

K = B/T;                            % Chirp rate


%% Generate the transmit pulse

% Generate Transmit signal 

% Tx_Signal = [];
tau = 0: ts: T;
bufTime = 0: ts: (PRI-T)-ts;
chirpSig = chirp(tau, fc - B/2, tau(end), fc + B/2, 'linear');

% for Count_PulseNum = 1: NumPulses    
%     Tx_Signal = [Tx_Signal chirpSig zeros(1, size(bufTime,2))];
% end

Tx_Signal = zeros(1, size(t,2));

 for count = 1: NumPulses
     tdn = PRI * (count - 1);
     Tx_Signal = Tx_Signal +  cos(2*pi*(fc*(t - T/2 - tdn) + 0.5*K*(t - T/2 - tdn).^2) ).* rect( (t - T/2 - tdn)/T );  % received signal 
 end

figure('Color','white'); 
plot(t, Tx_Signal);
title('Transmit Signal');
xlabel('Time [s]');
ylabel('Transmit Signal'); 

% Generate the transmit pulse 
N = ceil(T / ts);                     % number of samples of the transmit pulse 
Tx_p = Tx_Signal(1: N);             % transmit pulse only

% time = 0: ts: (length(Tx_Signal)-1)*ts;
% figure('Color','white'); 
% plot(time, Tx_Signal);
% title({'Transmit Signal', [num2str(NumPulses), ' Chirps']});
% xlabel('Time [s]');
% ylabel('Transmit Signal'); 

%% Record the Received Signal

recordLength = length(Tx_Signal) * ts;          % Set up the same time as transmitting signal
recordSamples = NumPulses * PRI;
recordObject = audiorecorder(fs, 24, 1);        % Sampling freq, bits, mono or stereo (channels)
record(recordObject, recordLength * 2);
pause(2);
soundsc(Tx_Signal, fs, 24);                     % 24 bit sound, sampled at 44.1 kHz
pause(recordLength * 2);
stop(recordObject);

Rx_Signal = (getaudiodata(recordObject));      % Store recorded audio from object in double-precision array
Rx_Signal = bandpass(Rx_Signal, [(fc - B/2) (fc + B/2)], fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);
Rx_Signal = transpose(Rx_Signal);
averageNoise = max(abs(Rx_Signal(1, 100:1000)));
index = find(Rx_Signal >= abs(averageNoise * 1.5), 10);
startNumber = (index(4));
Rx_Signal = Rx_Signal(1, startNumber: startNumber + (size(Tx_Signal,2)-1));         % Do this on matched filter signal

% start = (size(Rx_Signal,2) - size(Tx_Signal,2));
% Rx_Signal = Rx_Signal(1, start:size(Rx_Signal,2));

%% Plot Rx_Signal

time_s = 0: ts: (size(Rx_Signal,2)-1)*ts;

figure('Color','white');
plot(time_s,Rx_Signal);
title({'Received Signal', [num2str(NumPulses), ' Chirps']});
xlabel('Time [s]');
ylabel('Received Signal'); 
 
%% Complex Downmixing of Transmit Pulse and Received Signal

time_tp = (0:1:(N-1)) * ts;

tp = downMix(ts, B, fc, Tx_p, time_tp);         % Complex downmix and LPF Transmit Pulse


time_rs = (0: 1: length(Rx_Signal)-1)*ts;

r = downMix(ts, B, fc, Rx_Signal, time_rs);     % Complex downmix and LPF Received Signal

%% Matched Filtering in the Frequency Domain to obtain Range Line

RangeLine = matchedFilter(tp, r);
RangeLineAxis = time_rs * c / 2; 

figure('Color','white'); 
plot(RangeLineAxis, dB(RangeLine));
xlabel('Range [m]', 'fontsize', 12);
ylabel('Matched Filter Output', 'fontsize', 12);
title('Matched Filter Output', 'fontsize', 12);
grid on; 

%% Reshape to a matrix: Range Line per transmitted pulse 

% NewNumPulses = NumPulses - 3;

if mod((length(RangeLine)/NumPulses), 1) ~= 0
    temp = floor(length(RangeLine)/NumPulses) * NumPulses;
    RangeLine = RangeLine(1: temp);
end
 
RxSignalMatrix = transpose(reshape(RangeLine,  (size(RangeLine,2)/NumPulses), NumPulses));
% RxSignalMatrix = transpose(reshape(RangeLine,  size(Rx_Signal,2)/NumPulses, NumPulses));

NumCols_RxSignalMatrix = size(RxSignalMatrix, 2);
t_new = (0:1:(NumCols_RxSignalMatrix-1)) * ts;
RangeLineAxis_New = t_new * c / 2;

% figure('Color','white'); 
% imagesc( RangeLineAxis_New_m,1:NumPulses, 20*log10(abs(RxSignalMatrix)));
% xlabel('Range (m)', 'fontsize', 12);
% ylabel('Number of pulses', 'fontsize', 12); 
% title('Simulated Range Line', 'fontsize', 12);
% grid on;
% colorbar;
% colormap('jet');


%% Window the Received signal and apply FFT in slow time

RangeMatrix = window(RxSignalMatrix);

figure('Color','white');
imagesc( RangeLineAxis_New, 1: NumPulses, dB(RangeMatrix));
xlabel('Range [m]', 'fontsize', 12);
ylabel('Number of Pulses', 'fontsize', 12); 
title('Simulated Range Line - Windowed Old', 'fontsize', 12);
grid on;
colorbar;
colormap('jet');

%% Generate new Range Doppler Map with Windowing (Hamming) function

DopplerFreqAxis = (-N/2: 1: (N/2 - 1)) * PRF/N;  % Axis for Doppler Freq y
VelocityAxis = DopplerFreqAxis * lamda / 2;       % Axis for velocity y
RangeLineAxis_New = t_new*c/2;                % Range Axis for x

RangeDopplerMatrix = fftshift(fft(RxSignalMatrix, [], 1),1);

% figure('Color','white');                                                          % With Transpose
% % imagesc( RangeLineAxis_New_m,1:NumPulses, 20*log10(abs(RangeDopplerMatrix')));              
% imagesc( RangeLineAxis_New,1:NumPulses, 20*log10(abs(RangeMatrix')));
% xlabel('Range [m]', 'fontsize', 12);
% ylabel('Number of pulses', 'fontsize', 12); 
% title('Simulated Range Line - Windowed New', 'fontsize', 12);
% grid on;
% colorbar;
% colormap('jet');

figure('Color','white');
% imagesc(RangeLineAxis_New_m, DopplerFreqAxis, 20*log10(abs(RangeDopplerMatrix))); 
imagesc(RangeLineAxis_New, DopplerFreqAxis, 20*log10(abs(RangeMatrix))); 
xlabel('Range [m]', 'fontsize', 12);
ylabel('Doppler Frequency [Hz]', 'fontsize', 12); 
title('Range-Doppler Map - Windowed', 'fontsize', 12);
grid on;
colorbar;
colormap('jet');

figure('Color','white');
spectrogram(Tx_p,128,120,128,1e3,'yaxis');
title('Spectrogram - Windowed', 'fontsize', 12);
grid on;
colorbar;
colormap('jet');

figure('Color','white');
% imagesc(RangeLineAxis_New_m, VelocityAxis, 20*log10(abs(RangeDopplerMatrix))); 
imagesc(RangeLineAxis_New, VelocityAxis, 20*log10(abs(RangeMatrix))); 
xlabel('Range [m]', 'fontsize', 12);
ylabel('Velocity [m/s]', 'fontsize', 12); 
title('Range-Velocity Map - Windowed', 'fontsize', 12);
grid on;
colorbar;
colormap('jet');
axis xy
