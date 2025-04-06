from __future__ import annotations

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy, \
    PredictionMode

from .base_antlr_importer import BaseANTLRListenerImporter
from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .error_listener import ErrorListener
from .spine_importer import SpineImporter
from .generated.kernSpineLexer import kernSpineLexer
from .generated.kernSpineParser import kernSpineParser
from .tokens import TokenCategory, Token, SimpleToken


class RootSpineListener(BaseANTLRSpineParserListener):
    def __init__(self):
        super().__init__()


class RootListenerImporter(BaseANTLRListenerImporter):

    def createListener(self):
        return RootSpineListener()

    def createLexer(self, tokenStream):
        return kernSpineLexer(tokenStream)

    def createParser(self, tokenStream):
        return kernSpineParser(tokenStream)

    def startRule(self):
        return self.parser.start()


class RootSpineImporter(SpineImporter):
    def import_token(self, encoding: str) -> Token:
        if encoding is None:
            raise ValueError("Encoding cannot be None")
        if not isinstance(encoding, str):
            raise TypeError("Encoding must be a string")
        if encoding == '':
            raise ValueError("Encoding cannot be an empty string")

        return SimpleToken(encoding, TokenCategory.HARMONY)

        # TODO: fix this for loading measures!!
        error_listener = ErrorListener()

        # Lexer and Parser
        lexer = kernSpineLexer(InputStream(encoding))
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        stream = CommonTokenStream(lexer)
        parser = kernSpineParser(stream)
        parser._interp.predictionMode = PredictionMode.SLL  # it improves a lot the parsing
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        parser._errHandler = BailErrorStrategy()

        # Parse the input
        tree = parser.start()
        walker = ParseTreeWalker()
        listener = RootSpineListener()
        walker.walk(listener, tree)
        listener = RootSpineListener()
        walker.walk(listener, tree)

        if error_listener.getNumberErrorsFound() > 0:
            raise Exception(error_listener.errors)

        return listener.token

        #return SimpleToken(encoding, TokenCategory.HARMONY)
