import string

from .spine_importer import SpineImporter
from .tokens import TokenCategory, Token, SimpleToken


class RootSpineImporter(SpineImporter):
    def doImport(self, encoding: string)->Token:
        return SimpleToken(encoding, TokenCategory.HARMONY)
