import string
from abc import ABC, abstractmethod
from enum import Enum, auto
import copy

TOKEN_SEPARATOR = '@'
DECORATION_SEPARATOR = '·'


# We don't use inheritance here for all elements but enum, because we don't need any polymorphism mechanism, just a grouping one
# TODO Poner todos los tipos - p.ej. también comandos de layout - slurs, etc...
class TokenCategory(Enum):
    """
    Options for the category of a token.

    This is used to determine what kind of token should be exported.
    """
    STRUCTURAL = auto()  # header, spine operations
    CORE = auto()  # notes, rests, chords
    EMPTY = auto()  # placeholders, null interpretation
    SIGNATURES = auto()
    ENGRAVED_SYMBOLS = auto()
    OTHER_CONTEXTUAL = auto()
    BARLINES = auto()
    FIELD_COMMENTS = auto()
    LINE_COMMENTS = auto()
    DYNAMICS = auto()
    HARMONY = auto()
    FINGERING = auto()
    LYRICS = auto()
    INSTRUMENTS = auto()
    BOUNDING_BOXES = auto()
    OTHER = auto()


# TODO - de momento no lo usamos para filtrar
class SubTokenCategory(Enum):
    PITCH = auto()
    DURATION = auto()
    DECORATION = auto()  # todo, tipos...


