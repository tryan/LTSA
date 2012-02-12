% script to compute an LTSA for files that fit in memory

% see README for usage information and guidelines

clear; clc; close all;

% name of file to process, either provide the full file path or
% change the matlab/octave directory to the containing folder
file = 'C:\numb.wav';

% file is read in
[sig fs] = wavread(file);
sig = single( sig(:, 1) );
nsamples = length(sig);

% LTSA configuration
div_len = round(.5 * fs);
subdiv_len = floor(div_len/6);
nfft = subdiv_len;
noverlap = round( subdiv_len/4 );

tic
ltsa = ltsa_process(sig, div_len, subdiv_len, noverlap, nfft);
toc

% conversion to double necessary for octave's imagesc() not to crash
% ltsa = double(ltsa);

% display LTSA
figure;
ltsa_view(ltsa, fs, nsamples, [0 15000]);

clear sig;
