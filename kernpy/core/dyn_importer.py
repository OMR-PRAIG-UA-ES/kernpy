import string

from .spine_importer import SpineImporter
from .tokens import SimpleToken, TokenCategory, Token


class DynSpineImporter(SpineImporter):
    def import_token(self, encoding: string)->Token:
        return SimpleToken(encoding, TokenCategory.DYNAMICS)

