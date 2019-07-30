function [complex] = downMix(ts,B,fc,signal,time)
    % This function takes in sampling time, bandwidth of the chirp, center
    % frequency, the signal and the time over which it has been sampled.
    % It returns the down mixed and low pass filtered complex signal in baseband.
    
    fs = 1/ts;
    
    % I channel
    I_tp = signal .*  cos(2 * pi * fc * time); 
    I_tp_LPF = lowpass(I_tp, (fc + B/2), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);

    % Q channel
    Q_tp = signal .* -sin(2 * pi * fc * time);
    Q_tp_LPF = lowpass(Q_tp, (fc + B/2), fs, 'ImpulseResponse', 'fir', 'Steepness', 0.95);

    complex = I_tp_LPF + 1i*Q_tp_LPF;
    
end

