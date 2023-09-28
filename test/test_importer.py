# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import unittest
from src.kern2bekern import Kern2bekernConverter
import logging
import sys

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))


class ImporterTestCase(unittest.TestCase):
    # it loads a simple JSON file
    def testReadMinimalKern(self):
        importer = Kern2bekernConverter()
        importer.doImportFile('test/resource_dir/unit/minimal.krn')
        # self.assertEqual(1, len(ts.files))

    def testClefs(self):
        importer = Kern2bekernConverter()
        importer.doImportFile('test/resource_dir/unit/clefs.krn')
        # self.assertEqual(1, len(ts.files))


def test():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
