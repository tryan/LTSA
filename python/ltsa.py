from __future__ import division
import numpy as np
from numpy.fft import rfft
from scipy.io.wavfile import read as wavread
import matplotlib.pyplot as plt
from scipy.signal import decimate
from scipy.misc import imresize

class LTSA():

    # initialize with default parameters
    def __init__(self, _file, channel=0):

        if _file[-4:] == '.wav':
            self.fs, self.raw = wavread(_file)
            if np.ndim(self.raw) > 1:
                self.raw = self.raw[:,channel] # take only one channel

        # defaults for user adjustable values
        self.div_len = np.round(self.fs/2) # one second divisions
        self.subdiv_len = 2**np.round(np.log2(self.fs/5))
#        self.subdiv_len = np.round(self.div_len / 4.0)
#        self.subdiv_len += self.subdiv_len % 2
        self.nfft = self.subdiv_len
        self.noverlap = 0

        # useful values
        self.nsamples = np.size(self.raw, 0)
        self.ndivs = np.floor(self.nsamples / self.div_len)
        self.nsubdivs = np.floor(self.div_len / (self.subdiv_len - self.noverlap))

        # plotting values
        self.tmin = 0
        self.tmax = np.floor(self.nsamples / self.fs)
        self.fmin = 0
        self.fmax = np.floor(self.fs / 2)

# takes a dict of attribute name/value pairs and sets LTSA params accordingly
    def set_params(self, var_dict):
        for key, val in var_dict.iteritems():
            vars(self)[key] = val

    def crop(self, tmin = 0, tmax = -1, fmin = 0, fmax = -1):
        if tmax == -1:
            tmax = self.nsamples / self.fs
        if fmax == -1:
            fmax = self.fs / 2

        self.tmin = tmin
        self.tmax = tmax
        self.fmin = fmin
        self.fmax = fmax

        # crop time axis
        div_low = np.max([0, np.floor(tmin * self.fs / self.div_len)])
        div_high = np.ceil(tmax * self.fs / self.div_len)
        self.ltsa = self.ltsa[:,div_low:div_high]

        # crop frequency axis
        freq_low = np.max([0, fmin / (self.fs/2) * np.size(self.ltsa, 0)])
        freq_low = np.floor(freq_low)
        freq_high = np.ceil(fmax / (self.fs/2) * np.size(self.ltsa, 0))
        self.ltsa = self.ltsa[freq_low:freq_high,:]

#        print div_low, div_high, freq_low, freq_high
        
    def show(self, resize=None):
        if resize is not None:
            img = imresize(self.ltsa, resize)
        else:
#           downsample without lowpass filtering
            h = 800 # img height in pixels
            if h < np.size(self.ltsa, 0):
                idx = np.floor(np.linspace(0, np.size(self.ltsa, 0)-1, h))
                idx = np.int32(idx)
                img = np.zeros((h, np.size(self.ltsa, 1)))
                for i in xrange(int(np.size(self.ltsa, 1))):
                    img[:,i] = self.ltsa[idx,i] 
            else:
                img = self.ltsa
        self.handle = plt.imshow(img, origin='lower')
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        xtick_loc, tmp = plt.xticks()
        xtick_loc = filter(lambda(x): x >= 0 and x <= np.size(self.ltsa, 1), xtick_loc)
        xlbl_vals = np.round(np.linspace(self.tmin, self.tmax, len(xtick_loc)))
        xtick_lbl = [str(int(x)) for x in xlbl_vals]
        plt.xticks(xtick_loc, xtick_lbl)

    def compute(self): 
        self.raw = self.raw[: self.ndivs * self.div_len]
        self.ltsa = np.zeros((self.nfft/2, self.ndivs), dtype=np.single)
        divs = np.reshape(self.raw, (self.ndivs, self.div_len)).T

        for i in xrange(int(self.ndivs)):
            div = divs[:,i]
            self.ltsa[:,i] = self._calc_spectrum(div)

    def _calc_spectrum(self, div):
        spectrum = np.zeros((self.nfft/2,))
        window = np.hanning(self.subdiv_len)
        slip = self.subdiv_len - self.noverlap
        # assert(slip > 0)

        lo = 0
        hi = self.subdiv_len
        nsubdivs = 0
        while hi < self.div_len:
            nsubdivs += 1
            subdiv = div[lo:hi]
            tr = rfft(subdiv * window, int(self.nfft))
            spectrum += np.abs(tr[:self.nfft/2])
            lo += slip
            hi += slip

        spectrum = np.single(np.log(spectrum / self.nsubdivs))
        return spectrum


    def scale_to_uint8(self): pass
