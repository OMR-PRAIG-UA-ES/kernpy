import string

from src.spine_importer import SpineImporter
from src.tokens import Token, SimpleToken, TokenCategory


class FingSpineImporter(SpineImporter):
    def doImport(self, encoding: string)->Token:
        return SimpleToken(encoding, TokenCategory.FINGERING)
