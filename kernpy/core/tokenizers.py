from __future__ import annotations

from copy import deepcopy
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Union, Set

from kernpy.core import DECORATION_SEPARATOR, Token, TOKEN_SEPARATOR


class Encoding(Enum):  # TODO: Eventually, polymorphism will be used to export different types of kern files
    """
    Options for exporting a kern file.

    Example:
        >>> import kernpy as kp
        >>> # Load a file
        >>> doc, _ = kp.load('path/to/file.krn')
        >>>
        >>> # Save the file using the specified encoding
        >>> exported_content = kp.dumps(tokenizer=kp.Encoding.normalizedKern)
    """
    eKern = 'ekern'
    normalizedKern = 'kern'
    bKern = 'bkern'
    bEkern = 'bekern'

    def prefix(self) -> str:
        """
        Get the prefix of the kern type.

        Returns (str): Prefix of the kern type.
        """
        if self == Encoding.eKern:
            return 'e'
        elif self == Encoding.normalizedKern:
            return ''
        elif self == Encoding.bKern:
            return 'b'
        elif self == Encoding.bEkern:
            return 'be'
        else:
            raise ValueError(f'Unknown kern type: {self}. '
                             f'Supported types are: '
                             f"{'-'.join([kern_type.name for kern_type in Encoding.__members__.values()])}")


class Tokenizer(ABC):
    """
    Tokenizer interface. All tokenizers must implement this interface.

    Tokenizers are responsible for converting a token into a string representation.
    """
    def __init__(self, *, token_categories: Set['TokenCategory']):
        """
        Create a new Tokenizer.

        Args:
            token_categories Set[TokenCategory]: List of categories to be tokenized.
                If None, an exception will be raised.
        """
        if token_categories is None:
            raise ValueError('Categories must be provided. Found None.')

        self.token_categories = token_categories


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
    def __init__(self, *, token_categories: Set['TokenCategory']):
        """
        Create a new KernTokenizer.

        Args:
            token_categories (Set[TokenCategory]): List of categories to be tokenized. If None will raise an exception.
        """
        super().__init__(token_categories=token_categories)

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
        return EkernTokenizer(token_categories=self.token_categories).tokenize(token).replace(TOKEN_SEPARATOR, '').replace(DECORATION_SEPARATOR, '')


class EkernTokenizer(Tokenizer):
    """
    EkernTokenizer converts a Token into an eKern (Extended **kern) string representation. This format use a '@' separator for the \
    main tokens and a '·' separator for the decorations tokens.
    """

    def __init__(self, *, token_categories: Set['TokenCategory']):
        """
        Create a new EkernTokenizer

        Args:
            token_categories (List[TokenCategory]): List of categories to be tokenized. If None will raise an exception.
        """
        super().__init__(token_categories=token_categories)

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
        return token.export(filter_categories=lambda cat: cat in self.token_categories)


class BekernTokenizer(Tokenizer):
    """
    BekernTokenizer converts a Token into a bekern (Basic Extended **kern) string representation. This format use a '@' separator for the \
    main tokens but discards all the decorations tokens.
    """

    def __init__(self, *, token_categories: Set['TokenCategory']):
        """
        Create a new BekernTokenizer

        Args:
            token_categories (Set[TokenCategory]): List of categories to be tokenized. If None will raise an exception.
        """
        super().__init__(token_categories=token_categories)

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
        ekern_content = token.export(filter_categories=lambda cat: cat in self.token_categories)

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

    def __init__(self, *, token_categories: Set['TokenCategory']):
        """
        Create a new BkernTokenizer

        Args:
            token_categories (Set[TokenCategory]): List of categories to be tokenized. If None will raise an exception.
        """
        super().__init__(token_categories=token_categories)


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
        return BekernTokenizer(token_categories=self.token_categories).tokenize(token).replace(TOKEN_SEPARATOR, '')


class TokenizerFactory:
    @classmethod
    def create(cls, type: str, *, token_categories: List['TokenCategory']) -> Tokenizer:
        if type is None:
            raise ValueError('A tokenization type must be provided. Found None.')

        if type == Encoding.normalizedKern.value:
            return KernTokenizer(token_categories=token_categories)
        elif type == Encoding.eKern.value:
            return EkernTokenizer(token_categories=token_categories)
        elif type == Encoding.bKern.value:
            return BekernTokenizer(token_categories=token_categories)
        elif type == Encoding.bEkern.value:
            return BkernTokenizer(token_categories=token_categories)

        raise ValueError(f"Unknown kern type: {type}. "
                         f"Supported types are: "
                         f"{'-'.join([kern_type.name for kern_type in Encoding.__members__.values()])}")
