% quick ltsa test script

clear; clc;

[sig fs] = wavread('~/trains.wav');
sig = single( sig(:, 1) );

div_len = .5 * fs;
subdiv_len = floor(div_len/4);
nfft = subdiv_len;
noverlap = subdiv_len/2;

ltsa = ltsa_process_data(sig, div_len, subdiv_len, noverlap, nfft);


h = [0 length(sig)/fs];
v = [0 fs/2];

% conversion to double necessary for octave's imagesc() not to crash
ltsa_view(double(ltsa), fs, h(2));

clear sig;
