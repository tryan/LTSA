function h = ltsa_view(ltsa, fs, duration, freq_range, time_range)

assert(nargin >= 2, 'insufficient arguments passed to ltsa_view()');

time_units = 'seconds';

if nargin < 3
    duration = size(ltsa, 2);
    time_units = 'divisions';
end
if nargin < 5
    time_range = [0 duration/fs];
end
if nargin < 4
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
