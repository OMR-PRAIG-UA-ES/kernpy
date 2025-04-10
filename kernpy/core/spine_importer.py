from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy, \
    PredictionMode

from .generated.kernSpineLexer import kernSpineLexer
from .generated.kernSpineParser import kernSpineParser
from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .error_listener import ErrorListener
from .tokens import Token


class SpineImporter(ABC):
    def __init__(self, verbose: Optional[bool] = False):
        """
        SpineImporter constructor.
        This class is an abstract base class for importing all kinds of spines.

        Args:
            verbose (Optional[bool]): Level of verbosity for error messages.
        """
        self.import_listener = self.import_listener()
        self.error_listener = ErrorListener(verbose=verbose)

    @abstractmethod
    def import_listener(self) -> BaseANTLRSpineParserListener:
        pass

    @abstractmethod
    def import_token(self, encoding: str) -> Token:
        pass

    @classmethod
    def _raise_error_if_wrong_input(cls, encoding: str):
        if encoding is None:
            raise ValueError("Encoding cannot be None")
        if not isinstance(encoding, str):
            raise TypeError("Encoding must be a string")
        if encoding == '':
            raise ValueError("Encoding cannot be an empty string")


