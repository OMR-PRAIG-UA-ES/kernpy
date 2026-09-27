from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy, \
    PredictionMode
from antlr4.error.Errors import ParseCancellationException

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

    def _parse(self, encoding: str, lexer_class, parser_class, start_rule: str):
        """
        Parse one spine cell with the standard two-stage ANTLR strategy: the fast SLL prediction first,
        and only if it fails the full LL prediction, which is the one that decides.

        SLL alone rejects some valid cells: Humdrum does not fix the order of the signifiers in a token,
        so the note and rest rules need more context than SLL keeps to tell e.g. a rest with a position
        (`24rg`) from a chord. A cell LL also rejects is reported as before.

        Args:
            encoding (str): The spine cell.
            lexer_class: The generated lexer.
            parser_class: The generated parser.
            start_rule (str): The entry rule (`start` for **kern, `startMens` for **mens).

        Returns: The parse tree.
        """
        def parser_for(mode, listener):
            lexer = lexer_class(InputStream(encoding))
            lexer.removeErrorListeners()
            if listener is not None:
                lexer.addErrorListener(listener)
            parser = parser_class(CommonTokenStream(lexer))
            parser._interp.predictionMode = mode
            parser.removeErrorListeners()
            if listener is not None:
                parser.addErrorListener(listener)
            return parser

        # Stage 1: SLL, bailing out at the first error (the runtime reads `_errHandler`; the
        # `errHandler` this used to set was never read, so SLL errors were recovered, not bailed).
        lexical_errors = ErrorListener()
        fast = parser_for(PredictionMode.SLL, None)
        fast.getTokenStream().tokenSource.addErrorListener(lexical_errors)
        fast._errHandler = BailErrorStrategy()
        try:
            tree = getattr(fast, start_rule)()
            if lexical_errors.getNumberErrorsFound() == 0:
                return tree
        except ParseCancellationException:
            pass
        # Stage 2 (also when the lexer complained in stage 1, which a bailing parser does not see): full
        # LL, with the error listener, which reports what is really wrong.
        return getattr(parser_for(PredictionMode.LL, self.error_listener), start_rule)()

