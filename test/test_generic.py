import os
import unittest
import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import kernpy as kp
from parameterized import parameterized
from kernpy.core.generic import Generic


class GenericTestCase(unittest.TestCase):

    @classmethod
    def load_contents_of_input_concatenated_load_files(cls):
        path_names = ['0_0.krn', '0_1.krn', '0_2.krn', '0_3.krn', '0_4.krn', '0_5.krn', '0_6.krn',
                      '0_7.krn', '0_8.krn', '0_9.krn', '0_10.krn', '0_11.krn']
        paths = [os.path.join('test/resources', 'concat', p) for p in path_names if 'concat' not in p]
        contents = [open(p, 'r').read() for p in paths]
        return contents

    @classmethod
    def load_expected_contents_of_input_concatenated_load_files(cls):
        path_names = ['0_0.krn', '0_1.krn', '0_2.krn', '0_3.krn', '0_4.krn', '0_5.krn', '0_6.krn',
                      '0_7.krn', '0_8.krn', '0_9.krn', '0_10.krn', '0_11.krn']
        paths = [os.path.join('test/resources', 'concat', p) for p in path_names if 'concat' in p]
        contents = [open(p, 'r').read() for p in paths]
        return contents

    @classmethod
    def load_expected_indexes_of_input_concatenated_load_files(cls):
        return [(0, 5), (6, 11), (12, 16), (17, 21), (22, 26), (27, 31), (32, 37), (38, 43), (44, 49), (50, 54),
            (55, 59), (60, 66)]

    @classmethod
    def setUpClass(cls):
        cls.static_complex_doc, _ = kp.load('test/resources/legacy/chor048.krn')



    def test_read_export_easy(self):
        # Arrange
        expected_ekrn = 'test/resources/legacy/base_tuplet.ekrn'
        current_krn = 'test/resources/legacy/base_tuplet.krn'
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
        doc, _ = kp.read('test/resources/legacy/base_tuplet.krn')
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
        doc, _ = kp.read('test/resources/legacy/chor048.krn')

        # Act
        _ = kp.get_spine_types(doc)

        # Assert
        mock_get_spines_types.assert_called_once()

    @patch('kernpy.Importer.import_file')
    def test_read_use_importer_run(self, mock_importer_run):
        # Arrange
        file_path = 'test/resources/legacy/chor048.krn'

        # Act
        _ = kp.read(file_path)

        # Assert
        mock_importer_run.assert_called_once_with(Path(file_path))

    @patch('kernpy.Exporter.export_string')
    def test_export_use_exporter_run(self, mock_exporter_run):
        # Arrange
        doc, _ = kp.read('test/resources/legacy/chor048.krn')
        options = kp.ExportOptions()

        # Act
        _ = kp.export(doc, options)

        # Assert
        mock_exporter_run.assert_called_once_with(doc, options)

    def test_create_document(self):
        # Arrange
        file_path = 'test/resources/legacy/chor048.krn'
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
        with open(Path('test/resources/categories/empty.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=[])
        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all(self):
        with open(Path('test/resources/categories/all.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_only_barlines(self):
        with open(Path('test/resources/categories/only_barlines.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=kp.TokenCategory.BARLINES)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all_less_note_rest(self):
        with open(Path('test/resources/categories/all_less_note_rest.krn'), 'r') as f:
            expected = f.read()
        real_output = kp.dumps(self.static_complex_doc, exclude=kp.TokenCategory.NOTE_REST)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all_less_durations(self):
        with open(Path('test/resources/categories/all_less_durations.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, exclude=kp.TokenCategory.DURATION)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all_less_pitches(self):
        with open(Path('test/resources/categories/all_less_pitches.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, exclude=kp.TokenCategory.PITCH)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_include_all_less_decorators(self):
        with open(Path('test/resources/categories/all_less_decorators.krn'), 'r') as f:
            expected = f.read()
        real_output = kp.dumps(self.static_complex_doc, exclude=kp.TokenCategory.DECORATION)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_only_durations(self):
        with open(Path('test/resources/categories/only_durations.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=kp.TokenCategory.DURATION)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_only_pitches(self):
        with open(Path('test/resources/categories/only_pitches.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=kp.TokenCategory.PITCH)

        self.assertEqual(expected, real_output)

    def test_generic_dumps_only_decorators(self):
        with open(Path('test/resources/categories/only_decorators.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc, include=kp.TokenCategory.DECORATION)

        self.assertEqual(expected, real_output, f"Expected:\n{expected}\n\nReal:\n{real_output}")

    def test_generic_dumps_include_note_rest_exclude_decorators(self):
        with open(Path('test/resources/categories/note_rest_exclude_decorators.krn'), 'r') as f:
            expected = f.read()

        real_output = kp.dumps(self.static_complex_doc,
                               include=kp.TokenCategory.NOTE_REST,
                               exclude=kp.TokenCategory.DECORATION)

        self.assertEqual(expected, real_output)

    def test_normalize_and_bekern_categories(self):
        # Arrange
        input_file = Path('test/resources/samples/nine-voices-score.krn')
        expected_file = Path('test/resources/samples/nine-voices-score_normalized.krn')

        with open(expected_file, 'r') as f:
            expected = f.read()

        # Act
        doc, err = kp.load(input_file)

        # Assert
        self.assertEqual(len(doc.get_all_tokens()), 13095, "Tokens count mismatch")
        self.assertEqual(len(err), 0, f"Errors found: {err}")
        real_output = kp.dumps(doc, include=kp.BEKERN_CATEGORIES)
        self.assertEqual(expected, real_output, f"Expected:\n{expected}\n\nGot:\n{real_output}")


    def test_is_monophonic_when_true(self):
        # Arrange
        input_file = Path('test/resources/samples/monophonic-score.krn')

        # Act
        doc, _err = kp.load(input_file)

        # Assert
        self.assertTrue(kp.is_monophonic(doc), "Document should be monophonic")

    def test_is_monophonic_when_false(self):
        # Arrange
        input_file = Path('test/resources/samples/polyphonic-score.krn')

        # Act
        doc, _err = kp.load(input_file)

        # Assert
        self.assertFalse(kp.is_monophonic(doc), "Document should not be monophonic")


class MergeInternalStrategiesTestCase(unittest.TestCase):
    MERGE_RESOURCES_DIR = Path('test/resources/merge')
    GRANDSTAFF_PATH = Path('test/resources/grandstaff/5901766.krn')
    BACH_PATH = Path('test/resources/samples/bach-brandenburg-bwv1050a.krn')
    JAZZMXHM_PATH = Path('test/resources/samples/jazzmus_with_mxhm.krn')
    MONOPHONIC_PATH = Path('test/resources/samples/monophonic-score.krn')
    GRANDSTAFF_NON_CORE_MISMATCH_PATH = Path('test/resources/merge/grandstaff_5901766_non_core_mismatch.krn')

    @classmethod
    def setUpClass(cls):
        cls.monophonic_content = cls.MONOPHONIC_PATH.read_text()
        cls.grandstaff_content = cls.GRANDSTAFF_PATH.read_text()
        cls.bach_content = cls.BACH_PATH.read_text()
        cls.jazzmxhm_content = cls.JAZZMXHM_PATH.read_text()
        cls.grandstaff_non_core_mismatch_content = cls.GRANDSTAFF_NON_CORE_MISMATCH_PATH.read_text()

    @staticmethod
    def _kern_doc_a() -> str:
        return '**kern\n=1\n4c\n=2\n4d\n*-\n'

    @staticmethod
    def _kern_doc_b() -> str:
        return '**kern\n=1\n4e\n=2\n4f\n*-\n'

    @staticmethod
    def _kern_dynam_doc() -> str:
        return '**kern\t**dynam\n=1\t=1\n=2\t=2\n*-\t*-\n'

    @staticmethod
    def _kern_root_doc() -> str:
        return '**kern\t**root\n=1\t=1\n=2\t=2\n*-\t*-\n'

    def _expected_content(self, filename: str) -> str:
        return (self.MERGE_RESOURCES_DIR / filename).read_text()

    def _expected_header_mismatch_message(self) -> str:
        return (
            "Documents are not compatible for merge. "
            "Headers do not match with only_check_core_spines=False. "
            "left: ['**kern', '**dynam'], right: ['**kern', '**root']."
        )

    def test_merge_strategy_a_requires_at_least_two_documents(self):
        # Arrange
        expected_msg_empty = "Merge action requires at least two documents to merge. But 0 was given."
        expected_msg_one = "Merge action requires at least two documents to merge. But 1 was given."

        # Act + Assert
        with self.assertRaises(ValueError) as ctx_empty:
            Generic._merge_documents_via_add(contents=[])
        self.assertEqual(expected_msg_empty, str(ctx_empty.exception))

        with self.assertRaises(ValueError) as ctx_one:
            Generic._merge_documents_via_add(contents=[self._kern_doc_a()])
        self.assertEqual(expected_msg_one, str(ctx_one.exception))

    def test_merge_strategy_a_merges_two_basic_documents(self):
        # Arrange
        merged_doc, indexes = Generic._merge_documents_via_add(
            contents=[self._kern_doc_a(), self._kern_doc_b()],
            strict=True,
        )

        # Assert
        self.assertIsInstance(merged_doc, kp.Document)
        self.assertEqual(2, len(indexes))

        merged_content = kp.dumps(merged_doc)
        self.assertIn('4c', merged_content)
        self.assertIn('4f', merged_content)

    def test_merge_strategy_a_polyphonic_and_monophonic_snapshots(self):
        cases = [
            (
                'monophonic_x2',
                [self.monophonic_content, self.monophonic_content],
                'expected_merge_monophonic_x2.krn',
                False,
            ),
            (
                'grandstaff_x2',
                [self.grandstaff_content, self.grandstaff_content],
                'expected_merge_grandstaff_x2.krn',
                False,
            ),
            (
                'bach_x2',
                [self.bach_content, self.bach_content],
                'expected_merge_bach_x2.krn',
                False,
            ),
            (
                'grandstaff_non_core_only_core_true',
                [self.grandstaff_content, self.grandstaff_non_core_mismatch_content],
                'expected_merge_grandstaff_non_core_only_core_true.krn',
                True,
            ),
        ]

        for case_name, contents, expected_file, only_check_core_spines in cases:
            with self.subTest(case=case_name):
                # Arrange
                expected_content = self._expected_content(expected_file)

                # Act
                merged_doc, indexes = Generic._merge_documents_via_add(
                    contents=contents,
                    strict=True,
                    raise_on_header_mismatch=True,
                    only_check_core_spines=only_check_core_spines,
                )
                real_content = kp.dumps(merged_doc)

                # Assert
                self.assertEqual(expected_content, real_content)
                self.assertEqual(len(contents), len(indexes))

    def test_merge_strategy_a_rejects_header_mismatch_by_default(self):
        # Arrange
        expected_message = self._expected_header_mismatch_message()

        # Act + Assert
        with self.assertRaises(ValueError) as ctx:
            Generic._merge_documents_via_add(
                contents=[self._kern_dynam_doc(), self._kern_root_doc()],
                strict=True,
                raise_on_header_mismatch=True,
                only_check_core_spines=False,
            )
        self.assertEqual(expected_message, str(ctx.exception))

    def test_merge_strategy_a_flag_matrix_for_non_core_header_mismatch(self):
        contents = [self.grandstaff_content, self.grandstaff_non_core_mismatch_content]

        for raise_on_header_mismatch in [True, False]:
            for only_check_core_spines in [True, False]:
                with self.subTest(
                        raise_on_header_mismatch=raise_on_header_mismatch,
                        only_check_core_spines=only_check_core_spines,
                ):
                    # Arrange
                    expected_snapshot = None
                    if only_check_core_spines:
                        expected_snapshot = self._expected_content(
                            'expected_merge_grandstaff_non_core_only_core_true.krn'
                        )

                    # Act + Assert
                    if only_check_core_spines:
                        merged_doc, _ = Generic._merge_documents_via_add(
                            contents=contents,
                            strict=True,
                            raise_on_header_mismatch=raise_on_header_mismatch,
                            only_check_core_spines=only_check_core_spines,
                        )
                        self.assertEqual(expected_snapshot, kp.dumps(merged_doc))
                    elif raise_on_header_mismatch:
                        with self.assertRaises(ValueError):
                            Generic._merge_documents_via_add(
                                contents=contents,
                                strict=True,
                                raise_on_header_mismatch=raise_on_header_mismatch,
                                only_check_core_spines=only_check_core_spines,
                            )
                    else:
                        with self.assertRaises(Exception):
                            Generic._merge_documents_via_add(
                                contents=contents,
                                strict=True,
                                raise_on_header_mismatch=raise_on_header_mismatch,
                                only_check_core_spines=only_check_core_spines,
                            )

    def test_merge_strategy_a_flag_matrix_for_core_header_mismatch(self):
        contents = [self.monophonic_content, self.grandstaff_content]

        for raise_on_header_mismatch in [True, False]:
            for only_check_core_spines in [True, False]:
                with self.subTest(
                        raise_on_header_mismatch=raise_on_header_mismatch,
                        only_check_core_spines=only_check_core_spines,
                ):
                    # Act + Assert
                    if raise_on_header_mismatch:
                        with self.assertRaises(ValueError):
                            Generic._merge_documents_via_add(
                                contents=contents,
                                strict=True,
                                raise_on_header_mismatch=raise_on_header_mismatch,
                                only_check_core_spines=only_check_core_spines,
                            )
                    else:
                        with self.assertRaises(Exception):
                            Generic._merge_documents_via_add(
                                contents=contents,
                                strict=True,
                                raise_on_header_mismatch=raise_on_header_mismatch,
                                only_check_core_spines=only_check_core_spines,
                            )

    def test_merge_strategy_a_jazzmxhm_raises_parse_error_for_all_flag_combinations(self):
        contents = [self.monophonic_content, self.jazzmxhm_content]

        for raise_on_header_mismatch in [True, False]:
            for only_check_core_spines in [True, False]:
                with self.subTest(
                        raise_on_header_mismatch=raise_on_header_mismatch,
                        only_check_core_spines=only_check_core_spines,
                ):
                    with self.assertRaises(ValueError):
                        Generic._merge_documents_via_add(
                            contents=contents,
                            strict=False,
                            raise_on_header_mismatch=raise_on_header_mismatch,
                            only_check_core_spines=only_check_core_spines,
                        )

    def test_merge_strategy_a_allows_non_core_header_mismatch_when_only_check_core_spines(self):
        merged_doc, indexes = Generic._merge_documents_via_add(
            contents=[self._kern_dynam_doc(), self._kern_root_doc()],
            strict=True,
            raise_on_header_mismatch=True,
            only_check_core_spines=True,
        )

        self.assertIsInstance(merged_doc, kp.Document)
        self.assertEqual(2, len(indexes))

    def test_merge_strategy_b_roundtrip_basic(self):
        # Arrange
        merged_doc, indexes = Generic._merge_documents_via_filtered_roundtrip(
            contents=[self._kern_doc_a(), self._kern_doc_b()],
            strict=True,
            raise_on_header_mismatch=True,
            only_check_core_spines=False,
        )

        # Assert
        self.assertIsInstance(merged_doc, kp.Document)
        self.assertEqual(2, len(indexes))

        merged_content = kp.dumps(merged_doc)
        self.assertIn('4c', merged_content)
        self.assertIn('4f', merged_content)

    def test_merge_strategy_b_requires_at_least_two_documents(self):
        # Arrange
        expected_msg_empty = "Merge action requires at least two documents to merge. But 0 was given."
        expected_msg_one = "Merge action requires at least two documents to merge. But 1 was given."

        # Act + Assert
        with self.assertRaises(ValueError) as ctx_empty:
            Generic._merge_documents_via_filtered_roundtrip(contents=[])
        self.assertEqual(expected_msg_empty, str(ctx_empty.exception))

        with self.assertRaises(ValueError) as ctx_one:
            Generic._merge_documents_via_filtered_roundtrip(contents=[self._kern_doc_a()])
        self.assertEqual(expected_msg_one, str(ctx_one.exception))

    def test_merge_strategy_b_rejects_header_mismatch_by_default_with_exact_message(self):
        # Arrange
        expected_message = self._expected_header_mismatch_message()

        # Act + Assert
        with self.assertRaises(ValueError) as ctx:
            Generic._merge_documents_via_filtered_roundtrip(
                contents=[self._kern_dynam_doc(), self._kern_root_doc()],
                strict=True,
                raise_on_header_mismatch=True,
                only_check_core_spines=False,
            )
        self.assertEqual(expected_message, str(ctx.exception))

    def test_merge_strategy_b_polyphonic_snapshot(self):
        # Arrange
        expected_content = self._expected_content('expected_merge_grandstaff_x2.krn')

        # Act
        merged_doc, indexes = Generic._merge_documents_via_filtered_roundtrip(
            contents=[self.grandstaff_content, self.grandstaff_content],
            strict=True,
            raise_on_header_mismatch=True,
            only_check_core_spines=False,
        )
        real_content = kp.dumps(merged_doc)

        # Assert
        self.assertEqual(expected_content, real_content)
        self.assertEqual(2, len(indexes))

    def test_merge_strategy_b_jazzmxhm_raises_parse_error_for_all_flag_combinations(self):
        contents = [self.monophonic_content, self.jazzmxhm_content]

        for raise_on_header_mismatch in [True, False]:
            for only_check_core_spines in [True, False]:
                with self.subTest(
                        raise_on_header_mismatch=raise_on_header_mismatch,
                        only_check_core_spines=only_check_core_spines,
                ):
                    with self.assertRaises(ValueError):
                        Generic._merge_documents_via_filtered_roundtrip(
                            contents=contents,
                            strict=False,
                            raise_on_header_mismatch=raise_on_header_mismatch,
                            only_check_core_spines=only_check_core_spines,
                        )


class MergePublicApiDelegationTestCase(unittest.TestCase):

    MONOPHONIC_PATH = Path('test/resources/samples/monophonic-score.krn')
    GRANDSTAFF_PATH = Path('test/resources/grandstaff/5901766.krn')
    GRANDSTAFF_NON_CORE_MISMATCH_PATH = Path('test/resources/merge/grandstaff_5901766_non_core_mismatch.krn')

    @classmethod
    def setUpClass(cls):
        cls.monophonic_content = cls.MONOPHONIC_PATH.read_text()
        cls.grandstaff_content = cls.GRANDSTAFF_PATH.read_text()
        cls.grandstaff_non_core_mismatch_content = cls.GRANDSTAFF_NON_CORE_MISMATCH_PATH.read_text()

    def test_kp_merge_delegates_to_generic_merge(self):
        sentinel_document, _ = kp.loads(self.monophonic_content)
        sentinel_result = (sentinel_document, [(0, 1)])

        with patch('kernpy.io.public.generic.Generic.merge', return_value=sentinel_result) as mocked_merge:
            result = kp.merge(
                [self.monophonic_content, self.monophonic_content],
                raise_on_errors=True,
                raise_on_header_mismatch=True,
                only_check_core_spines=True,
            )

        mocked_merge.assert_called_once_with(
            contents=[self.monophonic_content, self.monophonic_content],
            strict=True,
            raise_on_header_mismatch=True,
            only_check_core_spines=True,
        )
        self.assertEqual(sentinel_result, result)

    def test_generic_merge_delegates_to_strategy_b(self):
        sentinel_document, _ = kp.loads(self.monophonic_content)
        sentinel_result = (sentinel_document, [(0, 1)])

        with patch.object(Generic, '_merge_documents_via_filtered_roundtrip', return_value=sentinel_result) as strategy_b:
            result = Generic.merge(
                contents=[self.monophonic_content, self.monophonic_content],
                strict=False,
                raise_on_header_mismatch=False,
                only_check_core_spines=True,
            )

        strategy_b.assert_called_once_with(
            contents=[self.monophonic_content, self.monophonic_content],
            strict=False,
            raise_on_header_mismatch=False,
            only_check_core_spines=True,
        )
        self.assertEqual(sentinel_result, result)

    def test_kp_merge_flag_matrix_non_core_mismatch(self):
        contents = [self.grandstaff_content, self.grandstaff_non_core_mismatch_content]

        for raise_on_header_mismatch in [True, False]:
            for only_check_core_spines in [True, False]:
                with self.subTest(
                        raise_on_header_mismatch=raise_on_header_mismatch,
                        only_check_core_spines=only_check_core_spines,
                ):
                    if only_check_core_spines:
                        doc, indexes = kp.merge(
                            contents,
                            raise_on_errors=True,
                            raise_on_header_mismatch=raise_on_header_mismatch,
                            only_check_core_spines=only_check_core_spines,
                        )
                        self.assertIsInstance(doc, kp.Document)
                        self.assertEqual(2, len(indexes))
                    elif raise_on_header_mismatch:
                        with self.assertRaises(ValueError):
                            kp.merge(
                                contents,
                                raise_on_errors=True,
                                raise_on_header_mismatch=raise_on_header_mismatch,
                                only_check_core_spines=only_check_core_spines,
                            )
                    else:
                        with self.assertRaises(Exception):
                            kp.merge(
                                contents,
                                raise_on_errors=True,
                                raise_on_header_mismatch=raise_on_header_mismatch,
                                only_check_core_spines=only_check_core_spines,
                            )


class MergeSpineOperationsTestCase(unittest.TestCase):

    @staticmethod
    def _build_spine_ops_doc(start_op: str, end_op: str) -> str:
        if start_op == '*^':
            rows = [
                '**kern',
                '*^',
                '4c\t4e',
            ]

            if end_op == '*^':
                rows.extend([
                    '*^\t*^',
                    '4g\t4b\t4d\t4f',
                    '*v\t*v\t*v\t*v',
                    '4a',
                ])
            else:
                rows.extend([
                    '*v\t*v',
                    '4g',
                ])
        else:
            rows = [
                '**kern',
                '*v',
                '4c',
            ]

            if end_op == '*^':
                rows.extend([
                    '*^',
                    '4d\t4f',
                    '*v\t*v',
                    '4g',
                ])
            else:
                rows.extend([
                    '*v',
                    '4d',
                ])

        rows.append('*-')
        return '\n'.join(rows) + '\n'

    @parameterized.expand([
        ('start_split_end_split', '*^', '*^'),
        ('start_split_end_join', '*^', '*v'),
        ('start_join_end_split', '*v', '*^'),
        ('start_join_end_join', '*v', '*v'),
    ])
    def test_merge_strategy_a_with_spine_ops_combinations(self, _case_name: str, start_op: str, end_op: str):
        # Arrange
        content = self._build_spine_ops_doc(start_op, end_op)

        # Act
        doc, indexes = Generic._merge_documents_via_add(
            contents=[content, content],
            strict=True,
            raise_on_header_mismatch=True,
            only_check_core_spines=False,
        )

        # Assert
        self.assertIsInstance(doc, kp.Document)
        self.assertEqual(2, len(indexes))
        self.assertIn('**kern', kp.dumps(doc))

    @parameterized.expand([
        ('start_split_end_split', '*^', '*^'),
        ('start_split_end_join', '*^', '*v'),
        ('start_join_end_split', '*v', '*^'),
        ('start_join_end_join', '*v', '*v'),
    ])
    def test_merge_strategy_b_with_spine_ops_combinations(self, _case_name: str, start_op: str, end_op: str):
        # Arrange
        content = self._build_spine_ops_doc(start_op, end_op)

        # Act
        doc, indexes = Generic._merge_documents_via_filtered_roundtrip(
            contents=[content, content],
            strict=True,
            raise_on_header_mismatch=True,
            only_check_core_spines=False,
        )

        # Assert
        self.assertIsInstance(doc, kp.Document)
        self.assertEqual(2, len(indexes))
        self.assertIn('**kern', kp.dumps(doc))