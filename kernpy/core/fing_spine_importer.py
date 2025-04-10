from __future__ import annotations
from typing import Optional

from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .kern_spine_importer import KernSpineListener, KernSpineImporter
from .spine_importer import SpineImporter
from .tokens import Token, SimpleToken, TokenCategory


class FingSpineImporter(SpineImporter):
    def __init__(self, verbose: Optional[bool] = False):
        """
        KernSpineImporter constructor.

        Args:
            verbose (Optional[bool]): Level of verbosity for error messages.
        """
        super().__init__(verbose=verbose)

    def import_listener(self) -> BaseANTLRSpineParserListener:
        return KernSpineListener()


    def import_token(self, encoding: str) -> Token:
        self._raise_error_if_wrong_input(encoding)

        kern_spine_importer = KernSpineImporter()
        token = kern_spine_importer.import_token(encoding)

        ACCEPTED_CATEGORIES = {
            TokenCategory.STRUCTURAL,
            TokenCategory.SIGNATURES,
            TokenCategory.EMPTY,
            TokenCategory.IMAGE_ANNOTATIONS,
            TokenCategory.BARLINES,
            TokenCategory.COMMENTS,
        }

        if not any(TokenCategory.is_child(child=token.category, parent=cat) for cat in ACCEPTED_CATEGORIES):
            return SimpleToken(encoding, TokenCategory.FINGERING)

        return token
