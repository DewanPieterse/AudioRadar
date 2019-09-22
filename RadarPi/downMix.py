#!/usr/bin/python3

import numpy as np
import cmath
import scipy.signal as signal

def downMix(ts,B,fc,signal,time):
    # This function takes in sampling time, bandwidth of the chirp, center
    # frequency, the signal and the time over which it has been sampled.
    # It returns the down mixed and low pass filtered complex signal in baseband.
    
    fs = 1/ts
    pi = np.pi
    
    [numtaps, f] = 101, (fc + B/2)
    coeffsLowPass = signal.firwin(numtaps, [f1, f2], pass_zero=False, fs=fs)#, window = "hamming")
    
    # I channel
    I_tp = signal * cos(2 * pi * fc * time)
    I_tp_LPF = signal.convolve(I_tp, coeffsLowPass)

    # Q channel
    Q_tp = signal * -sin(2 * pi * fc * time)
    Q_tp_LPF = signal.convolve(Q_tp, coeffsLowPass)

    return complex(I_tp_LPF ,Q_tp_LPF)