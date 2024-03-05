# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import os
import unittest
import logging
import sys

from pykern import (
    HumdrumImporter,
    ExportOptions,
    BEKERN_CATEGORIES,
    DynSpineImporter,
    DynamSpineImporter,
    FingSpineImporter,
    HarmSpineImporter,
    KernSpineImporter,
    MensSpineImporter,
    RootSpineImporter,
    TextSpineImporter,
)


logger = logging.getLogger()
logger.level = logging.INFO # change it DEBUG to trace errors
logger.addHandler(logging.StreamHandler(sys.stdout))


class ImporterTestCase(unittest.TestCase):
    def doJustImportTest(self, kern_file):
        logging.info(f'Importing {kern_file}')
        importer = HumdrumImporter()
        importer.doImportFile(kern_file)

    def checkEquals(self, kern_file, expected_ekern, from_measure, to_measure):
        importer = HumdrumImporter()
        importer.doImportFile(kern_file)
        # Read the content of both files
        with open(expected_ekern, 'r') as file1:
            expected_content = file1.read()

        export_options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
        export_options.from_measure = from_measure
        export_options.to_measure = to_measure
        exported_ekern = importer.doExportProcessed(export_options)

        if exported_ekern != expected_content:
            logging.info('---- Expected content ----')
            logging.info('--------------------------')
            logging.info(expected_content)

            logging.info('---- Exported content ----')
            logging.info('--------------------------')
            logging.info(exported_ekern)

        self.assertEquals(expected_content, exported_ekern)
        return importer

    def doEKernTest(self, kern_file, expected_measure_start_rows):
        """
        :param kern_file:
        :param expected_measure_start_rows: Rows after removing empty lines and line comments
        :return:
        """
        logging.info(f'Importing {kern_file} and checking the ekern')
        ekern = os.path.splitext(kern_file)[0] + '.ekrn'
        importer = self.checkEquals(kern_file, ekern, None, None)

        exported_measure_start_rows = importer.measure_start_rows
        self.assertEquals(expected_measure_start_rows, exported_measure_start_rows)

    def doEKernMeasureToMeasureTest(self, kern_file, from_measure, to_measure):
        logging.info(f'Importing {kern_file} and checking the ekern')
        ekern = f'{os.path.splitext(kern_file)[0]}-m{from_measure}-to-m{to_measure}.ekrn'
        importer = self.checkEquals(kern_file, ekern, from_measure, to_measure)


    def doTestCountSpines(self, kern_file, row_count, spine_counts):
        logging.info(f'Importing {kern_file}')
        importer = HumdrumImporter()
        importer.doImportFile(kern_file)
        self.assertEquals(row_count, importer.getMaxRows())
        num_rows = importer.getMaxRows()
        num_spines = len(importer.spines)
        self.assertEquals(num_spines, len(spine_counts), "Num. spines")
        for i in range(num_rows):
            for j in range(num_spines):
                subspines = importer.spines[j].getNumSubspines(i)
                self.assertEquals(spine_counts[j][i], subspines, f"Spine in row #{i+1} and spine #{j+1}")


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
        self.doJustImportTest('resource_dir/unit/accidentals_alteration_display.krn')
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
        self.doEKernTest('resource_dir/legacy/guide02-example2-3.krn', [8, 9, 18, 22, 30, 37])
        self.doEKernTest('resource_dir/legacy/guide02-example2-4.krn', [6, 12, 16, 23, 27, 33, 37, 47, 51])
        self.doEKernTest('resource_dir/legacy/guide06-example6-1.krn', [5, 18, 27])
        self.doEKernTest('resource_dir/legacy/guide06-example6-2.krn', [5, 14, 27, 40])
        self.doEKernTest('resource_dir/legacy/chor001.krn',
                         # rows with comments[26, 27, 32, 37, 43, 46, 50, 55, 57, 60, 67, 74, 77, 82, 88, 93, 96, 102, 107, 114, 117, 122, 128, 130])
                         # rows without comments
                         [11, 12, 17, 22, 28, 31, 35, 40, 42, 45, 52, 58, 61, 66, 72, 77, 80, 86, 91, 98, 101, 106, 112, 114])
        self.doJustImportTest(
            'resource_dir/legacy/chor009.krn')  # , [23, 32, 39, 48, 53, 57, 65, 74, 83, 90, 99, 107, 116, 122])
        self.doJustImportTest('resource_dir/legacy/chor048.krn')  # , [22, 27, 32, 41, 46, 56, 65, 74, 83, 91, 98])

    def testBoundingBoxes(self):
        self.doJustImportTest(
            'resource_dir/polish/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn')

    def testHeader(self):
        importer = HumdrumImporter()
        importer.doImportFile('resource_dir/unit/headers.krn')
        self.assertEquals(8, len(importer.spines))
        self.assertTrue(isinstance(importer.spines[0].importer, KernSpineImporter))
        self.assertTrue(isinstance(importer.spines[1].importer, MensSpineImporter))
        self.assertTrue(isinstance(importer.spines[2].importer, DynamSpineImporter))
        self.assertTrue(isinstance(importer.spines[3].importer, DynSpineImporter))
        self.assertTrue(isinstance(importer.spines[4].importer, HarmSpineImporter))
        self.assertTrue(isinstance(importer.spines[5].importer, RootSpineImporter))
        self.assertTrue(isinstance(importer.spines[6].importer, TextSpineImporter))
        self.assertTrue(isinstance(importer.spines[7].importer, FingSpineImporter))

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
        self.doTestCountSpines('resource_dir/spines/spines-from-piano-joplin-bethena-start.krn', 23, [[1,1,1,1,1,2,2,1,1,2,2,1,1,2,2,1,1,1,1,1,1,1,1,1], [1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,2,2,1,1,1], [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])
        self.doTestCountSpines('resource_dir/spines/spines-piano-hummel-prelude67-15.krn', 19, [[1,1,1,1,1,1,1,1,2,3,3,3,3,1,1,2,2,1,1],[1,1,2,2,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])

        # Tests extracted from the discussion in  https://github.com/humdrum-tools/vhv-documentation/issues/7#event-3236429526
        self.doTestCountSpines('resource_dir/spines/1.krn', 18, [[1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1]])
        self.doTestCountSpines('resource_dir/spines/2.krn', 18, [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], [1,1,1,1,2,2,2,1,1,1,1,2,2,2,2,2,1,1]])
        self.doTestCountSpines('resource_dir/spines/3.krn', 16, [[1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1],[1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1]])
        self.doTestCountSpines('resource_dir/spines/4.krn',17, [[1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,], [1,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1]])
        self.doTestCountSpines('resource_dir/spines/5.krn',24, [[1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,1,1], [1,1,1,1,2,2,2,3,3,3,1,1,2,3,3,3,3,3,3,1,1,1,1,1]])

    def testExtractMeasures(self):
        #self.doEKernMeasureToMeasureTest('resource_dir/polish/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn', 1, 2)
        self.doEKernMeasureToMeasureTest('resource_dir/polish/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn', 1, 3)
        #self.doEKernMeasureToMeasureTest('resource_dir/polish/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn', 1, 16)
        #self.doEKernMeasureToMeasureTest('resource_dir/legacy/chor001.krn', 1, 3)

#def test():
#    unittest.main()


if __name__ == '__main__':
    unittest.main()
