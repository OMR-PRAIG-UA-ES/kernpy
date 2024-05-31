import unittest

from kernpy import transposer

class TestTranscription(unittest.TestCase):
    def test_importer_factory(self):
        importer = transposer.PitchImporterFactory.create(transposer.NotationEncoding.HUMDRUM.value)
        self.assertIsInstance(importer, transposer.HumdrumPitchImporter)

        importer = transposer.PitchImporterFactory.create(transposer.NotationEncoding.HUMDRUM.value)
        self.assertIsInstance(importer, transposer.HumdrumPitchImporter)

        importer = transposer.PitchImporterFactory.create('kern')
        self.assertIsInstance(importer, transposer.HumdrumPitchImporter)

        importer = transposer.PitchImporterFactory.create('american')
        self.assertIsInstance(importer, transposer.AmericanPitchImporter)

        with self.assertRaises(ValueError):
            non_importer = transposer.PitchImporterFactory.create('invalid')

    def test_exporter_factory(self):
        exporter = transposer.PitchExporterFactory.create(transposer.NotationEncoding.HUMDRUM.value)
        self.assertIsInstance(exporter, transposer.HumdrumPitchExporter)

        exporter = transposer.PitchExporterFactory.create(transposer.NotationEncoding.AMERICAN.value)
        self.assertIsInstance(exporter, transposer.AmericanPitchExporter)

        exporter = transposer.PitchExporterFactory.create('kern')
        self.assertIsInstance(exporter, transposer.HumdrumPitchExporter)

        exporter = transposer.PitchExporterFactory.create('american')
        self.assertIsInstance(exporter, transposer.AmericanPitchExporter)

        with self.assertRaises(ValueError):
            non_exporter = transposer.PitchExporterFactory.create('invalid')

    def test_transposer_agnotic_pitch(self):
        pitch = transposer.AgnosticPitch('G', 4)
        self.assertEqual(pitch.name, 'G')
        self.assertEqual(pitch.octave, 4)

        pitch = transposer.AgnosticPitch('A', 5)
        self.assertEqual(pitch.name, 'A')
        self.assertEqual(pitch.octave, 5)

        pitch = transposer.AgnosticPitch('B', 60)
        self.assertEqual(pitch.name, 'B')
        self.assertEqual(pitch.octave, 60)

        pitch = transposer.AgnosticPitch('C+', 7)
        self.assertEqual(pitch.name, 'C+')
        self.assertEqual(pitch.octave, 7)

        pitch = transposer.AgnosticPitch('C++', 7)
        self.assertEqual(pitch.name, 'C++')
        self.assertEqual(pitch.octave, 7)

        pitch = transposer.AgnosticPitch('C+++', 7)
        self.assertEqual(pitch.name, 'C+++')
        self.assertEqual(pitch.octave, 7)

        pitch = transposer.AgnosticPitch('C-', 7)
        self.assertEqual(pitch.name, 'C-')
        self.assertEqual(pitch.octave, 7)

        pitch = transposer.AgnosticPitch('C--', 7)
        self.assertEqual(pitch.name, 'C--')
        self.assertEqual(pitch.octave, 7)

        pitch = transposer.AgnosticPitch('C---', 7)
        self.assertEqual(pitch.name, 'C---')
        self.assertEqual(pitch.octave, 7)

        with self.assertRaises(ValueError):
            pitch = transposer.AgnosticPitch('C----', 7)

        with self.assertRaises(ValueError):
            pitch = transposer.AgnosticPitch('C++++', 7)

        with self.assertRaises(ValueError):
            pitch = transposer.AgnosticPitch('invalid', 7)

    def test_transposer_american_pitch_importer(self):
        importer = transposer.AmericanPitchImporter()
        pitch1 = importer.import_pitch('G5')

        importer = transposer.AmericanPitchImporter()
        pitch11 = importer.import_pitch('g5')

        importer = transposer.AmericanPitchImporter()
        pitch2 = importer.import_pitch('A4')

        importer = transposer.AmericanPitchImporter()
        pitch3 = importer.import_pitch('B12')

        importer = transposer.AmericanPitchImporter()
        pitch4 = importer.import_pitch('c2')

        self.assertEqual(pitch1.octave, 5)
        self.assertEqual(pitch1.name, 'G')
        self.assertEqual(pitch11.name, 'G')
        self.assertEqual(pitch2.octave, 4)
        self.assertEqual(pitch2.name, 'A')
        self.assertEqual(pitch3.octave, 12)
        self.assertEqual(pitch3.name, 'B')
        self.assertEqual(pitch4.octave, 2)
        self.assertEqual(pitch4.name, 'C')

        importer = transposer.AmericanPitchImporter()
        with self.assertRaises(ValueError):
            pitch5 = importer.import_pitch('zzz')

    def test_transposer_american_pitch_exporter(self):
        exporter = transposer.AmericanPitchExporter()
        pitch1 = transposer.AgnosticPitch('g', 4)
        self.assertEqual(exporter.export_pitch(pitch1), 'G4')

        exporter = transposer.AmericanPitchExporter()
        pitch2 = transposer.AgnosticPitch('a', 5)
        self.assertEqual(exporter.export_pitch(pitch2), 'A5')

        exporter = transposer.AmericanPitchExporter()
        pitch3 = transposer.AgnosticPitch('b', 60)
        self.assertEqual(exporter.export_pitch(pitch3), 'B60')

        exporter = transposer.AmericanPitchExporter()
        pitch4 = transposer.AgnosticPitch('C-', 7)
        self.assertEqual(exporter.export_pitch(pitch4), 'Cb7')

        exporter = transposer.AmericanPitchExporter()
        with self.assertRaises(ValueError):
            pitch5 = exporter.export_pitch(transposer.AgnosticPitch('zzz', -1))

    def test_transposer_humdrum_pitch_importer(self):
        importer = transposer.HumdrumPitchImporter()
        pitch = importer.import_pitch('c')
        self.assertEqual('C', pitch.name)
        self.assertEqual(4, pitch.octave)

        pitch = importer.import_pitch('C')
        self.assertEqual('C', pitch.name)
        self.assertEqual(3, pitch.octave)

        pitch = importer.import_pitch('cccc')
        self.assertEqual('C', pitch.name)
        self.assertEqual(7, pitch.octave)

        pitch = importer.import_pitch('CCCC')
        self.assertEqual('C', pitch.name)
        self.assertEqual(0, pitch.octave)

        pitch = importer.import_pitch('c#')
        self.assertEqual('C+', pitch.name)
        self.assertEqual(4, pitch.octave)

        pitch = importer.import_pitch('c###')
        self.assertEqual('C+++', pitch.name)
        self.assertEqual(4, pitch.octave)

        pitch = importer.import_pitch('c-')
        self.assertEqual('C-', pitch.name)
        self.assertEqual(4, pitch.octave)

        pitch = importer.import_pitch('c---')
        self.assertEqual('C---', pitch.name)
        self.assertEqual(4, pitch.octave)

        pitch = importer.import_pitch('b')
        self.assertEqual('B', pitch.name)
        self.assertEqual(4, pitch.octave)

        pitch = importer.import_pitch('bb--')
        self.assertEqual('B--', pitch.name)
        self.assertEqual(5, pitch.octave)

    def test_transposer_humdrum_pitch_exporter(self):
        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c', 4)
        self.assertEqual('c', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c', 3)
        self.assertEqual('C', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c', 7)
        self.assertEqual('cccc', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c', 2)
        self.assertEqual('CC', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c', 0)
        self.assertEqual('CCCC', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c+', 4)
        self.assertEqual('c#', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c+', 6)
        self.assertEqual('ccc#', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c++', 4)
        self.assertEqual('c##', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c---', 4)
        self.assertEqual('c---', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c-', 6)
        self.assertEqual('ccc-', exporter.export_pitch(pitch))

        exporter = transposer.HumdrumPitchExporter()
        pitch = transposer.AgnosticPitch('c---', 6)
        self.assertEqual('ccc---', exporter.export_pitch(pitch))

    def test_transposer_get_chroma(self):
        pitch = transposer.AgnosticPitch('d', 4)
        self.assertEqual(168, pitch.get_chroma())

        pitch = transposer.AgnosticPitch('f+', 4)
        self.assertEqual(180, pitch.get_chroma())

        pitch = transposer.AgnosticPitch('b', 60)
        self.assertEqual(2437, pitch.get_chroma())

        pitch = transposer.AgnosticPitch('c', 7)
        self.assertEqual(282, pitch.get_chroma())

    def test_transposer_agnostic_pitch_transpose(self):
        pitch = transposer.AgnosticPitch('d', 4)
        pitch = transposer.AgnosticPitch.to_transposed(pitch, 1)
        self.assertEqual(169, pitch.get_chroma())

        pitch = transposer.AgnosticPitch('f+', 4)
        pitch = transposer.AgnosticPitch.to_transposed(pitch, 24)
        self.assertEqual(204, pitch.get_chroma())

        pitch = transposer.AgnosticPitch('b', 60)
        pitch = transposer.AgnosticPitch.to_transposed(pitch, -2400)
        self.assertEqual(37, pitch.get_chroma())

        pitch = transposer.AgnosticPitch('c', 7)
        pitch = transposer.AgnosticPitch.to_transposed(pitch, 0)
        self.assertEqual(282, pitch.get_chroma())

    def test_transposer_agnostic_pitch_get_intervals(self):
        pitch1 = transposer.AgnosticPitch('d', 4)
        pitch2 = transposer.AgnosticPitch('d+', 4)
        self.assertEqual(1, transposer.AgnosticPitch.get_chroma_from_interval(pitch1, pitch2))

    def test_transposer_public_transpose_american(self):
        content = transposer.transpose('G4', transposer.IntervalsByName['m3'], format='american')
        self.assertEqual('Bb4', content)

        content = transposer.transpose('G4', transposer.IntervalsByName['M3'], format='american')
        self.assertEqual('B4', content)

        content = transposer.transpose('C1', transposer.IntervalsByName['P4'], format='american')
        self.assertEqual('F1', content)

        content = transposer.transpose('A3', transposer.IntervalsByName['m2'], format='american')
        self.assertEqual('Bb3', content)

        content = transposer.transpose('C3', transposer.IntervalsByName['d4'], format='american')
        self.assertEqual('Fb3', content)

        content = transposer.transpose('C3', transposer.IntervalsByName['P4'], format='american')
        self.assertEqual('F3', content)

        content = transposer.transpose('G#4', transposer.IntervalsByName['P4'], format='american', direction='up')
        self.assertEqual('C#5', content)

        content = transposer.transpose('b#4', transposer.IntervalsByName['P4'], format='american', direction='down')
        self.assertEqual('Fbb4', content)

        content = transposer.transpose('C3', transposer.IntervalsByName['P4'], format='american', direction='down')
        self.assertEqual('G2', content)

        content = transposer.transpose('ccc', transposer.IntervalsByName['P4'], format=transposer.NotationEncoding.HUMDRUM.value)
        self.assertEqual('fff', content)

        content = transposer.transpose('ccc#', transposer.IntervalsByName['P4'], format=transposer.NotationEncoding.HUMDRUM.value)
        self.assertEqual('fff#', content)

        content = transposer.transpose('ccc', transposer.IntervalsByName['P4'], format=transposer.NotationEncoding.HUMDRUM.value, direction='down')
        self.assertEqual('gg', content)





