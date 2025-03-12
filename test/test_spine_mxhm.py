import kernpy as kp

import unittest


class MxhmSpineImporterTestCase(unittest.TestCase):
    def test_import(self):
        input_kern_file = 'resource_dir/samples/jazzmus_with_mxhm.krn'

        doc, _ = kp.load(input_kern_file)
        self.assertIsNotNone(doc)

