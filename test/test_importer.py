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
        with open(input_kern_file, 'r', newline='', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        importer = kp.Importer()
        document = importer.import_string(content)
        self.assertIsNotNone(document)

    def test_spine_ids(self):
        input_kern_file = 'resource_dir/legacy/chor001.krn'

        doc, err = kp.read(input_kern_file)
        header_tokens = doc.get_all_tokens()
        spines_ids = [t.spine_id for t in header_tokens if isinstance(t, kp.core.HeaderToken)]
        self.assertListEqual([0, 1, 2, 3, 4, 5], spines_ids)

