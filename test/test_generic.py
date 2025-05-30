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
    def load_contents_of_input_concatenated_load_files(cls):
        path_names = ['0_0.krn', '0_1.krn', '0_2.krn', '0_3.krn', '0_4.krn', '0_5.krn', '0_6.krn',
                      '0_7.krn', '0_8.krn', '0_9.krn', '0_10.krn', '0_11.krn']
        paths = [os.path.join('resource_dir', 'concat', p) for p in path_names if 'concat' not in p]
        contents = [open(p, 'r').read() for p in paths]
        return contents

    @classmethod
    def load_expected_contents_of_input_concatenated_load_files(cls):
        path_names = ['0_0.krn', '0_1.krn', '0_2.krn', '0_3.krn', '0_4.krn', '0_5.krn', '0_6.krn',
                      '0_7.krn', '0_8.krn', '0_9.krn', '0_10.krn', '0_11.krn']
        paths = [os.path.join('resource_dir', 'concat', p) for p in path_names if 'concat' in p]
        contents = [open(p, 'r').read() for p in paths]
        return contents

    @classmethod
    def load_expected_indexes_of_input_concatenated_load_files(cls):
        return [(0, 4), (5, 10), (11, 15), (16, 20), (21, 25), (26, 30), (31, 36), (37, 42), (43, 48), (49, 53),
                (54, 58), (59, 65)]

    @classmethod
    def setUpClass(cls):
        cls.static_complex_doc, _ = kp.load('resource_dir/legacy/chor048.krn')



    def test_read_export_easy(self):
        # Arrange
        expected_ekrn = 'resource_dir/legacy/base_tuplet.ekrn'
        current_krn = 'resource_dir/legacy/base_tuplet.krn'
        with open(expected_ekrn, 'r') as f:
            expected_content = f.read()

        # Act
        doc, _ = kp.read(current_krn)
        options = kp.ExportOptions(kern_type=kp.Encoding.eKern)
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

    def test_concat_1(self):
        # Arrange
        contents = self.load_contents_of_input_concatenated_load_files()
        expected_indexes = self.load_expected_indexes_of_input_concatenated_load_files()

        # Act
        doc, real_indexes = kp.concat(contents)

        # Assert
        self.assertIsInstance(doc, kp.Document)
        self.assertTrue(len(real_indexes) == len(expected_indexes))
        self.assertListEqual(expected_indexes, real_indexes)

    def test_concat_with_separators(self):
        # Arrange
        contents = self.load_contents_of_input_concatenated_load_files()

        # Act
        # Should fail when not using a separator \n between content
        with self.assertRaises(ValueError):
            doc, real_indexes = kp.concat(contents, separator='')

    def test_concat_and_read_exported_content_1(self):
        # Arrange
        contents = self.load_contents_of_input_concatenated_load_files()
        expected_indexes = self.load_expected_indexes_of_input_concatenated_load_files()
        expected_contents = self.load_expected_contents_of_input_concatenated_load_files()

        # Act
        doc, real_indexes = kp.concat(contents)

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


    def test_generic_dumps_include_empty(self):
        with open(Path('resource_dir/categories/empty.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=[])
        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all(self):
        with open(Path('resource_dir/categories/all.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_only_barlines(self):
        with open(Path('resource_dir/categories/only_barlines.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=kp.TokenCategory.BARLINES)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all_less_note_rest(self):
        with open(Path('resource_dir/categories/all_less_note_rest.krn'), 'r') as f:
            expected = f.read()
        real_output = kp.dumps(self.static_complex_doc, exclude=kp.TokenCategory.NOTE_REST)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all_less_durations(self):
        with open(Path('resource_dir/categories/all_less_durations.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, exclude=kp.TokenCategory.DURATION)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all_less_pitches(self):
        with open(Path('resource_dir/categories/all_less_pitches.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, exclude=kp.TokenCategory.PITCH)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all_less_decorators(self):
        with open(Path('resource_dir/categories/all_less_decorators.krn'), 'r') as f:
            expected = f.read()
        real_output = kp.dumps(self.static_complex_doc, exclude=kp.TokenCategory.DECORATION)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_only_durations(self):
        with open(Path('resource_dir/categories/only_durations.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=kp.TokenCategory.DURATION)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_only_pitches(self):
        with open(Path('resource_dir/categories/only_pitches.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=kp.TokenCategory.PITCH)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_only_decorators(self):
        with open(Path('resource_dir/categories/only_decorators.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=kp.TokenCategory.DECORATION)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_note_rest_exclude_decorators(self):
        with open(Path('resource_dir/categories/note_rest_exclude_decorators.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc,
                               include=kp.TokenCategory.NOTE_REST,
                               exclude=kp.TokenCategory.DECORATION)

        self.assertEqual(expected, real_output)