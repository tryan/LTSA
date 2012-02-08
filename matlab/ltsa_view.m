function h = ltsa_view(ltsa, fs, time_range, freq_range)

x = time_range;
y = freq_range;
h = imagesc(x, y, ltsa);
set(gca, 'YDir', 'normal');

end
