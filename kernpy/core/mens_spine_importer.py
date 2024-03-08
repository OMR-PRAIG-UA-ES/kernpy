import string

from .spine_importer import SpineImporter
from .tokens import Token


class MensSpineImporter(SpineImporter):
    def doImport(self, encoding: string) -> Token:
        pass
