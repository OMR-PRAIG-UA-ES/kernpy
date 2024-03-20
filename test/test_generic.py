import os
import unittest
import logging
import sys

import kernpy

class GenericTestCase(unittest.TestCase):
    @unittest.skip("Not implemented")
    def test_measure_from_time(self):
        score = kernpy.read_kern('path/to/file.krn')
        measure = score.measure_from_time(10)
        self.assertTrue(measure > 0)

    @unittest.skip
    def test_extract_spine(self):
        score = kernpy.read_kern('path/to/file.krn')
        spine = score.extract_spine(0)
        self.assertTrue(spine)

    @unittest.skip
    def test_extract_measures(self):
        score = kernpy.read_kern('path/to/file.krn')
        measures = score.extract_measures(0, 1)
        self.assertTrue(measures)

    @unittest.skip
    def test_tokens(self):
        score = kernpy.read_kern('path/to/file.krn')
        tokens = score.tokens()
        self.assertTrue(tokens)

    @unittest.skip
    def test_to_krn(self):
        score = kernpy.read_kern('path/to/file.krn')
        score.to_krn()
        self.assertTrue(os.path.exists('path/to/file.krn'))