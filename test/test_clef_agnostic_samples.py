"""
Clef sample tests: agnostic kern export and T/S staff-position encoding.

Fixtures:
  - test/resources/agnostic/samples/ (generate_fixtures.py)
  - test/resources/agnostic/samples_with_alterations/ (generate_altered_fixtures.py)

    uv sync --group test
    uv run python -m unittest test.test_clef_agnostic_samples -v
"""
from __future__ import annotations

import unittest
from pathlib import Path

from parameterized import parameterized

import kernpy as kp
from kernpy.core.gkern import ClefFactory, GKernExporter
from kernpy.core.pitch_models import HumdrumPitchExporter, HumdrumPitchImporter


class ClefAgnosticSamples:
    """Paths, builders, and assertions for test/resources/agnostic/samples/."""

    SAMPLES_DIR = Path('test/resources/agnostic/samples')
    METER_SIGNATURE = '*M14/4'

    FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC = 'from_different_semantic_to_equal_agnostic'
    FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC_2 = 'from_different_semantic_to_equal_agnostic_2'
    FROM_EQUAL_SEMANTIC_TO_DIFFERENT_AGNOSTIC = 'from_equal_semantic_to_different_agnostic'
    FROM_GRAPHICALLY_DIFFERENT_TO_EQUAL = 'from_graphically_different_to_graphically_equal'
    FROM_GRAPHICALLY_EQUAL_TO_DIFFERENT = 'from_graphically_equal_to_graphically_different'

    DIR_DIFFERENT_SEMANTIC_TO_EQUAL = SAMPLES_DIR / FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC
    DIR_DIFFERENT_SEMANTIC_TO_EQUAL_2 = SAMPLES_DIR / FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC_2
    DIR_EQUAL_SEMANTIC_TO_DIFFERENT = SAMPLES_DIR / FROM_EQUAL_SEMANTIC_TO_DIFFERENT_AGNOSTIC
    DIR_GRAPHICALLY_DIFFERENT_TO_EQUAL = SAMPLES_DIR / FROM_GRAPHICALLY_DIFFERENT_TO_EQUAL
    DIR_GRAPHICALLY_EQUAL_TO_DIFFERENT = SAMPLES_DIR / FROM_GRAPHICALLY_EQUAL_TO_DIFFERENT

    SEMANTIC_SCENARIO_CASES: tuple[tuple[Path, str], ...] = (
        (DIR_DIFFERENT_SEMANTIC_TO_EQUAL, FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC),
        (DIR_DIFFERENT_SEMANTIC_TO_EQUAL_2, FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC_2),
        (DIR_EQUAL_SEMANTIC_TO_DIFFERENT, FROM_EQUAL_SEMANTIC_TO_DIFFERENT_AGNOSTIC),
    )

    GRAPHICAL_SCENARIO_CASES: tuple[tuple[Path, str], ...] = (
        (DIR_GRAPHICALLY_DIFFERENT_TO_EQUAL, FROM_GRAPHICALLY_DIFFERENT_TO_EQUAL),
        (DIR_GRAPHICALLY_EQUAL_TO_DIFFERENT, FROM_GRAPHICALLY_EQUAL_TO_DIFFERENT),
    )

    ALL_SCENARIO_CASES: tuple[tuple[Path, str], ...] = (
        *SEMANTIC_SCENARIO_CASES,
        *GRAPHICAL_SCENARIO_CASES,
    )

    DIFFERENT_SEMANTIC_OUTPUT_SCENARIO_CASES: tuple[tuple[Path, str], ...] = (
        (DIR_DIFFERENT_SEMANTIC_TO_EQUAL, FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC),
        (DIR_DIFFERENT_SEMANTIC_TO_EQUAL_2, FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC_2),
        (DIR_EQUAL_SEMANTIC_TO_DIFFERENT, FROM_EQUAL_SEMANTIC_TO_DIFFERENT_AGNOSTIC),
        (DIR_GRAPHICALLY_DIFFERENT_TO_EQUAL, FROM_GRAPHICALLY_DIFFERENT_TO_EQUAL),
    )

    CLEF_DATA: list[tuple[str, str, type]] = [
        ('g_clef', '*clefG2', kp.GClef),
        ('f3_clef', '*clefF3', kp.F3Clef),
        ('f4_clef', '*clefF4', kp.F4Clef),
        ('c1_clef', '*clefC1', kp.C1Clef),
        ('c2_clef', '*clefC2', kp.C2Clef),
        ('c3_clef', '*clefC3', kp.C3Clef),
        ('c4_clef', '*clefC4', kp.C4Clef),
    ]

    _KERN_IMPORTER = HumdrumPitchImporter()

    _LEGACY_KRN_NAMES: dict[str, str] = {
        'from_different_semantic_encoding_to_equal_agnostic_encoding_input.krn':
            'from_different_semantic_to_equal_agnostic_input.krn',
        'from_different_semantic_encoding_to_equal_agnostic_encoding_output.krn':
            'from_different_semantic_to_equal_agnostic_output.krn',
        'from_different_semantic_encoding_to_equal_agnostic_encoding_2_input.krn':
            'from_different_semantic_to_equal_agnostic_2_input.krn',
        'from_different_semantic_encoding_to_equal_agnostic_encoding_2_output.krn':
            'from_different_semantic_to_equal_agnostic_2_output.krn',
        'from_different_semantic_encoding_to_equal_agnostic_2_encoding_input.krn':
            'from_different_semantic_to_equal_agnostic_2_input.krn',
        'from_different_semantic_encoding_to_equal_agnostic_2_encoding_output.krn':
            'from_different_semantic_to_equal_agnostic_2_output.krn',
        'from_equal_semantic_encoding_to_different_agnostic_encoding_input.krn':
            'from_equal_semantic_to_different_agnostic_input.krn',
        'from_equal_semantic_encoding_to_different_agnostic_encoding_output.krn':
            'from_equal_semantic_to_different_agnostic_output.krn',
    }

    @staticmethod
    def scenario_krn_path(scenario_dir: Path, scenario_name: str, role: str) -> Path:
        return scenario_dir / f'{scenario_name}_{role}.krn'

    @staticmethod
    def read_text(path: Path) -> str:
        return path.read_text(encoding='utf-8')

    @classmethod
    def migrate_legacy_krn_names(cls, scenario_dir: Path) -> None:
        if not scenario_dir.is_dir():
            return
        for path in scenario_dir.iterdir():
            new_name = cls._LEGACY_KRN_NAMES.get(path.name)
            if new_name is not None:
                path.rename(scenario_dir / new_name)

    @staticmethod
    def pitch_at_diatonic_steps(base: kp.AgnosticPitch, steps: int) -> kp.AgnosticPitch:
        letter_to_index = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
        letters = 'CDEFGAB'
        name = base.name.replace('+', '').replace('-', '')
        base_idx = letter_to_index[name]
        total = base_idx + steps
        target_idx = total % 7
        octave = base.octave + total // 7
        return kp.AgnosticPitch(letters[target_idx], octave)

    @classmethod
    def fourteen_agnostic_pitches(cls, clef: kp.Clef) -> list[kp.AgnosticPitch]:
        bottom = clef.bottom_line()
        return [cls.pitch_at_diatonic_steps(bottom, step) for step in range(14)]

    @classmethod
    def fourteen_kern_pitches(cls, clef: kp.Clef) -> list[str]:
        exporter = HumdrumPitchExporter()
        return [exporter.export_pitch(pitch) for pitch in cls.fourteen_agnostic_pitches(clef)]

    @classmethod
    def build_different_semantic_multi_clef_kern(cls) -> str:
        sep = '\t'
        lines = [sep.join(['**kern'] * len(cls.CLEF_DATA))]
        lines.append(sep.join(token for _, token, _ in cls.CLEF_DATA))
        lines.append(sep.join([cls.METER_SIGNATURE] * len(cls.CLEF_DATA)))
        lines.append(sep.join(['='] * len(cls.CLEF_DATA)))
        for row in zip(*[cls.fourteen_kern_pitches(clef_cls()) for _, _, clef_cls in cls.CLEF_DATA]):
            lines.append(sep.join(f'4{pitch}' for pitch in row))
        lines.append(sep.join(['=='] * len(cls.CLEF_DATA)))
        lines.append(sep.join(['*-'] * len(cls.CLEF_DATA)))
        return '\n'.join(lines) + '\n'

    @classmethod
    def build_equal_semantic_multi_clef_kern(cls) -> str:
        sep = '\t'
        g_pitches = cls.fourteen_kern_pitches(kp.GClef())
        lines = [sep.join(['**kern'] * len(cls.CLEF_DATA))]
        lines.append(sep.join(token for _, token, _ in cls.CLEF_DATA))
        lines.append(sep.join([cls.METER_SIGNATURE] * len(cls.CLEF_DATA)))
        lines.append(sep.join(['='] * len(cls.CLEF_DATA)))
        for pitch in g_pitches:
            lines.append(sep.join(f'4{pitch}' for _ in cls.CLEF_DATA))
        lines.append(sep.join(['=='] * len(cls.CLEF_DATA)))
        lines.append(sep.join(['*-'] * len(cls.CLEF_DATA)))
        return '\n'.join(lines) + '\n'

    @classmethod
    def build_graphically_different_input_kern(cls) -> str:
        return cls.build_equal_semantic_multi_clef_kern()

    @classmethod
    def build_graphically_equal_output_kern(cls) -> str:
        return cls.build_different_semantic_multi_clef_kern()

    @staticmethod
    def extended_cell_to_akern(cell: str) -> str:
        if '@' not in cell:
            return cell
        at = cell.index('@')
        return cell[:at] + cell[at + 1:]

    @classmethod
    def extended_line_to_akern(cls, line: str) -> str:
        return '\t'.join(cls.extended_cell_to_akern(part) for part in line.split('\t'))

    @classmethod
    def extended_export_to_akern(cls, content: str) -> str:
        lines = []
        for line in content.splitlines():
            line = line.replace('**aekern', '**akern')
            lines.append(cls.extended_line_to_akern(line))
        return '\n'.join(lines) + '\n'

    @classmethod
    def staff_positions_for_kern_pitches(
        cls, staff: kp.Staff, clef: kp.Clef, kern_pitches: list[str],
    ) -> list[str]:
        exporter = GKernExporter(clef)
        return [
            exporter.export(staff, cls._KERN_IMPORTER.import_pitch(kern_pitch))
            for kern_pitch in kern_pitches
        ]

    @classmethod
    def fourteen_staff_position_ts(cls, clef: kp.Clef, staff: kp.Staff | None = None) -> list[str]:
        staff = staff or kp.Staff()
        exporter = GKernExporter(clef)
        return [exporter.export(staff, pitch) for pitch in cls.fourteen_agnostic_pitches(clef)]

    @classmethod
    def write_scenario_bundle(
        cls, scenario_dir: Path, scenario_name: str, input_krn: str, output_krn: str,
    ) -> None:
        scenario_dir.mkdir(parents=True, exist_ok=True)
        cls.migrate_legacy_krn_names(scenario_dir)
        cls.scenario_krn_path(scenario_dir, scenario_name, 'input').write_text(input_krn, encoding='utf-8')
        cls.scenario_krn_path(scenario_dir, scenario_name, 'output').write_text(output_krn, encoding='utf-8')

    @staticmethod
    def agnostic_normalized_note_lines(exported: str) -> list[str]:
        return [
            line for line in exported.splitlines()
            if line.split('\t')[0].startswith('4') and '@' not in line.split('\t')[0]
        ]

    @classmethod
    def dumps_agnostic_exports(cls, document: kp.Document) -> tuple[str, str, str]:
        extended = kp.dumps(document, encoding=kp.Encoding.agnosticExtendedKern)
        normalized = cls.extended_export_to_akern(extended)
        akern = kp.dumps(document, encoding=kp.Encoding.agnosticKern)
        return extended, normalized, akern

    @classmethod
    def equal_staff_position_ts_rows(cls) -> list[str]:
        ts_rows = list(zip(*[cls.fourteen_staff_position_ts(clef_cls()) for _, _, clef_cls in cls.CLEF_DATA]))
        return ['\t'.join(row) for row in ts_rows]

    @staticmethod
    def _kern_note_cells(krn_content: str) -> tuple[list[str], list[list[str]]]:
        lines = [line for line in krn_content.splitlines() if line.strip()]
        clef_tokens = lines[1].split('\t')
        note_lines = [
            line.split('\t') for line in lines
            if line.split('\t')[0] and line.split('\t')[0][0].isdigit()
        ]
        return clef_tokens, note_lines

    @staticmethod
    def _duration_and_pitch(cell: str) -> tuple[str, str]:
        index = 0
        while index < len(cell) and (cell[index].isdigit() or cell[index] in '.%'):
            index += 1
        return cell[:index], cell[index:]

    @classmethod
    def staff_position_ts_rows_for_krn(cls, krn_content: str, staff: kp.Staff | None = None) -> list[list[str]]:
        staff = staff or kp.Staff()
        clef_tokens, note_lines = cls._kern_note_cells(krn_content)
        clefs = [ClefFactory.create_clef(token) for token in clef_tokens]
        rows: list[list[str]] = []
        for cells in note_lines:
            row: list[str] = []
            for clef, cell in zip(clefs, cells):
                _duration, pitch_token = cls._duration_and_pitch(cell)
                pitch = cls._KERN_IMPORTER.import_pitch(pitch_token)
                row.append(GKernExporter(clef).export(staff, pitch))
            rows.append(row)
        return rows

    @staticmethod
    def graphical_rows_all_equal(ts_rows: list[list[str]]) -> bool:
        return all(len(set(row)) == 1 for row in ts_rows)

    @staticmethod
    def graphical_rows_all_different(ts_rows: list[list[str]]) -> bool:
        return all(len(set(row)) == len(row) for row in ts_rows)

    @classmethod
    def all_samples_krn_paths(cls) -> list[Path]:
        return sorted(cls.SAMPLES_DIR.rglob('*.krn'))

    @classmethod
    def expected_samples_krn_paths(cls) -> list[Path]:
        return sorted(
            cls.scenario_krn_path(scenario_dir, scenario_name, role)
            for scenario_dir, scenario_name in cls.ALL_SCENARIO_CASES
            for role in ('input', 'output')
        )

    @classmethod
    def scenario_paths(cls, scenario_dir: Path, scenario_name: str) -> dict[str, Path]:
        return {
            'input': cls.scenario_krn_path(scenario_dir, scenario_name, 'input'),
            'output': cls.scenario_krn_path(scenario_dir, scenario_name, 'output'),
        }


