import string

from src.spine_importer import SpineImporter
from src.tokens import SimpleToken, TokenCategory, Token


class HarmSpineImporter(SpineImporter):
    def doImport(self, encoding: string)->Token:
        return SimpleToken(encoding, TokenCategory.HARMONY)
