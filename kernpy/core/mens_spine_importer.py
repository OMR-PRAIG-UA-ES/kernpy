from __future__ import annotations

from .spine_importer import SpineImporter
from .tokens import Token


class MensSpineImporter(SpineImporter):
    def import_token(self, encoding: str) -> Token:
        pass