ClefAgnosticSamples.FOURTEEN_TS_LADDER = ClefAgnosticSamples.fourteen_staff_position_ts(kp.GClef())

S = ClefAgnosticSamples


def _clef_param_name_func(testcase_func, param_num, param):
    slug, _token, _cls = param.args
    return f'{testcase_func.__name__}_{slug}'


def _clef_step_name_func(testcase_func, param_num, param):
    slug, _token, _cls, step, _ts = param.args
    return f'{testcase_func.__name__}_{slug}_step{step}'


def _scenario_name_func(testcase_func, param_num, param):
    return f'{testcase_func.__name__}_{param.args[1]}'


def _load_document(path: Path) -> kp.Document:
    document, errors = kp.loads(S.read_text(path))
    if errors:
        raise AssertionError(errors)
    return document


class TestAgnosticSamplesInventory(unittest.TestCase):

    def test_samples_dir_contains_only_expected_krn_files(self):
        self.assertEqual(
            {p.resolve() for p in S.expected_samples_krn_paths()},
            {p.resolve() for p in S.all_samples_krn_paths()},
        )

    def test_each_krn_loads_without_errors(self):
        for path in S.all_samples_krn_paths():
            with self.subTest(path=str(path)):
                _load_document(path)


class TestSemanticScenarioKernFixtures(unittest.TestCase):

    @parameterized.expand(S.SEMANTIC_SCENARIO_CASES, name_func=_scenario_name_func)
    def test_input_is_equal_semantic_columns(self, scenario_dir: Path, scenario_name: str):
        paths = S.scenario_paths(scenario_dir, scenario_name)
        input_krn = S.read_text(paths['input'])
        self.assertEqual(S.build_equal_semantic_multi_clef_kern(), input_krn)
        for line in input_krn.splitlines():
            if line.split('\t')[0].startswith('4'):
                self.assertEqual(1, len(set(line.split('\t'))))

    @parameterized.expand(S.SEMANTIC_SCENARIO_CASES, name_func=_scenario_name_func)
    def test_output_is_different_semantic_columns(self, scenario_dir: Path, scenario_name: str):
        paths = S.scenario_paths(scenario_dir, scenario_name)
        output_krn = S.read_text(paths['output'])
        self.assertEqual(S.build_different_semantic_multi_clef_kern(), output_krn)
        note_lines = [line for line in output_krn.splitlines() if line.split('\t')[0].startswith('4')]
        self.assertEqual(14, len(note_lines))
        for line in note_lines:
            self.assertGreater(len(set(line.split('\t'))), 1)

    @parameterized.expand(S.SEMANTIC_SCENARIO_CASES, name_func=_scenario_name_func)
    def test_output_agnostic_exports(self, scenario_dir: Path, scenario_name: str):
        paths = S.scenario_paths(scenario_dir, scenario_name)
        document = _load_document(paths['output'])
        extended, normalized, akern = S.dumps_agnostic_exports(document)
        self.assertIn(S.METER_SIGNATURE, extended)
        self.assertEqual(normalized, S.extended_export_to_akern(extended))
        self.assertEqual(normalized, akern)

    @parameterized.expand(S.SEMANTIC_SCENARIO_CASES, name_func=_scenario_name_func)
    def test_output_agnostic_columns_equal_per_row(self, scenario_dir: Path, scenario_name: str):
        paths = S.scenario_paths(scenario_dir, scenario_name)
        _, normalized, _ = S.dumps_agnostic_exports(_load_document(paths['output']))
        note_lines = S.agnostic_normalized_note_lines(normalized)
        self.assertEqual(14, len(note_lines))
        for line in note_lines:
            self.assertEqual(1, len(set(line.split('\t'))))

    @parameterized.expand(S.SEMANTIC_SCENARIO_CASES, name_func=_scenario_name_func)
    def test_input_agnostic_columns_differ_per_row(self, scenario_dir: Path, scenario_name: str):
        paths = S.scenario_paths(scenario_dir, scenario_name)
        _, normalized, _ = S.dumps_agnostic_exports(_load_document(paths['input']))
        note_lines = S.agnostic_normalized_note_lines(normalized)
        self.assertEqual(14, len(note_lines))
        for line in note_lines:
            self.assertGreater(len(set(line.split('\t'))), 1, msg=line)

    @parameterized.expand(S.SEMANTIC_SCENARIO_CASES, name_func=_scenario_name_func)
    def test_input_agnostic_extended_has_duration_prefix(self, scenario_dir: Path, scenario_name: str):
        paths = S.scenario_paths(scenario_dir, scenario_name)
        extended, _, _ = S.dumps_agnostic_exports(_load_document(paths['input']))
        for line in extended.splitlines():
            if line.split('\t')[0].startswith('4@'):
                for cell in line.split('\t'):
                    self.assertRegex(cell, r'^\d+@')

    @parameterized.expand(S.SEMANTIC_SCENARIO_CASES, name_func=_scenario_name_func)
    def test_output_staff_position_ts_equal_across_spines(self, scenario_dir: Path, scenario_name: str):
        expected_rows = S.equal_staff_position_ts_rows()
        self.assertEqual(14, len(expected_rows))
        for row_index, row in enumerate(expected_rows):
            columns = row.split('\t')
            self.assertEqual(len(S.CLEF_DATA), len(columns))
            self.assertEqual(1, len(set(columns)))
            self.assertEqual(S.FOURTEEN_TS_LADDER[row_index], columns[0])


