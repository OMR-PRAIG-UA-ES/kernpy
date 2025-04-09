from __future__ import annotations

from abc import ABC, abstractmethod

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy, \
    PredictionMode
from .generated.kernSpineLexer import kernSpineLexer
from .generated.kernSpineParser import kernSpineParser
from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .error_listener import ErrorListener
from .tokens import Token


class SpineImporter(ABC):
    def __init__(self):
        self.import_listener = self.import_listener()
        self.error_listener = ErrorListener()

    @abstractmethod
    def import_listener(self) -> BaseANTLRSpineParserListener:
        pass

    def import_token(self, encoding: str) -> Token:
        self._raise_error_if_wrong_input(encoding)

        # Set up lexer
        lexer = kernSpineLexer(InputStream(encoding))
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)

        # Set up parser
        stream = CommonTokenStream(lexer)
        parser = kernSpineParser(stream)
        parser._interp.predictionMode = PredictionMode.SLL
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        parser._errHandler = BailErrorStrategy()

        # Parse the input
        tree = parser.start()
        walker = ParseTreeWalker()
        walker.walk(self.import_listener, tree)

        # Return the token from the listener
        if self.error_listener.getNumberErrorsFound() > 0:
            raise Exception(self.error_listener.errors)

        return self.import_listener.token

    @classmethod
    def _raise_error_if_wrong_input(cls, encoding: str):
        if encoding is None:
            raise ValueError("Encoding cannot be None")
        if not isinstance(encoding, str):
            raise TypeError("Encoding must be a string")
        if encoding == '':
            raise ValueError("Encoding cannot be an empty string")


