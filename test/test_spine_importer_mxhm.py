import kernpy as kp

import unittest


class MxhmSpineImporterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc_with_mxhm, _ = kp.load('resource_dir/samples/jazzmus_with_mxhm.krn')

    def do_test_token_exported(self, input_encoding, expected):
        importer = kp.MxhmSpineImporter()
        token = importer.import_token(input_encoding)
        self.assertIsNotNone(token)
        self.assertEqual(expected, token.export())

        return token

    def do_test_token_category(self, input_encoding, expected_category):
        importer = kp.MxhmSpineImporter()
        token = importer.import_token(input_encoding)
        self.assertIsNotNone(token)
        self.assertEqual(expected_category, token.category)

        return token


