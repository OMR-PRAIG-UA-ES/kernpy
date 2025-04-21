from __future__ import annotations

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

    transposed_pitch = AgnosticPitch.to_transposed(pitch, interval, direction)

    exporter = PitchExporterFactory.create(output_format)
    content = exporter.export_pitch(transposed_pitch)

    return content


