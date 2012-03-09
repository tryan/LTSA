function ltsa = ltsa_process(signal, div_len, subdiv_len, noverlap, nfft)
%{
Process raw audio data into an LTSA image. 

signal
raw audio data (one dimension array of real numbers)

div_len
length of a division, in samples

subdiv_len
length of a subdivision, in samples
    
noverlap
overlap of subdivisions, in samples -- defaults to subdiv_len/2

nfft
length of fft to apply to each subdivision -- defaults to subdiv_len
%}

if nargin < 3
    error('Three arguments required by ltsa_process');
end
if nargin < 5
    nfft = -1;
end
if nargin < 4
    noverlap = floor(subdiv_len/2);
end

% nfft shouldn't be shorter than subdiv_len
if nfft < subdiv_len
    nfft = subdiv_len;
    warning('ltsa_process: nfft has been assigned subdiv_len (%d)',...
        subdiv_len);
end

% input sanity checks
assert(isvector(signal) && isreal(signal), 'signal is not usable for LTSA');
assert(div_len > subdiv_len);
assert(length(signal) > div_len, 'signal too short');

% ensure nfft is even
nfft = nfft + mod(nfft, 2);

if size(signal, 2) ~= 1
    signal = signal';
end

% number of time divisions in LTSA
ndiv = floor( length(signal)/div_len );

% remove data that doesn't fit into last division
signal = signal(1 : ndivs * div_len);

% separate divisions into columns
divs = reshape(signal, div_len, ndivs);

% allocate image
ltsa = single(zeros(nfft/2, ndivs));

for i = 1:ndivs
    div = divs(:, i);
    tmp = calc_spectrum(div, subdiv_len, nfft, noverlap);
    ltsa(:, i) = single( log(tmp) );
end

end % ltsa_process

function spectrum = calc_spectrum(div, subdiv_len, nfft, noverlap)

% Calculates the average spectrum of one time division of data.
% 
% For each subdivision of the signal, apply a Hanning window and calculate
% the spectrum. Average these together to get the spectrum of the division.

spectrum = zeros(nfft/2, 1);
window = hanning(subdiv_len);
slip = subdiv_len - noverlap;
assert(slip > 0, 'overlap exceeds subdiv_len');

lo = 1;
hi = subdiv_len;
nsubdivs = 0;
while hi <= length(div)
    nsubdivs = nsubdivs + 1;
    subdiv = div(lo:hi);
    tmp = fft(subdiv .* window, nfft);
    spectrum = spectrum + abs( tmp(1:nfft/2) );
    lo = lo + slip;
    hi = hi + slip;
end
    
% average rather than sum
spectrum = spectrum ./ nsubdivs;

end % calc_spectrum



