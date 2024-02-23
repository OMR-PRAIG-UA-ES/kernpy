import string

from .spine_importer import SpineImporter

from .spine_importer import SpineImporter
from .tokens import SimpleToken, TokenCategory, Token

class TextSpineImporter(SpineImporter):
    def doImport(self, encoding: string)->Token:
        return SimpleToken(encoding, TokenCategory.LYRICS)
