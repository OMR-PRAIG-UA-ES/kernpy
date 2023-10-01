# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import unittest
from src.kern_importer import HumdrumImporter
import logging
import sys

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))


class ImporterTestCase(unittest.TestCase):
    # it loads a simple file
    def testReadMinimalKern(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/minimal.krn')
        # self.assertEqual(1, len(ts.files))

    def testClefs(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/clefs.krn')
        # self.assertEqual(1, len(ts.files))

    def testOctaves(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/octaves.krn')
        # self.assertEqual(1, len(ts.files))

    def testBars(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/bars.krn')
        # self.assertEqual(1, len(ts.files))

    def testTime(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/time.krn')
        # self.assertEqual(1, len(ts.files))

    def testMensurations(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/mensurations.krn')
        # self.assertEqual(1, len(ts.files))

    def testAccidentals(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/accidentals.krn')
        # self.assertEqual(1, len(ts.files))

    def testAccidentalsWithAlterationDisplay(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/accidentals_alterationDisplay.krn')
        # self.assertEqual(1, len(ts.files))

    def testKey(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/key.krn')
        # self.assertEqual(1, len(ts.files))

    def testKeyDesignation(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/key_designation.krn')
        # self.assertEqual(1, len(ts.files))

    def testModal(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/modal.krn')
        # self.assertEqual(1, len(ts.files))

    def testChords(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/chords.krn')
        # self.assertEqual(1, len(ts.files))


def test():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
