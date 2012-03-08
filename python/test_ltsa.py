from __future__ import division
import unittest as ut
import numpy as np
from ltsa import *

class TestLTSA(ut.TestCase):

    def set_gram(self):
        self.gram = WavLTSA('/home/ryan/trains.wav')
        self.gram.compute()
        return self.gram

    def test_scale_to_uint8(self):
        self.set_gram()
        self.gram.scale_to_uint8()
        self.assertTrue(self.gram.ltsa.dtype == 'uint8')

    def test_magic_methods(self):
        # check setitem and getitem
        gram = self.set_gram()

        # these shouldn't raise errors
        tmp = gram[0,0]
        tmp = gram[:,1]
        tmp = gram[-1,-1]
        gram[0,0] = 13.34123

#       these are invalid access keys and should raise an error
        key_err_cases = [(1, 2, 3),
                         'invalid_index']

        for case in key_err_cases:
            self.assertRaises(Exception, gram.__getitem__, case)

        # these values should raise an error if assigned to gram[0,0]
        set_err_cases = ['invalid_value',
                         (3, 2),
                         lambda x: x + 1]

        for case in set_err_cases:
            self.assertRaises(Exception, gram.__setitem__, (0,0), case)

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
        type_err_cases = ['Fred',
                          (800, 800, 5),
                          (800.5, 800),
                          lambda: 800,
                          300.5]

        value_err_cases = [-1, 1000**2]

        for case in type_err_cases:
            self.assertRaises(TypeError, self.gram.show, case)

        for case in value_err_cases:
            self.assertRaises(ValueError, self.gram.show, case)

        # imresize should raise an error on bad interp values
        interp_err_cases = ['failme', 13, lambda: bilinear]
        for case in interp_err_cases:
            self.assertRaises(KeyError, self.gram.show, (800,800), case)

    
    def test_crop(self):
        self.set_gram()

        # in this test case we want to crop the middle half of both the time
        # and frequency ranges

        fs = self.gram.fs
        ndivs = self.gram.ndivs
        div_len = self.gram.div_len
        divs_per_second = fs / div_len
        pixels_per_hz = self.gram.ltsa.shape[0] / (fs/2)

        tmax = self.gram.tmax
        tmax_new = int(tmax * 3.0/4.0)
        tmin_new = int(tmax * 1.0/4.0)

        fmax = self.gram.fmax
        fmax_new = int(fmax * 3.0/4.0)
        fmin_new = int(fmax * 1.0/4.0)

        div_low = np.floor(tmin_new * divs_per_second)
        div_high = np.floor(tmax_new * divs_per_second) + 1
        freq_low = np.floor(fmin_new * pixels_per_hz)
        freq_high = np.ceil(fmax_new * pixels_per_hz) + 1
        expected_results = (div_low, div_high, freq_low, freq_high)

        crop_results = self.gram.crop(tmin_new, tmax_new, fmin_new, fmax_new)

        self.assertEqual(crop_results, expected_results)

        #####

        # check that malformed inputs throw errors

        self.set_gram()

        value_err_cases = [lambda: self.gram.crop(50, 30),
                           lambda: self.gram.crop(-1, 30),
                           lambda: self.gram.crop(tmax = -30),
                           lambda: self.gram.crop(fmax = -1),
                           lambda: self.gram.crop(fmin = 500, fmax = 300)]
        
        type_err_cases = [lambda: self.gram.crop('fred'),
                          lambda: self.gram.crop(1+1j),
                          lambda: self.gram.crop(lambda: 3)]

        for test_case in value_err_cases:
            self.assertRaises(ValueError, test_case)

        for test_case in type_err_cases:
            self.assertRaises(TypeError, test_case)


def suite():
    suite = ut.TestSuite()
    suite.addTest(ut.makeSuite(TestLTSA))
    return suite


#suite = ut.TestLoader().loadTestsFromTestCase(TestLTSA)
ut.TextTestRunner(verbosity=2).run(suite())
