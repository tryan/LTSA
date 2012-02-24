from matplotlib.pyplot import show
from ltsa import LTSA

s = LTSA('/home/ryan/gun.wav')

params = {}

s.compute()
s.crop(fmax=16000)
s.show(resize=800)
show()
