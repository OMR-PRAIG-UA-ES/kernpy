"""
Round trip of real **mens data: import, export, import again.

The export is kernpy's normalised form, as for **kern: global comments and hidden barlines (`=1-`)
are not written, and the marks of a note follow its pitch (`<S~a` is written `S~a<`; the shared
grammar reads both as the same ligature start). So the test is not "output == input" but:

- the export is a fixed point (exporting the re-imported export gives it back), and
- every note and rest cell of every **mens spine survives, with the same duration and pitch.

Fixtures and their licences: test/resources/mens/SOURCES.md. Set KERNPY_MENS_CORPUS to a directory
(e.g. SEILS_diplomatic_OMRgroundTruth, located with `muret-corpora path seils-diplomatic`) to run
the same checks over every **mens file below it.
"""
import os
import unittest
from pathlib import Path

import kernpy as kp

MENS_DIR = Path('test/resources/mens')
APEL = sorted((MENS_DIR / 'apel').glob('*.krn'))
REFERENCE = sorted((MENS_DIR / 'reference').glob('*.mens'))
SEILS_CLEAN = MENS_DIR / 'seils' / 'perue_seitu_choral.mns'
SEILS_DIALECT = MENS_DIR / 'seils' / 'belli_amorcon_C.mns'

# What the shared grammar rejects in SEILS, and SEILS only: a bare custos (the grammar wants its pitch,
# `*custosG`) and a stray `ui6G`. The orders SEILS writes (`s~id`, `Mp:~ee]`) are valid **mens: Humdrum
# does not fix the order of a token's signifiers.
SEILS_DIALECT_PREFIXES = ('*custos', 'ui6')


def mens_note_cells(text: str):
    """The note and rest cells of the **mens columns of a file without spine splits, in order."""
    cells = []
    mens_columns = None
    for line in text.splitlines():
        if not line.strip() or line.startswith('!!'):
            continue
        row = line.split('\t')
        if row[0].startswith('**'):
            mens_columns = [i for i, header in enumerate(row) if header == '**mens']
            continue
        for i in mens_columns or []:
            cell = row[i]
            if cell and cell != '.' and cell[0] not in '*!=':
                cells.append(cell)
    return cells


def canonical(cell: str) -> str:
    """A note cell with its characters sorted: the export reorders the marks, never the content."""
    return ''.join(sorted(cell))


class RoundTripCase(unittest.TestCase):
    """The round-trip assertion; no tests of its own."""

    def assert_round_trip(self, path: Path, expect_errors: bool = False):
        text = path.read_text(encoding='utf-8')
        document, errors = kp.loads(text)
        if not expect_errors:
            self.assertEqual([], errors, path)

        exported = kp.dumps(document)
        again, errors_again = kp.loads(exported)
        self.assertEqual(exported, kp.dumps(again), f'{path}: the export is not a fixed point')
        self.assertEqual(len(errors), len(errors_again), path)

        source_cells = mens_note_cells(text)
        exported_cells = mens_note_cells(exported)
        self.assertEqual(len(source_cells), len(exported_cells), f'{path}: notes or rests lost')
        self.assertEqual([canonical(c) for c in source_cells], [canonical(c) for c in exported_cells], path)
        return errors


class MensRoundTripTest(RoundTripCase):

    def test_apel_examples(self):
        self.assertEqual(15, len(APEL))
        for path in APEL:
            with self.subTest(path=path.name):
                self.assert_round_trip(path)

    def test_reference_set(self):
        # Sapp's **mens syntax, signifiers in several orders (see SOURCES.md)
        self.assertEqual(3, len(REFERENCE))
        for path in REFERENCE:
            with self.subTest(path=path.name):
                self.assert_round_trip(path)

    def test_seils_choral_score(self):
        self.assert_round_trip(SEILS_CLEAN)

    def test_seils_dialect_is_reported_and_kept_verbatim(self):
        errors = self.assert_round_trip(SEILS_DIALECT, expect_errors=True)
        # the 5 bare custodes; the perfection marks after the coloration (`s~id`) are read
        self.assertEqual(5, len(errors))
        document, _ = kp.load(SEILS_DIALECT)
        exported = kp.dumps(document).split()
        for line in SEILS_DIALECT.read_text(encoding='utf-8').splitlines():
            for cell in line.split('\t'):
                if cell == '*custos':
                    self.assertIn(cell, exported)
                if cell.startswith('s~i'):
                    self.assertIn('si~' + cell[3:], exported)

    def test_a_perfection_mark_after_the_coloration_is_the_perfection_mark(self):
        # Humdrum does not fix the order of a token's signifiers: `s~id` is `si~d`, and the `i` is the
        # imperfection, never a user-assignable decoration (it once was, and the imperfection was lost).
        for token in ('s~id', 'si~d', 'd~is', 'sd~i'):
            with self.subTest(token=token):
                document, errors = kp.loads(f'**mens\n*met(O)\n{token}\n*-\n', raise_on_errors=True)
                self.assertIn('si~d', kp.dumps(document).splitlines())

    def test_the_spine_type_decides_what_a_letter_means(self):
        # `L` is a beam in **kern and the longa in **mens (before the figure; after it, a beam: `UaL`)
        kern, _ = kp.loads('**kern\nL8c\n*-\n', raise_on_errors=True)
        self.assertIn('8cL', kp.dumps(kern).splitlines())
        mens, _ = kp.loads('**mens\naL\nUaL\n*-\n', raise_on_errors=True)
        self.assertEqual(['La', 'UaL'], kp.dumps(mens).splitlines()[1:3])
        # `p` is perfect in **mens, never an appoggiatura; `+` is altera
        mens, _ = kp.loads('**mens\ns~pa\nSd+\n*-\n', raise_on_errors=True)
        self.assertEqual(['sp~a', 'S+d'], kp.dumps(mens).splitlines()[1:3])

    def test_hidden_barlines_are_not_exported_but_still_count_measures(self):
        document, _ = kp.load(SEILS_CLEAN)
        self.assertNotIn('=1-', kp.dumps(document))
        self.assertGreater(document.measures_count(), 1)


@unittest.skipUnless(os.environ.get('KERNPY_MENS_CORPUS'),
                     'set KERNPY_MENS_CORPUS to a directory of **mens files to run the corpus round trip')
class MensCorpusRoundTripTest(RoundTripCase):
    """The same checks over a whole corpus on this machine (not in CI: the corpus is not in the repo)."""

    def test_corpus(self):
        root = Path(os.environ['KERNPY_MENS_CORPUS'])
        paths = sorted(p for p in root.rglob('*') if p.suffix in ('.mns', '.mens', '.krn') and p.is_file())
        checked = 0
        for path in paths:
            if '**mens' not in path.read_text(encoding='utf-8', errors='ignore'):
                continue
            with self.subTest(path=str(path.relative_to(root))):
                errors = self.assert_round_trip(path, expect_errors=True)
                for error in errors:
                    cell = error.split("): '", 1)[1].split("'. Parsing", 1)[0]
                    self.assertTrue(cell.startswith(SEILS_DIALECT_PREFIXES), error)
            checked += 1
        self.assertGreater(checked, 0, f'no **mens file under {root}')


if __name__ == '__main__':
    unittest.main()
