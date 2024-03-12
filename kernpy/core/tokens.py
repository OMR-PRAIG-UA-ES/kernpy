import string
from abc import ABC, abstractmethod
from enum import Enum, auto

TOKEN_SEPARATOR = '·'


# We don't use inheritance here for all elements but enum, because we don't need any polymorphism mechanism, just a grouping one
# TODO Poner todos los tipos - p.ej. también comandos de layout - slurs, etc...
class TokenCategory(Enum):
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


BEKERN_CATEGORIES = [TokenCategory.STRUCTURAL, TokenCategory.CORE, TokenCategory.EMPTY, TokenCategory.SIGNATURES,
                     TokenCategory.BARLINES, TokenCategory.ENGRAVED_SYMBOLS]


# TODO - de momento no lo usamos para filtrar
class SubTokenCategory(Enum):
    PITCH = auto()
    DURATION = auto()
    DECORATION = auto()  # todo, tipos...


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

    def export(self) -> string:
        return self.encoding


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


class ClefToken(SimpleToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.SIGNATURES)


class TimeSignatureToken(SimpleToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.SIGNATURES)


class MeterSymbolToken(SimpleToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.SIGNATURES)


class KeySignatureToken(SimpleToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.SIGNATURES)


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
