from enum import Enum
from abc import ABC, abstractmethod

from kernpy.core import DECORATION_SEPARATOR, Token, TOKEN_SEPARATOR


class KernTypeExporter(Enum):  # TODO: Eventually, polymorphism will be used to export different types of kern files
    """
    Options for exporting a kern file.

    Examples:
        >>> import kernpy as kp
        >>> doc, err = kp.load('path/to/file.krn')
        >>> kp.dump(doc, 'path/to/file.krn', tokenizer=kp.KernTypeExporter.eKern)
        ...
        >>> kp.dump(doc, 'path/to/file.krn', tokenizer=kp.KernTypeExporter.normalizedKern)
        ...

        >>> KernTypeExporter.eKern.value
        'ekern'
        >>> KernTypeExporter.normalizedKern.value
        'kern'

    """
    eKern = 'ekern'
    normalizedKern = 'kern'
    bKern = 'bkern'
    bEkern = 'bekern'
    gKern = 'gkern'


class Tokenizer(ABC):
    """
    Tokenizer interface. All tokenizers must implement this interface.

    Tokenizers are responsible for converting a token into a string representation.
    """

    @abstractmethod
    def tokenize(self, token: Token) -> str:
        """
        Tokenize a token into a string representation.

        Args:
            token (Token): Token to be tokenized.

        Returns (str): Tokenized string representation.

        """
        pass


class KernTokenizer(Tokenizer):
    """
    KernTokenizer converts a Token into a normalized kern string representation.
    """

    def tokenize(self, token: Token) -> str:
        """
        Tokenize a token into a normalized kern string representation.
        This format is the classic Humdrum **kern representation.

        Args:
            token (Token): Token to be tokenized.

        Returns (str): Normalized kern string representation. This is the classic Humdrum **kern representation.

        Examples:
            >>> token.encoding
            '2@.@bb@-·_·L'
            >>> KernTokenizer().tokenize(token)
            '2.bb-_L'
        """
        return token.encoding


class EkernTokenizer(Tokenizer):
    """
    EkernTokenizer converts a Token into an eKern (Extended **kern) string representation. This format use a '@' separator for the \
    main tokens and a '·' separator for the decorations tokens.
    """

    def tokenize(self, token: Token) -> str:
        """
        Tokenize a token into an eKern string representation.
        Args:
            token (Token): Token to be tokenized.

        Returns (str): eKern string representation.

        Examples:
            >>> token.encoding
            '2@.@bb@-·_·L'
            >>> EkernTokenizer().tokenize(token)
            '2@.@bb@-·_·L'

        """
        return token.export()


class BekernTokenizer(Tokenizer):
    """
    BekernTokenizer converts a Token into a bekern (Basic Extended **kern) string representation. This format use a '@' separator for the \
    main tokens but discards all the decorations tokens.
    """

    def tokenize(self, token: Token) -> str:
        """
        Tokenize a token into a bekern string representation.
        Args:
            token (Token): Token to be tokenized.

        Returns (str): bekern string representation.

        Examples:
            >>> token.encoding
            '2@.@bb@-·_·L'
            >>> BekernTokenizer().tokenize(token)
            '2@.@bb@-'
        """
        ekern_content = token.export()

        if DECORATION_SEPARATOR not in ekern_content:
            return ekern_content

        reduced_content = ekern_content.split(DECORATION_SEPARATOR)[0]
        if reduced_content.endswith(TOKEN_SEPARATOR):
            reduced_content = reduced_content[:-1]

        return reduced_content


class BkernTokenizer(Tokenizer):
    """
    BkernTokenizer converts a Token into a bkern (Basic **kern) string representation. This format use \
    the main tokens but not the decorations tokens. This format is a lightweight version of the classic
    Humdrum **kern format.
    """

    def tokenize(self, token: Token) -> str:
        """
        Tokenize a token into a bkern string representation.
        Args:
            token (Token): Token to be tokenized.

        Returns (str): bkern string representation.

        Examples:
            >>> token.encoding
            '2@.@bb@-·_·L'
            >>> BkernTokenizer().tokenize(token)
            '2.bb-'
        """
        return BekernTokenizer().tokenize(token).replace(TOKEN_SEPARATOR, '')

class GkernTokenizer(Tokenizer):
    """
    GkernTokenizer converts a Token into a gkern (Graphic **kern) string representation. \
        This format use a non-semantic approach to represent the pitch in a **kern-based format. \
        The pitches are represented by a number depending on the line in the staff. \
    """

    def tokenize(self, token: Token) -> str:
        """
        Tokenize a token into a gkern string representation.
        Args:
            token (Token): Token to be tokenized.

        Returns (str): gkern string representation.

        Examples:
            >>> token.encoding
            '2@.@bb@-·_·L'
            >>> GkernTokenizer().tokenize(token)
            '2@.@4@-·_·L'
        """
        raise NotImplementedError('GkernTokenizer is not implemented yet.')


class TokenizerFactory:
    @classmethod
    def create(cls, type: str) -> Tokenizer:
        if type is None:
            raise ValueError('A tokenization type must be provided. Found None.')

        if type == KernTypeExporter.normalizedKern.value:
            return KernTokenizer()
        elif type == KernTypeExporter.eKern.value:
            return EkernTokenizer()
        elif type == KernTypeExporter.bKern.value:
            return BekernTokenizer()
        elif type == KernTypeExporter.bEkern.value:
            return BkernTokenizer()
        elif type == KernTypeExporter.gKern.value:
            return GkernTokenizer()

        raise ValueError(f"Unknown kern type: {type}. "
                         f"Supported types are: "
                         f"{'-'.join([kern_type.name for kern_type in KernTypeExporter.__members__.values()])}")
