"""Agnostic export tests for key signatures and score-visible note accidentals.

All kern / expected score data lives under test/resources/agnostic/key_accidentals/
(case dirs with input.krn, expected.akrn, expected.aekrn). This module only wires tests.

    uv sync --group test
    uv run pytest test/test_agnostic_key_signatures.py -v --no-cov
"""
from __future__ import annotations

import unittest
from pathlib import Path

from parameterized import parameterized

import kernpy as kp

FIXTURES_DIR = Path('test/resources/agnostic/key_accidentals')
CASES_FILE = FIXTURES_DIR / 'cases.txt'
REQUIRED_FILES = ('input.krn', 'expected.akrn', 'expected.aekrn')


def _read_case_names() -> list[str]:
    return [
        line.strip()
        for line in CASES_FILE.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.strip().startswith('#')
    ]


def _case_dirs_on_disk() -> list[Path]:
    return sorted(
        path for path in FIXTURES_DIR.iterdir()
        if path.is_dir() and (path / 'input.krn').is_file()
    )


def _case_name_func(testcase_func, param_num, param):
    return f'{testcase_func.__name__}_{param.args[0]}'


class KeyAccidentalsFixtures:
    """Load and inspect key_accidentals resource fixtures."""

    @staticmethod
    def read_text(path: Path) -> str:
        return path.read_text(encoding='utf-8')

    @classmethod
    def case_dir(cls, case_name: str) -> Path:
        return FIXTURES_DIR / case_name

    @classmethod
    def load_input(cls, case_name: str) -> kp.Document:
        case_dir = cls.case_dir(case_name)
        document, errors = kp.load(str(case_dir / 'input.krn'))
        if errors:
            raise AssertionError(f'{case_name}: load errors: {errors}')
        return document

    @staticmethod
    def note_lines(exported: str) -> list[str]:
        lines = []
        for line in exported.splitlines():
            first = line.split('\t')[0]
            if first and first[0].isdigit():
                lines.append(line)
        return lines

    @staticmethod
    def key_lines(exported: str) -> list[str]:
        return [line for line in exported.splitlines() if '*k[' in line]


CASE_NAMES = _read_case_names()


class TestKeyAccidentalsInventory(unittest.TestCase):

    def test_cases_file_matches_fixture_directories(self):
        # Arrange
        from_file = set(CASE_NAMES)
        on_disk = {path.name for path in _case_dirs_on_disk()}

        # Act / Assert
        self.assertEqual(from_file, on_disk)

    def test_each_case_has_required_files(self):
        for case_name in CASE_NAMES:
            with self.subTest(case=case_name):
                # Arrange
                case_dir = KeyAccidentalsFixtures.case_dir(case_name)

                # Act / Assert
                for filename in REQUIRED_FILES:
                    self.assertTrue(
                        (case_dir / filename).is_file(),
                        msg=f'missing {filename} in {case_dir}',
                    )

    def test_each_input_loads_without_errors(self):
        for case_name in CASE_NAMES:
            with self.subTest(case=case_name):
                # Arrange / Act / Assert
                KeyAccidentalsFixtures.load_input(case_name)


class TestAgnosticKeyAccidentalsDumps(unittest.TestCase):

    @parameterized.expand([(name,) for name in CASE_NAMES], name_func=_case_name_func)
    def test_agnostic_kern_matches_expected(self, case_name: str):
        # Arrange
        document = KeyAccidentalsFixtures.load_input(case_name)
        expected = KeyAccidentalsFixtures.read_text(
            KeyAccidentalsFixtures.case_dir(case_name) / 'expected.akrn'
        )

        # Act
        actual = kp.dumps(document, encoding=kp.Encoding.agnosticKern)

        # Assert
        self.assertEqual(expected, actual)

    @parameterized.expand([(name,) for name in CASE_NAMES], name_func=_case_name_func)
    def test_agnostic_extended_kern_matches_expected(self, case_name: str):
        # Arrange
        document = KeyAccidentalsFixtures.load_input(case_name)
        expected = KeyAccidentalsFixtures.read_text(
            KeyAccidentalsFixtures.case_dir(case_name) / 'expected.aekrn'
        )

        # Act
        actual = kp.dumps(document, encoding=kp.Encoding.agnosticExtendedKern)

        # Assert
        self.assertEqual(expected, actual)


class TestScoreVisibleNoteAccidentals(unittest.TestCase):
    """Note / key display checks against resource goldens (no inline kern data)."""

    @parameterized.expand([(name,) for name in CASE_NAMES], name_func=_case_name_func)
    def test_key_header_matches_expected_akrn(self, case_name: str):
        # Arrange — agnostic may remap *k[...] through the spine clef
        case_dir = KeyAccidentalsFixtures.case_dir(case_name)
        expected_keys = KeyAccidentalsFixtures.key_lines(
            KeyAccidentalsFixtures.read_text(case_dir / 'expected.akrn')
        )
        document = KeyAccidentalsFixtures.load_input(case_name)

        # Act
        akern_keys = KeyAccidentalsFixtures.key_lines(
            kp.dumps(document, encoding=kp.Encoding.agnosticKern)
        )

        # Assert
        self.assertEqual(expected_keys, akern_keys)

    @parameterized.expand([(name,) for name in CASE_NAMES], name_func=_case_name_func)
    def test_note_lines_match_expected_akrn(self, case_name: str):
        # Arrange
        case_dir = KeyAccidentalsFixtures.case_dir(case_name)
        expected_notes = KeyAccidentalsFixtures.note_lines(
            KeyAccidentalsFixtures.read_text(case_dir / 'expected.akrn')
        )
        document = KeyAccidentalsFixtures.load_input(case_name)

        # Act
        actual_notes = KeyAccidentalsFixtures.note_lines(
            kp.dumps(document, encoding=kp.Encoding.agnosticKern)
        )

        # Assert
        self.assertEqual(expected_notes, actual_notes)

    @parameterized.expand([(name,) for name in CASE_NAMES], name_func=_case_name_func)
    def test_note_lines_match_expected_aekrn_without_separators(self, case_name: str):
        # Arrange
        case_dir = KeyAccidentalsFixtures.case_dir(case_name)
        expected_akern_notes = KeyAccidentalsFixtures.note_lines(
            KeyAccidentalsFixtures.read_text(case_dir / 'expected.akrn')
        )
        document = KeyAccidentalsFixtures.load_input(case_name)

        # Act
        aekern = kp.dumps(document, encoding=kp.Encoding.agnosticExtendedKern)
        actual_notes = [
            line.replace('@', '').replace('·', '')
            for line in KeyAccidentalsFixtures.note_lines(aekern)
        ]

        # Assert
        self.assertEqual(expected_akern_notes, actual_notes)


if __name__ == '__main__':
    unittest.main()
