import os
import unittest
import sys

import kernpy


class TokenTestCase(unittest.TestCase):
    def test_PitchRest_creation_generic(self):
        pitch_rest = kernpy.PitchRest('c')
        self.assertEqual(pitch_rest.pitch, 'c')
        self.assertEqual(pitch_rest.octave, 4)
        self.assertEqual(pitch_rest.is_rest(), False)

    def test_PitchRest_creation_pitch(self):
        pitch_rest = kernpy.PitchRest('c')
        self.assertEqual(pitch_rest.pitch, 'c')
        pitch_rest = kernpy.PitchRest('ccc')
        self.assertEqual(pitch_rest.pitch, 'c')
        pitch_rest = kernpy.PitchRest('C')
        self.assertEqual(pitch_rest.pitch, 'c')
        pitch_rest = kernpy.PitchRest('CCCCC')
        self.assertEqual(pitch_rest.pitch, 'c')

    def test_PitchRest_creation_octave(self):
        pitch_rest = kernpy.PitchRest('c')
        self.assertEqual(pitch_rest.octave, 4)
        pitch_rest = kernpy.PitchRest('ccc')
        self.assertEqual(pitch_rest.octave, 6)
        pitch_rest = kernpy.PitchRest('ccccc')
        self.assertEqual(pitch_rest.octave, 8)
        pitch_rest = kernpy.PitchRest('C')
        self.assertEqual(pitch_rest.octave, 3)
        pitch_rest = kernpy.PitchRest('CCC')
        self.assertEqual(pitch_rest.octave, 1)
        pitch_rest = kernpy.PitchRest('CCCCC')
        self.assertEqual(pitch_rest.octave, -1)

    def test_PitchRest_creation_rest(self):
        pitch_rest = kernpy.PitchRest('r')
        self.assertEqual(pitch_rest.pitch, 'r')
        self.assertEqual(pitch_rest.octave, None)
        self.assertEqual(pitch_rest.is_rest(), True)

    def test_PitchRest_eq(self):
        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('c')
        self.assertTrue(pitch_rest_a == pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('ccc')
        self.assertFalse(pitch_rest_a == pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('r')
        self.assertFalse(pitch_rest_a == pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('r')
        pitch_rest_b = kernpy.PitchRest('r')
        self.assertTrue(pitch_rest_a == pitch_rest_b)

    def test_PitchRest_ne(self):
        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('d')
        self.assertTrue(pitch_rest_a != pitch_rest_b)


    def test_PitchRest_gt(self):
        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('c')
        self.assertFalse(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('ccc')
        self.assertFalse(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('C')
        pitch_rest_b = kernpy.PitchRest('C')
        self.assertFalse(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('C')
        pitch_rest_b = kernpy.PitchRest('CCC')
        self.assertTrue(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('CCC')
        pitch_rest_b = kernpy.PitchRest('C')
        self.assertFalse(pitch_rest_a > pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('r')
        pitch_rest_b = kernpy.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a > pitch_rest_b

    def test_PitchRest_lt(self):
        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('c')
        self.assertFalse(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('ccc')
        self.assertTrue(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('C')
        pitch_rest_b = kernpy.PitchRest('C')
        self.assertFalse(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('C')
        pitch_rest_b = kernpy.PitchRest('CCC')
        self.assertFalse(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('CCC')
        pitch_rest_b = kernpy.PitchRest('C')
        self.assertTrue(pitch_rest_a < pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('r')
        pitch_rest_b = kernpy.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a < pitch_rest_b

    def test_PitchRest_ge(self):
        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('c')
        self.assertTrue(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('ccc')
        self.assertFalse(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('C')
        pitch_rest_b = kernpy.PitchRest('C')
        self.assertTrue(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('C')
        pitch_rest_b = kernpy.PitchRest('CCC')
        self.assertTrue(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('CCC')
        pitch_rest_b = kernpy.PitchRest('C')
        self.assertFalse(pitch_rest_a >= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('r')
        pitch_rest_b = kernpy.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a >= pitch_rest_b

        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a >= pitch_rest_b

    def test_PitchRest_le(self):
        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('c')
        self.assertTrue(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('ccc')
        self.assertTrue(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('C')
        pitch_rest_b = kernpy.PitchRest('C')
        self.assertTrue(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('C')
        pitch_rest_b = kernpy.PitchRest('CCC')
        self.assertFalse(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('CCC')
        pitch_rest_b = kernpy.PitchRest('C')
        self.assertTrue(pitch_rest_a <= pitch_rest_b)

        pitch_rest_a = kernpy.PitchRest('r')
        pitch_rest_b = kernpy.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a <= pitch_rest_b

        pitch_rest_a = kernpy.PitchRest('c')
        pitch_rest_b = kernpy.PitchRest('r')
        with self.assertRaises(ValueError):
            pitch_rest_a <= pitch_rest_b

    def test_Duration_creation_generic(self):
        duration = kernpy.Duration('2')
        self.assertEqual(duration.duration, 2)

        duration = kernpy.Duration('16')
        self.assertEqual(duration.duration, 16)

        duration = kernpy.Duration('1')
        self.assertEqual(duration.duration, 1)

        with self.assertRaises(ValueError):
            duration = kernpy.Duration('0')

        with self.assertRaises(ValueError):
            duration = kernpy.Duration('abcde')

    def test_Duration_eq(self):
        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('2')
        self.assertTrue(duration_a == duration_b)

        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('16')
        self.assertFalse(duration_a == duration_b)

    def test_Duration_ne(self):
        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('2')
        self.assertFalse(duration_a != duration_b)

        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('16')
        self.assertTrue(duration_a != duration_b)

    def test_Duration_gt(self):
        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('2')
        self.assertFalse(duration_a > duration_b)

        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('16')
        self.assertFalse(duration_a > duration_b)

        duration_a = kernpy.Duration('16')
        duration_b = kernpy.Duration('2')
        self.assertTrue(duration_a > duration_b)

    def test_Duration_lt(self):
        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('2')
        self.assertFalse(duration_a < duration_b)

        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('16')
        self.assertTrue(duration_a < duration_b)

        duration_a = kernpy.Duration('16')
        duration_b = kernpy.Duration('2')
        self.assertFalse(duration_a < duration_b)

    def test_Duration_ge(self):
        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('2')
        self.assertTrue(duration_a >= duration_b)

        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('16')
        self.assertFalse(duration_a >= duration_b)

        duration_a = kernpy.Duration('16')
        duration_b = kernpy.Duration('2')
        self.assertTrue(duration_a >= duration_b)

    def test_Duration_le(self):
        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('2')
        self.assertTrue(duration_a <= duration_b)

        duration_a = kernpy.Duration('2')
        duration_b = kernpy.Duration('16')
        self.assertTrue(duration_a <= duration_b)

        duration_a = kernpy.Duration('16')
        duration_b = kernpy.Duration('2')
        self.assertFalse(duration_a <= duration_b)

    def test_Duration_modify_duration(self):
        duration = kernpy.Duration('2')
        new_duration = duration.modify_duration(4)
        self.assertEqual(new_duration.duration, 8)

        duration = kernpy.Duration('16')
        new_duration = duration.modify_duration(2)
        self.assertEqual(new_duration.duration, 32)

        duration = kernpy.Duration('2')
        new_duration = duration.modify_duration(1)
        self.assertEqual(new_duration.duration, 2)

        duration = kernpy.Duration('2')
        with self.assertRaises(ValueError):
            new_duration = duration.modify_duration(0)

        duration = kernpy.Duration('2')
        with self.assertRaises(ValueError):
            new_duration = duration.modify_duration(-1)

        duration = kernpy.Duration('2')
        with self.assertRaises(ValueError):
            new_duration = duration.modify_duration(1.5)





