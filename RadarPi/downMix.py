#!/usr/bin/python3

import numpy as np
import cmath
import scipy.signal

def downMix(ts,B,fc,signal,time):
    # This function takes in sampling time, bandwidth of the chirp, center
    # frequency, the signal and the time over which it has been sampled.
    # It returns the down mixed and low pass filtered complex signal in baseband.
    
    fs = 1/ts
    pi = np.pi
    
    [numtaps, f] = 101, (fc + B/2)
    coeffsLowPass = scipy.signal.firwin(numtaps, f, pass_zero=False, fs=fs)#, window = "hamming")
    
    # I channel
    cos = np.cos(2 * pi * fc) * time
    
    I_tp = np.multiply(signal, np.transpose(cos))
    I_tp_LPF = scipy.signal.convolve(I_tp, coeffsLowPass)

    # Q channel
    sin = -np.sin(2 * pi * fc ) * time
    Q_tp = np.multiply(signal, np.transpose(sin))
    Q_tp_LPF = scipy.signal.convolve(Q_tp, coeffsLowPass)
    
#     print(np.iscomplex(I_tp_LPF + (1j * Q_tp_LPF)))

    return I_tp_LPF + (1j * Q_tp_LPF)