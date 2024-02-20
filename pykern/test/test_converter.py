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

    def testReadAccidentalsKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/accidentals.krn', os.path.join(output_folder, 'accidentals.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadAccidentalsAlterationDisplayKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/accidentals_alterationDisplay.krn', os.path.join(output_folder, 'accidentals_alterationDisplay.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadArticulationsKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/articulations.krn', os.path.join(output_folder, 'articulations.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadAutoBeamingKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/auto_beaming.krn', os.path.join(output_folder, 'auto_beaming.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadBarsKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/bars.krn', os.path.join(output_folder, 'bars.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadBeamingKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/beaming.krn', os.path.join(output_folder, 'beaming.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadChordsKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/chords.krn', os.path.join(output_folder, 'chords.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadClefsKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/clefs.krn', os.path.join(output_folder, 'clefs.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadKeyKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/key.krn', os.path.join(output_folder, 'key.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadKeyDesignationKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/key_designation.krn', os.path.join(output_folder, 'key_designation.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadMensurationsKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/mensurations.krn', os.path.join(output_folder, 'mensurations.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadModalKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/modal.krn', os.path.join(output_folder, 'modal.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadOctavesKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/octaves.krn', os.path.join(output_folder, 'octaves.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadOrnaments(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/ornaments.krn', os.path.join(output_folder, 'ornaments.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadRestsKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/rests.krn', os.path.join(output_folder, 'rests.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadRythmKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/rythm.krn', os.path.join(output_folder, 'rythm.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadSlursKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/slurs.krn', os.path.join(output_folder, 'slurs.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadTiesKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/ties.krn', os.path.join(output_folder, 'ties.ekrn') )
        # self.assertEqual(1, len(ts.files))

    def testReadTimeKern(self):
        importer = Kern2EkernConverter()
        importer.doConvertFile('resource_dir/unit/time.krn', os.path.join(output_folder, 'time.ekrn') )
        # self.assertEqual(1, len(ts.files))


def test():
    print(f'Output of test files into {output_folder}')
    unittest.main()


if __name__ == '__main__':
    unittest.main()
