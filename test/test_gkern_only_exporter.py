import logging
import unittest

from parameterized import parameterized

import kernpy as kp

logger = logging.getLogger(__name__)


class TestGKernExporter(unittest.TestCase):

    def setUp(self):
        self.gclef = kp.GClef()
        self.staff = kp.Staff()
        self.exporter = kp.GKernExporter(self.gclef)

    def test_init_stores_clef(self):
        self.assertEqual(self.gclef, self.exporter.clef)

    @parameterized.expand([('E', 4, 'T@1')])
    def test_export_middle_e4(self, name, octave, expected_ts):
        self.assertEqual(expected_ts, self.exporter.export(self.staff, kp.AgnosticPitch(name, octave)))

    @parameterized.expand([('E+', 4, 'T@1'), ('E-', 4, 'T@1')])
    def test_export_with_accidentals(self, name, octave, expected_ts):
        self.assertEqual(expected_ts, self.exporter.export(self.staff, kp.AgnosticPitch(name, octave)))

    @parameterized.expand([
        ('F', 4, 'S@1'), ('G', 4, 'T@2'), ('A', 4, 'S@2'), ('B', 4, 'T@3'),
        ('C', 5, 'S@3'), ('D', 5, 'T@4'), ('E', 5, 'S@4'), ('F', 5, 'T@5'), ('G', 5, 'S@5'),
    ])
    def test_export_scale_up(self, name, octave, expected_ts):
        self.assertEqual(expected_ts, self.exporter.export(self.staff, kp.AgnosticPitch(name, octave)))

    @parameterized.expand([
        ('D', 4, 'S@0'), ('C', 4, 'T@0'), ('B', 3, 'S@-1'), ('A', 3, 'T@-1'),
        ('G', 3, 'S@-2'), ('F', 3, 'T@-2'), ('E', 3, 'S@-3'),
    ])
    def test_export_scale_down(self, name, octave, expected_ts):
        self.assertEqual(expected_ts, self.exporter.export(self.staff, kp.AgnosticPitch(name, octave)))

    @parameterized.expand([
        kp.GClef, kp.F3Clef, kp.F4Clef, kp.C1Clef, kp.C2Clef, kp.C3Clef, kp.C4Clef,
    ])
    def test_export_bottom_line_ts(self, clef_cls):
        clef = clef_cls()
        self.assertEqual(
            'T@1',
            kp.GKernExporter(clef).export(self.staff, clef.bottom_line()),
        )

    def test_agnostic_position_equivalence(self):
        pitch = kp.AgnosticPitch('F', 4)
        expected_pos = kp.PositionInStaff.from_space(1)
        self.assertEqual(expected_pos, self.exporter.agnostic_position(self.staff, pitch))
        self.assertEqual(str(expected_pos), self.exporter.export(self.staff, pitch))

    @parameterized.expand([
        ('C', 2), ('E', 2), ('G', 2), ('B', 5), ('C', 6), ('D', 6),
    ])
    def test_export_with_large_range(self, name, octave):
        result = self.exporter.export(self.staff, kp.AgnosticPitch(name, octave))
        self.assertRegex(result, r'^(T|S)@-?\d+$')

    @parameterized.expand([('F++', 4, 'S@1'), ('F--', 4, 'S@1')])
    def test_export_pitch_with_enharmonic_spelling(self, name, octave, expected_ts):
        self.assertEqual(expected_ts, self.exporter.export(self.staff, kp.AgnosticPitch(name, octave)))


class TestPitchToGKernString(unittest.TestCase):

    def setUp(self):
        self.staff = kp.Staff()

    @parameterized.expand([
        ('E', 4, kp.GClef, 'e'),
        ('E', 4, kp.F3Clef, 'aa'),
        ('C', 4, kp.C1Clef, 'e'),
        ('A-', 4, kp.GClef, 'a-'),
        ('C+', 5, kp.GClef, 'cc#'),
        ('A', 3, kp.C2Clef, 'e'),
        ('B', 5, kp.GClef, 'bb'),
    ])
    def test_pitch_to_gkern_string(self, name, octave, clef_cls, expected):
        pitch = kp.AgnosticPitch(name, octave)
        self.assertEqual(expected, kp.pitch_to_gkern_string(pitch, clef_cls()))

    @parameterized.expand([
        (kp.GClef, 'S@0'),
        (kp.F3Clef, 'S@5'),
        (kp.F4Clef, 'S@6'),
        (kp.C1Clef, 'S@1'),
        (kp.C2Clef, 'S@2'),
        (kp.C3Clef, 'S@3'),
        (kp.C4Clef, 'S@4'),
    ])
    def test_same_pitch_different_clefs_ts(self, clef_cls, expected_ts):
        pitch = kp.AgnosticPitch('D', 4)
        result = kp.GKernExporter(clef_cls()).export(self.staff, pitch)
        logger.info('D4 on %s: expected %s, got %s', clef_cls.__name__, expected_ts, result)
        self.assertEqual(expected_ts, result)

    @parameterized.expand([
        ('T@0', 'c'), ('S@0', 'd'), ('T@1', 'e'),
        ('S@3', 'cc'), ('T@4', 'dd'), ('S@-2', 'G'), ('T@-4', 'BB'),
    ])
    def test_gkern_to_g_clef_pitch(self, token, expected):
        self.assertEqual(expected, kp.gkern_to_g_clef_pitch(token))

    @parameterized.expand(['X@1', 'T@foo', 'bogus'])
    def test_gkern_to_g_clef_pitch_bad_inputs(self, token):
        with self.assertRaises(ValueError):
            kp.gkern_to_g_clef_pitch(token)

    @parameterized.expand([
        'ccc', 'bb', 'aa', 'gg', 'ff', 'ee', 'dd', 'cc', 'b', 'a', 'f', 'e', 'd', 'c',
        'B', 'A', 'G', 'F', 'E', 'D', 'C', 'BB',
    ])
    def test_import_kern_pitch_and_export_agnostic(self, g_clef_pitch):
        clef = kp.GClef()
        pitch_importer = kp.PitchImporterFactory.create('kern')
        agnostic_pitch = pitch_importer.import_pitch(g_clef_pitch)
        encoded = kp.pitch_to_gkern_string(agnostic_pitch, clef)
        self.assertEqual(encoded, kp.pitch_to_gkern_string(agnostic_pitch, clef))


if __name__ == '__main__':
    unittest.main()
