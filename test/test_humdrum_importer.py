# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import os
import unittest
import logging
import sys
from pathlib import Path

from _pytest.mark.expression import TokenType

import kernpy as kp

logger = logging.getLogger()
logger.level = logging.INFO  # change it DEBUG to trace errors
logger.addHandler(logging.StreamHandler(sys.stdout))


class ImporterTestCase(unittest.TestCase):
    def doJustImportTest(self, kern_file) -> kp.Document:
        logging.info(f'Importing {kern_file}')
        importer = kp.Importer()
        document = importer.import_file(kern_file)
        return document

    def checkEquals(self, kern_file, expected_ekern, from_measure, to_measure) -> kp.Document:
        importer = kp.Importer()
        document = importer.import_file(kern_file)
        if len(importer.errors) > 0:
            logging.error(f'Import errors for {kern_file}')
            for error in importer.errors:
                logging.error(f'\t{error}')

        dot_exporter = kp.GraphvizExporter()
        filename = os.path.basename(kern_file)
        #TODO No sé por qué me da error de recursión
        #dot_exporter.export_to_dot(document.tree, f'/tmp/{filename}.dot')

        # Read the content of both files
        with open(expected_ekern, 'r') as file1:
            expected_content = file1.read()

        exported_ekern = kp.dumps(document,
                                  spine_types=['**kern'],
                                  from_measure=from_measure,
                                  to_measure=to_measure,
                                  include=kp.BEKERN_CATEGORIES,
                                  tokenizer=kp.Encoding.eKern)

        if exported_ekern != expected_content:
            logging.info('---- Expected content ----')
            logging.info('--------------------------')
            logging.info(expected_content)

            logging.info('---- Exported content ----')
            logging.info('--------------------------')
            logging.info(exported_ekern)

        self.assertEqual(expected_content, exported_ekern)
        return document

    def doEKernTest(self, kern_file, expected_measure_start_rows):
        """
        :param kern_file:
        :param expected_measure_start_rows: Rows after removing empty lines and line comments
        :return:
        """
        logging.info(f'Importing {kern_file} and checking the ekern')
        ekern = os.path.splitext(kern_file)[0] + '.ekrn'
        document = self.checkEquals(kern_file, ekern, None, None)

        measure_start_tree_stages = document.measure_start_tree_stages
        self.assertEqual(expected_measure_start_rows, measure_start_tree_stages)

    def doEKernMeasureToMeasureTest(self, kern_file, from_measure, to_measure):
        logging.info(f'Importing {kern_file} and checking the ekern')
        ekern = f'{os.path.splitext(kern_file)[0]}-m{from_measure}-to-m{to_measure}.ekrn'
        self.checkEquals(kern_file, ekern, from_measure, to_measure)

    # it loads a simple file
    def testReadMinimalKern(self):
        document = self.doJustImportTest('resource_dir/unit/minimal.krn')
        dot_exporter = kp.GraphvizExporter()
        dot_exporter.export_to_dot(document.tree, '/tmp/minimal.dot')
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

    def testHeader(self):
        importer = kp.Importer()
        document = importer.import_file('resource_dir/unit/headers.krn')
        self.assertEqual(8, document.get_spine_count())
        header_stage = document.tree.stages[document.header_stage]
        expected_importers = [kp.KernSpineImporter, kp.MensSpineImporter, kp.DynamSpineImporter, kp.DynSpineImporter,
                              kp.HarmSpineImporter, kp.RootSpineImporter, kp.TextSpineImporter, kp.FingSpineImporter]
        for node, expected_importer in zip(header_stage, expected_importers):
            importer = kp.createImporter(node.token.encoding)
            self.assertTrue(isinstance(importer, expected_importer))

    def doTestCountSpines(self, kern_file, expected_stage_count, expected_spine_counts):
        logging.info(f'Importing {kern_file}')
        importer = kp.Importer()
        document = importer.import_file(kern_file)
        dot_exporter = kp.GraphvizExporter()
        filename = os.path.basename(kern_file)
        dot_exporter.export_to_dot(document.tree, f'/tmp/{filename}.dot')
        self.assertEqual(expected_stage_count, len(document.tree.stages) - 1, "Stage count")  # -1 to remove the root
        self.assertEqual(document.get_spine_count(), len(expected_spine_counts), "Num. spines")

        spine_counts = []
        for node in document.get_header_stage():
            spine_counts.append(node.count_nodes_by_stage())

        for i in range(document.get_spine_count()):
            self.assertListEqual(expected_spine_counts[i], spine_counts[i], f"{kern_file}, spine #{i + 1}")

    def testSpines(self):
        # Tests extracted from the discussion in  https://github.com/humdrum-tools/vhv-documentation/issues/7#event-3236429526
        self.doTestCountSpines('resource_dir/spines/non_stacked_ends.krn', 12,
                               [[1, 1, 2, 2, 3, 3, 4, 4, 2, 2, 1, 1]])  # in this test, three spines merge into one
        self.doTestCountSpines('resource_dir/spines/non_stacked_ends_2.krn', 10,
                               [[1, 1, 1, 1, 1, 1, 2, 2, 1, 1], [1, 1, 2, 2, 3, 3, 6, 6, 1, 1],
                                [1, 1, 1, 1, 1, 1, 2, 2, 1,
                                 1]])  # the last join in VHV leads to just one main spine - we've added an issue

        self.doTestCountSpines('resource_dir/spines/1.krn', 18,
                               [[1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1]])
        self.doTestCountSpines('resource_dir/spines/2.krn', 18, [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                                 [1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1,
                                                                  1]])
        self.doTestCountSpines('resource_dir/spines/3.krn', 16, [[1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1],
                                                                 [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1]])
        self.doTestCountSpines('resource_dir/spines/4.krn', 17, [[1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
                                                                 [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1]])
        self.doTestCountSpines('resource_dir/spines/5.krn', 24,
                               [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
                                [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 1, 1, 2, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1]])

        self.doTestCountSpines('resource_dir/spines/spines-from-piano-joplin-bethena-start.krn', 23,
                               [[1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
        self.doTestCountSpines('resource_dir/spines/spines-piano-hummel-prelude67-15.krn', 19,
                               [[1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 1, 1, 2, 2, 1, 1],
                                [1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

    def testLegacyTests(self):
        self.doEKernTest('resource_dir/legacy/base_tuplet.krn', [5])
        self.doEKernTest('resource_dir/legacy/guide02-example2-1.krn', [5, 8, 11, 15])
        self.doEKernTest('resource_dir/legacy/guide02-example2-3.krn', [8, 9, 18, 22, 30, 38])
        self.doEKernTest('resource_dir/legacy/guide02-example2-4.krn', [6, 12, 16, 23, 27, 33, 37, 47, 51])
        self.doEKernTest('resource_dir/legacy/guide06-example6-1.krn', [5, 18, 27])
        self.doEKernTest('resource_dir/legacy/guide06-example6-2.krn', [6, 15, 28, 41])
        self.doEKernTest('resource_dir/legacy/chor001.krn',
                         # rows with comments
                         [26, 27, 32, 37, 43, 46, 50, 55, 57, 60, 67, 74, 77, 82, 88, 93, 96, 102, 107, 114, 117, 122,
                          128, 130])
        # rows without comments
        #[11, 12, 17, 22, 28, 31, 35, 40, 42, 45, 52, 58, 61, 66, 72, 77, 80, 86, 91, 98, 101, 106, 112, 114])
        self.doJustImportTest(
            'resource_dir/legacy/chor009.krn')  # , [23, 32, 39, 48, 53, 57, 65, 74, 83, 90, 99, 107, 116, 122])
        self.doJustImportTest('resource_dir/legacy/chor048.krn')  # , [22, 27, 32, 41, 46, 56, 65, 74, 83, 91, 98])

    def testBoundingBoxes(self):
        self.doJustImportTest(
            'resource_dir/polish/test1/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn')

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

    def testExtractMeasures(self):
        self.doEKernMeasureToMeasureTest(
            'resource_dir/grandstaff/5901766.krn', 24, 28)

        self.doEKernMeasureToMeasureTest('resource_dir/spines/2.krn', 2, 2)
        self.doEKernMeasureToMeasureTest('resource_dir/legacy/chor001.krn', 1, 3)

        self.doEKernMeasureToMeasureTest(
            'resource_dir/polish/test2/pl-wn--mus-iii-123-982--001-004_wieniawski-henryk--l-ecole-moderne-etudes-caprices-pour-violon-seul-op-10-4-le-staccato.krn',
            1, 2)
        self.doEKernMeasureToMeasureTest(
            'resource_dir/polish/test1/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn', 1, 2)
        self.doEKernMeasureToMeasureTest(
            'resource_dir/polish/test1/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn', 1, 3)
        self.doEKernMeasureToMeasureTest(
            'resource_dir/polish/test1/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn', 1, 16)

        #self.doEKernMeasureToMeasureTest('resource_dir/polish/test2/pl-wn--mus-iii-123-982--001-004_wieniawski-henryk--l-ecole-moderne-etudes-caprices-pour-violon-seul-op-10-4-le-staccato.krn', 0, 1) # TODO: Correct it. It doesn't export all the required token_categories

    #TODO Joan: este test se puede hacer como el doEKernMeasureToMeasureTest, sin repetir tanto código...
    def test_extract_measures_same_measure(self):
        options = kp.ExportOptions(spine_types=['**kern'], kern_type=kp.Encoding.normalizedKern, from_measure=3,
                                   to_measure=3)
        importer = kp.Importer()
        document = importer.import_file('resource_dir/legacy/base_tuplet_longer.krn')

        exporter = kp.Exporter()
        real_ouputput = exporter.export_string(document, options)

        with open('resource_dir/legacy/base_tuplet_longer_m3-m3.krn', 'r') as f:
            expected_output = f.read()
        self.assertEqual(real_ouputput, expected_output)

    def test_extract_measures_middle_measures_to_krn(self):
        options = kp.ExportOptions(spine_types=['**kern'], kern_type=kp.Encoding.normalizedKern, from_measure=2,
                                   to_measure=4)
        importer = kp.Importer()
        document = importer.import_file('resource_dir/legacy/base_tuplet_longer.krn')

        exporter = kp.Exporter()
        real_ouputput = exporter.export_string(document, options)
        with open('resource_dir/legacy/base_tuplet_longer_m2-m4.krn', 'r') as f:
            expected_output = f.read()
        self.assertEqual(real_ouputput, expected_output)

    def test_extract_measures_middle_measures_to_ekrn(self):
        options = kp.ExportOptions(spine_types=['**kern'], kern_type=kp.Encoding.eKern, from_measure=2,
                                   to_measure=4)
        importer = kp.Importer()
        document = importer.import_file('resource_dir/legacy/base_tuplet_longer.krn')

        dot_exporter = kp.GraphvizExporter()
        dot_exporter.export_to_dot(document.tree, f'/tmp/base_tuplet_longer.dot')

        exporter = kp.Exporter()
        actual_output = exporter.export_string(document, options)
        with open('resource_dir/legacy/base_tuplet_longer_m2-m4.ekrn', 'r') as f:
            expected_output = f.read()
        self.assertEqual(actual_output, expected_output)

    def test_extract_measures_bad_measures_input(self):
        importer = kp.Importer()
        document = importer.import_file('resource_dir/legacy/base_tuplet_longer.krn')

        options = kp.ExportOptions(spine_types=['**kern'], from_measure=-1, to_measure=2)
        exporter = kp.Exporter()
        with self.assertRaises(ValueError):
            exporter.export_string(document, options)

        options = kp.ExportOptions(spine_types=['**kern'], from_measure=2, to_measure=-1)
        with self.assertRaises(ValueError):
            exporter.export_string(document, options)

        options = kp.ExportOptions(spine_types=['**kern'], from_measure=3, to_measure=2)
        with self.assertRaises(ValueError):
            exporter.export_string(document, options)

        options = kp.ExportOptions(spine_types=['**kern'], from_measure=None, to_measure=99999)
        with self.assertRaises(ValueError):
            exporter.export_string(document, options)

        options = kp.ExportOptions(spine_types=['**kern'], from_measure=None, to_measure=7)
        with self.assertRaises(ValueError):
            exporter.export_string(document, options)

    def test_extract_measures_when_spines_split_one_spine(self):
        doc, err = kp.load('resource_dir/samples/score_with_dividing_one_spine.krn')

        kp.store_graph(doc, '/tmp/x.dot')
        exported_real = kp.dumps(doc,
                                 spine_types=['**kern'],
                                 tokenizer=kp.Encoding.normalizedKern,
                                 from_measure=9,
                                 to_measure=13)

        with open('resource_dir/samples/score_with_dividing_one_spine_m9-m13.krn', 'r') as f:
            expected_output = f.read()
        with open('resource_dir/samples/score_with_dividing_one_spine_m9-m13.krn', 'w') as f:
            f.write(exported_real)
        self.assertEqual(expected_output, exported_real)

    def test_extract_measures_when_spines_split_two_spines(self):
        doc, err = kp.read('resource_dir/samples/score_with_dividing_two_spines.krn')
        export_otions = kp.ExportOptions(spine_types=['**kern'],
                                         kern_type=kp.Encoding.normalizedKern,
                                         from_measure=49,
                                         to_measure=56)

        exported_real = kp.export(doc, export_otions)

        with open('resource_dir/samples/score_with_dividing_two_spines_m49-m56.krn', 'r') as f:
            expected_output = f.read()
        self.assertEqual(expected_output, exported_real)

    def testOther(self):
        importer = self.doJustImportTest(
            'resource_dir/polish/test3/pl-wn--sd-xvi-qu-273--001-020_gomolka-mikolaj--melodiae-na-psalterz-polski-xx-wsiadaj-z-dobrym-sercem-o-krolu-cnotliwy.krn')
        print(importer)

    def testStringImporter(self):
        input_kern = "**kern\n4c\n4d\n4e\n4f\n*-"
        importer = kp.Importer()
        document = importer.import_string(input_kern)
        output_kern = kp.dumps(document,
                               spine_types=['**kern'],
                               include=kp.BEKERN_CATEGORIES,
                               tokenizer=kp.Encoding.eKern, )
        expected_ekern = "**ekern\n4@c\n4@d\n4@e\n4@f\n*-\n"
        self.assertEqual(expected_ekern, output_kern)

    def testLexicalError(self):
        input_kern = "**kern\ncleF4\n4c\n4d\n4e\n4f\n*-"
        importer = kp.Importer()
        importer.import_string(input_kern)
        self.assertEqual(1, len(importer.errors))

    def testParserError_only_the_last(self):
        input_kern = "**kern\n*clefF4\n4d\n4e\n4f\nc4\n*-"
        importer = kp.Importer()
        importer.import_string(input_kern)
        self.assertEqual(1, len(importer.errors))


    def testParserError_only_the_first_ensure_one_error_is_not_being_propagated(self):
        input_kern = "**kern\n*clefF4\nc4\n4d\n4e\n4f\n*-"
        importer = kp.Importer()
        importer.import_string(input_kern)
        self.assertNotEqual(4, len(importer.errors))
        self.assertEqual(1, len(importer.errors))

    def testLexicalParserError(self):
        input_kern = "**kern\ncleF4\nc4\n4d\n4e\n4f\n*-"
        importer = kp.Importer()
        importer.import_string(input_kern)
        self.assertEqual(2, len(importer.errors))

    def testMetacomment(self):
        input_kern = "!!!M1\n**kern\n*clefF4\n4c\n4d\n!!!M2\n4e\n4f\n*-"
        importer = kp.Importer()
        importer.import_string(input_kern)
        self.assertFalse(importer.has_errors())

    def test_metadatacomments_generic(self):
        input_kern_file = 'resource_dir/legacy/chor001.krn'
        output_metadata_array_expected = []
        with open('resource_dir/legacy/chor001-metadata-generic.txt', 'r') as f:
            for line in f:
                output_metadata_array_expected.append(line.strip())

        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        output_metadata_real = document.get_metacomments()

        self.assertListEqual(output_metadata_array_expected, output_metadata_real)

    def test_metadatacomments_specific_option(self):
        input_kern_file = 'resource_dir/legacy/chor001.krn'
        output_metadata_array_expected = ['!!!COM: Bach, Johann Sebastian']

        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        output_metadata_array_output = document.get_metacomments(KeyComment='COM')

        self.assertListEqual(output_metadata_array_expected, output_metadata_array_output)  # composer

    def test_metadatacomments_specific_option_clear(self):
        input_kern_file = 'resource_dir/legacy/chor001.krn'
        output_metadata_array_expected = ['Bach, Johann Sebastian']

        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        output_metadata_array_output = document.get_metacomments(KeyComment='COM', clear=True)

        self.assertListEqual(output_metadata_array_expected, output_metadata_array_output)  # composer

    def has_token(self, tokens, encoding):
        for token in tokens:
            if token.encoding == encoding:
                return True
        return False

    def test_has_token(self):
        input_kern_file = Path('resource_dir/legacy/chor001.krn')
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        all_tokens = document.get_all_tokens()
        self.assertTrue(self.has_token(all_tokens, '**kern'))
        self.assertTrue(self.has_token(all_tokens, '*clefF4'))
        self.assertTrue(self.has_token(all_tokens, '4e'))
        self.assertTrue(self.has_token(all_tokens, '8BB'))
        self.assertTrue(self.has_token(all_tokens, '*-'))
        self.assertFalse(self.has_token(all_tokens, '=3'))  # the number is removed from the original file
        self.assertTrue(self.has_token(all_tokens, '='))
        self.assertTrue(self.has_token(all_tokens, '=='))
        self.assertTrue(self.has_token(all_tokens, '.'))
        self.assertTrue(self.has_token(all_tokens, '!tenor'))
        self.assertTrue(self.has_token(all_tokens, '*M3/4'))
        self.assertTrue(self.has_token(all_tokens, '*MM60'))
        self.assertTrue(self.has_token(all_tokens, '*Iorgan'))

    def has_category(self, tokens, category):
        for token in tokens:
            if kp.TokenCategory.is_child(child=token.category, parent=category):
                return True
        return False

    def test_has_token_category(self):
        input_kern_file = Path('resource_dir/legacy/chor001.krn')
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        all_tokens = document.get_all_tokens()

        self.assertTrue(self.has_category(all_tokens, kp.TokenCategory.LINE_COMMENTS))
        self.assertTrue(self.has_category(all_tokens, kp.TokenCategory.CORE))
        self.assertTrue(self.has_category(all_tokens, kp.TokenCategory.EMPTY))
        self.assertTrue(self.has_category(all_tokens, kp.TokenCategory.OTHER))
        self.assertTrue(self.has_category(all_tokens, kp.TokenCategory.OTHER_CONTEXTUAL))
        self.assertTrue(self.has_category(all_tokens, kp.TokenCategory.BARLINES))
        self.assertTrue(self.has_category(all_tokens, kp.TokenCategory.SIGNATURES))
        self.assertTrue(self.has_category(all_tokens, kp.TokenCategory.STRUCTURAL))

    def test_get_all_tokens(self):
        # Arrange
        input_kern_file = Path('resource_dir/legacy/chor001.krn')
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        expected_tokens = []
        with open('resource_dir/legacy/chor001-all_tokens.txt', 'r') as f:
            for line in f:
                expected_tokens.append(line.strip())

        # Act
        tokens = document.get_all_tokens()
        tokens = [token.encoding for token in tokens]

        # Assert
        self.assertEqual(len(expected_tokens), len(tokens))
        self.assertListEqual(expected_tokens, tokens)

    def test_get_unique_tokens(self):
        # Arrange
        input_kern_file = Path('resource_dir/legacy/chor001.krn')
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        with open('resource_dir/legacy/chor001-unique_tokens.txt', 'r') as f:
            expected_tokens = f.read().splitlines()

        # Act
        encodings = document.get_unique_token_encodings()
        encodings.sort()
        expected_tokens.sort()


        # Assert
        self.assertEqual(len(expected_tokens), len(encodings))
        self.assertListEqual(expected_tokens, encodings)

    @unittest.skip("TODO: Add remove measure numbers")
    def test_get_unique_tokens_when_removing_measure_numbers(self):
        # Arrange
        input_kern_file = Path('resource_dir/legacy/chor001.krn')
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        with open('resource_dir/legacy/chor001-unique_tokens_without_measure_numbers.txt', 'r') as f:
            expected_tokens = f.read().splitlines()

        # Act
        encodings = document.get_unique_token_encodings()
        encodings.sort()
        expected_tokens.sort()

        # Assert
        self.assertEqual(len(expected_tokens), len(encodings))
        self.assertListEqual(expected_tokens, encodings)

    def test_get_unique_tokens_when_filter_by_categories(self):
        # Arrange
        input_kern_file = Path('resource_dir/legacy/chor001.krn')
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        with open('resource_dir/legacy/chor001-unique_tokens_with_category.txt', 'r') as f:
            expected_tokens = f.read().splitlines()

        # Act
        encodings = document.get_unique_token_encodings(
            filter_by_categories=[kp.TokenCategory.CORE, kp.TokenCategory.SIGNATURES])
        encodings.sort()
        expected_tokens.sort()

        # Assert
        self.assertEqual(len(expected_tokens), len(encodings))
        self.assertListEqual(expected_tokens, encodings)

    @unittest.skip("TODO: Instrument is not a valid category yet")
    def test_document_get_voices(self):
        input_kern_file = Path('resource_dir/legacy/chor048.krn')
        expected_voices = ['!bass', '!tenor', '!alto', '!soprno']
        expected_voices_cleaned = ['bass', 'tenor', 'alto', 'soprno']

        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        voices = document.get_voices()
        voices_cleaned = document.get_voices(clean=True)

        self.assertListEqual(expected_voices, voices)
        self.assertListEqual(expected_voices_cleaned, voices_cleaned)

    @unittest.skip
    def test_voices_range(self):
        pass

    def test_get_kern_from_ekern(self):
        input_ekern = "**ekern\n4@c\n4@d\n4@e\n4@f\n*-"
        expected_kern = "**kern\n4c\n4d\n4e\n4f\n*-"
        real_kern = kp.get_kern_from_ekern(input_ekern)

        self.assertEqual(expected_kern, real_kern)

    def test_document_get_first_measure_ok(self):
        input_kern_file = Path('resource_dir/legacy/chor001.krn')  # This score is correctly formatted
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        first_measure = document.get_first_measure()
        self.assertEqual(1, first_measure)

    def test_document_get_first_measure_empty(self):
        importer = kp.Importer()
        document = importer.import_string('**kern\n*-')
        with self.assertRaises(Exception):
            first_measure = document.get_first_measure()

    def test_document_get_last_measure_ok(self):
        input_kern_file = 'resource_dir/legacy/chor048.krn'  # This score has 10 measures
        importer = kp.Importer()
        document = importer.import_file(input_kern_file)
        measures = document.measures_count()
        self.assertEqual(11, measures)

    def test_document_get_last_measure_empty(self):
        importer = kp.Importer()
        document = importer.import_string('**kern\n*-')
        with self.assertRaises(Exception):
            last_measure = document.measures_count()

    def test_document_iterator_basic(self):
        # Arrange
        all_sub_kerns = []
        importer = kp.Importer()
        document = importer.import_file(Path('resource_dir/legacy/chor048.krn'))
        expected_sub_kerns_size = document.measures_count()
        count = 0
        options = kp.ExportOptions(spine_types=['**kern'], kern_type=kp.Encoding.normalizedKern)

        # Act
        for i in range(document.get_first_measure(), document.measures_count() + 1):
            count += 1
            options.from_measure = i
            options.to_measure = i
            exporter = kp.Exporter()
            content = exporter.export_string(document, options)
            print(content)
            all_sub_kerns.append(content)

        # Assert
        self.assertEqual(expected_sub_kerns_size, count)
        # TODO: Check if exported content is correct
        #for kern in all_sub_kerns:
        #    iter_importer = Importer()
        #    iter_document = iter_importer.import_string(kern)
        #    # if the import doesn't raise an exception, the kern is valid
        #    #self.assertFalse(iter_importer.has_errors())

    def test_document_method__iter__(self):
        # Arrange
        all_sub_kerns = []
        all_indexes = []
        importer = kp.Importer()
        document = importer.import_file(Path('resource_dir/legacy/chor048.krn'))
        expected_sub_kerns_size = document.measures_count()

        # Act
        for index in document:
            all_indexes.append(index)
            options = kp.ExportOptions(from_measure=index, to_measure=index, spine_types=['**kern'])
            exporter = kp.Exporter()
            content = exporter.export_string(document, options)
            all_sub_kerns.append(content)

        # Assert
        self.assertEqual(expected_sub_kerns_size, len(all_sub_kerns))

    def test_document_method__next__(self):
        # Arrange
        all_sub_kerns = []
        all_indexes = []
        importer = kp.Importer()
        document = importer.import_file(Path('resource_dir/legacy/chor048.krn'))
        expected_sub_kerns_size = document.measures_count()

        # Act
        iterator = iter(document)
        for index in iterator:
            all_indexes.append(index)
            options = kp.ExportOptions(from_measure=index, to_measure=index, spine_types=['**kern'])
            exporter = kp.Exporter()
            content = exporter.export_string(document, options)
            all_sub_kerns.append(content)

        # Assert
        self.assertEqual(expected_sub_kerns_size, len(all_sub_kerns))

    def test_export_spines(self):
        # Arrange
        importer = kp.Importer()
        document = importer.import_file('resource_dir/legacy/chor048.krn')
        expected_kern_spines = ['**kern', '**kern', '**kern', '**kern']
        expected_all_spines = ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']

        # Act
        exporter = kp.Exporter()
        real_1 = exporter.get_spine_types(document, spine_types=['**kern'])
        real_2 = exporter.get_spine_types(document, spine_types=['**kern', '**root', '**harm'])
        real_3 = exporter.get_spine_types(document, spine_types=None)

        # Assert
        self.assertListEqual(expected_kern_spines, real_1)
        self.assertListEqual(expected_all_spines, real_2)
        self.assertListEqual(expected_all_spines, real_3)

    @unittest.skip("TODO: Complete bug. ISSUE #12 test Eliseo")
    def test_export_string_two_different_spines(self):
        # Arrange
        doc, err = kp.load('resource_dir/legacy/chor048.krn')

        content = kp.dumps(doc, spine_types=['**kern', '**root', '**harm'],
                           tokenizer=kp.Encoding.eKern)

        doc_2, _ = kp.loads(content)  # raise error if the content is not valid

        print(content)

    def test_never_export_measure_numbers(self):
        # Arrange
        importer = kp.Importer()
        document = importer.import_file(Path('resource_dir/legacy/chor009.krn'))
        options = kp.ExportOptions(spine_types=None,
                                   kern_type=kp.Encoding.eKern,
                                   show_measure_numbers=False)
        exporter = kp.Exporter()
        content = exporter.export_string(document, options)
        print(content)
        measures = range(1, document.measures_count() + 1)
        measures = [f'={m}' for m in
                    measures]  # TODO: David. En los spines que no son kerns siempre se exportan los números de compás
        for measure in measures:
            self.assertNotIn(measure, content)

    def test_always_export_measure_numbers(self):
        # Arrange
        importer = kp.Importer()
        document = importer.import_file(Path('resource_dir/legacy/chor009.krn'))
        options = kp.ExportOptions(spine_types=None,
                                   kern_type=kp.Encoding.eKern,
                                   show_measure_numbers=True)
        exporter = kp.Exporter()
        content = exporter.export_string(document, options)
        print(content)
        measures = range(1, document.measures_count() + 1)
        measures = [f'={m}' for m in measures]
        for measure in measures:
            for line in content.splitlines():  # Find the line with the measure numbers
                if measure in line:
                    tokens = line.split('\t')  # Split the line in tokens
                    for token in tokens:
                        self.assertEqual(measure, token)

    def test_kern_with_first_measure_is_exported_without_the_measure_number_in_all_spines(self):
        # Arrange
        input_kern_file = 'resource_dir/samples/haydn-sonate-15_1-original.krn'
        output_kern_file = 'resource_dir/samples/haydn-sonate-15_1-output.krn'
        with open(output_kern_file, 'r') as f:
            expected_output = f.read()

        # Act
        doc, err = kp.load(input_kern_file)
        real_output = kp.dumps(doc)
        kp.graph(doc, '/tmp/graph.dot')

        # Assert
        self.assertEqual(expected_output, real_output)


if __name__ == '__main__':
    unittest.main()
