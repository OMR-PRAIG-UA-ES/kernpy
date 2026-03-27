import unittest
import os
from pathlib import Path
from unittest.mock import patch

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

    def test_load_raises_on_duration_mismatch_when_enabled(self):
        content = "**kern\n*M4/4\n=1\n4c\n4d\n=2\n*-\n"

        with self.assertRaises(ValueError) as context:
            kp.loads(content, raise_on_duration_mismatch=True)

        self.assertIn("duration mismatch", str(context.exception))

    def test_load_does_not_raise_on_duration_mismatch_when_disabled(self):
        content = "**kern\n*M4/4\n=1\n4c\n4d\n=2\n*-\n"

        document, errors = kp.loads(content, raise_on_duration_mismatch=False)

        self.assertIsNotNone(document)
        self.assertIsInstance(errors, list)

    def test_load_raises_when_signature_missing_and_no_fallback(self):
        content = "**kern\n=1\n4c\n4d\n=2\n*-\n"

        with self.assertRaises(ValueError) as context:
            kp.loads(
                content,
                raise_on_duration_mismatch=True,
                meter_signature_fallback_if_not_found=None,
            )

        self.assertIn("No time signature available", str(context.exception))

    def test_load_uses_fallback_signature_when_missing(self):
        content = "**kern\n=1\n4c\n4d\n4e\n4f\n=2\n*-\n"

        document, errors = kp.loads(
            content,
            raise_on_duration_mismatch=True,
            meter_signature_fallback_if_not_found="*M4/4",
        )

        self.assertIsNotNone(document)
        self.assertEqual([], errors)

    @patch("kernpy.core.importer.MeasureSignatureValidator.assert_measure", return_value=(True, ""))
    def test_importer_uses_memo_for_repeated_measure_patterns(self, mock_assert_measure):
        content = "**kern\n*M4/4\n=1\n4c\n4d\n4e\n4f\n=2\n4g\n4a\n4b\n4cc\n=3\n*-\n"

        importer = kp.Importer(error_on_duration_mismatch=True)
        importer.import_string(content)

        # Both measures have identical rhythmic pattern (4,4,4,4), so validation should be cached.
        self.assertEqual(1, mock_assert_measure.call_count)

    def test_load_counts_dotted_duration_correctly(self):
        content = "**kern\n*M4/4\n=1\n2.c\n8.c\n16c\n=2\n*-\n"

        document, errors = kp.loads(
            content,
            raise_on_duration_mismatch=True,
        )

        self.assertIsNotNone(document)
        self.assertEqual([], errors)

