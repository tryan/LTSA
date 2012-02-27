from __future__ import division
import numpy as np
from numpy.fft import rfft
from scipy.io.wavfile import read as wavread
import matplotlib.pyplot as plt
from scipy.misc import imresize

class InputError(Exception):
    
    def __init__(self, detail):
        self.detail = detail

class LTSA():
    '''
    Long-Term Spectral Average

    A class for computing spectral visualizations of long audio signals.

    Accepts a path to a WAV file and an optional channel argument (default: 0).
    Several class attributes allow the user to customize the computation (see
    README) via set_params() or direct assignment. 

    The computation is run with compute() and the resulting image is stored in
    the ltsa attribute. The crop() method crops the image to a specified
    time/frequency space. 

    show() displays the LTSA in the current figure using pyplot.imshow() and
    has optional resizing arguments.
    '''

    # initialize with default parameters
    def __init__(self, _file, channel=0):

        self.ltsa = None

        if isinstance(_file, str) and _file[-4:] == '.wav':
            self.fs, self.raw = wavread(_file)
            if self.raw.ndim > 1:
                self.raw = self.raw[:,channel] # take only one channel
        else:
            raise InputError('Input must be a path to a .wav file')

        # defaults for user adjustable values
        self.div_len = np.round(self.fs/2) # half second divisions
        self.subdiv_len = 2**np.round(np.log2(self.fs/5))
        self.nfft = self.subdiv_len
        self.noverlap = 0

        # useful values
        self.nsamples = len(self.raw)
        self.ndivs = np.floor(self.nsamples / self.div_len)
        self.nsubdivs = np.floor(self.div_len / (self.subdiv_len - self.noverlap))

        # time and frequency limits, used for displaying results
        self.tmin = 0
        self.tmax = np.floor(self.nsamples / self.fs)
        self.fmin = 0
        self.fmax = np.floor(self.fs / 2)

# takes a dict of attribute name/value pairs and sets LTSA params accordingly
    def set_params(self, var_dict):
        '''
        Allows the user to set custom values for computation parameters.

        It is recommended that only these variables be manipulated:
            div_len
            subdiv_len
            nfft
            noverlap

        Input should be a dictionary, for example:
        var_dict = {'div_len':8192, 'subdiv_len':1024}
        '''
        for key, val in var_dict.iteritems():
            vars(self)[key] = val

    def crop(self, tmin = 0, tmax = -1, fmin = 0, fmax = -1):
        '''
        Crop the computed LTSA in time and/or frequency

        Input times should be given in seconds, frequencies in Hertz

        Cropping the LTSA throws away any data that is cropped out
        '''
        if tmax < 0:
            tmax = self.nsamples / self.fs
        if fmax < 0:
            fmax = self.fs / 2

# update time and frequency limits
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
        '''
        Displays the LTSA image in the current axis using
        matplotlib.pyplot.imshow()

        If no resize input is given, the self.ltsa is displayed without
        modification

        If resize is a tuple of two ints, scipy.misc.imresize is called:
        imresize(self.ltsa, resize)

        If resize is an int, the ltsa data is downsampled to a height of resize

        It is often useful to manually adjust the color axis using
        pyplot.clim(), as the default clim is usually wider than it should be
        '''
        if isinstance(resize, tuple):
# use scipy.misc.imresize
            img = imresize(self.ltsa, resize)
        elif isinstance(resize, int):
# downsample (without lowpass filtering)
            h = resize # img height in pixels
            idx = np.floor(np.linspace(0, np.size(self.ltsa, 0)-1, h))
            idx = np.int32(idx)
            img = np.zeros((h, np.size(self.ltsa, 1)))
            for i in xrange(int(np.size(self.ltsa, 1))):
                img[:,i] = self.ltsa[idx,i] 
        else:
            img = self.ltsa

        self.handle = plt.imshow(img, origin='lower')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Frequency (Hertz)')

# set time axis ticks & labels
        xtick_loc, xtick_lbl = plt.xticks() # value of xtick_lbl will not be used
        xtick_loc = xtick_loc[(xtick_loc >= 0) * (xtick_loc <= np.size(self.ltsa, 1))]
        xlbl_vals = np.round(np.linspace(self.tmin, self.tmax, len(xtick_loc)))
        xtick_lbl = [str(int(x)) for x in xlbl_vals]
        plt.xticks(xtick_loc, xtick_lbl)

# set frequency axis ticks & labels
        ytick_loc, ytick_lbl = plt.yticks() # value of ytick_lbl will not be used
        ytick_loc = ytick_loc[(ytick_loc >= 0) * (ytick_loc <= np.size(self.ltsa, 0))]
        ylbl_vals = np.round(np.linspace(self.fmin, self.fmax, len(ytick_loc)))
        ytick_lbl = [str(int(y)) for y in ylbl_vals]
        plt.yticks(ytick_loc, ytick_lbl)

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

    def _tighten_color_axis(self, vmin, vmax):
        spread = vmin - vmax


    def scale_to_uint8(self): pass
