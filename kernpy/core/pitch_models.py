from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


pitches = {
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G'
}


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

class NotationEncoding(Enum):
    AMERICAN = 'american'
    HUMDRUM = 'kern'

class Direction(Enum):
    UP = 'up'
    DOWN = 'down'


class AgnosticPitch:
    """
    Represents a pitch in a generic way, independent of the notation system used.
    """

    ASCENDANT_ACCIDENTAL_ALTERATION = '+'
    DESCENDENT_ACCIDENTAL_ALTERATION = '-'
    ACCIDENTAL_ALTERATIONS = {
        ASCENDANT_ACCIDENTAL_ALTERATION,
        DESCENDENT_ACCIDENTAL_ALTERATION
    }


    def __init__(self, name: str, octave: int):
        """
        Initialize the AgnosticPitch object.

        Args:
            name (str): The name of the pitch (e.g., 'C', 'D#', 'Bb').
            octave (int): The octave of the pitch (e.g., 4 for middle C).
        """
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

    def accidentals(self):
        accidentals_encoding = ''
        for c in self.name:
            if c == self.ASCENDANT_ACCIDENTAL_ALTERATION:
                accidentals_encoding += '#'
            elif c == self.DESCENDENT_ACCIDENTAL_ALTERATION:
                accidentals_encoding += '-'

        return accidentals_encoding

    @classmethod
    def to_transposed(cls, agnostic_pitch: 'AgnosticPitch', raw_interval, direction: str = Direction.UP.value) -> 'AgnosticPitch':
        delta = raw_interval if direction == Direction.UP.value else - raw_interval
        chroma = agnostic_pitch.get_chroma() + delta
        name = ChromasByValue[chroma % 40]
        octave = chroma // 40
        return AgnosticPitch(name, octave)

    @classmethod
    def get_chroma_from_interval(cls, pitch_a: 'AgnosticPitch', pitch_b: 'AgnosticPitch'):
        return pitch_b.get_chroma() - pitch_a.get_chroma()

    def __str__(self):
        return f"<{self.name}, {self.octave}>"

    def __repr__(self):
        return f"{self.__name}(name={self.name}, octave={self.octave})"

    def __eq__(self, other):
        if not isinstance(other, AgnosticPitch):
            return False
        return self.name == other.name and self.octave == other.octave

    def __ne__(self, other):
        if not isinstance(other, AgnosticPitch):
            return True
        return self.name != other.name or self.octave != other.octave

    def __hash__(self):
        return hash((self.name, self.octave))

    def __lt__(self, other):
        if not isinstance(other, AgnosticPitch):
            return NotImplemented
        if self.octave == other.octave:
            return Chromas[self.name] < Chromas[other.name]
        return self.octave < other.octave

    def __gt__(self, other):
        if not isinstance(other, AgnosticPitch):
            return NotImplemented
        if self.octave == other.octave:
            return Chromas[self.name] > Chromas[other.name]
        return self.octave > other.octave



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

_HUMDRUM_PITCH_LETTERS = 'abcdefgABCDEFG'
_PITCH_CLASSES = 'abcdefg'


def split_kern_pitch_encoding(encoding: str) -> tuple[str, str, bool]:
    """
    Split a Humdrum pitch+alteration encoding into pitch letters, written accidental, and hide flag.

    Returns:
        tuple[str, str, bool]: ``(pitch_letters, written_accidental, is_hidden)`` where
        ``written_accidental`` is ``''``, ``'n'``, or one or more ``#`` / ``-`` as encoded
        on the token (before key/measure display logic). Hidden ``y``/``yy`` clears the written glyph.
    """
    pitch_letters = ''.join(c for c in encoding if c in _HUMDRUM_PITCH_LETTERS)
    if not pitch_letters:
        raise ValueError(f"Invalid pitch encoding: {encoding!r}")

    sharp_count = encoding.count('#')
    flat_count = encoding.count('-')
    has_natural = 'n' in encoding

    remainder = encoding
    for c in pitch_letters:
        remainder = remainder.replace(c, '', 1)
    remainder = remainder.replace('#', '').replace('-', '').replace('n', '')
    is_hidden = 'y' in remainder.lower()

    if is_hidden:
        written_accidental = ''
    elif sharp_count:
        written_accidental = '#' * sharp_count
    elif flat_count:
        written_accidental = '-' * flat_count
    elif has_natural:
        written_accidental = 'n'
    else:
        written_accidental = ''

    return pitch_letters, written_accidental, is_hidden


def kern_pitch_sounding_accidental(encoding: str) -> str:
    """
    Absolute Humdrum pitch alteration: ``#``/``-`` runs, or ``''`` for natural (bare or ``n``).

    Key signatures do not affect Humdrum pitch tokens; bare ``b`` is always B natural.
    """
    sharp_count = encoding.count('#')
    flat_count = encoding.count('-')
    if sharp_count:
        return '#' * sharp_count
    if flat_count:
        return '-' * flat_count
    return ''


