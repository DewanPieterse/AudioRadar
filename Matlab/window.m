function [RangeMatrix] = window(RxSignalMatrix)

    % This function takes in a Matrix of the 
    % radar to perform windowing and FFT in slow time. The Matrix is also
    % corrected for the phase leakage experienced due to the sound card
    % introducing a phase delay in the transmitted signal.
    % It returns the matrix after going through a Hamming window and FFT.
    
    %  The FFT needs to be taken in the 'Slow Time' and this corresponds to the
    %  Pulse Repetition Frequency.
    
    n = size(RxSignalMatrix, 1);                            % RxSignalMatrix is a matrix nxm (NumPulses)
    m = size(RxSignalMatrix, 2);                            % We want to reproduce that but windowed.
    h = hamming(n);
    Window = repmat(h, 1, m);
    
    phaseLeakageVector = angle(RxSignalMatrix( : , 1));     % First column of received matrix
    phaseLeakageMatrix = repmat(phaseLeakageVector, 1, m);  % Reproduce the phase leakage correction matrix
    
%     RangeMatrix_Windowed = RxSignalMatrix .* Window;        % Window with W
    

    RangeMatrix_Window_PhaseLeak = RxSignalMatrix .* conj(phaseLeakageMatrix) .* Window;
    
    RangeMatrix = fft(RangeMatrix_Window_PhaseLeak, [], 1); % FFT windowed/phaseLeakage funtion
    
%     RangeMatrix = fftshift(RangeMatrix_FFT, 1);             
%     FFT Shift result for display - Display not necessary now
    
end