class PitchRest:
    """
    Represents a pitch or a rest in a note.

    The pitch is represented using the International Standard Organization (ISO) pitch notation.
    The first line below the staff is the C4 in G clef. The above C is C5, the below C is C3, etc.

    The Humdrum Kern format uses the following pitch representation:
    'c' = C4
    'cc' = C5
    'ccc' = C6
    'cccc' = C7

    'C' = C3
    'CC' = C2
    'CCC' = C1

    The rests are represented by the letter 'r'. The rests do not have pitch.

    This class do not limit the pitch ranges.


    In the following example, the pitch is represented by the letter 'c'. The pitch of 'c' is C4, 'cc' is C5, 'ccc' is C6.
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
    REST_CHARACTER = 'r'

    VALID_PITCHES = 'abcdefg' + 'ABCDEFG' + REST_CHARACTER

    def __init__(self, raw_pitch: str):
        """
        Create a new PitchRest object.

        Args:
            raw_pitch (str): pitch representation in Humdrum Kern format

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest = PitchRest('DDD')
        """
        if raw_pitch is None or len(raw_pitch) == 0:
            raise ValueError(f'Empty pitch: pitch can not be None or empty. But {raw_pitch} was provided.')

        self.encoding = raw_pitch
        self.pitch, self.octave = self.__parse_pitch_octave()

    def __parse_pitch_octave(self) -> (str, int):
        if self.encoding == PitchRest.REST_CHARACTER:
            return PitchRest.REST_CHARACTER, None

        if self.encoding.islower():
            min_octave = PitchRest.C4_OCATAVE
            octave = min_octave + (len(self.encoding) - 1)
            pitch = self.encoding[0].lower()
            return pitch, octave

        if self.encoding.isupper():
            max_octave = PitchRest.C3_OCATAVE
            octave = max_octave - (len(self.encoding) - 1)
            pitch = self.encoding[0].lower()
            return pitch, octave

        raise ValueError(f'Invalid pitch: pitch {self.encoding} is not a valid pitch representation.')

    def is_rest(self) -> bool:
        """
        Check if the pitch is a rest.

        Returns:
            bool: True if the pitch is a rest, False otherwise.

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest.is_rest()
            False
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest.is_rest()
            True
        """
        return self.octave is None

    @staticmethod
    def pitch_comparator(pitch_a: string, pitch_b: string) -> int:
        """
        Compare two pitches of the same octave.

        The lower pitch is 'a'. So 'a' < 'b' < 'c' < 'd' < 'e' < 'f' < 'g'

        Args:
            pitch_a: One pitch of 'abcdefg'
            pitch_b: Another pitch of 'abcdefg'

        Returns:
            -1 if pitch1 is lower than pitch2
            0 if pitch1 is equal to pitch2
            1 if pitch1 is higher than pitch2

        Examples:
            >>> PitchRest.pitch_comparator('c', 'c')
            0
            >>> PitchRest.pitch_comparator('c', 'd')
            -1
            >>> PitchRest.pitch_comparator('d', 'c')
            1
        """
        if pitch_a < pitch_b:
            return -1
        if pitch_a > pitch_b:
            return 1
        return 0

    def __str__(self):
        return f'{self.encoding}'

    def __repr__(self):
        return f'[PitchRest: {self.encoding}, pitch={self.pitch}, octave={self.octave}]'

    def __eq__(self, other):
        """
        Compare two pitches and rests.

        Args:
            other: The other pitch to compare

        Returns:
            True if the pitches are equal, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest == pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('ccc')
            >>> pitch_rest == pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest == pitch_rest2
            False
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest == pitch_rest2
            True

        """
        if not isinstance(other, PitchRest):
            return False
        if self.is_rest() and other.is_rest():
            return True
        if self.is_rest() or other.is_rest():
            return False
        return self.pitch == other.pitch and self.octave == other.octave

    def __ne__(self, other):
        """
        Compare two pitches and rests.
        Args:
            other: The other pitch to compare

        Returns:
            True if the pitches are different, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest != pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('ccc')
            >>> pitch_rest != pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest != pitch_rest2
            True
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest != pitch_rest2
            False
        """
        return not self.__eq__(other)

    def __gt__(self, other):
        """
        Compare two pitches.

        If any of the pitches is a rest, the comparison raise an exception.

        Args:
            other: The other pitch to compare

        Returns: True if this pitch is higher than the other, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('d')
            >>> pitch_rest > pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest > pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('b')
            >>> pitch_rest > pitch_rest2
            True
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest > pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest > pitch_rest2
            Traceback (most recent call last):
            ValueError: ...


        """
        if self.is_rest() or other.is_rest():
            raise ValueError(f'Invalid comparison: > operator can not be used to compare pitch of a rest.\n\
            self={repr(self)} > other={repr(other)}')

        if self.octave > other.octave:
            return True
        if self.octave == other.octave:
            return PitchRest.pitch_comparator(self.pitch, other.pitch) > 0
        return False

    def __lt__(self, other):
        """
        Compare two pitches.

        If any of the pitches is a rest, the comparison raise an exception.

        Args:
            other: The other pitch to compare

        Returns:
            True if this pitch is lower than the other, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('d')
            >>> pitch_rest < pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest < pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('b')
            >>> pitch_rest < pitch_rest2
            False
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest < pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest < pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...

        """
        if self.is_rest() or other.is_rest():
            raise ValueError(f'Invalid comparison: < operator can not be used to compare pitch of a rest.\n\
            self={repr(self)} < other={repr(other)}')

        if self.octave < other.octave:
            return True
        if self.octave == other.octave:
            return PitchRest.pitch_comparator(self.pitch, other.pitch) < 0
        return False

    def __ge__(self, other):
        """
        Compare two pitches. If any of the PitchRest is a rest, the comparison raise an exception.
        Args:
            other: The other pitch to compare

        Returns:
            True if this pitch is higher or equal than the other, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('d')
            >>> pitch_rest >= pitch_rest2
            False
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest >= pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('b')
            >>> pitch_rest >= pitch_rest2
            True
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest >= pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest >= pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...


        """
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        """
        Compare two pitches. If any of the PitchRest is a rest, the comparison raise an exception.
        Args:
            other: The other pitch to compare

        Returns: True if this pitch is lower or equal than the other, False otherwise

        Examples:
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('d')
            >>> pitch_rest <= pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest <= pitch_rest2
            True
            >>> pitch_rest = PitchRest('c')
            >>> pitch_rest2 = PitchRest('b')
            >>> pitch_rest <= pitch_rest2
            False
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('c')
            >>> pitch_rest <= pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...
            >>> pitch_rest = PitchRest('r')
            >>> pitch_rest2 = PitchRest('r')
            >>> pitch_rest <= pitch_rest2
            Traceback (most recent call last):
            ...
            ValueError: ...

        """
        return self.__lt__(other) or self.__eq__(other)


class Duration(ABC):
    """
    Represents the duration of a note or a rest.

    The duration is represented using the Humdrum Kern format.
    The duration is a number that represents the number of units of the duration.

    The duration of a whole note is 1, half note is 2, quarter note is 4, eighth note is 8, etc.

    The duration of a note is represented by a number. The duration of a rest is also represented by a number.

    This class do not limit the duration ranges.

    In the following example, the duration is represented by the number '2'.
    ```
    **kern
    *clefG2
    2c          // whole note
    4c          // half note
    8c          // quarter note
    16c         // eighth note
    *-
    ```
    """

    def __init__(self, raw_duration):
        self.encoding = str(raw_duration)

    @abstractmethod
    def modify(self, ratio: int):
        pass

    @abstractmethod
    def __deepcopy__(self, memo=None):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __ge__(self, other):
        pass

    @abstractmethod
    def __le__(self, other):
        pass

    @abstractmethod
    def __str__(self):
        pass


class DurationFactory:
    @staticmethod
    def create_duration(duration: str) -> Duration:
        return DurationClassical(int(duration))


class DurationMensural(Duration):
    """
    Represents the duration in mensural notation of a note or a rest.
    """

    def __init__(self, duration):
        super().__init__(duration)
        self.duration = duration

    def __eq__(self, other):
        raise NotImplementedError()

    def modify(self, ratio: int):
        raise NotImplementedError()

    def __deepcopy__(self, memo=None):
        raise NotImplementedError()

    def __gt__(self, other):
        raise NotImplementedError()

    def __lt__(self, other):
        raise NotImplementedError()

    def __le__(self, other):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __ge__(self, other):
        raise NotImplementedError()

    def __ne__(self, other):
        raise NotImplementedError()


class DurationClassical(Duration):
    """
    Represents the duration in classical notation of a note or a rest.
    """

    def __init__(self, duration: int):
        """
        Create a new Duration object.

        Args:
            raw_duration (str): duration representation in Humdrum Kern format

        Examples:
            >>> duration = DurationClassical(2)
            True
            >>> duration = DurationClassical(4)
            True
            >>> duration = DurationClassical(32)
            True
            >>> duration = DurationClassical(1)
            True
            >>> duration = DurationClassical(0)
            False
            >>> duration = DurationClassical(-2)
            False
            >>> duration = DurationClassical(3)
            False
            >>> duration = DurationClassical(7)
            False
        """
        super().__init__(duration)
        if not DurationClassical.__is_valid_duration(duration):
            raise ValueError(f'Bad duration: {duration} was provided.')

        self.duration = int(duration)

    def modify(self, ratio: int):
        """
        Modify the duration of a note or a rest of the current object.

        Args:
            ratio (int): The factor to modify the duration. The factor must be greater than 0.

        Returns:
            DurationClassical: The new duration object with the modified duration.

        Examples:
            >>> duration = DurationClassical(2)
            >>> new_duration = duration.modify(2)
            >>> new_duration.duration
            4
            >>> duration = DurationClassical(2)
            >>> new_duration = duration.modify(0)
            Traceback (most recent call last):
            ...
            ValueError: Invalid factor provided: 0. The factor must be greater than 0.
            >>> duration = DurationClassical(2)
            >>> new_duration = duration.modify(-2)
            Traceback (most recent call last):
            ...
            ValueError: Invalid factor provided: -2. The factor must be greater than 0.
        """
        if not isinstance(ratio, int):
            raise ValueError(f'Invalid factor provided: {ratio}. The factor must be an integer.')
        if ratio <= 0:
            raise ValueError(f'Invalid factor provided: {ratio}. The factor must be greater than 0.')

        return copy.deepcopy(DurationClassical(self.duration * ratio))

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}

        new_instance = DurationClassical(self.duration)
        new_instance.duration = self.duration
        return new_instance

    def __str__(self):
        return f'{self.duration}'

    def __eq__(self, other):
        """
        Compare two durations.

        Args:
            other: The other duration to compare

        Returns:
            True if the durations are equal, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(2)
            >>> duration == duration2
            True
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration == duration2
            False
        """
        if not isinstance(other, DurationClassical):
            return False
        return self.duration == other.duration

    def __ne__(self, other):
        """
        Compare two durations.

        Args:
            other: The other duration to compare

        Returns:
            True if the durations are different, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(2)
            >>> duration != duration2
            False
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration != duration2
            True
        """
        return not self.__eq__(other)

    def __gt__(self, other):
        """
        Compare two durations.

        Args:
            other: The other duration to compare

        Returns:
            True if this duration is higher than the other, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration > duration2
            False
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(2)
            >>> duration > duration2
            True
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(4)
            >>> duration > duration2
            False
        """
        if not isinstance(other, DurationClassical):
            raise ValueError(f'Invalid comparison: > operator can not be used to compare duration with {type(other)}')
        return self.duration > other.duration

    def __lt__(self, other):
        """
        Compare two durations.

        Args:
            other: The other duration to compare

        Returns:
            True if this duration is lower than the other, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration < duration2
            True
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(2)
            >>> duration < duration2
            False
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(4)
            >>> duration < duration2
            False
        """
        if not isinstance(other, DurationClassical):
            raise ValueError(f'Invalid comparison: < operator can not be used to compare duration with {type(other)}')
        return self.duration < other.duration

    def __ge__(self, other):
        """
        Compare two durations.

        Args:
            other: The other duration to compare

        Returns:
            True if this duration is higher or equal than the other, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration >= duration2
            False
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(2)
            >>> duration >= duration2
            True
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(4)
            >>> duration >= duration2
            True
        """
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        """
        Compare two durations.

        Args:
            other: The other duration to compare

        Returns:
            True if this duration is lower or equal than the other, False otherwise

        Examples:
            >>> duration = DurationClassical(2)
            >>> duration2 = DurationClassical(4)
            >>> duration <= duration2
            True
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(2)
            >>> duration <= duration2
            False
            >>> duration = DurationClassical(4)
            >>> duration2 = DurationClassical(4)
            >>> duration <= duration2
            True
        """
        return self.__lt__(other) or self.__eq__(other)

    @staticmethod
    def __is_valid_duration(duration: int) -> bool:
        try:
            duration = int(duration)
            if duration is None or duration <= 0:
                return False

            return duration > 0 and (duration % 2 == 0 or duration == 1)
        except ValueError:
            return False


class Subtoken:
    DECORATION = None

    def __init__(self, encoding, category):
        """
        :param encoding: The complete unprocessed encoding
        :param category: The subtoken category, one of SubTokenCategory
        """
        self.encoding = encoding
        self.category = category


class AbstractToken(ABC):
    def __init__(self, encoding, category):
        self.encoding = encoding
        self.category = category
        self.hidden = False

    @abstractmethod
    def export(self) -> string:
        pass


class ErrorToken(AbstractToken):
    """Used to wrap tokens that have not been parsed"""

    def __init__(self, encoding, line, error):
        super().__init__(encoding, TokenCategory.EMPTY)
        self.error = error
        self.line = line

    def export(self) -> string:
        return ''  # TODO Qué exportamos?

    def __str__(self):
        return f'Error token at line {self.line} with encoding "{self.encoding}": {self.error}'


class MetacommentToken(AbstractToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.LINE_COMMENTS)

    def export(self) -> string:
        return self.encoding


class InstrumentToken(AbstractToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.INSTRUMENTS)

    def export(self) -> string:
        return self.encoding


class FieldCommentToken(AbstractToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.FIELD_COMMENTS)

    def export(self) -> string:
        return self.encoding


class HeaderToken(AbstractToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.STRUCTURAL)

    def export(self) -> string:
        extended_header = '**e' + self.encoding[2:]  # remove the **, and append the e
        return extended_header


class SpineOperationToken(AbstractToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.STRUCTURAL)
        self.cancelled_at_stage = None

    def export(self) -> string:
        return self.encoding

    def is_cancelled_at(self, stage):
        if self.cancelled_at_stage is None:
            return False
        else:
            return self.cancelled_at_stage < stage


class Token(AbstractToken, ABC):
    def __init__(self, encoding, category):
        super().__init__(encoding, category)


class SimpleToken(Token):
    def __init__(self, encoding, category):
        super().__init__(encoding, category)

    def export(self) -> string:
        return self.encoding


class BarToken(SimpleToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.BARLINES)


class SignatureToken(SimpleToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.SIGNATURES)


class ClefToken(SignatureToken):
    def __init__(self, encoding):
        super().__init__(encoding)


class TimeSignatureToken(SignatureToken):
    def __init__(self, encoding):
        super().__init__(encoding)


class MeterSymbolToken(SignatureToken):
    def __init__(self, encoding):
        super().__init__(encoding)


class KeySignatureToken(SignatureToken):
    def __init__(self, encoding):
        super().__init__(encoding)


class KeyToken(SignatureToken):
    def __init__(self, encoding):
        super().__init__(encoding)


class CompoundToken(Token):
    def __init__(self, encoding, category, subtokens):
        """
        :param encoding: The complete unprocessed encoding
        :param category: The token category, one of TokenCategory
        :param subtokens: The individual elements of the token, of type Subtoken
        """
        super().__init__(encoding, category)
        self.subtokens = subtokens

    def export(self) -> string:
        result = ''
        for subtoken in self.subtokens:
            if len(result) > 0:
                result += TOKEN_SEPARATOR

            result += subtoken.encoding
        return result


class NoteRestToken(Token):
    def __init__(self, encoding, pitch_duration_subtokens, decoration_subtokens):
        """
        :param encoding: The complete unprocessed encoding
        :param category: The token category, one of TokenCategory
        :param subtokens: The individual elements of the token, of type Subtoken
        """
        super().__init__(encoding, TokenCategory.CORE)
        if not pitch_duration_subtokens or len(pitch_duration_subtokens) == 0:
            raise Exception('Empty pitch-duration subtokens')

        self.pitch_duration_subtokens = pitch_duration_subtokens
        self.decoration_subtokens = decoration_subtokens
        #self.duration = DurationClassical(''.join([subtoken for subtoken in decoration_subtokens if subtoken.isnumeric()]))
        duration_token = ''.join([n for n in self.encoding if n.isnumeric()])
        if duration_token is None or len(duration_token) == 0:
            self.duration = None
        else:
            self.duration = DurationFactory.create_duration(duration_token)

        pitch_rest_token = ''.join([n for n in self.encoding if n in PitchRest.VALID_PITCHES])
        if pitch_rest_token is None or len(pitch_rest_token) == 0:
            self.pitch = None
        else:
            self.pitch = PitchRest(pitch_rest_token)
        # TODO: Ahora entran muchos tokens diferentes, filtrar solo los de pitch

    def export(self) -> string:
        result = ''
        for subtoken in self.pitch_duration_subtokens:
            if len(result) > 0:
                result += TOKEN_SEPARATOR

            result += subtoken.encoding

        decorations = set()
        # we order them and avoid repetitions
        for subtoken in self.decoration_subtokens:
            decorations.add(subtoken)
        for decoration in sorted(decorations):
            result += DECORATION_SEPARATOR
            result += decoration
        return result


class ChordToken(SimpleToken):
    """
    It contains a list of compound tokens
    """

    def __init__(self, encoding, category, notes_tokens):
        super().__init__(encoding, category)
        self.notes_tokens = notes_tokens

    def export(self) -> string:
        result = ''
        for note_token in self.notes_tokens:
            if len(result) > 0:
                result += ' '

            result += note_token.export()

        return result


class BoundingBox:
    def __init__(self, x, y, w, h):
        self.from_x = x
        self.from_y = y
        self.to_x = x + w
        self.to_y = y + h

    def w(self):
        return self.to_x - self.from_x

    def h(self):
        return self.to_y - self.from_y

    def extend(self, bounding_box):
        self.from_x = min(self.from_x, bounding_box.from_x)
        self.from_y = min(self.from_y, bounding_box.from_y)
        self.to_x = max(self.to_x, bounding_box.to_x)
        self.to_y = max(self.to_y, bounding_box.to_y)

    def __str__(self):
        return f'(x={self.from_x}, y={self.from_y}, w={self.w()}, h={self.h()})'

    def xywh(self):
        return f'{self.from_x},{self.from_y},{self.w()},{self.h()}'


class BoundingBoxToken(AbstractToken):
    def __init__(self, encoding, page_number, bounding_box):
        super().__init__(encoding, TokenCategory.BOUNDING_BOXES)
        self.page_number = page_number
        self.bounding_box = bounding_box

    def export(self) -> string:
        return self.encoding


class MHXMToken(AbstractToken):
    def export(self) -> string:
        return self.encoding
