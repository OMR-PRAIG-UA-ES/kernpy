import unittest
import os
from pathlib import Path

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

    def test_raise_handled_exception_when_can_not_import(self):
        input_kern_file = 'resource_dir/samples/wrong_header.krn'
        with self.assertRaises(ValueError):
            doc, err = kp.read(input_kern_file)

    def test_raise_wrong_number_of_columns(self):
        input_kern_file = 'resource_dir/samples/wrong_number_of_columns.krn'
        with self.assertRaises(ValueError):
            doc, err = kp.read(input_kern_file)

    @unittest.skip
    def test_fix_error_wrong_number_of_columns(self):
        # Arrange
        input_kern_file = 'resource_dir/samples/wrong_number_of_columns.krn'
        output_kern_file = 'resource_dir/samples/wrong_number_of_columns_fixed.krn'
        with open(output_kern_file, 'r') as f:
            expected_content = f.read()

        # Act
        doc, err = kp.read(input_kern_file)
        real_content = kp.export(doc, kp.ExportOptions())

        # Assert
        self.assertEqual(expected_content, real_content)

    def test_has_instrument_tokens(self):
        input_kern_file = 'resource_dir/legacy/chor001.krn'
        doc, err = kp.read(input_kern_file)
        self.assertTrue(len(doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.INSTRUMENTS])) > 0)
