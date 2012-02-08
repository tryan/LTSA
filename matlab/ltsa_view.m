function h = ltsa_view(ltsa, duration, fs, time_range, freq_range)

h = time_range;
v = freq_range;
imagesc(h, v, ltsa);
set(gca, 'YDir', 'normal');

end
