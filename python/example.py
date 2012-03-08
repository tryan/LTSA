from matplotlib.pyplot import show, colorbar
from ltsa import WavLTSA

# initialize the object with raw data from wav file
s = WavLTSA('/home/ryan/trains.wav')

# some reasonable settings for a 44.1kHz sampling rate
params = {'div_len': 22050,
          'subdiv_len': 4096,
          'nfft': 4096,
          'noverlap': 1000}

# apply the parameters
s.set_params(params)

# compute the LTSA -- identical to s.compute()
s()

# throw out data over 6kHz as there isn't much interesting activity there
# in a typical song
s.crop(fmax=6000)
s.show()

colorbar()
show()
