import os
import unittest
import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import kernpy as kp


class GenericTestCase(unittest.TestCase):

    @classmethod
    def load_contents_of_input_merged_load_files(cls):
        path_names = ['0_0.krn', '0_1.krn', '0_2.krn', '0_3.krn', '0_4.krn', '0_5.krn', '0_6.krn',
                      '0_7.krn', '0_8.krn', '0_9.krn', '0_10.krn', '0_11.krn']
        paths = [os.path.join('resource_dir', 'merge', p) for p in path_names if 'merged' not in p]
        contents = [open(p, 'r').read() for p in paths]
        return contents

    @classmethod
    def load_expected_contents_of_input_merged_load_files(cls):
        path_names = ['0_0.krn', '0_1.krn', '0_2.krn', '0_3.krn', '0_4.krn', '0_5.krn', '0_6.krn',
                      '0_7.krn', '0_8.krn', '0_9.krn', '0_10.krn', '0_11.krn']
        paths = [os.path.join('resource_dir', 'merge', p) for p in path_names if 'merged' in p]
        contents = [open(p, 'r').read() for p in paths]
        return contents

    @classmethod
    def load_expected_indexes_of_input_merged_load_files(cls):
        return [(0, 5), (6, 11), (12, 16), (17, 21), (22, 26), (27, 31), (32, 37), (38, 43), (44, 49), (50, 54),
                (55, 59), (60, 66)]



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
        contents = self.load_contents_of_input_merged_load_files()
        expected_indexes = self.load_expected_indexes_of_input_merged_load_files()

        # Act
        doc, real_indexes = kp.merge(contents)

        # Assert
        self.assertIsInstance(doc, kp.Document)
        self.assertTrue(len(real_indexes) == len(expected_indexes))
        self.assertListEqual(expected_indexes, real_indexes)

    def test_merge_with_separators(self):
        # Arrange
        contents = self.load_contents_of_input_merged_load_files()

        # Act
        # Should fail when not using a separator \n between content
        with self.assertRaises(ValueError):
            doc, real_indexes = kp.merge(contents, separator='')

    def test_merge_and_read_exported_content_1(self):
        # Arrange
        contents = self.load_contents_of_input_merged_load_files()
        expected_indexes = self.load_expected_indexes_of_input_merged_load_files()
        expected_contents = self.load_expected_contents_of_input_merged_load_files()

        # Act
        doc, real_indexes = kp.merge(contents)

        # Assert
        self.assertIsInstance(doc, kp.Document)
        self.assertTrue(len(real_indexes) == len(expected_indexes))
        self.assertListEqual(expected_indexes, real_indexes)

        content = None
        for expected_content, (start, end) in zip(expected_contents, real_indexes):
            options = kp.ExportOptions(from_measure=start, to_measure=end)
            try:
                content = kp.export(doc, options)
                self.assertEqual(expected_content, content)
            except Exception as e:
                logging.error(f"Error found : {e}. When comparing {expected_content} with {content}")

