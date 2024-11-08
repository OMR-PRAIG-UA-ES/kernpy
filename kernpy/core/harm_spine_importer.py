from __future__ import annotations

from .spine_importer import SpineImporter
from .tokens import SimpleToken, TokenCategory, Token


class HarmSpineImporter(SpineImporter):
    def import_token(self, encoding: str) -> Token:
        return SimpleToken(encoding, TokenCategory.HARMONY)
