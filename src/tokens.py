import string
from abc import ABC, abstractmethod
from enum import Enum, auto

TOKEN_SEPARATOR = '·'

# We don't use inheritance here for all elements but enum, because we don't need any polymorphism mechanism, just a grouping one
#TODO Poner todos los tipos - p.ej. también comandos de layout - slurs, etc...
class TokenCategory(Enum):
    STRUCTURAL = auto() # header, spine operations
    CORE = auto() # notes, rests, chords
    EMPTY = auto() # placeholders, null interpretation
    SIGNATURES = auto()
    OTHER_CONTEXTUAL = auto()
    BARLINES = auto()
    FIELD_COMMENTS = auto()
    DYNAMICS = auto()
    HARMONY = auto()
    FINGERING = auto()
    LYRICS = auto()
    OTHER = auto()

BEKERN_CATEGORIES = [TokenCategory.STRUCTURAL, TokenCategory.CORE, TokenCategory.EMPTY, TokenCategory.SIGNATURES, TokenCategory.BARLINES]

# TODO - de momento no lo usamos para filtrar
class SubTokenCategory(Enum):
    PITCH = auto()
    DURATION = auto()
    DECORATION = auto() # todo, tipos...

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

class HeaderToken(AbstractToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.STRUCTURAL)

    def export(self) -> string:
        extended_header = '**e' + self.encoding[2:] # remove the **, and append the e
        return extended_header

class SpineOperationToken(AbstractToken):
    def __init__(self, encoding):
        super().__init__(encoding, TokenCategory.STRUCTURAL)

    def export(self) -> string:
        return self.encoding

class Token(AbstractToken):
    def __init__(self, encoding, category):
        super().__init__(encoding, category)

class SimpleToken(Token):
    def __init__(self, encoding, category):
        super().__init__(encoding, category)

    def export(self) -> string:
        return self.encoding

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
