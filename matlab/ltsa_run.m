% script to compute an LTSA for files that fit in memory

% see README for usage information and guidelines

clear; clc; close all;

% name of file to process, either provide the full file path or
% change the matlab/octave directory to the containing folder
file = '~/trains.wav';

% file is read in
[sig fs] = wavread(file);
sig = single( sig(:, 1) );
nsamples = length(sig);

% LTSA configuration
div_len = .5 * fs;
subdiv_len = floor(div_len/4);
nfft = subdiv_len;
noverlap = subdiv_len/2;

ltsa = ltsa_process(sig, div_len, subdiv_len, noverlap, nfft);

% conversion to double necessary for octave's imagesc() not to crash
ltsa = double(ltsa);

% display LTSA
figure;
ltsa_view(double(ltsa), fs, nsamples);

clear sig;
