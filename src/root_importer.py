import string

from src.spine_importer import SpineImporter
from src.tokens import TokenCategory, Token, SimpleToken


class RootSpineImporter(SpineImporter):
    def doImport(self, encoding: string)->Token:
        return SimpleToken(encoding, TokenCategory.HARMONY)
