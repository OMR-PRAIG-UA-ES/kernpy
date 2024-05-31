from abc import ABC, abstractmethod
from enum import Enum


pitches = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G'
]

Chromas = {
    'C--': 0,
    'C-': 1,
    'C': 2,
    'C+': 3,
    'C++': 4,
    'D---': 5,
    'D--': 6,
    'D-': 7,
    'D': 8,
    'D+': 9,
    'D++': 10,
    'E---': 11,
    'E--': 12,
    'E-': 13,
    'E': 14,
    'E+': 15,
    'E++': 16,
    'F--': 17,
    'F-': 18,
    'F': 19,
    'F+': 20,
    'F++': 21,
    # 22 is unused
    'G--': 23,
    'G-': 24,
    'G': 25,
    'G+': 26,
    'G++': 27,
    'A---': 28,
    'A--': 29,
    'A-': 30,
    'A': 31,
    'A+': 32,
    'A++': 33,
    'B---': 34,
    'B--': 35,
    'B-': 36,
    'B': 37,
    'B+': 38,
    'B++': 39
}

ChromasByValue = {v: k for k, v in Chromas.items()}  # reverse the key-value pairs


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


class NotationEncoding(Enum):
    AMERICAN = 'american'
    HUMDRUM = 'kern'

class Direction(Enum):
    UP = 'up'
    DOWN = 'down'


class AgnosticPitch:
    def __init__(self, name: str, octave: int):
        self.name = name
        self.octave = octave

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        accidentals = ''.join([c for c in name if c in ['-', '+']])
        name = name.upper()
        name = name.replace('#', '+').replace('b', '-')

        check_name = name.replace('+', '').replace('-', '')
        if check_name not in pitches:
            raise ValueError(f"Invalid pitch: {name}")
        if len(accidentals) > 3:
            raise ValueError(f"Invalid pitch: {name}. Maximum of 3 accidentals allowed. ")
        self.__name = name

    @property
    def octave(self):
        return self.__octave

    @octave.setter
    def octave(self, octave):
        if not isinstance(octave, int):
            raise ValueError(f"Invalid octave: {octave}")
        self.__octave = octave

    def get_chroma(self):
        return 40 * self.octave + Chromas[self.name]

    @classmethod
    def to_transposed(cls, agnostic_pitch: 'AgnosticPitch', raw_interval, direction: str = Direction.UP.value) -> 'AgnosticPitch':
        delta = raw_interval if direction == Direction.UP.value else -raw_interval
        chroma = agnostic_pitch.get_chroma() + delta
        name = ChromasByValue[chroma % 40]
        octave = chroma // 40
        return AgnosticPitch(name, octave)

    @classmethod
    def get_chroma_from_interval(cls, pitch_a: 'AgnosticPitch', pitch_b: 'AgnosticPitch'):
        return pitch_b.get_chroma() - pitch_a.get_chroma()

class PitchImporter(ABC):
    def __init__(self):
        self.octave = None
        self.name = None

    @abstractmethod
    def import_pitch(self, encoding: str) -> AgnosticPitch:
        pass

    @abstractmethod
    def _parse_pitch(self, pitch: str):
        pass

class HumdrumPitchImporter(PitchImporter):
    """
    Represents the pitch in the Humdrum Kern format.

    The name is represented using the International Standard Organization (ISO) name notation.
    The first line below the staff is the C4 in G clef. The above C is C5, the below C is C3, etc.

    The Humdrum Kern format uses the following name representation:
    'c' = C4
    'cc' = C5
    'ccc' = C6
    'cccc' = C7

    'C' = C3
    'CC' = C2
    'CCC' = C1

    This class do not limit the name ranges.

    In the following example, the name is represented by the letter 'c'. The name of 'c' is C4, 'cc' is C5, 'ccc' is C6.
    ```
    **kern
    *clefG2
    2c          // C4
    2cc         // C5
    2ccc        // C6
    2C          // C3
    2CC         // C2
    2CCC        // C1
    *-
    ```
    """
    C4_PITCH_LOWERCASE = 'c'
    C4_OCATAVE = 4
    C3_PITCH_UPPERCASE = 'C'
    C3_OCATAVE = 3
    VALID_PITCHES = 'abcdefg' + 'ABCDEFG'

    def __init__(self):
        super().__init__()

    def import_pitch(self, encoding: str) -> AgnosticPitch:
        self.name, self.octave = self._parse_pitch(encoding)
        return AgnosticPitch(self.name, self.octave)

    def _parse_pitch(self, encoding: str) -> tuple:
        accidentals = ''.join([c for c in encoding if c in ['#', '-']])
        accidentals = accidentals.replace('#', '+')
        encoding = encoding.replace('#', '').replace('-', '')
        pitch = encoding[0].lower()
        octave = None
        if encoding[0].islower():
            min_octave = HumdrumPitchImporter.C4_OCATAVE
            octave = min_octave + (len(encoding) - 1)
        elif encoding[0].isupper():
            max_octave = HumdrumPitchImporter.C3_OCATAVE
            octave = max_octave - (len(encoding) - 1)
        name = f"{pitch}{accidentals}"
        return name, octave


