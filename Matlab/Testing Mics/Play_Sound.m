
clear all;
close all;
clc;

SpeedSoundWave_ms = 343;           
Fc_Hz = 16e3;     % change this value to hear audio tone at different frequencies                 
PulseWidth_s = 5;    % change to adjust how long audio tone plays out              
Fs = 44.1e3;                   
Ts = 1/Fs;                        
t = 0:Ts:(PulseWidth_s);         

TxPulse = sin(2*pi*Fc_Hz*t);

% figure;
% axes('fontsize', 12);
% plot(t,TxPulse);
% xlabel('Time (s)', 'fontsize', 12);
% ylabel('Amplitude (linear)', 'fontsize', 12);
% title('Transmit pulse', 'fontsize', 12);

NumOfZeros = 1;
TransmitSignal = [zeros(1, NumOfZeros) 1*sin(2*pi*Fc_Hz*t) zeros(1, NumOfZeros)];
TimeAxis_TxSignal_s = (0:1:(length(TransmitSignal)-1))*1/Fs;


soundsc(TransmitSignal,Fs, 24) 



