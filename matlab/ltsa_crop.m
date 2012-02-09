function ltsa = ltsa_crop(ltsa, fs, duration, freq_range, time_range)

y_range = round( freq_range ./ (fs/2) * size(ltsa, 1) );
y_range(y_range < 1) = 1;
y_range(y_range > size(ltsa, 1)) = size(ltsa, 1);
x_range = round( time_range ./ duration * fs * size(ltsa, 2) );
x_range(x_range < 1) = 1;
x_range(x_range > size(ltsa, 2)) = size(ltsa, 2);

ltsa = ltsa(y_range(1):y_range(2), x_range(1):x_range(2));

end
