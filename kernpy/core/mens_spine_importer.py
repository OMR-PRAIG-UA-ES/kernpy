from __future__ import annotations
from typing import Optional

from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .spine_importer import SpineImporter
from .tokens import Token


class MensSpineImporter(SpineImporter):
    def __init__(self, verbose: Optional[bool] = False):
        """
        MensSpineImporter constructor.

        Args:
            verbose (Optional[bool]): Level of verbosity for error messages.
        """
        super().__init__(verbose=verbose)

    def import_listener(self) -> BaseANTLRSpineParserListener:
        raise NotImplementedError()

    def import_token(self, encoding: str) -> Token:
        raise NotImplementedError()
