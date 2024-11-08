from __future__ import annotations

from .spine_importer import SpineImporter
from .tokens import Token, TokenCategory, SimpleToken


class DynamSpineImporter(SpineImporter):
    def import_token(self, encoding: str) -> Token:
        return SimpleToken(encoding, TokenCategory.DYNAMICS)
