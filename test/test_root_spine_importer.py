import unittest
import logging
import sys

import kernpy as kp

logger = logging.getLogger()
logger.level = logging.INFO  # change it DEBUG to trace errors
logger.addHandler(logging.StreamHandler(sys.stdout))


class RootSpineImporterTest(unittest.TestCase):
    """Used to test individual tokens"""

    def do_test_token_exported(self, input_encoding, expected):
        importer = kp.RootSpineImporter()
        token = importer.import_token(input_encoding)
        self.assertIsNotNone(token)
        self.assertEqual(expected, token.export())

        return token

    def do_test_token_category(self, input_encoding, expected_category):
        importer = kp.KernSpineImporter()
        token = importer.import_token(input_encoding)
        self.assertIsNotNone(token)
        self.assertEqual(expected_category, token.category)

        return token

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

