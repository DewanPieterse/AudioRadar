%% Hamming window theory
fs = 44.1e3;
ts = 1/fs;
N = 10e4;
ham = hamming(N);
t = (0:1:(N-1))*ts; 
x = sin(2*pi*10000*t);
% 
% FreqAxis_Hz = (-N/2:1:(N/2-1))*fs/N; 
% fft_y = fftshift(fft(y*ham));
% plot(FreqAxis_Hz, 20*log10(abs(fft_y)));
% grid on; 
% xlabel('Frequency (Hz)');
% ylabel('Magnitude of spectrum of y');
% title('MAX4466 Microphone - With Amp');

%%
Y = x'.*ham; 
Power_Y = sum(Y.^2) % power in time domain
fftY = fft(Y); 
Power_fftY = sum(fftY.*conj(fftY))/length(fftY) % power in frequency domain

subplot(311), plot(Y); % original signal
subplot(312), plot(abs(fftY)); % fft
subplot(313), plot(ifft(fftY)); % ifft

%%

ham = hamming(10e4);
[h,w] = freqz(ham,x,N);
plot(abs(h))

%%

N=16383;
Fs=1.024e6;
Ts=1/Fs;
hn=hamming(2048);
f = [0:N-1]/N;
hn_abs=(abs(fft(hn,N)));
hn_ss=hn_abs(1:N/2);
hn_dc(1)=hn_ss(1);
hn_rest(2:N/2)=2*hn_ss(2:N/2);
hn_final(1)=hn_rest(1);
hn_final(2:N/2)=(hn_rest(2:N/2))./sqrt(2);
op=mag2db(hn_final);
%f=(0:Fs/N:(Fs/2-Fs/N));
plot(f(1:N/2),op);