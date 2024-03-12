import string

from .spine_importer import SpineImporter
from .tokens import MHXMToken, Token


class MxhmSpineImporter(SpineImporter):
    def doImport(self, encoding: string)->Token:
        return MHXMToken(encoding)

