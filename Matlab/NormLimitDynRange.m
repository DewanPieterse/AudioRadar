

%NormLimitDynRange
% Normalises the peak to 0dB and limits the dynamic range of a matrix (linear) for plotting purposes only
%                         
%
%SYNTAX:
% [MatrixNormDynRangeLimited_dB]=NormLimitDynRange(MatrixLinear,DynamicRange_dB)
%
%ARGUMENTS/INPUTS:
% MatrixLinear - matrix of values in linear units
% DynamicRange_dB - dynamic range to limit matrix values in dBs (positive number)
%
%DETAILED DESCRIPTION:
%Limit the dynamic range values in a matrix 
% 
%SEE ALSO:
% 
%
%AUTHOR:
%Yunus Abdul Gaffar
%
%
%REVISION HISTORY:
% 
%(2015-09-04) - Created

function [ MatrixNormDynRangeLimited_dB ] = NormLimitDynRange( MatrixLinear,DynamicRange_dB)

Matrix_dB = 20*log10(abs(MatrixLinear));
MaxValMatrix_dB = max(max(Matrix_dB));
RangeDopplerMapNorm_dB = Matrix_dB - MaxValMatrix_dB;

IndxVec = RangeDopplerMapNorm_dB < -DynamicRange_dB;
RangeDopplerMapNorm_dB(IndxVec) = -DynamicRange_dB;

MatrixNormDynRangeLimited_dB = RangeDopplerMapNorm_dB;

end

