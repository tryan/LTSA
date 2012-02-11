function h = ltsa_view(ltsa, fs, duration, freq_range, time_range)

% display LTSA in the current figure window and return handle
% 
% ltsa
% grayscale image output by ltsa_process (matrix of real values)
% 
% fs
% sampling frequency of signal, in Hertz
% 
% duration
% length of signal, in samples
% if omitted, time will be labeled in divisions rather than seconds
% 
% freq_range
% range of frequencies to display, in Hertz, others will be cropped
% format: freq_range = [0 1200]
% default: [0 fs/2]
% 
% time_range
% time period to display, in elapsed seconds, others will be cropped
% format: time_range = [200 500]
% default: [0 duration/fs]

assert(nargin >= 2, 'insufficient arguments passed to ltsa_view()');

time_units = 'seconds';

if nargin < 3
    duration = size(ltsa, 2);
    time_units = 'divisions';
end
if nargin < 5 || isempty(time_range)
    time_range = [0 duration/fs];
end
if nargin < 4 || isempty(freq_range)
    freq_range = [0 fs/2];
end

% crop image to the time and frequencies that we want to see
ltsa = ltsa_crop(ltsa, fs, duration, freq_range, time_range);

h = imagesc(time_range, freq_range, ltsa);
set(gca, 'YDir', 'normal');
xlabel(sprintf('Time (%s)', time_units));
ylabel('Frequency (Hz)');
title('Long Term Spectral Average');

end
