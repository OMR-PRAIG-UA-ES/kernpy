import unittest
import logging

import kernpy as kp


logger = logging.getLogger(__name__)


class TestGKernExporter(unittest.TestCase):

    def setUp(self):
        self.gclef = kp.GClef()
        self.staff = kp.Staff()
        self.exporter = kp.GKernExporter(self.gclef)

    def assertExport(self, pitch: kp.AgnosticPitch, expected_str: str):
        self.assertEqual(self.exporter.export(self.staff, pitch), expected_str)

    def assertAgnosticPosition(self, pitch: kp.AgnosticPitch, expected_pos: kp.PositionInStaff):
        pos = self.exporter.agnostic_position(self.staff, pitch)
        self.assertEqual(pos, expected_pos)

    def test_init_stores_clef(self):
        self.assertEqual(self.exporter.clef, self.gclef)

    def test_export_middle_E4(self):
        pitch = kp.AgnosticPitch('E', 4)
        expected = f"T@1"
        self.assertExport(pitch, expected)

    def test_export_with_accidentals(self):
        self.assertExport(kp.AgnosticPitch('E+', 4), f"T@1")
        self.assertExport(kp.AgnosticPitch('E-', 4), f"T@1")

    def test_export_scale_up(self):
        pitches_positions = [
            ('F', 4, 'S@1'),
            ('G', 4, 'T@2'),
            ('A', 4, 'S@2'),
            ('B', 4, 'T@3'),
            ('C', 5, 'S@3'),
            ('D', 5, 'T@4'),
            ('E', 5, 'S@4'),
            ('F', 5, 'T@5'),
            ('G', 5, 'S@5'),
        ]
        for name, octave, pos_str in pitches_positions:
            with self.subTest(pitch=f"{name}{octave}"):
                pitch = kp.AgnosticPitch(name, octave)
                expected = f"{pos_str}"
                self.assertExport(pitch, expected)

    def test_export_scale_down(self):
        pitches_positions = [
            ('D', 4, 'S@0'),
            ('C', 4, 'T@0'),
            ('B', 3, 'S@-1'),
            ('A', 3, 'T@-1'),
            ('G', 3, 'S@-2'),
            ('F', 3, 'T@-2'),
            ('E', 3, 'S@-3'),
        ]
        for name, octave, pos_str in pitches_positions:
            with self.subTest(pitch=f"{name}{octave}"):
                pitch = kp.AgnosticPitch(name, octave)
                expected = f"{pos_str}"
                self.assertExport(pitch, expected)

    def test_export_multiple_clefs(self):
        clefs = [
            (kp.GClef(), kp.AgnosticPitch('E', 4), 'T@1'),
            (kp.F3Clef(), kp.AgnosticPitch('B', 3), 'T@1'),
            (kp.F4Clef(), kp.AgnosticPitch('G', 2), 'T@1'),
            (kp.C1Clef(), kp.AgnosticPitch('C', 3), 'T@1'),
            (kp.C2Clef(), kp.AgnosticPitch('A', 2), 'T@1'),
            (kp.C3Clef(), kp.AgnosticPitch('B', 2), 'T@1'),
            (kp.C4Clef(), kp.AgnosticPitch('D', 2), 'T@1'),
        ]
        for clef, pitch, pos_str in clefs:
            with self.subTest(clef=clef, pitch=pitch):
                exporter = kp.GKernExporter(clef)
                result = exporter.export(self.staff, pitch)
                self.assertEqual(result, f"{pos_str}")

    def test_agnostic_position_equivalence(self):
        pitch = kp.AgnosticPitch('F', 4)
        expected_pos = kp.PositionInStaff.from_space(1)
        self.assertAgnosticPosition(pitch, expected_pos)

    def test_export_with_large_range(self):
        pitches = [
            kp.AgnosticPitch('C', 2),
            kp.AgnosticPitch('E', 2),
            kp.AgnosticPitch('G', 2),
            kp.AgnosticPitch('B', 5),
            kp.AgnosticPitch('C', 6),
            kp.AgnosticPitch('D', 6),
        ]
        for pitch in pitches:
            with self.subTest(pitch=pitch):
                result = self.exporter.export(self.staff, pitch)
                self.assertRegex(result, rf"(T|S)@-?\d+")

    def test_export_pitch_with_double_sharps(self):
        self.assertExport(kp.AgnosticPitch('F++', 4), f"S@1")

    def test_export_pitch_with_double_flats(self):
        self.assertExport(kp.AgnosticPitch('F--', 4), f"S@1")


class TestPitchToGKernString(unittest.TestCase):
    def assertPitchToGKern(self, name: str, octave: int, clef: kp.Clef, expected: str):
        pitch = kp.AgnosticPitch(name, octave)
        self.assertEqual(kp.pitch_to_gkern_string(pitch, clef), expected)

    def test_basic_conversion(self):
        self.assertPitchToGKern('E', 4, kp.GClef(), 'T@1')

    def test_conversion_multiple_clefs(self):
        test_cases = [
            ('E', 4, kp.GClef(), 'T@1'),
            ('B', 3, kp.F3Clef(), 'T@1'),
            ('C', 3, kp.C1Clef(), 'T@1'),
        ]
        for name, octave, clef, expected in test_cases:
            with self.subTest(pitch=f"{name}{octave}", clef=clef):
                self.assertPitchToGKern(name, octave, clef, expected)

    def test_with_accidentals_flat(self):
        self.assertPitchToGKern('A-', 4, kp.GClef(), 'S@2')

    def test_with_accidentals_sharp(self):
        self.assertPitchToGKern('C+', 5, kp.GClef(), 'S@3')

    def test_pitch_extremes(self):
        extremes = [
            ('C', 2, kp.C2Clef()),
            ('B', 5, kp.GClef()),
        ]
        for name, octave, clef in extremes:
            with self.subTest(pitch=f"{name}{octave}", clef=clef):
                result = kp.pitch_to_gkern_string(kp.AgnosticPitch(name, octave), clef)
                self.assertRegex(result, rf"(T|S)@-?\d+")

    def test_same_pitch_different_clefs(self):
        pitch = kp.AgnosticPitch('D', 4)
        clefs_position_representation = [
            (kp.GClef(), f'S@0'),
            (kp.F3Clef(), f'T@2'),
            (kp.F4Clef(), f'S@6'),
            (kp.C1Clef(), f'T@5'),
            (kp.C2Clef(), f'T@6'),
            (kp.C3Clef(), f'S@5'),
            (kp.C4Clef(), f'T@8'),
        ]

        for clef, expected in clefs_position_representation:
            result = kp.pitch_to_gkern_string(pitch, clef)
            logger.info(f"Testing {pitch} with {clef}:\Expected: {expected}.\nGot: {result}")
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
