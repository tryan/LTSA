function ltsa = ltsa_process_data(data, div_len, subdiv_len, ...
    noverlap, nfft)
%{
Process raw audio data into an LTSA image. 

data
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
    error('Three arguments required by ltsa_process_data');
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
    warning('ltsa_process_data: nfft has been assigned subdiv_len (%d)',...
        subdiv_len);
end

% input sanity checks
assert(isvector(data) && isreal(data), 'data is not usable for LTSA');
assert(div_len > subdiv_len);
assert(length(data) > div_len, 'data too short');

% ensure nfft is even
nfft = nfft + mod(nfft, 2);

if size(data, 2) ~= 1
    data = data';
end

% number of time divisions in LTSA
ndivs = floor( length(data)/div_len );

% remove data that doesn't fit into last division
data = data(1 : ndivs * div_len);

% separate divisions into columns
divs = reshape(data, div_len, ndivs);

ltsa = zeros(nfft/2, ndivs);

for i = 1:ndivs
    div = divs(:, i);
    tmp = calc_spectrum(div, subdiv_len, nfft, noverlap);
    ltsa(:, i) = single(tmp);
end

end % ltsa_process_data

function spectrum = calc_spectrum(div, subdiv_len, nfft, noverlap)

% Calculates the average spectrum of one time division of data.
% 
% For each subdivision of the data, apply a Hanning window and calculate
% the spectrum. Average these together to get the spectrum of the division.

spectrum = zeros(nfft/2, 1);
window = hanning(subdiv_len);
slip = subdiv_len - noverlap;

lo = 1;
hi = subdiv_len;
nsubdivs = 0;
while 1
    nsubdivs = nsubdivs + 1;
    subdiv = div(lo:hi);
    tmp = fft(subdiv .* window, nfft);
    spectrum = spectrum + abs( tmp(1:nfft/2) );
    lo = lo + slip;
    hi = hi + slip;
    if hi > length(div)
        break
    end
end
    
% average rather than sum
spectrum = spectrum ./ nsubdivs;

end % calc_spectrum



