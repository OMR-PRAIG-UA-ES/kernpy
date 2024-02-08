import string
from abc import ABC, abstractmethod


class SpineImporter(ABC):
    def doImport(self, token: string):
        return token # by default, it returns the token itself
