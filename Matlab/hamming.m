% HAMMING.M
%
% COPYRIGHT : (c) NUHAG, Dept.Math., University of Vienna, AUSTRIA
%             http://nuhag.eu/
%             Permission is granted to modify and re-distribute this
%             code in any manner as long as this notice is preserved.
%             All standard disclaimers apply.
%
% HAMMING.M	- returns the N-point Hamming window.
%
% Input		: n = number
%
% Output	: w = vector
%
% Usage		: w = hamming (n)
%
% Comments	: allows also the call:  hamming(xx), taking only format from signal xx
%
% See also	: HAMMING2

% modification of original MATLAB (3.5)  file
% HGFei, 1990  

function w = hamming(n)

if nargin == 0
 help hamming;
 return;
end;

n = n(:); 
[hig, wid] = size(n);

if  wid > 1;  n = wid; end; 

w = (.54 - .46*cos(2*pi*(0:n-1)'/(n-1))).';

if  hig > 1;
ww = w;  
 for jj = 2 : hig;
 w(jj,:) =  ww;
 end; 
end; 

 w =  w.';