class TestGraphicallyDifferentToEqual(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._paths = S.scenario_paths(S.DIR_GRAPHICALLY_DIFFERENT_TO_EQUAL, S.FROM_GRAPHICALLY_DIFFERENT_TO_EQUAL)

    def test_input_kern_is_equal_semantic_literals(self):
        self.assertEqual(S.build_graphically_different_input_kern(), S.read_text(self._paths['input']))

    def test_output_kern_is_staff_equivalent_columns(self):
        self.assertEqual(S.build_graphically_equal_output_kern(), S.read_text(self._paths['output']))

    def test_input_ts_differ_output_ts_equal_per_row(self):
        in_rows = S.staff_position_ts_rows_for_krn(S.read_text(self._paths['input']))
        out_rows = S.staff_position_ts_rows_for_krn(S.read_text(self._paths['output']))
        self.assertEqual(14, len(in_rows))
        self.assertTrue(S.graphical_rows_all_different(in_rows), msg=in_rows[0])
        self.assertTrue(S.graphical_rows_all_equal(out_rows), msg=out_rows[0])

    def test_input_agnostic_columns_differ_output_equal(self):
        _, in_norm, _ = S.dumps_agnostic_exports(_load_document(self._paths['input']))
        _, out_norm, _ = S.dumps_agnostic_exports(_load_document(self._paths['output']))
        for line in S.agnostic_normalized_note_lines(in_norm):
            self.assertGreater(len(set(line.split('\t'))), 1, msg=line)
        for line in S.agnostic_normalized_note_lines(out_norm):
            self.assertEqual(1, len(set(line.split('\t'))))


class TestGraphicallyEqualToDifferent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._paths = S.scenario_paths(S.DIR_GRAPHICALLY_EQUAL_TO_DIFFERENT, S.FROM_GRAPHICALLY_EQUAL_TO_DIFFERENT)

    def test_input_kern_is_staff_equivalent_columns(self):
        self.assertEqual(S.build_graphically_equal_output_kern(), S.read_text(self._paths['input']))

    def test_output_kern_is_equal_semantic_literals(self):
        self.assertEqual(S.build_graphically_different_input_kern(), S.read_text(self._paths['output']))

    def test_input_ts_equal_output_ts_differ_per_row(self):
        in_rows = S.staff_position_ts_rows_for_krn(S.read_text(self._paths['input']))
        out_rows = S.staff_position_ts_rows_for_krn(S.read_text(self._paths['output']))
        self.assertTrue(S.graphical_rows_all_equal(in_rows), msg=in_rows[0])
        self.assertTrue(S.graphical_rows_all_different(out_rows), msg=out_rows[0])

    def test_input_agnostic_columns_equal_output_differ(self):
        _, in_norm, _ = S.dumps_agnostic_exports(_load_document(self._paths['input']))
        _, out_norm, _ = S.dumps_agnostic_exports(_load_document(self._paths['output']))
        for line in S.agnostic_normalized_note_lines(in_norm):
            self.assertEqual(1, len(set(line.split('\t'))))
        for line in S.agnostic_normalized_note_lines(out_norm):
            self.assertGreater(len(set(line.split('\t'))), 1, msg=line)


class TestGraphicalScenarioOppositePair(unittest.TestCase):

    def test_opposite_pairs_use_swapped_kern(self):
        diff_to_eq = S.scenario_paths(S.DIR_GRAPHICALLY_DIFFERENT_TO_EQUAL, S.FROM_GRAPHICALLY_DIFFERENT_TO_EQUAL)
        eq_to_diff = S.scenario_paths(S.DIR_GRAPHICALLY_EQUAL_TO_DIFFERENT, S.FROM_GRAPHICALLY_EQUAL_TO_DIFFERENT)
        self.assertEqual(S.read_text(diff_to_eq['input']), S.read_text(eq_to_diff['output']))
        self.assertEqual(S.read_text(diff_to_eq['output']), S.read_text(eq_to_diff['input']))


class TestClefAgnosticPerClef(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._staff = kp.Staff()

    @parameterized.expand(S.DIFFERENT_SEMANTIC_OUTPUT_SCENARIO_CASES, name_func=_scenario_name_func)
    def test_fourteen_pitches_match_output_spine_columns(self, scenario_dir: Path, scenario_name: str):
        output_krn = S.read_text(S.scenario_krn_path(scenario_dir, scenario_name, 'output'))
        note_lines = [
            line for line in output_krn.splitlines()
            if line.split('\t')[0].startswith('4')
        ]
        for spine_index, (_slug, _token, clef_cls) in enumerate(S.CLEF_DATA):
            column = [line.split('\t')[spine_index] for line in note_lines]
            isolated = [f'4{pitch}' for pitch in S.fourteen_kern_pitches(clef_cls())]
            self.assertEqual(isolated, column)

    @parameterized.expand(S.CLEF_DATA, name_func=_clef_param_name_func)
    def test_clef_token_matches_factory(self, slug: str, clef_token: str, clef_cls: type):
        self.assertIsInstance(ClefFactory.create_clef(clef_token), clef_cls)

    @parameterized.expand(S.CLEF_DATA, name_func=_clef_param_name_func)
    def test_fourteen_staff_position_ts(self, slug: str, clef_token: str, clef_cls: type):
        kern_pitches = S.fourteen_kern_pitches(clef_cls())
        expected = S.fourteen_staff_position_ts(clef_cls())
        actual = S.staff_positions_for_kern_pitches(self._staff, clef_cls(), kern_pitches)
        self.assertEqual(expected, actual)


class TestClefStaffPositionTsEncoding(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._staff = kp.Staff()

    @parameterized.expand(
        [
            (slug, token, cls, step, ts)
            for slug, token, cls in S.CLEF_DATA
            for step, ts in enumerate(S.FOURTEEN_TS_LADDER)
        ],
        name_func=_clef_step_name_func,
    )
    def test_staff_position_ts_step(
        self, slug: str, clef_token: str, clef_cls: type, step: int, expected_ts: str,
    ):
        kern_pitches = S.fourteen_kern_pitches(clef_cls())
        pitch = kp.HumdrumPitchImporter().import_pitch(kern_pitches[step])
        self.assertEqual(expected_ts, GKernExporter(clef_cls()).export(self._staff, pitch))

    @parameterized.expand(
        [
            ('T@0', 'c'), ('S@0', 'd'), ('T@1', 'e'),
            ('S@3', 'cc'), ('T@4', 'dd'), ('S@-2', 'G'), ('T@-4', 'BB'),
        ],
    )
    def test_gkern_ts_token_to_g_clef_pitch(self, token: str, expected_kern: str):
        self.assertEqual(expected_kern, kp.gkern_to_g_clef_pitch(token))

    @parameterized.expand(['X@1', 'T@foo', 'bogus'])
    def test_gkern_ts_token_bad_inputs(self, bad_token: str):
        with self.assertRaises(ValueError):
            kp.gkern_to_g_clef_pitch(bad_token)


if __name__ == '__main__':
    unittest.main()
