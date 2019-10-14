%%
close all;clc;
figure;semilogx(Frequency,GainMAX9814,'LineWidth',2.0);title('RS Pro 2W');set(gcf,'color','w');xlabel('Frequency [Hz]');ylabel('Gain [dB]');
figure;semilogx(Frequency,GainMAX4466edit,'LineWidth',2.0);title('Visaton 2W');set(gcf,'color','w');xlabel('Frequency [Hz]');ylabel('Gain [dB]');
figure;semilogx(Frequency,GainMAX9814edit,'LineWidth',2.0);title('RS Pro 1W');set(gcf,'color','w');xlabel('Frequency [Hz]');ylabel('Gain [dB]');
% figure;semilogx(Frequency,GainMAX4466edit);title('MAX4466 Edit');

%%
in = 3.3;
Gain = 20.*log10(VarName8);
figure;semilogx(Frequency,Gain,'LineWidth',2.0);title('MAX4466');set(gcf,'color','w');xlabel('Frequency [Hz]');ylabel('Gain [dB]');