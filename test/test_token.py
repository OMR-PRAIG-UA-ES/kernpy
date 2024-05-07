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

