from __future__ import annotations

from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .spine_importer import SpineImporter
from .spine_importer import SpineImporter
from .kern_spine_importer import KernSpineImporter, KernSpineListener
from .tokens import SimpleToken, TokenCategory, Token


class TextSpineImporter(SpineImporter):
    def import_listener(self) -> BaseANTLRSpineParserListener:
        return KernSpineListener()  # TODO: Create a custom functional listener for TextSpineImporter

    def import_token(self, encoding: str) -> Token:
        self._raise_error_if_wrong_input(encoding)

        kern_spine_importer = KernSpineImporter()
        token = kern_spine_importer.import_token(encoding)

        ACCEPTED_CATEGORIES = {
            TokenCategory.STRUCTURAL,
            TokenCategory.SIGNATURES,
            TokenCategory.EMPTY,
            TokenCategory.BARLINES,
            TokenCategory.IMAGE_ANNOTATIONS,
            TokenCategory.BARLINES,
            TokenCategory.COMMENTS,
        }

        if not any(TokenCategory.is_child(child=token.category, parent=cat) for cat in ACCEPTED_CATEGORIES):
            return SimpleToken(encoding, TokenCategory.LYRICS)

        return token