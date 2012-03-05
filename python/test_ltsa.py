import unittest as ut
import numpy as np
from ltsa import *

class TestLTSA(ut.TestCase):

    def setUp(self):
        self.gram = WavLTSA('/home/ryan/trains.wav')

    def test_show(self):
        # setup the tests
        self.setUp()
        self.gram.compute()

        # test that with no args, self.gram.ltsa is shown
        img = self.gram.show()
        self.assertTrue(img is self.gram.ltsa)

        # no need to recompute here

        # with an int arg, downsample frequency axis
        t_size = self.gram.ltsa.shape[1]
        img = self.gram.show(600)
        self.assertEqual(img.shape, (600, t_size))

        self.assertRaises(ValueError, lambda: int('john'))

        self.assertRaises(TypeError, lambda: self.gram.show(resize="Fred"))

        # 
        self.assertRaises(TypeError, lambda: self.gram.show((800, 800, 5)))

        self.assertRaises(TypeError, lambda: self.gram.show((800.5, 800)))
    
    def test_crop(self):
        x = 1
        self.assertEqual(x, 1)

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