def parse_key_signature_accidentals(encoding: str) -> dict[str, str]:
    """
    Parse ``*k[f#c#]`` / ``*k[b-e-a-]`` / ``*k[]`` into pitch-class → accidental map.

    Accidental values are ``'#'``, ``'-'``, or longer runs (``'##'``, ``'--'``, ...).
    Pitch classes absent from the key are omitted (treated as natural).

    Args:
        encoding (str): The encoding of the key signature.

    Returns:
        dict[str, str]: A dictionary of pitch-class -> accidental map.

    Examples:
        >>> parse_key_signature_accidentals('*k[f#c#]')
        {'f': '#', 'c': '#'}
        >>> parse_key_signature_accidentals('*k[b-e-a-]')
        {'b': '-', 'e': '-', 'a': '-'}
        >>> parse_key_signature_accidentals('*k[]')
        {}
        >>> parse_key_signature_accidentals('random string')
        {}
    """
    start = encoding.find('[')
    end = encoding.find(']', start + 1) if start >= 0 else -1
    if start < 0 or end < 0:  # if no key signature, return empty dictionary. treat as natural ("C major" so so..)
        return {}

    body = encoding[start + 1:end]
    result: dict[str, str] = {}
    index = 0
    while index < len(body):
        char = body[index]
        if char in _PITCH_CLASSES:
            letter = char
            index += 1
            accidental = ''
            while index < len(body) and body[index] in '#-':
                accidental += body[index]
                index += 1
            result[letter] = accidental
        else:
            index += 1
    return result


def kern_pitch_octave(pitch_letters: str) -> int:
    """Humdrum octave from pitch-letter run (``c``/``cc``/``C``/``CC``...)."""
    if not pitch_letters:
        raise ValueError('pitch_letters must be non-empty')
    extra = len(pitch_letters[1:])
    if pitch_letters[0].islower():
        return HumdrumPitchImporter.C4_OCATAVE + extra
    if pitch_letters[0].isupper():
        return HumdrumPitchImporter.C3_OCATAVE - extra
    raise ValueError(f'Invalid pitch letters: {pitch_letters!r}')


class AccidentalDisplayState:
    """
    Score-visible accidental state for agnostic export.

    Humdrum pitches are absolute. Display follows common notation:
    - key signature sets the default alteration for every octave of a pitch class
    - a written accidental applies only to later notes of the same pitch and octave
      until changed or the barline
    - barlines clear measure overrides (defaults fall back to the key again)
    """

    def __init__(self) -> None:
        self.key: dict[str, str] = {}
        # (pitch_class, octave) -> sounding accidental after a note in this measure
        self.measure_overrides: dict[tuple[str, int], str] = {}

    def set_key_signature(self, encoding: str) -> None:
        self.key = parse_key_signature_accidentals(encoding)
        self.reset_measure()

    def reset_measure(self) -> None:
        self.measure_overrides = {}

    def _current_for(self, pitch_class: str, octave: int) -> str:
        key = (pitch_class, octave)
        if key in self.measure_overrides:
            return self.measure_overrides[key]
        return self.key.get(pitch_class, '')

    def display_accidental(self, pitch_subtoken: str) -> str:
        """
        Return the accidental glyph to show on this note (``''``, ``'n'``, ``'#'``, ``'-'``, ...),
        then update measure state for that pitch+octave.
        """
        pitch_letters, _written, is_hidden = split_kern_pitch_encoding(pitch_subtoken)
        pitch_class = pitch_letters[0].lower()
        octave = kern_pitch_octave(pitch_letters)
        sounding = kern_pitch_sounding_accidental(pitch_subtoken)
        current = self._current_for(pitch_class, octave)

        if sounding == current:
            to_show = ''
        elif sounding == '':
            to_show = 'n'
        else:
            to_show = sounding

        if is_hidden:
            to_show = ''

        self.measure_overrides[(pitch_class, octave)] = sounding
        return to_show


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
    VALID_PITCHES = _HUMDRUM_PITCH_LETTERS

    def __init__(self):
        super().__init__()

    def import_pitch(self, encoding: str) -> AgnosticPitch:
        self.name, self.octave = self._parse_pitch(encoding)
        return AgnosticPitch(self.name, self.octave)

    def _parse_pitch(self, encoding: str) -> tuple:
        pitch_letters, _written, _is_hidden = split_kern_pitch_encoding(encoding)
        # Absolute Humdrum alteration for chroma; naturals do not alter AgnosticPitch name.
        chroma_accidentals = kern_pitch_sounding_accidental(encoding).replace('#', '+')
        pitch = pitch_letters[0].lower()
        octave = kern_pitch_octave(pitch_letters)
        name = f"{pitch}{chroma_accidentals}"
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
