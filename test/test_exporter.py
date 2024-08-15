import os
import unittest

import kernpy as kp


class ExporterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read the basic score document once before all tests
        cls.doc, _ = kp.read('resource_dir/legacy/chor048.krn')

    def test_get_spine_types_1(self):
        spine_types = kp.get_spine_types(self.doc)
        self.assertEqual(['**kern', '**kern', '**kern', '**kern', '**root', '**harm'], spine_types)

    def test_get_spine_types_2(self):
        spine_types = kp.get_spine_types(self.doc, spine_types=None)
        self.assertEqual(['**kern', '**kern', '**kern', '**kern', '**root', '**harm'], spine_types)

    def test_get_spine_types_3(self):
        spine_types = kp.get_spine_types(self.doc, spine_types=['**kern'])
        self.assertEqual(['**kern', '**kern', '**kern', '**kern'], spine_types)

    def test_get_spine_types_4(self):
        spine_types = kp.get_spine_types(self.doc, spine_types=['**root'])
        self.assertEqual(['**root'], spine_types)

    def test_get_spine_types_5(self):
        spine_types = kp.get_spine_types(self.doc, spine_types=['**harm'])
        self.assertEqual(['**harm'], spine_types)

    def test_get_spine_types_6(self):
        spine_types = kp.get_spine_types(self.doc, spine_types=['**not-exists'])
        self.assertEqual([], spine_types)

    def test_get_spine_types_7(self):
        spine_types = kp.get_spine_types(self.doc, spine_types=[])
        self.assertEqual([], spine_types)