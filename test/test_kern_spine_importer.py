# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import os
import unittest
import logging
import sys
import tempfile
from PIL import Image


from pykern import HumdrumImporter, KernSpineImporter
from pykern.polish_scores.download_polish_dataset import convert_and_download_file

logger = logging.getLogger()
logger.level = logging.INFO  # change it DEBUG to trace errors
logger.addHandler(logging.StreamHandler(sys.stdout))


class KernSpineImporterTest(unittest.TestCase):
    """Used to test individual tokens"""

    def test1(self):
        input = "32qqbb-\LLL"
        importer = KernSpineImporter()
        token = importer.doImport(input)


if __name__ == '__main__':
    unittest.main()
