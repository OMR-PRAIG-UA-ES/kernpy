import unittest
import os

import kernpy as kp


class ImporterTestCase(unittest.TestCase):

    def test_import_from_file(self):
        input_kern_file = 'resource_dir/legacy/chor001.krn'
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        self.assertIsNotNone(document)

    def test_import_from_string(self):
        input_kern_file = 'resource_dir/legacy/chor001.krn'
        with open(input_kern_file,  'r', newline='', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        importer = kp.Importer()
        document = importer.import_string(content)
        self.assertIsNotNone(document)