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

% determine what part of image to display
y_range = round( freq_range ./ (fs/2) * size(ltsa, 1) );
y_range(y_range < 1) = 1;
y_range(y_range > size(ltsa, 1)) = size(ltsa, 1);
x_range = round( time_range ./ duration * fs * size(ltsa, 2) );
x_range(x_range < 1) = 1;
x_range(x_range > size(ltsa, 2)) = size(ltsa, 2);

ltsa = ltsa(y_range(1):y_range(2), x_range(1):x_range(2));

h = imagesc(time_range, freq_range, ltsa);
set(gca, 'YDir', 'normal');
xlabel(sprintf('Time (%s)', time_units));
ylabel('Frequency (Hz)');
title('Long Term Spectral Average');

end
