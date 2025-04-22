from __future__ import annotations

from copy import deepcopy
from typing import Optional

from .pitch_models import (
    NotationEncoding,
    AgnosticPitch,
    PitchExporterFactory,
    PitchImporterFactory,
    Direction,
)


Intervals = {
    -2: 'dd1',
    -1: 'd1',
    0: 'P1',
    1: 'A1',
    2: 'AA1',
    3: 'dd2',
    4: 'd2',
    5: 'm2',
    6: 'M2',
    7: 'A2',
    8: 'AA2',
    9: 'dd3',
    10: 'd3',
    11: 'm3',
    12: 'M3',
    13: 'A3',
    14: 'AA3',
    15: 'dd4',
    16: 'd4',
    17: 'P4',
    18: 'A4',
    19: 'AA4',
    21: 'dd5',
    # 20 is unused
    22: 'd5',
    23: 'P5',
    24: 'A5',
    25: 'AA5',
    26: 'dd6',
    27: 'd6',
    28: 'm6',
    29: 'M6',
    30: 'A6',
    31: 'AA6',
    32: 'dd7',
    33: 'd7',
    34: 'm7',
    35: 'M7',
    36: 'A7',
    37: 'AA7',
    40: 'octave'
}
"""
Base-40 interval classes (d=diminished, m=minor, M=major, P=perfect, A=augmented)
"""

IntervalsByName = {v: k for k, v in Intervals.items()}  # reverse the key-value pairs
AVAILABLE_INTERVALS = sorted(IntervalsByName.keys())

LETTER_TO_SEMITONES = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11,
}


def transpose_agnostics(
        input_pitch: AgnosticPitch,
        interval: int,
        direction: str = Direction.UP.value
) -> AgnosticPitch:
    """
    Transpose an AgnosticPitch by a given interval.

    Args:
        input_pitch (AgnosticPitch): The pitch to transpose.
        interval (int): The interval to transpose the pitch.
        direction (str): The direction of the transposition. 'UP' or 'DOWN'. Default is 'UP'.

    Returns :
        AgnosticPitch: The transposed pitch.

    Examples:
        >>> transpose_agnostics(AgnosticPitch('C', 4), IntervalsByName['P4'])
        AgnosticPitch('F', 4)
        >>> transpose_agnostics(AgnosticPitch('C', 4), IntervalsByName['P4'], direction='down')
        AgnosticPitch('G', 3)
        >>> transpose_agnostics(AgnosticPitch('C#', 4), IntervalsByName['P4'])
        AgnosticPitch('F#', 4)
        >>> transpose_agnostics(AgnosticPitch('G', 4), IntervalsByName['m3'], direction='down')
        AgnosticPitch('Bb', 4)

    """
    return AgnosticPitch.to_transposed(input_pitch, interval, direction)


def transpose_encoding_to_agnostic(
        input_encoding: str,
        interval: int,
        input_format: str = NotationEncoding.HUMDRUM.value,
        direction: str = Direction.UP.value
) -> AgnosticPitch:
    """
    Transpose a pitch by a given interval.

    The pitch must be in the American notation.

    Args:
        input_encoding (str): The pitch to transpose.
        interval (int): The interval to transpose the pitch.
        input_format (str): The encoding format of the pitch. Default is HUMDRUM.
        direction (str): The direction of the transposition.'UP' or 'DOWN' Default is 'UP'.

    Returns:
        AgnosticPitch: The transposed pitch.

    Examples:
        >>> transpose_encoding_to_agnostic('ccc', IntervalsByName['P4'], input_format='kern')
        AgnosticPitch('fff', 4)
        >>> transpose_encoding_to_agnostic('ccc', IntervalsByName['P4'], input_format=NotationEncoding.HUMDRUM.value)
        AgnosticPitch('fff', 4)
        >>> transpose_encoding_to_agnostic('ccc', IntervalsByName['P4'], input_format='kern', direction='down')
        AgnosticPitch('gg', 3)
        >>> transpose_encoding_to_agnostic('ccc#', IntervalsByName['P4'])
        AgnosticPitch('fff#', 4)
        >>> transpose_encoding_to_agnostic('G4', IntervalsByName['m3'], input_format='american')
        AgnosticPitch('Bb4', 4)
        >>> transpose_encoding_to_agnostic('C3', IntervalsByName['P4'], input_format='american', direction='down')
        AgnosticPitch('G2', 2)

    """
    importer = PitchImporterFactory.create(input_format)
    pitch: AgnosticPitch = importer.import_pitch(input_encoding)

    return transpose_agnostics(pitch, interval, direction=direction)


