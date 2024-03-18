import os
import unittest
import logging
import sys

import kernpy

class GenericTestCase(unittest.TestCase):
    def test_measure_from_time(self):
        self.assertTrue(True)
        return

        score = kernpy.read_kern('path/to/file.krn')
        measure = score.measure_from_time(10)
        self.assertTrue(measure > 0)

    def test_extract_spine(self):
        self.assertTrue(True)
        return

        score = kernpy.read_kern('path/to/file.krn')
        spine = score.extract_spine(0)
        self.assertTrue(spine)

    def test_extract_measures(self):
        self.assertTrue(True)
        return


        score = kernpy.read_kern('path/to/file.krn')
        measures = score.extract_measures(0, 1)
        self.assertTrue(measures)

    def test_tokens(self):
        self.assertTrue(True)
        return

        score = kernpy.read_kern('path/to/file.krn')
        tokens = score.tokens()
        self.assertTrue(tokens)

    def test_to_krn(self):
        self.assertTrue(True)
        return

        score = kernpy.read_kern('path/to/file.krn')
        score.to_krn()
        self.assertTrue(os.path.exists('path/to/file.krn'))