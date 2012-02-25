from matplotlib.pyplot import show
from ltsa import LTSA

s = LTSA('/home/ryan/gun.wav')

params = {'div_len': 22050,
          'subdiv_len': 4096,
          'nfft': 4096
          'noverlap': 1000}

s.set_params(params)
s.compute()
s.crop(fmax=16000)
s.show(resize=800)
show()
