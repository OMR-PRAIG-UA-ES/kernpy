# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import os
import unittest
import logging
import sys

from src.import_humdrum import HumdrumImporter, ExportOptions
from src.tokens import BEKERN_CATEGORIES

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))


class ImporterTestCase(unittest.TestCase):
    def doJustImportTest(self, kern_file):
        print(f'Importing {kern_file}')
        importer = HumdrumImporter()
        importer.doImportFile(kern_file)

    def doEKernTest(self, kern_file, expected_measure_start_rows):
        print(f'Importing {kern_file} and checking the ekern')
        importer = HumdrumImporter()
        importer.doImportFile(kern_file)

        ekern = os.path.splitext(kern_file)[0] + '.ekrn'

        # Read the content of both files
        with open(ekern, 'r') as file1:
            expected_content = file1.read()

        export_options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
        exported_ekern = importer.doExportProcessed(export_options)
        exported_measure_start_rows = importer.measure_start_rows

        if exported_ekern != expected_content:
            print('---- Expected content ----')
            print('--------------------------')
            print(expected_content)

            print('---- Exported content ----')
            print('--------------------------')
            print(exported_ekern)

        self.assertEquals(expected_content, exported_ekern)
        self.assertEquals(expected_measure_start_rows, exported_measure_start_rows)

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
        self.doEKernTest('resource_dir/legacy/base_tuplet.krn', [5])
        self.doEKernTest('resource_dir/legacy/guide02-example2-1.krn', [5, 8, 11, 15])
        self.doEKernTest('resource_dir/legacy/guide02-example2-3.krn', [8, 9, 18, 22, 30, 38])
        self.doEKernTest('resource_dir/legacy/guide02-example2-4.krn', [6, 12, 16, 23, 27, 33, 37, 47, 51])
        self.doEKernTest('resource_dir/legacy/guide06-example6-1.krn', [5, 18, 27])
        self.doEKernTest('resource_dir/legacy/guide06-example6-2.krn', [6, 15, 28, 41])
        self.doEKernTest('resource_dir/legacy/chor001.krn', [26, 27, 32, 37, 43, 46, 50, 55, 57, 60, 67, 74, 77, 82, 88, 93, 96, 102, 107, 114, 117, 122, 128, 130])
        self.doJustImportTest('resource_dir/legacy/chor009.krn') #, [23, 32, 39, 48, 53, 57, 65, 74, 83, 90, 99, 107, 116, 122])
        self.doJustImportTest('resource_dir/legacy/chor048.krn') #, [22, 27, 32, 41, 46, 56, 65, 74, 83, 91, 98])

    def testBoundingBoxes(self):
        self.doJustImportTest('resource_dir/polish/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn')

def test():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
