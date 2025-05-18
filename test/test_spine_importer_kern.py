import unittest
import sys
from pathlib import Path

import kernpy as kp


class KernSpineImporterTest(unittest.TestCase):
    """Used to test individual tokens"""

    def do_test_token_exported(self, input, expected):
        importer = kp.KernSpineImporter()
        token = importer.import_token(input)
        self.assertIsNotNone(token)
        self.assertEqual(expected, token.export())

        return token

    def do_test_token_category(self, input, expected_category):
        importer = kp.KernSpineImporter()
        token = importer.import_token(input)
        self.assertIsNotNone(token)
        self.assertEqual(expected_category, token.category)

        return token

    def test_complex(self):
        encoding_input = "32qqbb-\LLL"
        self.do_test_token_exported(encoding_input, "32@qq@bb@-·L·\\")
        self.do_test_token_category(encoding_input, kp.TokenCategory.NOTE_REST)

    def test_time_signature(self):
        self.do_test_token_exported("*M4/4", "*M4/4")
        self.do_test_token_category("*M4/4", kp.TokenCategory.TIME_SIGNATURE)

    def test_empty(self):
        self.do_test_token_exported("*", "*")
        self.do_test_token_category("*", kp.TokenCategory.EMPTY)

    def test_measure(self):
        encoding_input = "=:|!-"
        self.do_test_token_exported(encoding_input, "=:|!")
        self.do_test_token_category(encoding_input, kp.TokenCategory.BARLINES)

    def test_duration_pitch(self):
        self.do_test_token_exported("4a", "4@a")

    def test_pitch_duration(self):
        self.do_test_token_exported("a4", "4@a")

    def test_duration_rest(self):
        self.do_test_token_exported("2r", "2@r")

    def test_rest_duration(self):
        self.do_test_token_exported("r2", "2@r")

    def test_open_slur_wrong_order(self):
        self.do_test_token_exported("4E#(", "4@E@#·(")
        self.do_test_token_exported("4E(#", "4@E@#·(")
        self.do_test_token_exported("4(E#", "4@E@#·(")
        self.do_test_token_exported("(4E#", "4@E@#·(")

    def test_close_slur_wrong_order(self):
        self.do_test_token_exported("4E#)", "4@E@#·)")
        self.do_test_token_exported("4E)#", "4@E@#·)")
        self.do_test_token_exported("4)E#", "4@E@#·)")
        self.do_test_token_exported(")4E#", "4@E@#·)")

    def test_open_tie_wrong_order(self):
        self.do_test_token_exported("4E#[", "4@E@#·[")
        self.do_test_token_exported("4E[#", "4@E@#·[")
        self.do_test_token_exported("4[E#", "4@E@#·[")
        self.do_test_token_exported("[4E#[", "4@E@#·[")

    def test_close_tie_wrong_order(self):
        self.do_test_token_exported("4E#]", "4@E@#·]")
        self.do_test_token_exported("4E]#", "4@E@#·]")
        self.do_test_token_exported("4]E#", "4@E@#·]")
        self.do_test_token_exported("]4E#", "4@E@#·]")

    def test_all_permutations(self):
        expected_exported = '2@.@bb@-@·_'
        all_permutations_path = Path('resource_dir/samples/permutations_of_2.bb-_ .krn')
        lines = [L for L in all_permutations_path.read_text(encoding="utf-8").splitlines() if L.strip()]

        for line in lines:
            with self.subTest(line=line):
                try:
                    importer = kp.KernSpineImporter()
                    token = importer.import_token(line)
                except Exception as e:
                    self.fail(f"Importing raised {type(e).__name__} for line {line!r}: {e}")

                # if import_token returns None we treat it as failure
                self.assertIsNotNone(token, f"import_token returned None for {line!r}")

                exported = token.export()
                self.assertEqual(
                    token.category, kp.TokenCategory.NOTE_REST,
                    f"Category mismatch: {token.category} != {kp.TokenCategory.NOTE_REST} for line {line!r}"
                )
                self.assertEqual(
                    exported, expected_exported,
                    f"Round-trip mismatch: exported {exported!r} != expected_exported ({expected_exported!r}). original {line!r}"
                )


    def test_remove_repeated(self):
        self.do_test_token_exported("8aLL", "8@a·L")
        self.do_test_token_exported("8aJJJ", "8@a·J")
        self.do_test_token_exported("32qqbb-///LLL", "32@qq@bb@-·/·L")
        self.do_test_token_exported("32qqbb-\\\\\\LLL", "32@qq@bb@-·L·\\")
        self.do_test_token_exported("4b::::", "4@b·:")

    def test_barline_simple(self):
        self.do_test_token_category("=", kp.TokenCategory.BARLINES)

    def test_barline_double(self):
        self.do_test_token_category("==", kp.TokenCategory.BARLINES)

    def test_with_more_elements(self):
        self.do_test_token_category("====", kp.TokenCategory.BARLINES)

    def test_barlines_with_numbers(self):
        self.do_test_token_category("=1-", kp.TokenCategory.BARLINES)
        self.do_test_token_category("=2", kp.TokenCategory.BARLINES)
        self.do_test_token_category("=3", kp.TokenCategory.BARLINES)
        self.do_test_token_category("=4", kp.TokenCategory.BARLINES)

    def test_barlines_with_repetitions_without_numbers(self):
        self.do_test_token_category("=!|:", kp.TokenCategory.BARLINES)
        self.do_test_token_category("=:|!|:", kp.TokenCategory.BARLINES)
        self.do_test_token_category("=:|!", kp.TokenCategory.BARLINES)

    def test_barlines_with_repetitions_with_numbers(self):
        self.do_test_token_category("=5!|:", kp.TokenCategory.BARLINES)
        self.do_test_token_category("=6:|!|:", kp.TokenCategory.BARLINES)
        self.do_test_token_category("=7:|!", kp.TokenCategory.BARLINES)

    def test_load_instrument(self):
        self.do_test_token_category("*IPiano", kp.TokenCategory.INSTRUMENTS)
        self.do_test_token_category("*I\"Cklav", kp.TokenCategory.INSTRUMENTS)


if __name__ == '__main__':
    unittest.main()
