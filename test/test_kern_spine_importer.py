# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import os
import unittest
import logging
import sys
import tempfile
from PIL import Image

from kernpy import HumdrumImporter, KernSpineImporter
from kernpy.polish_scores.download_polish_dataset import convert_and_download_file

logger = logging.getLogger()
logger.level = logging.INFO  # change it DEBUG to trace errors
logger.addHandler(logging.StreamHandler(sys.stdout))


class KernSpineImporterTest(unittest.TestCase):
    """Used to test individual tokens"""

    def doTest(self, input, expected):
        importer = KernSpineImporter()
        token = importer.doImport(input)
        self.assertIsNotNone(token)
        self.assertEquals(expected, token.export())

    def test1(self):
        self.doTest("32qqbb-\LLL", "32@qq@bb@-·LLL·\\")

    def test2(self):
        self.doTest("=:|!-", "=:|!")

    def testRemoveRepeated(self):
        self.doTest("32qqbb-///LLL", "32@qq@bb@-·/·LLL")
        self.doTest("32qqbb-\\\\\\LLL", "32@qq@bb@-·LLL·\\")


if __name__ == '__main__':
    unittest.main()
