#!/usr/bin/env python3
"""Regenerate clef agnostic sample **kern files under this directory.

Run from repository root:
    uv run python test/resources/agnostic/samples/generate_fixtures.py
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from test.test_clef_agnostic_samples import ClefAgnosticSamples

S = ClefAgnosticSamples

OLD_ALL_CLEFS = S.SAMPLES_DIR / 'all_clefs_14_pitches'
PER_CLEF_SLUGS = [slug for slug, _, _ in S.CLEF_DATA]

SCENARIO_DIRS = (
    S.DIR_DIFFERENT_SEMANTIC_TO_EQUAL,
    S.DIR_DIFFERENT_SEMANTIC_TO_EQUAL_2,
    S.DIR_EQUAL_SEMANTIC_TO_DIFFERENT,
    S.DIR_GRAPHICALLY_DIFFERENT_TO_EQUAL,
    S.DIR_GRAPHICALLY_EQUAL_TO_DIFFERENT,
)


def _remove_aux_files() -> None:
    for scenario_dir in SCENARIO_DIRS:
        if not scenario_dir.exists():
            continue
        S.migrate_legacy_krn_names(scenario_dir)
        for path in scenario_dir.iterdir():
            if path.suffix != '.krn':
                path.unlink()


def _assert_graphical_bundles() -> None:
    diff_in = S.build_graphically_different_input_kern()
    eq_out = S.build_graphically_equal_output_kern()
    in_rows = S.staff_position_ts_rows_for_krn(diff_in)
    out_rows = S.staff_position_ts_rows_for_krn(eq_out)
    if not S.graphical_rows_all_different(in_rows):
        raise RuntimeError('graphically-different input must have distinct T/S per row')
    if not S.graphical_rows_all_equal(out_rows):
        raise RuntimeError('graphically-equal output must have identical T/S per row')

    eq_in = S.build_graphically_equal_output_kern()
    diff_out = S.build_graphically_different_input_kern()
    if not S.graphical_rows_all_equal(S.staff_position_ts_rows_for_krn(eq_in)):
        raise RuntimeError('graphically-equal input must have identical T/S per row')
    if not S.graphical_rows_all_different(S.staff_position_ts_rows_for_krn(diff_out)):
        raise RuntimeError('graphically-different output must have distinct T/S per row')


def main() -> None:
    equal_semantic = S.build_equal_semantic_multi_clef_kern()
    different_semantic = S.build_different_semantic_multi_clef_kern()

    _assert_graphical_bundles()

    for scenario_dir, scenario_name in (
        (S.DIR_DIFFERENT_SEMANTIC_TO_EQUAL, S.FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC),
        (S.DIR_DIFFERENT_SEMANTIC_TO_EQUAL_2, S.FROM_DIFFERENT_SEMANTIC_TO_EQUAL_AGNOSTIC_2),
    ):
        S.write_scenario_bundle(
            scenario_dir,
            scenario_name,
            input_krn=equal_semantic,
            output_krn=different_semantic,
        )

    S.write_scenario_bundle(
        S.DIR_EQUAL_SEMANTIC_TO_DIFFERENT,
        S.FROM_EQUAL_SEMANTIC_TO_DIFFERENT_AGNOSTIC,
        input_krn=equal_semantic,
        output_krn=different_semantic,
    )

    S.write_scenario_bundle(
        S.DIR_GRAPHICALLY_DIFFERENT_TO_EQUAL,
        S.FROM_GRAPHICALLY_DIFFERENT_TO_EQUAL,
        input_krn=S.build_graphically_different_input_kern(),
        output_krn=S.build_graphically_equal_output_kern(),
    )

    S.write_scenario_bundle(
        S.DIR_GRAPHICALLY_EQUAL_TO_DIFFERENT,
        S.FROM_GRAPHICALLY_EQUAL_TO_DIFFERENT,
        input_krn=S.build_graphically_equal_output_kern(),
        output_krn=S.build_graphically_different_input_kern(),
    )

    if OLD_ALL_CLEFS.exists():
        shutil.rmtree(OLD_ALL_CLEFS)

    _remove_aux_files()

    for slug in PER_CLEF_SLUGS:
        per_clef = S.SAMPLES_DIR / slug
        if per_clef.exists():
            shutil.rmtree(per_clef)

    print(f'Wrote scenarios under {S.SAMPLES_DIR}')


if __name__ == '__main__':
    main()
