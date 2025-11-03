import unittest
from pathlib import Path

import kernpy as kp


class TestAgnostic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.static_complex_doc, _ = kp.load('resource_dir/kern-scores/beethoven_sonata_12_4.krn')

    def test_agnostic_dumps(self):
        with open(Path('resource_dir/agnostic/beethoven_sonata_12_4.akrn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, encoding=kp.Encoding.agnosticKern)

        self.assertEqual(expected, real_output,
                         msg=f'Expected and real output differ:\nExpected:\n{expected}\n\nReal Output:\n{real_output}')

    def test_agnostic_extended_dumps(self):
        with open(Path('resource_dir/agnostic/beethoven_sonata_12_4_extended.aekrn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, encoding=kp.Encoding.agnosticExtendedKern)

        self.assertEqual(expected, real_output,
                         msg=f'Expected and real output differ:\nExpected:\n{expected}\n\nReal Output:\n{real_output}')