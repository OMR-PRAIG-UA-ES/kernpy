import string

from .spine_importer import SpineImporter
from .tokens import MHXMToken, Token


class MxhmSpineImporter(SpineImporter):
    def import_token(self, encoding: string) -> Token:
        return MHXMToken(encoding) # TODO: implement constructor for MHXMToken

