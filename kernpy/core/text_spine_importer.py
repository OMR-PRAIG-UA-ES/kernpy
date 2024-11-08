from __future__ import annotations

from .spine_importer import SpineImporter
from .spine_importer import SpineImporter
from .tokens import SimpleToken, TokenCategory, Token


class TextSpineImporter(SpineImporter):
    def import_token(self, encoding: str) -> Token:
        return SimpleToken(encoding, TokenCategory.LYRICS)
