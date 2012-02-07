% quick ltsa test script

clear; clc;

[sig fs] = mp3read('test.mp3');
sig = sig(:, 1);

div_len = .5 * fs;
subdiv_len = floor(div_len/4);
nfft = subdiv_len;
noverlap = subdiv_len/2;

ltsa = ltsa_process_data(sig, div_len, subdiv_len, noverlap, nfft);
ltsa = log( ltsa );

h = [0 length(sig)/fs];
v = [0 fs/2];
im = imagesc(h, v, ltsa);
set(gca, 'YDir', 'normal');
