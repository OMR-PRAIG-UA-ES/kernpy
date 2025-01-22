# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import unittest
import logging
import sys

import kernpy as kp

logger = logging.getLogger()
logger.level = logging.INFO  # change it DEBUG to trace errors
logger.addHandler(logging.StreamHandler(sys.stdout))


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
        self.do_test_token_exported("32qqbb-\LLL", "32@qq@bb@-·L·\\")

    def test_measure(self):
        self.do_test_token_exported("=:|!-", "=:|!")

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
        self.do_test_token_category("*ICklav", kp.TokenCategory.INSTRUMENTS)


if __name__ == '__main__':
    unittest.main()