def transpose_agnostic_to_encoding(
        agnostic_pitch: AgnosticPitch,
        interval: int,
        output_format: str = NotationEncoding.HUMDRUM.value,
        direction: str = Direction.UP.value
) -> str:
    """
    Transpose an AgnosticPitch by a given interval.

    Args:
        agnostic_pitch (AgnosticPitch): The pitch to transpose.
        interval (int): The interval to transpose the pitch.
        output_format (Optional[str]): The encoding format of the transposed pitch. Default is HUMDRUM.
        direction (Optional[str]): The direction of the transposition.'UP' or 'DOWN' Default is 'UP'.

    Returns (str):
        str: The transposed pitch.

    Examples:
        >>> transpose_agnostic_to_encoding(AgnosticPitch('C', 4), IntervalsByName['P4'])
        'F4'
        >>> transpose_agnostic_to_encoding(AgnosticPitch('C', 4), IntervalsByName['P4'], direction='down')
        'G3'
        >>> transpose_agnostic_to_encoding(AgnosticPitch('C#', 4), IntervalsByName['P4'])
        'F#4'
        >>> transpose_agnostic_to_encoding(AgnosticPitch('G', 4), IntervalsByName['m3'], direction='down')
        'Bb4'
    """
    exporter = PitchExporterFactory.create(output_format)
    transposed_pitch = transpose_agnostics(agnostic_pitch, interval, direction=direction)
    content = exporter.export_pitch(transposed_pitch)

    return content





def transpose(
        input_encoding: str,
        interval: int,
        input_format: str = NotationEncoding.HUMDRUM.value,
        output_format: str = NotationEncoding.HUMDRUM.value,
        direction: str = Direction.UP.value
) -> str:
    """
    Transpose a pitch by a given interval.

    The pitch must be in the American notation.

    Args:
        input_encoding (str): The pitch to transpose.
        interval (int): The interval to transpose the pitch.
        input_format (str): The encoding format of the pitch. Default is HUMDRUM.
        output_format (str): The encoding format of the transposed pitch. Default is HUMDRUM.
        direction (str): The direction of the transposition.'UP' or 'DOWN' Default is 'UP'.

    Returns:
        str: The transposed pitch.

    Examples:
        >>> transpose('ccc', IntervalsByName['P4'], input_format='kern', output_format='kern')
        'fff'
        >>> transpose('ccc', IntervalsByName['P4'], input_format=NotationEncoding.HUMDRUM.value)
        'fff'
        >>> transpose('ccc', IntervalsByName['P4'], input_format='kern', direction='down')
        'gg'
        >>> transpose('ccc', IntervalsByName['P4'], input_format='kern', direction=Direction.DOWN.value)
        'gg'
        >>> transpose('ccc#', IntervalsByName['P4'])
        'fff#'
        >>> transpose('G4', IntervalsByName['m3'], input_format='american')
        'Bb4'
        >>> transpose('G4', IntervalsByName['m3'], input_format=NotationEncoding.AMERICAN.value)
        'Bb4'
        >>> transpose('C3', IntervalsByName['P4'], input_format='american', direction='down')
        'G2'


    """
    importer = PitchImporterFactory.create(input_format)
    pitch: AgnosticPitch = importer.import_pitch(input_encoding)

    transposed_pitch = transpose_agnostics(pitch, interval, direction=direction)

    exporter = PitchExporterFactory.create(output_format)
    content = exporter.export_pitch(transposed_pitch)

    return content


def agnostic_distance(
    first_pitch: AgnosticPitch,
    second_pitch: AgnosticPitch,
) -> int:
    """
    Calculate the distance in semitones between two pitches.

    Args:
        first_pitch (AgnosticPitch): The first pitch to compare.
        second_pitch (AgnosticPitch): The second pitch to compare.

    Returns:
        int: The distance in semitones between the two pitches.

    Examples:
        >>> agnostic_distance(AgnosticPitch('C4'), AgnosticPitch('E4'))
        4
        >>> agnostic_distance(AgnosticPitch('C4'), AgnosticPitch('B3'))
        -1
    """
    def semitone_index(p: AgnosticPitch) -> int:
        # base letter:
        letter = p.name.replace('+', '').replace('-', '')
        base = LETTER_TO_SEMITONES[letter]
        # accidentals: '+' is one sharp, '-' one flat
        alteration = p.name.count('+') - p.name.count('-')
        return p.octave * 12 + base + alteration

    return semitone_index(second_pitch) - semitone_index(first_pitch)


def distance(
    first_encoding: str,
    second_encoding: str,
    *,
    first_format: str = NotationEncoding.HUMDRUM.value,
    second_format: str = NotationEncoding.HUMDRUM.value,
) -> int:
    """
    Calculate the distance in semitones between two pitches.

    Args:
        first_encoding (str): The first pitch to compare.
        second_encoding (str): The second pitch to compare.
        first_format (str): The encoding format of the first pitch. Default is HUMDRUM.
        second_format (str): The encoding format of the second pitch. Default is HUMDRUM.

    Returns:
        int: The distance in semitones between the two pitches.

    Examples:
        >>> distance('C4', 'E4')
        4
        >>> distance('C4', 'B3')
        -1
    """
    first_importer = PitchImporterFactory.create(first_format)
    first_pitch: AgnosticPitch = first_importer.import_pitch(first_encoding)

    second_importer = PitchImporterFactory.create(second_format)
    second_pitch: AgnosticPitch = second_importer.import_pitch(second_encoding)

    return agnostic_distance(first_pitch, second_pitch)
