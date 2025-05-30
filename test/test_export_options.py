import unittest

import kernpy as kp


class TestExportOptions(unittest.TestCase):
    def test_default_values(self):
        expected_options = kp.ExportOptions()
        expected_options.spine_types = kp.core.HEADERS
        expected_options.token_categories = [c for c in kp.TokenCategory]
        expected_options.from_measure = None
        expected_options.to_measure = None
        expected_options.kern_type = kp.Encoding.normalizedKern
        expected_options.instruments = None
        expected_options.show_measure_numbers = False
        expected_options.spine_ids = None

        real_options = kp.ExportOptions()

        self.assertEqual(expected_options, real_options)

    def test__eq__(self):
        a = kp.ExportOptions()
        b = kp.ExportOptions()
        self.assertEqual(a, b)

    def test__ne__(self):
        a = kp.ExportOptions()
        b = kp.ExportOptions(instruments=['piano'])
        self.assertNotEqual(a, b)


