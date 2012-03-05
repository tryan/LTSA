from __future__ import division
import unittest as ut
import numpy as np
from ltsa import *

class TestLTSA(ut.TestCase):

    def setUp(self):
        self.gram = WavLTSA('/home/ryan/trains.wav')
        self.gram.compute()

    def test_show(self):
        # setup the tests
        self.setUp()

        # test that with no args, self.gram.ltsa is shown
        img = self.gram.show()
        self.assertTrue(img is self.gram.ltsa)

        # no need to recompute here as show() does not modify gram.ltsa

        # with an int arg, downsample frequency axis
        t_size = self.gram.ltsa.shape[1]
        img = self.gram.show(600)
        self.assertEqual(img.shape, (600, t_size))

        # nonsensical types passed as resize should raise TypeError
        self.assertRaises(TypeError, lambda: self.gram.show('Fred'))
        self.assertRaises(TypeError, lambda: self.gram.show((800, 800, 5)))
        self.assertRaises(TypeError, lambda: self.gram.show((800.5, 800)))
        self.assertRaises(TypeError, lambda: self.gram.show(800.5))
        self.assertRaises(TypeError, lambda: self.gram.show(lambda: 800))
        self.assertRaises(ValueError, lambda: self.gram.show(-1))
        self.assertRaises(ValueError, lambda: self.gram.show(1000**2))

        # imresize should raise an error on bad interp values
        self.assertRaises(KeyError, lambda: self.gram.show((800, 800), 'failme'))
        self.assertRaises(KeyError, lambda: self.gram.show((800, 800), 13))
        self.assertRaises(KeyError, lambda: self.gram.show((800, 800), lambda: 'bilinear'))

    
    def test_crop(self):
        self.setUp()

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

def suite():
    suite = ut.TestSuite()
    suite.addTest(ut.makeSuite(TestLTSA))
    return suite

'''
if __name__ == '__main__':
    ut.main()
'''

#suite = ut.TestLoader().loadTestsFromTestCase(TestLTSA)
ut.TextTestRunner(verbosity=2).run(suite())
