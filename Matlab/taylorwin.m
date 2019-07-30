function w = taylorwin(N,SLL,nb)
%TAYLORWIN Taylor window
%   w = taylor(N,SLL,nb) returns the N-point Taylor
%	window such that its Fourier transfrom has the
%	first nb sidelobes approximately equal and SLL
%	dB below the main lobe.

% Adapted by JCS from code by Hans
% (xx-xx-2002) - Started

% Determine main lobe to side lobe ratio
R = 10^(SLL/20);

% Sidelobes kept at constant level
n = 1:nb-1;

% Determine Taylor window scaling variables
A = acosh(R)/pi;
sigma = nb/(sqrt(A^2+(nb-0.5)^2));
xn = sigma*sqrt(A^2+(n-0.5).^2);

% Determine coefficients of short cosine transform
%	Note: gamma(n+1) = n! = prod(1:n)
H = (gamma(nb)^2)./(gamma(nb+n).*gamma(nb-n)).*prod((1-(n'.^2 * (1 ./ xn.^2)))');

% Construct window function
fs = [0:N-1]/(N-1)-0.5;
w = 1 + 2*H*cos(2*pi*n'*fs);
w = w(:);