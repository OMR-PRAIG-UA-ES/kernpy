from __future__ import annotations

from .spine_importer import SpineImporter
from .tokens import TokenCategory, Token, SimpleToken


class RootSpineImporter(SpineImporter):
    def import_token(self, encoding: str) -> Token:
        return SimpleToken(encoding, TokenCategory.HARMONY)
