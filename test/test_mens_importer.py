import unittest

import kernpy as kp
from kernpy.core.mens_spine_importer import MensSpineImporter

FIXTURE = 'test/resources/mens/mensural_vocabulary.mens'


class MensImporterTest(unittest.TestCase):
    """**mens is read with the combined **kern/**mens grammar vendored from mOOsicae."""

    def test_every_standard_token_parses(self):
        document, errors = kp.load(FIXTURE, raise_on_errors=True)
        self.assertEqual([], errors)

    def test_export_is_a_fixed_point(self):
        document, _ = kp.load(FIXTURE, raise_on_errors=True)
        exported = kp.dumps(document)
        again, _ = kp.loads(exported, raise_on_errors=True)
        self.assertEqual(exported, kp.dumps(again))

    def test_the_mensural_duration_is_one_subtoken_as_written(self):
        importer = MensSpineImporter()
        for encoding, duration in (('Sp:B', 'Sp:'), ('s~g', 's~'), ('M.e', 'M.'), ('Lic', 'Li'), ('Xpa', 'Xp')):
            token = importer.import_token(encoding)
            durations = [s.encoding for s in token.pitch_duration_subtokens if s.category == kp.TokenCategory.DURATION]
            self.assertEqual([duration], durations, encoding)

    def test_the_division_dot_keeps_its_place(self):
        document, _ = kp.loads('**mens\n*met(O)\ns:d\n*-\n', raise_on_errors=True)
        self.assertIn('s:d', kp.dumps(document).splitlines())

    def test_a_ligature_mark_before_the_note_is_kept(self):
        token = MensSpineImporter().import_token('<Sa')
        self.assertIn('<', [s.encoding for s in token.decoration_subtokens])

    def test_custos_and_rests(self):
        importer = MensSpineImporter()
        self.assertEqual(kp.TokenCategory.ENGRAVED_SYMBOLS, importer.import_token('*custosG').category)
        self.assertEqual(kp.TokenCategory.NOTE_REST, importer.import_token('sr').category)

    def test_a_custos_needs_its_pitch(self):
        # SEILS writes a bare `*custos`: a dialect, normalised by its readers, not by the grammar
        with self.assertRaises(ValueError):
            MensSpineImporter().import_token('*custos')

    def test_kern_spines_are_untouched(self):
        document, errors = kp.loads('**kern\n*M3/4\n4c\n4d\n4e\n=\n*-\n', raise_on_errors=True)
        self.assertEqual([], errors)


if __name__ == '__main__':
    unittest.main()
