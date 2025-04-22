import unittest
import os
from pathlib import Path

import kernpy as kp


class GkernTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.LINE_CHARACTER = 'L'
        cls.SPACE_CHARACTER = 'S'

    def test_line_character(self):
        self.assertEqual(kp.PositionInStaff.LINE_CHARACTER, self.LINE_CHARACTER)

    def test_space_character(self):
        self.assertEqual(kp.PositionInStaff.SPACE_CHARACTER, self.SPACE_CHARACTER)

    def test_from_line_bottom(self):
        p = kp.PositionInStaff.from_line(1)
        self.assertEqual(p, kp.PositionInStaff(0))

    def test_from_line_third(self):
        p = kp.PositionInStaff.from_line(3)
        self.assertEqual(p, kp.PositionInStaff(4))

    def test_from_space_bottom(self):
        p = kp.PositionInStaff.from_space(1)
        self.assertEqual(p, kp.PositionInStaff(1))

    def test_from_space_second(self):
        p = kp.PositionInStaff.from_space(2)
        self.assertEqual(p, kp.PositionInStaff(3))

    def test_from_encoded_line(self):
        p = kp.PositionInStaff.from_encoded(self.LINE_CHARACTER + '2')
        self.assertEqual(p, kp.PositionInStaff.from_line(2))

    def test_from_encoded_space(self):
        p = kp.PositionInStaff.from_encoded(self.SPACE_CHARACTER + '3')
        self.assertEqual(p, kp.PositionInStaff.from_space(3))

    def test_from_encoded_invalid(self):
        with self.assertRaises(ValueError):
            kp.PositionInStaff.from_encoded('X1')

    def test_line_number_1(self):
        p =kp. PositionInStaff(4)
        self.assertEqual(p.line(), 3.0)

    def test_line_number_2(self):
        p = kp.PositionInStaff(3)
        self.assertEqual(p.line(), 2)

    def test_line_number_3(self):
        p = kp.PositionInStaff(2)
        self.assertEqual(p.line(), 2.0)

    def test_line_number_4(self):
        p = kp.PositionInStaff(-5)
        self.assertEqual(p.line(), -2)

    def test_space_number_1(self):
        p = kp.PositionInStaff(3)
        self.assertEqual(p.space(), 2)

    def test_space_number_2(self):
        p = kp.PositionInStaff(1)
        self.assertEqual(p.space(), 1)

    def test_space_number_3(self):
        p = kp.PositionInStaff(2)
        self.assertEqual(p.space(), 1)

    def test_space_number_4(self):
        p = kp.PositionInStaff(5)
        self.assertEqual(p.space(), 3)

    def test_is_line_true(self):
        self.assertTrue(kp.PositionInStaff(0).is_line())
        self.assertTrue(kp.PositionInStaff(2).is_line())
        self.assertTrue(kp.PositionInStaff(4).is_line())
        self.assertTrue(kp.PositionInStaff(6).is_line())
        self.assertTrue(kp.PositionInStaff(8).is_line())
        self.assertTrue(kp.PositionInStaff(10).is_line())
        self.assertTrue(kp.PositionInStaff(-2).is_line())
        self.assertTrue(kp.PositionInStaff(-4).is_line())
        self.assertTrue(kp.PositionInStaff(-6).is_line())

    def test_is_line_false(self):
        self.assertFalse(kp.PositionInStaff(1).is_line())
        self.assertFalse(kp.PositionInStaff(3).is_line())
        self.assertFalse(kp.PositionInStaff(5).is_line())
        self.assertFalse(kp.PositionInStaff(7).is_line())
        self.assertFalse(kp.PositionInStaff(9).is_line())
        self.assertFalse(kp.PositionInStaff(11).is_line())
        self.assertFalse(kp.PositionInStaff(-1).is_line())
        self.assertFalse(kp.PositionInStaff(-3).is_line())
        self.assertFalse(kp.PositionInStaff(-5).is_line())


    def test_move_positive(self):
        p = kp.PositionInStaff(2).move(3)
        self.assertEqual(p, kp.PositionInStaff(5))

    def test_move_negative(self):
        p = kp.PositionInStaff(2).move(-2)
        self.assertEqual(p, kp.PositionInStaff(0))

    def test_position_above(self):
        p = kp.PositionInStaff(0).position_above()
        self.assertEqual(p, kp.PositionInStaff(2))

    def test_position_below(self):
        p = kp.PositionInStaff(2).position_below()
        self.assertEqual(p, kp.PositionInStaff(0))

    def test_str_from_line(self):
        p = kp.PositionInStaff.from_line(1)
        self.assertEqual(str(p), self.LINE_CHARACTER + '1')
        p = kp.PositionInStaff.from_line(2)
        self.assertEqual(str(p), self.LINE_CHARACTER + '2')
        p = kp.PositionInStaff.from_line(3)
        self.assertEqual(str(p), self.LINE_CHARACTER + '3')
        p = kp.PositionInStaff.from_line(4)
        self.assertEqual(str(p), self.LINE_CHARACTER + '4')
        p = kp.PositionInStaff.from_line(5)
        self.assertEqual(str(p), self.LINE_CHARACTER + '5')
        p = kp.PositionInStaff.from_line(-1)
        self.assertEqual(str(p), self.LINE_CHARACTER + '-1')
        p = kp.PositionInStaff.from_line(-2)
        self.assertEqual(str(p), self.LINE_CHARACTER + '-2')
        p = kp.PositionInStaff.from_line(-3)
        self.assertEqual(str(p), self.LINE_CHARACTER + '-3')

    def test_str_from_space(self):
        p = kp.PositionInStaff.from_space(1)
        self.assertEqual(str(p), self.SPACE_CHARACTER + '1')
        p = kp.PositionInStaff.from_space(2)
        self.assertEqual(str(p), self.SPACE_CHARACTER + '2')
        p = kp.PositionInStaff.from_space(3)
        self.assertEqual(str(p), self.SPACE_CHARACTER + '3')
        p = kp.PositionInStaff.from_space(4)
        self.assertEqual(str(p), self.SPACE_CHARACTER + '4')
        p = kp.PositionInStaff.from_space(5)
        self.assertEqual(str(p), self.SPACE_CHARACTER + '5')
        p = kp.PositionInStaff.from_space(-1)
        self.assertEqual(str(p), self.SPACE_CHARACTER + '-1')
        p = kp.PositionInStaff.from_space(-2)
        self.assertEqual(str(p), self.SPACE_CHARACTER + '-2')
        p = kp.PositionInStaff.from_space(-3)
        self.assertEqual(str(p), self.SPACE_CHARACTER + '-3')

    def test_equality(self):
        self.assertEqual(kp.PositionInStaff(2), kp.PositionInStaff(2))

    def test_inequality(self):
        self.assertNotEqual(kp.PositionInStaff(2), kp.PositionInStaff(3))

    def test_eq_different_type(self):
        self.assertFalse(kp.PositionInStaff(2) == 2)

    def test_lt(self):
        self.assertTrue(kp.PositionInStaff(1) < kp.PositionInStaff(2))

    def test_hash(self):
        s = {kp.PositionInStaff(2), kp.PositionInStaff(2)}
        self.assertEqual(len(s), 1)

    def test_from_line_ledger_line(self):
        p = kp.PositionInStaff.from_line(0)
        self.assertEqual(p, kp.PositionInStaff(-2))
        self.assertEqual(p.line(), 0.0)
        self.assertTrue(p.is_line())

    def test_from_space_ledger_space(self):
        p = kp.PositionInStaff.from_space(0)
        self.assertEqual(p, kp.PositionInStaff(-1))
        self.assertFalse(p.is_line())
        self.assertEqual(p.space(), 0)

    def test_str_ledger_line(self):
        p = kp.PositionInStaff.from_line(0)
        self.assertEqual(str(p), 'L0')

    def test_str_ledger_space(self):
        p = kp.PositionInStaff.from_space(0)
        self.assertEqual(str(p), 'S0')

    def test_is_line_negative_even(self):
        p = kp.PositionInStaff(-4)
        self.assertTrue(p.is_line())

    def test_is_line_negative_odd(self):
        p = kp.PositionInStaff(-3)
        self.assertFalse(p.is_line())

    def test_comparison_negative(self):
        low = kp.PositionInStaff(-3)
        high = kp.PositionInStaff(-1)
        self.assertTrue(low < high)


    def do_test_pitches_to_positions(self, reference: kp.PitchPositionReferenceSystem, pitch: kp.AgnosticPitch, expected_position: kp.PositionInStaff):
        computed_position = reference.compute_position(pitch)
        self.assertEqual(expected_position, computed_position)

    def test_compute_position(self):
        g_clef_reference = kp.PitchPositionReferenceSystem(kp.AgnosticPitch('E', 4))

        expected_position_in_staff = kp.PositionInStaff.from_line(1)
        computed_position_in_staff = g_clef_reference.compute_position(kp.AgnosticPitch('E', 4))

        self.assertEqual(expected_position_in_staff, computed_position_in_staff)

    def test_compute_position_bunch_of_samples_positives(self):
        g_clef_reference = kp.PitchPositionReferenceSystem(kp.AgnosticPitch('E', 4))

        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E', 4), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('F', 4), kp.PositionInStaff.from_space(1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('G', 4), kp.PositionInStaff.from_line(2))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('A', 4), kp.PositionInStaff.from_space(2))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('B', 4), kp.PositionInStaff.from_line(3))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('C', 5), kp.PositionInStaff.from_space(3))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('D', 5), kp.PositionInStaff.from_line(4))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E', 5), kp.PositionInStaff.from_space(4))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('F', 5), kp.PositionInStaff.from_line(5))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('G', 5), kp.PositionInStaff.from_space(5))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('A', 5), kp.PositionInStaff.from_line(6))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('B', 5), kp.PositionInStaff.from_space(6))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('C', 6), kp.PositionInStaff.from_line(7))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('D', 6), kp.PositionInStaff.from_space(7))

    def test_compute_position_bunch_of_samples_negatives(self):
        g_clef_reference = kp.PitchPositionReferenceSystem(kp.AgnosticPitch('E', 4))

        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E', 4), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('D', 4), kp.PositionInStaff.from_space(0))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('C', 4), kp.PositionInStaff.from_line(0))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('B', 3), kp.PositionInStaff.from_space(-1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('A', 3), kp.PositionInStaff.from_line(-1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('G', 3), kp.PositionInStaff.from_space(-2))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('F', 3), kp.PositionInStaff.from_line(-2))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E', 3), kp.PositionInStaff.from_space(-3))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('D', 3), kp.PositionInStaff.from_line(-3))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('C', 3), kp.PositionInStaff.from_space(-4))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('B', 2), kp.PositionInStaff.from_line(-4))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('A', 2), kp.PositionInStaff.from_space(-5))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('G', 2), kp.PositionInStaff.from_line(-5))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('F', 2), kp.PositionInStaff.from_space(-6))

    def test_compute_position_bunch_of_samples_with_alterations(self):
        g_clef_reference = kp.PitchPositionReferenceSystem(kp.AgnosticPitch('E', 4))

        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E', 4), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E+', 4), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E++', 4), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E-', 4), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(g_clef_reference, kp.AgnosticPitch('E--', 4), kp.PositionInStaff.from_line(1))

    def test_clef_ordinal_suffix(self):
        self.assertEqual(kp.Clef._ordinal_suffix(1), 'st')
        self.assertEqual(kp.Clef._ordinal_suffix(2), 'nd')
        self.assertEqual(kp.Clef._ordinal_suffix(3), 'rd')
        self.assertEqual(kp.Clef._ordinal_suffix(4), 'th')
        self.assertEqual(kp.Clef._ordinal_suffix(11), 'th')
        self.assertEqual(kp.Clef._ordinal_suffix(12), 'th')
        self.assertEqual(kp.Clef._ordinal_suffix(13), 'th')
        self.assertEqual(kp.Clef._ordinal_suffix(21), 'st')
        self.assertEqual(kp.Clef._ordinal_suffix(1_000_000_000_000_000_000_000), 'th')

    def test_g_clef_scale(self):
        gclef = kp.GClef()
        self.assertEqual(kp.AgnosticPitch('E', 4), gclef.bottom_line())
        self.do_test_pitches_to_positions(gclef.reference_point(), kp.AgnosticPitch('E', 4), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(gclef.reference_point(), kp.AgnosticPitch('F', 4), kp.PositionInStaff.from_space(1))
        self.do_test_pitches_to_positions(gclef.reference_point(), kp.AgnosticPitch('G', 4), kp.PositionInStaff.from_line(2))
        self.do_test_pitches_to_positions(gclef.reference_point(), kp.AgnosticPitch('A', 4), kp.PositionInStaff.from_space(2))
        self.do_test_pitches_to_positions(gclef.reference_point(), kp.AgnosticPitch('B', 4), kp.PositionInStaff.from_line(3))
        self.do_test_pitches_to_positions(gclef.reference_point(), kp.AgnosticPitch('C', 5), kp.PositionInStaff.from_space(3))
        self.do_test_pitches_to_positions(gclef.reference_point(), kp.AgnosticPitch('D', 5), kp.PositionInStaff.from_line(4))
        self.do_test_pitches_to_positions(gclef.reference_point(), kp.AgnosticPitch('E', 5), kp.PositionInStaff.from_space(4))

    def test_f3_clef_scale(self):
        f3clef = kp.F3Clef()
        self.assertEqual(kp.AgnosticPitch('B', 3), f3clef.bottom_line())
        self.do_test_pitches_to_positions(f3clef.reference_point(), kp.AgnosticPitch('B', 3), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(f3clef.reference_point(), kp.AgnosticPitch('C', 4), kp.PositionInStaff.from_space(1))
        self.do_test_pitches_to_positions(f3clef.reference_point(), kp.AgnosticPitch('D', 4), kp.PositionInStaff.from_line(2))
        self.do_test_pitches_to_positions(f3clef.reference_point(), kp.AgnosticPitch('E', 4), kp.PositionInStaff.from_space(2))
        self.do_test_pitches_to_positions(f3clef.reference_point(), kp.AgnosticPitch('F', 4), kp.PositionInStaff.from_line(3))
        self.do_test_pitches_to_positions(f3clef.reference_point(), kp.AgnosticPitch('G', 4), kp.PositionInStaff.from_space(3))
        self.do_test_pitches_to_positions(f3clef.reference_point(), kp.AgnosticPitch('A', 4), kp.PositionInStaff.from_line(4))
        self.do_test_pitches_to_positions(f3clef.reference_point(), kp.AgnosticPitch('B', 4), kp.PositionInStaff.from_space(4))

    def test_f4_clef_scale(self):
        f4clef = kp.F4Clef()
        self.assertEqual(kp.AgnosticPitch('G', 2), f4clef.bottom_line())
        self.do_test_pitches_to_positions(f4clef.reference_point(), kp.AgnosticPitch('G', 2), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(f4clef.reference_point(), kp.AgnosticPitch('A', 2), kp.PositionInStaff.from_space(1))
        self.do_test_pitches_to_positions(f4clef.reference_point(), kp.AgnosticPitch('B', 2), kp.PositionInStaff.from_line(2))
        self.do_test_pitches_to_positions(f4clef.reference_point(), kp.AgnosticPitch('C', 3), kp.PositionInStaff.from_space(2))
        self.do_test_pitches_to_positions(f4clef.reference_point(), kp.AgnosticPitch('D', 3), kp.PositionInStaff.from_line(3))
        self.do_test_pitches_to_positions(f4clef.reference_point(), kp.AgnosticPitch('E', 3), kp.PositionInStaff.from_space(3))
        self.do_test_pitches_to_positions(f4clef.reference_point(), kp.AgnosticPitch('F', 3), kp.PositionInStaff.from_line(4))
        self.do_test_pitches_to_positions(f4clef.reference_point(), kp.AgnosticPitch('G', 3), kp.PositionInStaff.from_space(4))

    def test_c1_clef_scale(self):
        c1clef = kp.C1Clef()
        self.assertEqual(kp.AgnosticPitch('C', 3), c1clef.bottom_line())
        self.do_test_pitches_to_positions(c1clef.reference_point(), kp.AgnosticPitch('C', 3), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(c1clef.reference_point(), kp.AgnosticPitch('D', 3), kp.PositionInStaff.from_space(1))
        self.do_test_pitches_to_positions(c1clef.reference_point(), kp.AgnosticPitch('E', 3), kp.PositionInStaff.from_line(2))
        self.do_test_pitches_to_positions(c1clef.reference_point(), kp.AgnosticPitch('F', 3), kp.PositionInStaff.from_space(2))
        self.do_test_pitches_to_positions(c1clef.reference_point(), kp.AgnosticPitch('G', 3), kp.PositionInStaff.from_line(3))
        self.do_test_pitches_to_positions(c1clef.reference_point(), kp.AgnosticPitch('A', 3), kp.PositionInStaff.from_space(3))
        self.do_test_pitches_to_positions(c1clef.reference_point(), kp.AgnosticPitch('B', 3), kp.PositionInStaff.from_line(4))
        self.do_test_pitches_to_positions(c1clef.reference_point(), kp.AgnosticPitch('C', 4), kp.PositionInStaff.from_space(4))

    def test_c2_clef_scale(self):
        c2clef = kp.C2Clef()
        self.assertEqual(kp.AgnosticPitch('A', 2), c2clef.bottom_line())
        self.do_test_pitches_to_positions(c2clef.reference_point(), kp.AgnosticPitch('A', 2), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(c2clef.reference_point(), kp.AgnosticPitch('B', 2), kp.PositionInStaff.from_space(1))
        self.do_test_pitches_to_positions(c2clef.reference_point(), kp.AgnosticPitch('C', 2), kp.PositionInStaff.from_line(2))
        self.do_test_pitches_to_positions(c2clef.reference_point(), kp.AgnosticPitch('D', 2), kp.PositionInStaff.from_space(2))
        self.do_test_pitches_to_positions(c2clef.reference_point(), kp.AgnosticPitch('E', 2), kp.PositionInStaff.from_line(3))
        self.do_test_pitches_to_positions(c2clef.reference_point(), kp.AgnosticPitch('F', 2), kp.PositionInStaff.from_space(3))
        self.do_test_pitches_to_positions(c2clef.reference_point(), kp.AgnosticPitch('G', 2), kp.PositionInStaff.from_line(4))
        self.do_test_pitches_to_positions(c2clef.reference_point(), kp.AgnosticPitch('A', 3), kp.PositionInStaff.from_space(4))

    def test_c3_clef_scale(self):
        c3clef = kp.C3Clef()
        self.assertEqual(kp.AgnosticPitch('B', 2), c3clef.bottom_line())
        self.do_test_pitches_to_positions(c3clef.reference_point(), kp.AgnosticPitch('B', 2), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(c3clef.reference_point(), kp.AgnosticPitch('C', 2), kp.PositionInStaff.from_space(1))
        self.do_test_pitches_to_positions(c3clef.reference_point(), kp.AgnosticPitch('D', 2), kp.PositionInStaff.from_line(2))
        self.do_test_pitches_to_positions(c3clef.reference_point(), kp.AgnosticPitch('E', 2), kp.PositionInStaff.from_space(2))
        self.do_test_pitches_to_positions(c3clef.reference_point(), kp.AgnosticPitch('F', 2), kp.PositionInStaff.from_line(3))
        self.do_test_pitches_to_positions(c3clef.reference_point(), kp.AgnosticPitch('G', 2), kp.PositionInStaff.from_space(3))
        self.do_test_pitches_to_positions(c3clef.reference_point(), kp.AgnosticPitch('A', 2), kp.PositionInStaff.from_line(4))
        self.do_test_pitches_to_positions(c3clef.reference_point(), kp.AgnosticPitch('B', 3), kp.PositionInStaff.from_space(4))

    def test_c4_clef_scale(self):
        c4clef = kp.C4Clef()
        self.assertEqual(kp.AgnosticPitch('D', 2), c4clef.bottom_line())
        self.do_test_pitches_to_positions(c4clef.reference_point(), kp.AgnosticPitch('D', 2), kp.PositionInStaff.from_line(1))
        self.do_test_pitches_to_positions(c4clef.reference_point(), kp.AgnosticPitch('E', 2), kp.PositionInStaff.from_space(1))
        self.do_test_pitches_to_positions(c4clef.reference_point(), kp.AgnosticPitch('F', 2), kp.PositionInStaff.from_line(2))
        self.do_test_pitches_to_positions(c4clef.reference_point(), kp.AgnosticPitch('G', 2), kp.PositionInStaff.from_space(2))
        self.do_test_pitches_to_positions(c4clef.reference_point(), kp.AgnosticPitch('A', 2), kp.PositionInStaff.from_line(3))
        self.do_test_pitches_to_positions(c4clef.reference_point(), kp.AgnosticPitch('B', 2), kp.PositionInStaff.from_space(3))
        self.do_test_pitches_to_positions(c4clef.reference_point(), kp.AgnosticPitch('C', 3), kp.PositionInStaff.from_line(4))
        self.do_test_pitches_to_positions(c4clef.reference_point(), kp.AgnosticPitch('D', 3), kp.PositionInStaff.from_space(4))


class TestClefFactory(unittest.TestCase):
    def test_G_clef_without_decorators(self):
        clef = kp.ClefFactory.create_clef('*clefG2')
        self.assertIsInstance(clef, kp.GClef)

    def test_G_clef_single_v(self):
        clef = kp.ClefFactory.create_clef('*clefGv2')
        self.assertIsInstance(clef, kp.GClef)

    def test_G_clef_double_vv(self):
        clef = kp.ClefFactory.create_clef('*clefGvv2')
        self.assertIsInstance(clef, kp.GClef)

    def test_G_clef_single_caret(self):
        clef = kp.ClefFactory.create_clef('*clefG^2')
        self.assertIsInstance(clef, kp.GClef)

    def test_G_clef_double_caret(self):
        clef = kp.ClefFactory.create_clef('*clefG^^^^2')
        self.assertIsInstance(clef, kp.GClef)

    # F‑clef (bass), line 3
    def test_F3_clef_without_decorators(self):
        clef = kp.ClefFactory.create_clef('*clefF3')
        self.assertIsInstance(clef, kp.F3Clef)

    def test_F3_clef_with_v(self):
        clef = kp.ClefFactory.create_clef('*clefFv3')
        self.assertIsInstance(clef, kp.F3Clef)

    def test_F4_clef_without_decorators(self):
        clef = kp.ClefFactory.create_clef('*clefF4')
        self.assertIsInstance(clef, kp.F4Clef)

    def test_F4_clef_with_caret(self):
        clef = kp.ClefFactory.create_clef('*clefF^4')
        self.assertIsInstance(clef, kp.F4Clef)

    # C‑clefs, lines 1–4
    def test_C1_clef_basic(self):
        clef = kp.ClefFactory.create_clef('*clefC1')
        self.assertIsInstance(clef, kp.C1Clef)

    def test_C2_clef_with_vv(self):
        clef = kp.ClefFactory.create_clef('*clefCvv2')
        self.assertIsInstance(clef, kp.C2Clef)

    def test_C3_clef_with_caret(self):
        clef = kp.ClefFactory.create_clef('*clefC^3')
        self.assertIsInstance(clef, kp.C3Clef)

    def test_C4_clef_with_double_caret(self):
        clef = kp.ClefFactory.create_clef('*clefC^^4')
        self.assertIsInstance(clef, kp.C4Clef)

    # invalid name
    def test_invalid_clef_name(self):
        with self.assertRaises(ValueError):
            kp.ClefFactory.create_clef('*clefH2')

    # invalid F‑clef line
    def test_invalid_F_line(self):
        with self.assertRaises(ValueError):
            kp.ClefFactory.create_clef('*clefF2')

    # invalid C‑clef line
    def test_invalid_C_line(self):
        with self.assertRaises(ValueError):
            kp.ClefFactory.create_clef('*clefC5')

    # missing leading *
    def test_missing_prefix(self):
        with self.assertRaises(ValueError):
            kp.ClefFactory.create_clef('clefG2')
        with self.assertRaises(ValueError):
            kp.ClefFactory.create_clef('random')



