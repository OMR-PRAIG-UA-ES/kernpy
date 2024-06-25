import os
import unittest

import kernpy


class ExporterTestCase(unittest.TestCase):
    def test_get_spine_types(self):
        # Arrange
        doc, _ = kernpy.read('resource_dir/legacy/chor048.krn')

        spine_types = kernpy.get_spine_types(doc)
        self.assertEqual(['**kern', '**kern', '**kern', '**kern', '**root', '**harm'], spine_types)

        spine_types = kernpy.get_spine_types(doc, spine_types=None)
        self.assertEqual(['**kern', '**kern', '**kern', '**kern', '**root', '**harm'], spine_types)

        spine_types = kernpy.get_spine_types(doc, spine_types=['**kern'])
        self.assertEqual(['**kern', '**kern', '**kern', '**kern'], spine_types)

        spine_types = kernpy.get_spine_types(doc, spine_types=['**root'])
        self.assertEqual(['**root'], spine_types)

        spine_types = kernpy.get_spine_types(doc, spine_types=['**not-exists'])
        self.assertEqual([], spine_types)

        spine_types = kernpy.get_spine_types(doc, spine_types=[])
        self.assertEqual([], spine_types)