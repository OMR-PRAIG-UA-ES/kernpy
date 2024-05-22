import string

from .spine_importer import SpineImporter
from .tokens import Token, TokenCategory, SimpleToken


class DynamSpineImporter(SpineImporter):
    def import_token(self, encoding: string)->Token:
        return SimpleToken(encoding, TokenCategory.DYNAMICS)
