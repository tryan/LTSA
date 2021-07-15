from __future__ import division
import unittest as ut
import numpy as np
from ltsa import *
from scipy.signal import chirp

class TestLTSA(ut.TestCase):

    def set_gram(self):
        '''
        Abstract method 
        
        Subclasses implement this method to initialize the LTSA, compute it,
        and return the LTSA object in preparation for tests to be run using the
        LTSA object
        '''
        self.gram = None

    def test_set_params(self):
        gram = self.set_gram()
        params = { 
            'div_len': 44100,
            'subdiv_len': 4096,
            'nfft': 4096,
            'noverlap': 500
        }

        # check that parameters have been set
        gram.set_params(params)
        for key, val in params.iteritems():
            self.assertEqual(val, vars(gram)[key])

        # check that gram still computes
        gram()

    def test_sanity(self):
        # some general sanity checks
        gram = self.set_gram()

#       default parameters shouldn't be too weird
        self.assertTrue(gram.div_len >= gram.subdiv_len)
        self.assertTrue(gram.nfft >= gram.subdiv_len)
        
#       number of divs should equal number of columns in the ltsa
        self.assertEqual(gram.ndivs, gram.ltsa.shape[1])

#       should be nfft/2 pixels per column in the ltsa
        self.assertEqual(gram.nfft/2, gram.ltsa.shape[0])

        # if noverlap >= subdiv_len, raise an error
        gram.noverlap = gram.subdiv_len
        self.assertRaises(ValueError, gram.compute)
        gram.noverlap = gram.subdiv_len + 50000
        self.assertRaises(ValueError, gram.compute)

    def test_scale_to_uint8(self):
        gram = self.set_gram()
        gram.scale_to_uint8()
        self.assertTrue(gram.ltsa.dtype == 'uint8')

    def test_magic_methods(self):
        gram = self.set_gram()

        # check setitem and getitem
        # these shouldn't raise errors
        tmp = gram[0,0]
        tmp = gram[:,1]
        tmp = gram[-1,-1]
        gram[0,0] = 13.34123

#       these are invalid access keys and should raise an error
        key_err_cases = [(1, 2, 3),
                         ('invalid_index',)]

        for case in key_err_cases:
            self.assertRaises(Exception, gram.__getitem__, *case)

        # these values should raise an error if assigned to gram[0,0]
        set_err_cases = [('invalid_value',),
                         (3, 2),
                         ((3, 2),)]

        for case in set_err_cases:
            self.assertRaises(Exception, gram.__setitem__, 0, 0, *case)

    def test_show(self):
        # setup the tests
        self.set_gram()

        # test that with no args, self.gram.ltsa is shown
        img = self.gram.show()
        self.assertTrue(img is self.gram.ltsa)

        # no need to recompute here as show() does not modify gram.ltsa

        # with an int arg, downsample frequency axis
        t_size = self.gram.ltsa.shape[1]
        img = self.gram.show(600)
        self.assertEqual(img.shape, (600, t_size))

        # nonsensical types passed as resize should raise TypeError
        type_err_cases = [('Fred',),
                          (800, 800, 5),
                          (800.5, 800),
                          (300.5,)]

        value_err_cases = [-1, 1000**2]

        for case in type_err_cases:
            self.assertRaises(TypeError, self.gram.show, *case)

        for case in value_err_cases:
            self.assertRaises(ValueError, self.gram.show, case)

        # imresize should raise an error on bad interp values
        interp_err_cases = ['failme', 13, lambda: 'bilinear']
        for case in interp_err_cases:
            self.assertRaises(ValueError, self.gram.show, (800,800), case)

    
    def test_crop(self):
        gram = self.set_gram()

        # in this test case we want to crop the middle half of both the time
        # and frequency ranges

        fs = gram.fs
        ndivs = gram.ndivs
        self.assertEqual(ndivs, gram.ltsa.shape[1])
        div_len = gram.div_len

        tmax = gram.tmax
        tmax_new = int(tmax * 3.0/4.0)
        tmin_new = int(tmax * 1.0/4.0)

        fmax = gram.fmax
        fmax_new = int(fmax * 3.0/4.0)
        fmin_new = int(fmax * 1.0/4.0)

        shape = gram.ltsa.shape
        div_low = np.floor(shape[1] * 1.0/4.0)
        div_high = np.ceil(shape[1] * 3.0/4.0) + 1
        freq_low = np.floor(shape[0] * 1.0/4.0) - 1
        freq_high = np.ceil(shape[0] * 3.0/4.0) + 1
        expected_results = (div_low, div_high, freq_low, freq_high)

        crop_results = gram.crop(tmin_new, tmax_new, fmin_new, fmax_new)

        self.assertEqual(crop_results, expected_results)

        #####

        # check that malformed inputs throw errors

        gram = self.set_gram()

        value_err_cases = [(50, 30),
                           (-1, 30),
                           (0, -30),
                           (0, 1000, -1),
                           (0, 1000, 500, 300)]
        
        type_err_cases = ['fred',
                          1+1j,
                          lambda: 3,
                          (30, 50)]

        for case in value_err_cases:
            self.assertRaises(ValueError, gram.crop, *case)

        for case in type_err_cases:
            self.assertRaises(TypeError, gram.crop, case)


class TestWavLTSA(TestLTSA):
    '''
    Class for testing the WavLTSA class. The LTSA class tests are independent
    of the origin of the raw signal data, so the only difference in testing is
    in the initialization
    '''
    def set_gram(self):
        '''
        Create a WavLTSA for testing. 
        '''
        wav = '/home/tk/bensound-slowmotion.wav'
        self.gram = WavLTSA(wav)
        self.gram()
        return self.gram

    def test_init(self):
        test_cases = [
            'fred.mp3',
            lambda: 3,
            14
        ]

        for case in test_cases:
            self.assertRaises(TypeError, WavLTSA, case)

class TestRawLTSA(TestLTSA):
    '''
    Class for testing the RawLTSA class. The LTSA class tests are independent
    of the origin of the raw signal data, so the only difference in testing is
    in the initialization
    '''
    def set_gram(self):
        '''
        Generate some raw data for testing. 

        Data is a chirp sweeping from 100Hz to 10kHz logarithmically over 10
        seconds at a 44.1kHz sampling rate.
        '''
        fs = 44100
        t_begin = 0
        t_end = 100
        t = np.linspace(t_begin, t_end, (t_end - t_begin)*fs)
        signal = chirp(t, f0=100, t1=100, f1=10000, method='logarithmic')
        self.gram = RawLTSA(signal, fs)
        self.gram()
        return self.gram

    def test_init(self):
        test_cases = [
            np.zeros((5,5)),
            3,
            'fred'
        ]

        for case in test_cases:
            self.assertRaises(TypeError, RawLTSA, case)
    

def get_suite():
    suite = ut.TestSuite()
    suite.addTest(ut.makeSuite(TestWavLTSA))
    suite.addTest(ut.makeSuite(TestRawLTSA))
    return suite


#suite = ut.TestLoader().loadTestsFromTestCase(TestLTSA)
ut.TextTestRunner(verbosity=2).run(get_suite())
