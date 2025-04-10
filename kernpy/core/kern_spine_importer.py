from __future__ import annotations

from typing import List

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy, \
    PredictionMode
from typing import Optional

from .base_antlr_importer import BaseANTLRListenerImporter
from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .error_listener import ErrorListener
from .generated.kernSpineLexer import kernSpineLexer
from .generated.kernSpineParser import kernSpineParser
from .spine_importer import SpineImporter
from .tokens import SimpleToken, TokenCategory, Subtoken, ChordToken, BoundingBox, \
    BoundingBoxToken, ClefToken, KeySignatureToken, TimeSignatureToken, MeterSymbolToken, BarToken, NoteRestToken, \
    KeyToken, InstrumentToken


class KernSpineListener(BaseANTLRSpineParserListener):

    def __init__(self):
        super().__init__()

class KernListenerImporter(BaseANTLRListenerImporter):

    def createListener(self):
        return KernSpineListener()

    def createLexer(self, charStream):
        return kernSpineLexer(charStream)

    def createParser(self, tokenStream):
        return kernSpineParser(tokenStream)

    def startRule(self):
        return self.parser.start()


class KernSpineImporter(SpineImporter):
    def __init__(self, verbose: Optional[bool] = False):
        """
        KernSpineImporter constructor.

        Args:
            verbose (Optional[bool]): Level of verbosity for error messages.
        """
        super().__init__(verbose=verbose)

    def import_listener(self) -> BaseANTLRSpineParserListener:
        return KernSpineListener()

    def import_token(self, encoding: str):
        self._raise_error_if_wrong_input(encoding)

        # self.listenerImporter = KernListenerImporter(token) # TODO ¿Por qué no va esto?
        # self.listenerImporter.start()
        lexer = kernSpineLexer(InputStream(encoding))
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)
        stream = CommonTokenStream(lexer)
        parser = kernSpineParser(stream)
        parser._interp.predictionMode = PredictionMode.SLL  # it improves a lot the parsing
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        parser.errHandler = BailErrorStrategy()
        tree = parser.start()
        walker = ParseTreeWalker()
        listener = KernSpineListener()
        walker.walk(listener, tree)
        if self.error_listener.getNumberErrorsFound() > 0:
            raise Exception(self.error_listener.errors)
        return listener.token
