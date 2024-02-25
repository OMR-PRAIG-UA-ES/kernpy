# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import os
import unittest
import logging
import sys

# import pykern # pythonic way: import pykern; pykern.HumdrumImporter...
from pykern import HumdrumImporter, ExportOptions, BEKERN_CATEGORIES

# from core.import_humdrum import HumdrumImporter, ExportOptions
# from core.tokens import BEKERN_CATEGORIES


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

    def doTestCountSpines(self, kern_file, row_count, spine_counts):
        print(f'Importing {kern_file}')
        importer = HumdrumImporter()
        importer.doImportFile(kern_file)
        self.assertEquals(row_count, importer.getMaxRows())
        num_rows = importer.getMaxRows()
        num_spines = len(importer.spines)
        self.assertEquals(num_spines, len(spine_counts), "Num. spines")
        for i in range(num_rows):
            for j in range(num_spines):
                subspines = importer.spines[j].getNumSubspines(i)
                self.assertEquals(spine_counts[j][i], subspines, f"Spine in row #{i+1} and column #{j+1}")


        #self.assertEquals(len(importer.spines), len(spine_counts))
        #for i in range(len(spine_counts))

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

    def testRhythm(self):
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
        self.doEKernTest('resource_dir/legacy/chor001.krn',
                         [26, 27, 32, 37, 43, 46, 50, 55, 57, 60, 67, 74, 77, 82, 88, 93, 96, 102, 107, 114, 117, 122,
                          128, 130])
        self.doJustImportTest(
            'resource_dir/legacy/chor009.krn')  # , [23, 32, 39, 48, 53, 57, 65, 74, 83, 90, 99, 107, 116, 122])
        self.doJustImportTest('resource_dir/legacy/chor048.krn')  # , [22, 27, 32, 41, 46, 56, 65, 74, 83, 91, 98])

    def testBoundingBoxes(self):
        self.doJustImportTest(
            'resource_dir/polish/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn')

    def testSamples(self):
        self.doJustImportTest('resource_dir/samples/bach-brandenburg-bwv1050a.krn')
        self.doJustImportTest('resource_dir/samples/bach-chorale-chor205.krn')
        self.doJustImportTest('resource_dir/samples/corelli-op01n12d.krn')
        self.doJustImportTest('resource_dir/samples/harmonized-song-erk052.krn')
        self.doJustImportTest('resource_dir/samples/haydn-quartet-op54n2-01.krn')
        self.doJustImportTest('resource_dir/samples/piano-beethoven-sonata21-3.krn')
        self.doJustImportTest('resource_dir/samples/piano-chopin-prelude28-17.krn')
        self.doJustImportTest('resource_dir/samples/piano-hummel-prelude67-15.krn')
        self.doJustImportTest('resource_dir/samples/piano-joplin-bethena.krn')
        self.doJustImportTest('resource_dir/samples/piano-mozart-sonata07-3.krn')
        self.doJustImportTest('resource_dir/samples/piano-scarlatti-L523K205.krn')
        self.doJustImportTest('resource_dir/samples/quartet-beethoven-quartet13-6.krn')
        self.doJustImportTest('resource_dir/samples/quartet-mozart-k590-04.krn')
        self.doJustImportTest('resource_dir/samples/unaccompanied-songs-nova073.krn')

    def testSpines(self):
        # Tests extracted from the discussion in  https://github.com/humdrum-tools/vhv-documentation/issues/7#event-3236429526
        self.doTestCountSpines('resource_dir/spines/1.krn', 18, [[1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1]])
        self.doTestCountSpines('resource_dir/spines/2.krn', 18, [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], [1,1,1,1,2,2,2,1,1,1,1,2,2,2,2,2,1,1]])
        self.doTestCountSpines('resource_dir/spines/3.krn', 16, [[1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1],[1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1]])
        self.doTestCountSpines('resource_dir/spines/4.krn',17, [[1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,], [1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1]])
        self.doTestCountSpines('resource_dir/spines/5.krn',24, [[1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,1,1], [1,1,1,1,2,2,2,3,3,3,1,1,2,3,3,3,3,3,3,1,1,1,1,1]])

#def test():
#    unittest.main()


if __name__ == '__main__':
    unittest.main()
