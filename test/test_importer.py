import unittest
import os
from pathlib import Path

import kernpy as kp


class ImporterTestCase(unittest.TestCase):

    def _assert_raise_error_when_writing_after_eof(self, input_kern_file: Path, expected_message: str):
        importer = kp.Importer()

        with self.assertRaises(ValueError) as context:
            importer.import_file(input_kern_file)

        self.assertEqual(str(context.exception), expected_message)

    def test_import_from_file(self):
        input_kern_file = 'test/resources/legacy/chor001.krn'
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        self.assertIsNotNone(document)

    def test_import_from_string(self):
        input_kern_file = 'test/resources/legacy/chor001.krn'
        with open(input_kern_file, 'r', newline='', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        importer = kp.Importer()
        document = importer.import_string(content)
        self.assertIsNotNone(document)

    def test_spine_ids(self):
        input_kern_file = 'test/resources/legacy/chor001.krn'

        doc, err = kp.read(input_kern_file)
        header_tokens = doc.get_all_tokens()
        spines_ids = [t.spine_id for t in header_tokens if isinstance(t, kp.core.HeaderToken)]
        self.assertListEqual([0, 1, 2, 3, 4, 5], spines_ids)

    def test_not_raise_handled_exception_when_can_bad_header(self):
        input_kern_file = 'test/resources/samples/wrong_header.krn'
        doc, err = kp.load(input_kern_file)

        self.assertTrue(True, "Should not raise an exception when handling a bad header")

    def test_raise_wrong_number_of_columns(self):
        input_kern_file = 'test/resources/samples/wrong_number_of_columns.krn'
        with self.assertRaises(ValueError):
            doc, err = kp.load(input_kern_file)

    @unittest.skip
    def test_fix_error_wrong_number_of_columns(self):
        # Arrange
        input_kern_file = 'test/resources/samples/wrong_number_of_columns.krn'
        output_kern_file = 'test/resources/samples/wrong_number_of_columns_fixed.krn'
        with open(output_kern_file, 'r') as f:
            expected_content = f.read()

        # Act
        doc, err = kp.read(input_kern_file)
        real_content = kp.export(doc, kp.ExportOptions())

        # Assert
        self.assertEqual(expected_content, real_content)

    def test_has_instrument_tokens(self):
        input_kern_file = 'test/resources/legacy/chor001.krn'
        doc, err = kp.read(input_kern_file)
        self.assertTrue(len(doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.INSTRUMENTS])) > 0)

    def test_import_unexpected_header_is_ok(self):
        input_kern_file = 'test/resources/samples/unexpected_header.krn'

        doc, err = kp.load(input_kern_file)
        self.assertIsNotNone(doc, "Document should not be None")

    def test_any_header_found(self):
        input_kern_file = Path('test/resources/samples/any_header.krn')
        expected_message = (
f'Any spine header found in the column #0. '
f'Expected a previous line with valid content. The token in column #0 and row '
f'#0 was not created correctly. Error detected in column #0 in row #1. Found '
f'*ClefF2. '
)

        with self.assertRaises(ValueError) as context:
            doc, _ = kp.load(input_kern_file)

        # Assert that the error message is as expected
        self.assertEqual(str(context.exception), expected_message)

    def test_assertRaiseErrorWhenWritingAfterEndOfFile_monophonic_only_kern(self):
        input_kern_file = Path('test/resources/end-of-file/eof_monophonic_only_kern_from_base_tuplet_longer.krn')
        expected_message = 'Token found in column #0 and row #42 after an end-of-program token (*-) in row #41. Found 4A.'
        self._assert_raise_error_when_writing_after_eof(input_kern_file=input_kern_file, expected_message=expected_message)

    def test_assertRaiseErrorWhenWritingAfterEndOfFile_polyphonic_only_kern(self):
        input_kern_file = Path('test/resources/end-of-file/eof_polyphonic_only_kern_from_grandstaff.krn')
        expected_message = 'Token found in column #0 and row #10 after an end-of-program token (*-) in row #9. Found 4c.'
        self._assert_raise_error_when_writing_after_eof(input_kern_file=input_kern_file, expected_message=expected_message)

    def test_assertRaiseErrorWhenWritingAfterEndOfFile_polyphonic_with_other_spines(self):
        input_kern_file = Path('test/resources/end-of-file/eof_polyphonic_mixed_from_didone.krn')
        expected_message = 'Token found in column #0 and row #15 after an end-of-program token (*-) in row #14. Found 4dd.'
        self._assert_raise_error_when_writing_after_eof(input_kern_file=input_kern_file, expected_message=expected_message)

    def test_assertRaiseErrorWhenWritingAfterEndOfFile_not_raised_when_valid(self):
        input_kern_file = Path('test/resources/end-of-file/eof_valid_no_write_after_terminator.krn')

        importer = kp.Importer()
        document = importer.import_file(input_kern_file)

        self.assertIsNotNone(document)

