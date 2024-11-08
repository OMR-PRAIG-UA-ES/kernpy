from __future__ import annotations

from .spine_importer import SpineImporter
from .tokens import MHXMToken, Token


class MxhmSpineImporter(SpineImporter):
    def import_token(self, encoding: str) -> Token:
        return MHXMToken(encoding) # TODO: implement constructor for MHXMToken

