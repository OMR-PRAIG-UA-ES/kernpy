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

}



class NotationEncoding(Enum):
    AMERICAN = 'american'
    HUMDRUM = 'kern'


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
    def to_transposed(cls, agnostic_pitch, interval) -> 'AgnosticPitch':
        chroma = agnostic_pitch.get_chroma() + interval
        octave = chroma // 40
        name = ChromasByValue[chroma % 40]
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
    def __init__(self):
        super().__init__()

    def import_pitch(self, encoding: str) -> AgnosticPitch:
        self.octave, self.name = self._parse_pitch(encoding)
        return AgnosticPitch(self.name, self.octave)

    def _parse_pitch(self, pitch: str):
        raise NotImplementedError


class AmericanPitchImporter(PitchImporter):
    def __init__(self):
        super().__init__()

    def import_pitch(self, encoding: str) -> AgnosticPitch:
        self.octave, self.name = self._parse_pitch(encoding)
        return AgnosticPitch(self.name, self.octave)

    def _parse_pitch(self, encoding: str):
        octave = int(''.join([n for n in encoding if n.isnumeric()]))
        chroma = ''.join([c.lower() for c in encoding if c.isalpha()])

        return octave, chroma


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
    def __init__(self):
        super().__init__()

    def export_pitch(self, pitch: AgnosticPitch) -> str:
        raise NotImplementedError


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


def transpose(input_encoding: str, interval: int, format: str = NotationEncoding.HUMDRUM.value) -> str:
    """
    Transpose a pitch by a given interval.

    The pitch must be in the American notation.

    Args:
        input_encoding (str): The pitch to transpose.
        interval (int): The interval to transpose the pitch.
        format (str): The encoding format of the pitch. Default is HUMDRUM.

    Returns:
        str: The transposed pitch.
    """
    importer = PitchImporterFactory.create(format)
    pitch: AgnosticPitch = importer.import_pitch(input_encoding)
    transposed_pitch = AgnosticPitch.to_transposed(pitch, interval)
    exporter = PitchExporterFactory.create(format)
    content = exporter.export_pitch(transposed_pitch)

    return content


