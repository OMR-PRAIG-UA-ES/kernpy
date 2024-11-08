from __future__ import annotations

from .spine_importer import SpineImporter
from .tokens import Token, SimpleToken, TokenCategory


class FingSpineImporter(SpineImporter):
    def import_token(self, encoding: str) -> Token:
        return SimpleToken(encoding, TokenCategory.FINGERING)
