import unittest

import kernpy as kp


class TestTranscription(unittest.TestCase):
    def test_importer_factory(self):
        importer = kp.PitchImporterFactory.create(kp.NotationEncoding.HUMDRUM.value)
        self.assertIsInstance(importer, kp.HumdrumPitchImporter)

        importer = kp.PitchImporterFactory.create(kp.NotationEncoding.HUMDRUM.value)
        self.assertIsInstance(importer, kp.HumdrumPitchImporter)

        importer = kp.PitchImporterFactory.create('kern')
        self.assertIsInstance(importer, kp.HumdrumPitchImporter)

        importer = kp.PitchImporterFactory.create('american')
        self.assertIsInstance(importer, kp.AmericanPitchImporter)

        with self.assertRaises(ValueError):
            non_importer = kp.PitchImporterFactory.create('invalid')

    def test_exporter_factory(self):
        exporter = kp.PitchExporterFactory.create(kp.NotationEncoding.HUMDRUM.value)
        self.assertIsInstance(exporter, kp.HumdrumPitchExporter)

        exporter = kp.PitchExporterFactory.create(kp.NotationEncoding.AMERICAN.value)
        self.assertIsInstance(exporter, kp.AmericanPitchExporter)

        exporter = kp.PitchExporterFactory.create('kern')
        self.assertIsInstance(exporter, kp.HumdrumPitchExporter)

        exporter = kp.PitchExporterFactory.create('american')
        self.assertIsInstance(exporter, kp.AmericanPitchExporter)

        with self.assertRaises(ValueError):
            non_exporter = kp.PitchExporterFactory.create('invalid')

    def test_transposer_agnostic_pitch(self):
        pitch = kp.AgnosticPitch('G', 4)
        self.assertEqual(pitch.name, 'G')
        self.assertEqual(pitch.octave, 4)

        pitch = kp.AgnosticPitch('A', 5)
        self.assertEqual(pitch.name, 'A')
        self.assertEqual(pitch.octave, 5)

        pitch = kp.AgnosticPitch('B', 60)
        self.assertEqual(pitch.name, 'B')
        self.assertEqual(pitch.octave, 60)

        pitch = kp.AgnosticPitch('C+', 7)
        self.assertEqual(pitch.name, 'C+')
        self.assertEqual(pitch.octave, 7)

        pitch = kp.AgnosticPitch('C++', 7)
        self.assertEqual(pitch.name, 'C++')
        self.assertEqual(pitch.octave, 7)

        pitch = kp.AgnosticPitch('C+++', 7)
        self.assertEqual(pitch.name, 'C+++')
        self.assertEqual(pitch.octave, 7)

        pitch = kp.AgnosticPitch('C-', 7)
        self.assertEqual(pitch.name, 'C-')
        self.assertEqual(pitch.octave, 7)

        pitch = kp.AgnosticPitch('C--', 7)
        self.assertEqual(pitch.name, 'C--')
        self.assertEqual(pitch.octave, 7)

        pitch = kp.AgnosticPitch('C---', 7)
        self.assertEqual(pitch.name, 'C---')
        self.assertEqual(pitch.octave, 7)

        with self.assertRaises(ValueError):
            pitch = kp.AgnosticPitch('C----', 7)

        with self.assertRaises(ValueError):
            pitch = kp.AgnosticPitch('C++++', 7)

        with self.assertRaises(ValueError):
            pitch = kp.AgnosticPitch('invalid', 7)

    def test_transposer_american_pitch_importer(self):
        importer = kp.AmericanPitchImporter()
        pitch1 = importer.import_pitch('G5')

        importer = kp.AmericanPitchImporter()
        pitch11 = importer.import_pitch('g5')

        importer = kp.AmericanPitchImporter()
        pitch2 = importer.import_pitch('A4')

        importer = kp.AmericanPitchImporter()
        pitch3 = importer.import_pitch('B12')

        importer = kp.AmericanPitchImporter()
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

        importer = kp.AmericanPitchImporter()
        with self.assertRaises(ValueError):
            pitch5 = importer.import_pitch('zzz')

    def test_transposer_american_pitch_exporter(self):
        exporter = kp.AmericanPitchExporter()
        pitch1 = kp.AgnosticPitch('g', 4)
        self.assertEqual(exporter.export_pitch(pitch1), 'G4')

        exporter = kp.AmericanPitchExporter()
        pitch2 = kp.AgnosticPitch('a', 5)
        self.assertEqual(exporter.export_pitch(pitch2), 'A5')

        exporter = kp.AmericanPitchExporter()
        pitch3 = kp.AgnosticPitch('b', 60)
        self.assertEqual(exporter.export_pitch(pitch3), 'B60')

        exporter = kp.AmericanPitchExporter()
        pitch4 = kp.AgnosticPitch('C-', 7)
        self.assertEqual(exporter.export_pitch(pitch4), 'Cb7')

        exporter = kp.AmericanPitchExporter()
        with self.assertRaises(ValueError):
            pitch5 = exporter.export_pitch(kp.AgnosticPitch('zzz', -1))

    def test_transposer_humdrum_pitch_importer(self):
        importer = kp.HumdrumPitchImporter()
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
        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c', 4)
        self.assertEqual('c', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c', 3)
        self.assertEqual('C', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c', 7)
        self.assertEqual('cccc', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c', 2)
        self.assertEqual('CC', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c', 0)
        self.assertEqual('CCCC', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c+', 4)
        self.assertEqual('c#', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c+', 6)
        self.assertEqual('ccc#', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c++', 4)
        self.assertEqual('c##', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c---', 4)
        self.assertEqual('c---', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c-', 6)
        self.assertEqual('ccc-', exporter.export_pitch(pitch))

        exporter = kp.HumdrumPitchExporter()
        pitch = kp.AgnosticPitch('c---', 6)
        self.assertEqual('ccc---', exporter.export_pitch(pitch))

    def test_transposer_get_chroma(self):
        pitch = kp.AgnosticPitch('d', 4)
        self.assertEqual(168, pitch.get_chroma())

        pitch = kp.AgnosticPitch('f+', 4)
        self.assertEqual(180, pitch.get_chroma())

        pitch = kp.AgnosticPitch('b', 60)
        self.assertEqual(2437, pitch.get_chroma())

        pitch = kp.AgnosticPitch('c', 7)
        self.assertEqual(282, pitch.get_chroma())

    def test_transposer_agnostic_pitch_transpose(self):
        pitch = kp.AgnosticPitch('d', 4)
        pitch = kp.AgnosticPitch.to_transposed(pitch, 1)
        self.assertEqual(169, pitch.get_chroma())

        pitch = kp.AgnosticPitch('f+', 4)
        pitch = kp.AgnosticPitch.to_transposed(pitch, 24)
        self.assertEqual(204, pitch.get_chroma())

        pitch = kp.AgnosticPitch('b', 60)
        pitch = kp.AgnosticPitch.to_transposed(pitch, -2400)
        self.assertEqual(37, pitch.get_chroma())

        pitch = kp.AgnosticPitch('c', 7)
        pitch = kp.AgnosticPitch.to_transposed(pitch, 0)
        self.assertEqual(282, pitch.get_chroma())

    def test_transposer_agnostic_pitch_get_intervals(self):
        pitch1 = kp.AgnosticPitch('d', 4)
        pitch2 = kp.AgnosticPitch('d+', 4)
        self.assertEqual(1, kp.AgnosticPitch.get_chroma_from_interval(pitch1, pitch2))

    def test_transposer_public_transpose_american_to_american(self):
        content = kp.transpose('G4', kp.IntervalsByName['m3'], input_format='american',
                                          output_format='american')
        self.assertEqual('Bb4', content)

        content = kp.transpose('G4', kp.IntervalsByName['M3'], input_format='american',
                                          output_format='american')
        self.assertEqual('B4', content)

        content = kp.transpose('C1', kp.IntervalsByName['P4'], input_format='american',
                                          output_format='american')
        self.assertEqual('F1', content)

        content = kp.transpose('A3', kp.IntervalsByName['m2'], input_format='american',
                                          output_format='american')
        self.assertEqual('Bb3', content)

        content = kp.transpose('C3', kp.IntervalsByName['d4'], input_format='american',
                                          output_format='american')
        self.assertEqual('Fb3', content)

        content = kp.transpose('C3', kp.IntervalsByName['P4'], input_format='american',
                                          output_format='american')
        self.assertEqual('F3', content)

        content = kp.transpose('G#4', kp.IntervalsByName['P4'], input_format='american',
                                          output_format='american', direction='up')
        self.assertEqual('C#5', content)

        content = kp.transpose('b#4', kp.IntervalsByName['P4'], input_format='american',
                                          output_format='american',
                                          direction='down')
        self.assertEqual('Fbb4', content)

        content = kp.transpose('C3', kp.IntervalsByName['P4'], input_format='american',
                                          output_format='american',
                                          direction='down')
        self.assertEqual('G2', content)

    def test_transposer_public_transpose_humdrum_to_humdrum(self):
        content = kp.transpose('ccc', kp.IntervalsByName['P4'],
                                          input_format=kp.NotationEncoding.HUMDRUM.value,
                                          output_format=kp.NotationEncoding.HUMDRUM.value)
        self.assertEqual('fff', content)

        content = kp.transpose('ccc', kp.IntervalsByName['P4'],
                                          input_format=kp.NotationEncoding.HUMDRUM.value,
                                          output_format=kp.NotationEncoding.HUMDRUM.value, direction='up')
        self.assertEqual('fff', content)

        content = kp.transpose('ccc#', kp.IntervalsByName['P4'],
                                          input_format=kp.NotationEncoding.HUMDRUM.value,
                                          output_format=kp.NotationEncoding.HUMDRUM.value, direction='up')
        self.assertEqual('fff#', content)

        content = kp.transpose('ccc', kp.IntervalsByName['P4'],
                                          input_format=kp.NotationEncoding.HUMDRUM.value, direction='down',
                                          output_format=kp.NotationEncoding.HUMDRUM.value)
        self.assertEqual('gg', content)

        content = kp.transpose('ccc#', kp.IntervalsByName['P4'],
                                          input_format=kp.NotationEncoding.HUMDRUM.value, direction='down',
                                          output_format=kp.NotationEncoding.HUMDRUM.value)
        self.assertEqual('gg#', content)


    def test_transposer_public_transpose_american_to_humdrum(self):
        content = kp.transpose('G4', kp.IntervalsByName['m3'],
                                          input_format=kp.NotationEncoding.AMERICAN.value,
                                          output_format=kp.NotationEncoding.HUMDRUM.value)
        self.assertEqual('b-', content)

        content = kp.transpose('G4', kp.IntervalsByName['M3'],
                                          input_format=kp.NotationEncoding.AMERICAN.value,
                                          output_format=kp.NotationEncoding.HUMDRUM.value)
        self.assertEqual('b', content)

        content = kp.transpose('C1', kp.IntervalsByName['P4'],
                                          input_format=kp.NotationEncoding.AMERICAN.value,
                                          output_format=kp.NotationEncoding.HUMDRUM.value)
        self.assertEqual('FFF', content)

        content = kp.transpose('C1', kp.IntervalsByName['P4'],
                                          input_format=kp.NotationEncoding.AMERICAN.value,
                                          output_format=kp.NotationEncoding.HUMDRUM.value)
        self.assertEqual('FFF', content)

    def test_transposer_public_transpose_humdrum_to_american(self):
        content = kp.transpose('b-', kp.IntervalsByName['m3'],
                                          input_format=kp.NotationEncoding.HUMDRUM.value,
                                          output_format=kp.NotationEncoding.AMERICAN.value)
        self.assertEqual('Db5', content)

        content = kp.transpose('b', kp.IntervalsByName['M3'],
                                          input_format=kp.NotationEncoding.HUMDRUM.value,
                                          output_format=kp.NotationEncoding.AMERICAN.value)
        self.assertEqual('D#5', content)




