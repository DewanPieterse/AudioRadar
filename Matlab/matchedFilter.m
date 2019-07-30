function [RangeLine] = matchedFilter(tp,r)
    % This function takes in Complex Downmixed Received Signal and the
    % Complex Downmixed Transmitted Pulse.
    % It returns the Range Line.
    
    % 1. Zero pad the transmit pulse
    N1 = size(tp, 2);
    N2 = size(r, 2);
    N3 = N2 - N1; 

    tp_ZP = [tp zeros(1, N3)];

    % 2. Find FFT_conj_tp_ZP
    FFT_conj_tp_ZP = conj(fft(tp_ZP));

    % 3. Find FFT_r
    FFT_r = fft(r);

    % 4. Compute the matched filter output
    RangeLine = ifft(FFT_conj_tp_ZP .* FFT_r);
    
end


