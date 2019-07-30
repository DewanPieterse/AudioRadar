function [dB] = dB(signal)
    % This function takes in a signal.
    % It returns the signal in dB scale.
    
    dB = 20 * log10 ( abs( signal));
    
end


