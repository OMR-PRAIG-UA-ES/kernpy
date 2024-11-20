import os
import unittest
import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import kernpy as kp


class GenericTestCase(unittest.TestCase):
    def test_read_export_easy(self):
        # Arrange
        expected_ekrn = 'resource_dir/legacy/base_tuplet.ekrn'
        current_krn = 'resource_dir/legacy/base_tuplet.krn'
        with open(expected_ekrn, 'r') as f:
            expected_content = f.read()

        # Act
        doc, _ = kp.read(current_krn)
        options = kp.ExportOptions(kern_type=kp.KernTypeExporter.eKern)
        real_content = kp.export(doc, options)

        # Assert
        self.assertEqual(expected_content, real_content, f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}")

    def test_store_non_existing_file(self):
        # Arrange
        doc, _ = kp.read('resource_dir/legacy/base_tuplet.krn')
        options = kp.ExportOptions()
        with TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, 'test.krn')

            # Act
            kp.store(doc, file_path, options)

            # Assert
            self.assertTrue(os.path.exists(file_path), f"File not created: {file_path}")

    @patch('kernpy.Exporter.get_spine_types')
    def test_get_spine_types_uses_exporter_get_spines_types(self, mock_get_spines_types):
        # Arrange
        doc, _ = kp.read('resource_dir/legacy/chor048.krn')

        # Act
        _ = kp.get_spine_types(doc)

        # Assert
        mock_get_spines_types.assert_called_once()

    @patch('kernpy.Importer.import_file')
    def test_read_use_importer_run(self, mock_importer_run):
        # Arrange
        file_path = 'resource_dir/legacy/chor048.krn'

        # Act
        _ = kp.read(file_path)

        # Assert
        mock_importer_run.assert_called_once_with(Path(file_path))

    @patch('kernpy.Exporter.export_string')
    def test_export_use_exporter_run(self, mock_exporter_run):
        # Arrange
        doc, _ = kp.read('resource_dir/legacy/chor048.krn')
        options = kp.ExportOptions()

        # Act
        _ = kp.export(doc, options)

        # Assert
        mock_exporter_run.assert_called_once_with(doc, options)

    def test_create_document(self):
        # Arrange
        file_path = 'resource_dir/legacy/chor048.krn'
        with open(file_path, 'r') as f:
            content = f.read()

        # Act
        doc, _ = kp.create(content)

        # Assert
        self.assertIsInstance(doc, kp.Document)

    def test_merge_1(self):
        # Arrange
        path_names = ['0_0.krn', '0_1.krn', '0_2.krn', '0_3.krn', '0_4.krn', '0_5.krn', '0_6.krn',
                      '0_7.krn', '0_8.krn', '0_9.krn', '0_10.krn', '0_11.krn']
        paths = [os.path.join('resource_dir', 'merge', p) for p in path_names]
        contents = [open(p, 'r').read() for p in paths]
        expected_indexes = [(0, 4), (4, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 36), (36, 42), (42, 48),
                            (48, 53), (53, 58), (58, 65)]

        # Act
        doc, real_indexes = kp.merge(contents)

        # Assert
        self.assertIsInstance(doc, kp.Document)
        self.assertListEqual(expected_indexes, real_indexes)
        kp.store_graph(doc, '/tmp/test_merge_1.dot')
        kp.store(doc, '/tmp/test_merge_1.krn', kp.ExportOptions())

    def test_merge_with_separators(self):
        # Arrange
        path_names = ['0_0.krn', '0_1.krn', '0_2.krn', '0_3.krn', '0_4.krn', '0_5.krn', '0_6.krn',
                      '0_7.krn', '0_8.krn', '0_9.krn', '0_10.krn', '0_11.krn']
        paths = [os.path.join('resource_dir', 'merge', p) for p in path_names]
        contents = [open(p, 'r').read() for p in paths]

        # Act
        # Should fail when not using a separator \n between content
        with self.assertRaises(ValueError):
            doc, real_indexes = kp.merge(contents, separator='')


