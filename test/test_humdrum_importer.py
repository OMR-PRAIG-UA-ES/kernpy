# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import os
import unittest
import logging
import sys

from src.import_humdrum import HumdrumImporter

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))


class ImporterTestCase(unittest.TestCase):
    def doJustImportTest(self, kern_file):
        print(f'Importing {kern_file}')
        importer = HumdrumImporter()
        importer.doImportFile(kern_file)

    def doEKernTest(self, kern_file):
        print(f'Importing {kern_file} and checking the ekern')
        importer = HumdrumImporter()
        importer.doImportFile(kern_file)

        ekern = os.path.splitext(kern_file)[0] + '.ekrn'

        # Read the content of both files
        with open(ekern, 'r') as file1:
            expected_content = file1.read()

        exported_ekern = importer.doExportProcessed()
        self.assertEquals(expected_content, exported_ekern)

    # it loads a simple file
    def testReadMinimalKern(self):
        self.doJustImportTest('resource_dir/unit/minimal.krn')
        # self.assertEqual(1, len(ts.files))

    def testClefs(self):
        self.doJustImportTest('resource_dir/unit/clefs.krn')
        # self.assertEqual(1, len(ts.files))

    def testOctaves(self):
        self.doJustImportTest('resource_dir/unit/octaves.krn')
        # self.assertEqual(1, len(ts.files))

    def testBars(self):
        self.doJustImportTest('resource_dir/unit/bars.krn')
        # self.assertEqual(1, len(ts.files))

    def testTime(self):
        self.doJustImportTest('resource_dir/unit/time.krn')
        # self.assertEqual(1, len(ts.files))

    def testMensurations(self):
        self.doJustImportTest('resource_dir/unit/mensurations.krn')
        # self.assertEqual(1, len(ts.files))

    def testAccidentals(self):
        self.doJustImportTest('resource_dir/unit/accidentals.krn')
        # self.assertEqual(1, len(ts.files))

    def testAccidentalsWithAlterationDisplay(self):
        self.doJustImportTest('resource_dir/unit/accidentals_alterationDisplay.krn')
        # self.assertEqual(1, len(ts.files))

    def testKey(self):
        self.doJustImportTest('resource_dir/unit/key.krn')
        # self.assertEqual(1, len(ts.files))

    def testKeyDesignation(self):
        self.doJustImportTest('resource_dir/unit/key_designation.krn')
        # self.assertEqual(1, len(ts.files))

    def testModal(self):
        self.doJustImportTest('resource_dir/unit/modal.krn')
        # self.assertEqual(1, len(ts.files))

    def testChords(self):
        self.doJustImportTest('resource_dir/unit/chords.krn')
        # self.assertEqual(1, len(ts.files))

    def testRythm(self):
        self.doJustImportTest('resource_dir/unit/rhythm.krn')
        # self.assertEqual(1, len(ts.files))

    def testTies(self):
        self.doJustImportTest('resource_dir/unit/ties.krn')
        # self.assertEqual(1, len(ts.files))

    def testBeams(self):
        self.doJustImportTest('resource_dir/unit/beaming.krn')
        # self.assertEqual(1, len(ts.files))

    def testAutoBeam(self):
        self.doJustImportTest('resource_dir/unit/auto_beaming.krn')
        # self.assertEqual(1, len(ts.files))

    def testRests(self):
        self.doJustImportTest('resource_dir/unit/rests.krn')
        # self.assertEqual(1, len(ts.files))

    def testSlurs(self):
        self.doJustImportTest('resource_dir/unit/slurs.krn')
        # self.assertEqual(1, len(ts.files))

    def testArticulations(self):
        self.doJustImportTest('resource_dir/unit/articulations.krn')
        # self.assertEqual(1, len(ts.files))

    def testOrnaments(self):
        self.doJustImportTest('resource_dir/unit/ornaments.krn')
        # self.assertEqual(1, len(ts.files))

    def testLegacyTests(self):
        self.doEKernTest('resource_dir/legacy/base_tuplet.krn')
        self.doJustImportTest('resource_dir/legacy/chor001.krn')
        self.doJustImportTest('resource_dir/legacy/chor009.krn')
        self.doJustImportTest('resource_dir/legacy/chor048.krn')
        self.doJustImportTest('resource_dir/legacy/guide02-example2-1.krn')
        self.doJustImportTest('resource_dir/legacy/guide02-example2-3.krn')
        self.doJustImportTest('resource_dir/legacy/guide02-example2-4.krn')
        self.doJustImportTest('resource_dir/legacy/guide06-example6-1.krn')
        self.doJustImportTest('resource_dir/legacy/guide06-example6-2.krn')



def test():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
