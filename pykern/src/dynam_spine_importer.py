import string

from src.spine_importer import SpineImporter
from src.tokens import Token, TokenCategory, SimpleToken


class DynamSpineImporter(SpineImporter):
    def doImport(self, encoding: string)->Token:
        return SimpleToken(encoding, TokenCategory.DYNAMICS)
