import unittest

import kernpy as kp


class TestExportOptions(unittest.TestCase):
    def test_default_values(self):
        expected_options = kp.ExportOptions(
            spine_types=None,
            token_categories=None,
            to_measure=None,
            kern_type=kp.KernTypeExporter.normalizedKern,
            instruments=None,
            show_measure_numbers=False
        )
        real_options = kp.ExportOptions()

        self.assertEqual(expected_options, real_options)


