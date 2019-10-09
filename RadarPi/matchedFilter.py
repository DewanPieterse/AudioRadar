#!/usr/bin/python3

import numpy as np
import cmath
import scipy.signal as signal
from scipy.fftpack import fft, ifft

def matchedFilter(tp,r):
    # This function takes in Complex Downmixed Received Signal and the
    # Complex Downmixed Transmitted Pulse.
    # It returns the Range Line.
    
#     tp = np.flip(tp)
    
    # 1. Zero pad the transmit pulse
    N1 = len(tp)
    N2 = len(r)
    N3 = N2 - N1; 

    tp_ZP = np.pad(tp, (0, N3), 'constant')
#     tp_ZP = np.flip(tp_ZP)

    # 2. Find FFT_conj_tp_ZP
    FFT_conj_tp_ZP = np.conj(fft(tp_ZP))

    # 3. Find FFT_r
    FFT_r = fft(r)

    # 4. Compute the matched filter output
    
    fftTpR = ifft(FFT_conj_tp_ZP * FFT_r)
    
    return fftTpR
    


