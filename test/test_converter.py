# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import unittest
from src.kern_2_ekern import Kern2EkernConverter
import logging
import sys
import tempfile
import os


logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

output_folder = tempfile.gettempdir()


class ImporterTestCase(unittest.TestCase):
    # it converts a simple file
    def testReadMinimalKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/minimal.krn', os.path.join(output_folder, 'minimal.ekrn') )
        # self.assertEqual(1, len(ts.files))

    # it converts a simple file
    def testCorelli(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/samples/corelli-op01n12d.krn', os.path.join(output_folder, 'corelli.ekrn') )
        # self.assertEqual(1, len(ts.files))


def test():
    print(f'Output of test files into {output_folder}')
    unittest.main()


if __name__ == '__main__':
    unittest.main()