class AmericanPitchImporter(PitchImporter):
    def __init__(self):
        super().__init__()

    def import_pitch(self, encoding: str) -> AgnosticPitch:
        self.name, self.octave = self._parse_pitch(encoding)
        return AgnosticPitch(self.name, self.octave)

    def _parse_pitch(self, encoding: str):
        octave = int(''.join([n for n in encoding if n.isnumeric()]))
        chroma = ''.join([c.lower() for c in encoding if c.isalpha() or c in ['-', '+', '#', 'b']])

        return chroma, octave


class PitchImporterFactory:
    @classmethod
    def create(cls, encoding: str) -> PitchImporter:
        if encoding == NotationEncoding.AMERICAN.value:
            return AmericanPitchImporter()
        elif encoding == NotationEncoding.HUMDRUM.value:
            return HumdrumPitchImporter()
        else:
            raise ValueError(f"Invalid encoding: {encoding}. \nUse one of {NotationEncoding.__members__.values()}")


class PitchExporter(ABC):
    def __init__(self):
        self.pitch = None

    @abstractmethod
    def export_pitch(self, pitch: AgnosticPitch) -> str:
        pass

    def _is_valid_pitch(self):
        clean_pitch = ''.join([c for c in self.pitch.name if c.isalpha()])
        clean_pitch = clean_pitch.upper()
        if len(clean_pitch) > 1:
            clean_pitch = clean_pitch[0]
        return clean_pitch in pitches


class HumdrumPitchExporter(PitchExporter):
    C4_PITCH_LOWERCASE = 'c'
    C4_OCATAVE = 4
    C3_PITCH_UPPERCASE = 'C'
    C3_OCATAVE = 3

    def __init__(self):
        super().__init__()

    def export_pitch(self, pitch: AgnosticPitch) -> str:
        accidentals = ''.join([c for c in pitch.name if c in ['-', '+']])
        accidentals = accidentals.replace('+', '#')
        accidentals_output = len(accidentals) * accidentals[0] if len(accidentals) > 0 else ''
        pitch.name = pitch.name.replace('+', '').replace('-', '')

        if pitch.octave >= HumdrumPitchExporter.C4_OCATAVE:
            return f"{pitch.name.lower() * (pitch.octave - HumdrumPitchExporter.C4_OCATAVE + 1)}{accidentals_output}"
        else:
            return f"{pitch.name.upper() * (HumdrumPitchExporter.C3_OCATAVE - pitch.octave + 1)}{accidentals_output}"


class AmericanPitchExporter(PitchExporter):
    def __init__(self):
        super().__init__()

    def export_pitch(self, pitch: AgnosticPitch) -> str:
        self.pitch = pitch

        if not self._is_valid_pitch():
            raise ValueError(f"Invalid pitch: {self.pitch.name}")

        clean_name = ''.join([c for c in self.pitch.name if c.isalpha()])
        clean_name = clean_name.upper()
        accidentals = ''.join([c for c in self.pitch.name if c in ['-', '+']])
        total_accidentals = len(accidentals)
        accidentals_output = ''
        if total_accidentals > 0:
            accidentals_output = total_accidentals * '#' if accidentals == '+' else total_accidentals * 'b'
        return f"{clean_name}{accidentals_output}{self.pitch.octave}"


class PitchExporterFactory:
    @classmethod
    def create(cls, encoding: str) -> PitchExporter:
        if encoding == NotationEncoding.AMERICAN.value:
            return AmericanPitchExporter()
        elif encoding == NotationEncoding.HUMDRUM.value:
            return HumdrumPitchExporter()
        else:
            raise ValueError(f"Invalid encoding: {encoding}. \nUse one of {NotationEncoding.__members__.values()}")


def transpose(input_encoding: str, interval: int, format: str = NotationEncoding.HUMDRUM.value, direction: str = Direction.UP.value) -> str:
    """
    Transpose a pitch by a given interval.

    The pitch must be in the American notation.

    Args:
        input_encoding (str): The pitch to transpose.
        interval (int): The interval to transpose the pitch.
        format (str): The encoding format of the pitch. Default is HUMDRUM.
        direction (str): The direction of the transposition.'UP' or 'DOWN' Default is 'UP'.

    Returns:
        str: The transposed pitch.

    Examples:
        >>> transpose('ccc', IntervalsByName['P4'], format='kern')
        'fff'
        >>> transpose('ccc', IntervalsByName['P4'], format=NotationEncoding.HUMDRUM.value)
        'fff'
        >>> transpose('ccc', IntervalsByName['P4'], format='kern', direction='down')
        'gg'
        >>> transpose('ccc', IntervalsByName['P4'], format='kern', direction=Direction.DOWN.value)
        'gg'
        >>> transpose('ccc#', IntervalsByName['P4'])
        'fff#'
        >>> transpose('G4', IntervalsByName['m3'], format='american')
        'Bb4'
        >>> transpose('G4', IntervalsByName['m3'], format=NotationEncoding.AMERICAN.value)
        'Bb4'
        >>> transpose('C3', IntervalsByName['P4'], format='american', direction='down')
        'G2'


    """
    importer = PitchImporterFactory.create(format)
    pitch: AgnosticPitch = importer.import_pitch(input_encoding)
    transposed_pitch = AgnosticPitch.to_transposed(pitch, interval, direction)
    exporter = PitchExporterFactory.create(format)
    content = exporter.export_pitch(transposed_pitch)

    return content


