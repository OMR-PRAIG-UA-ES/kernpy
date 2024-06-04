import os
import unittest
import logging
import sys
from tempfile import TemporaryDirectory

import kernpy

class GenericTestCase(unittest.TestCase):
    def test_read_export_easy(self):
        # Arrange
        expected_ekrn = 'resource_dir/legacy/base_tuplet.ekrn'
        current_krn = 'resource_dir/legacy/base_tuplet.krn'
        with open(expected_ekrn, 'r') as f:
            expected_content = f.read()

        # Act
        doc = kernpy.read(current_krn)
        options = kernpy.ExportOptions(kern_type=kernpy.KernTypeExporter.eKern)
        real_content = kernpy.export(doc, options)

        # Assert
        self.assertEqual(expected_content, real_content, f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}")

    def test_store_non_existing_file(self):
        # Arrange
        doc = kernpy.read('resource_dir/legacy/base_tuplet.krn')
        options = kernpy.ExportOptions()
        with TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, 'test.krn')

            # Act
            kernpy.store(doc, file_path, options)

            # Assert
            self.assertTrue(os.path.exists(file_path), f"File not created: {file_path}")
