import unittest
import pytest
from src.importer import KernImporter

class ImporterTestCase(unittest.TestCase):
    # it loads a simple JSON file
    def testReadMinimalKern(self):
        importer = KernImporter()
        importer.doImportFile('resource_dir/minimal.json')
        # self.assertEqual(1, len(ts.files))

def test():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
