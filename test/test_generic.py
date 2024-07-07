import os
import unittest
import logging
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

import kernpy

class GenericTestCase(unittest.TestCase):
    def test_read_export_easy(self):
        # Arrange
        expected_ekrn = 'resource_dir/legacy/base_tuplet.ekrn'
        current_krn = 'resource_dir/legacy/base_tuplet.krn'
        with open(expected_ekrn, 'r') as f:
            expected_content = f.read()

        # Act
        doc, _ = kernpy.read(current_krn)
        options = kernpy.ExportOptions(kern_type=kernpy.KernTypeExporter.eKern)
        real_content = kernpy.export(doc, options)

        # Assert
        self.assertEqual(expected_content, real_content, f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}")

    def test_store_non_existing_file(self):
        # Arrange
        doc, _ = kernpy.read('resource_dir/legacy/base_tuplet.krn')
        options = kernpy.ExportOptions()
        with TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, 'test.krn')

            # Act
            kernpy.store(doc, file_path, options)

            # Assert
            self.assertTrue(os.path.exists(file_path), f"File not created: {file_path}")

    @patch('kernpy.Exporter.get_spine_types')
    def test_get_spine_types_uses_exporter_get_spines_types(self, mock_get_spines_types):
        # Arrange
        doc, _ = kernpy.read('resource_dir/legacy/chor048.krn')

        # Act
        _ = kernpy.get_spine_types(doc)

        # Assert
        mock_get_spines_types.assert_called_once()

    @patch('kernpy.Importer.import_file')
    def test_read_use_importer_run(self, mock_importer_run):
        # Arrange
        file_path = 'resource_dir/legacy/chor048.krn'

        # Act
        _ = kernpy.read(file_path)

        # Assert
        mock_importer_run.assert_called_once_with(file_path)

    @patch('kernpy.Exporter.export_string')
    def test_export_use_exporter_run(self, mock_exporter_run):
        # Arrange
        doc, _ = kernpy.read('resource_dir/legacy/chor048.krn')
        options = kernpy.ExportOptions()

        # Act
        _ = kernpy.export(doc, options)

        # Assert
        mock_exporter_run.assert_called_once_with(doc, options)

    def test_create_document(self):
        # Arrange
        file_path = 'resource_dir/legacy/chor048.krn'
        with open(file_path, 'r') as f:
            content = f.read()

        # Act
        doc, _ = kernpy.create(content)

        # Assert
        self.assertIsInstance(doc, kernpy.Document)

