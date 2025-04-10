from __future__ import annotations
from typing import Optional

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy, \
    PredictionMode

from .base_antlr_importer import BaseANTLRListenerImporter
from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .error_listener import ErrorListener
from .kern_spine_importer import KernSpineListener, KernSpineImporter
from .spine_importer import SpineImporter
from .generated.kernSpineLexer import kernSpineLexer
from .generated.kernSpineParser import kernSpineParser
from .tokens import TokenCategory, Token, SimpleToken


class RootSpineListener(BaseANTLRSpineParserListener):
    def __init__(self):
        super().__init__()


class RootListenerImporter(BaseANTLRListenerImporter):

    def createListener(self):
        return KernSpineListener()

    def createLexer(self, tokenStream):
        return kernSpineLexer(tokenStream)

    def createParser(self, tokenStream):
        return kernSpineParser(tokenStream)

    def startRule(self):
        return self.parser.start()


class RootSpineImporter(SpineImporter):
    def __init__(self, verbose: Optional[bool] = False):
        """
        KernSpineImporter constructor.

        Args:
            verbose (Optional[bool]): Level of verbosity for error messages.
        """
        super().__init__(verbose=verbose)

    def import_listener(self) -> BaseANTLRSpineParserListener:
        #return RootSpineListener() # TODO: Create a custom functional listener for RootSpineImporter
        return KernSpineListener()

    def import_token(self, encoding: str) -> Token:
        self._raise_error_if_wrong_input(encoding)

        kern_spine_importer = KernSpineImporter()
        token = kern_spine_importer.import_token(encoding)

        return token  # The **root spine tokens are always a subset of the **kern spine tokens

