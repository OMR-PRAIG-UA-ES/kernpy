"""
MuRET's own `**mens` semantic encodings, read by kernpy and by mOOsicae alike.

`test/resources/mens/muret/muret_semantic_sample.json` holds the smallest set of rows of MuRET's
mensural semantic export (mOOsicae's `testbed/io/muret/muret_mensural_semantic_23_july_2024.csv`,
9,948 staves) that contains every distinct cell of it, with the `@ids` stripped, next to mOOsicae's
export of the same row. The two libraries share the `**mens` grammar; this checks that they also read
the same notes out of it: for every note and rest, the same figure, perfection, coloration, dots,
pitch and accidental, in the same order. Export orders differ (the reading does not), so the cells are
compared by what they contain, not by how they are spelt.

Set KERNPY_MURET_CSV to the CSV to parse all 9,948 rows (without the mOOsicae reading, which is not
in the CSV).
"""
import csv
import json
import os
import re
import unittest
from pathlib import Path

import kernpy as kp

SAMPLE = Path('test/resources/mens/muret/muret_semantic_sample.json')


def as_mens_document(staff: str) -> str:
    """A MuRET staff (no header, `@ids` stripped) as a single-spine `**mens` document."""
    return '**mens\n' + staff.strip('\n') + '\n*-\n'


def strip_ids(staff: str) -> str:
    return '\n'.join(line.split('@')[0] for line in staff.split('\n'))


def durational_cells(text: str):
    return [line for line in text.split('\n') if line and line[0] not in '*!=' and line != '.']


def reading(cell: str):
    """What a note or rest cell says, whatever the order it is written in."""
    figures = re.findall(r'[XLSsMmUu]', cell)
    return (
        figures[0] if figures else None,  # the first figure letter is the figure; a later L/J is a beam
        ''.join(sorted(re.findall(r'[pi+I]', cell))),
        '~' in cell,
        cell.count('.'),
        cell.count(':'),
        ''.join(re.findall(r'[a-gA-G]', cell)),
        ''.join(sorted(re.findall(r'[#\-n]', cell))),
        'r' in cell,
    )


class MuRETMensTest(unittest.TestCase):

    def test_kernpy_reads_what_moosicae_reads(self):
        rows = json.loads(SAMPLE.read_text(encoding='utf-8'))['rows']
        self.assertGreater(len(rows), 600)
        for row in rows:
            with self.subTest(row=row['row']):
                document, errors = kp.loads(as_mens_document(row['mens']))
                self.assertEqual([], errors)
                ours = [reading(c) for c in durational_cells(kp.dumps(document))]
                theirs = [reading(c) for c in durational_cells(row['moosicae'])]
                self.assertEqual(theirs, ours)

    @unittest.skipUnless(os.environ.get('KERNPY_MURET_CSV'),
                         'set KERNPY_MURET_CSV to muret_mensural_semantic_23_july_2024.csv to parse every row')
    def test_every_row_of_the_csv_parses(self):
        with open(os.environ['KERNPY_MURET_CSV'], newline='', encoding='utf-8') as f:
            staves = [row['semantic_encoding'] for row in csv.DictReader(f)]
        self.assertGreater(len(staves), 0)
        for i, staff in enumerate(staves):
            with self.subTest(row=i):
                _, errors = kp.loads(as_mens_document(strip_ids(staff)))
                self.assertEqual([], errors)


if __name__ == '__main__':
    unittest.main()
