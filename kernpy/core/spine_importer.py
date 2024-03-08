import string
from abc import ABC, abstractmethod

from .tokens import Token


class SpineImporter(ABC):
    @abstractmethod
    def doImport(self, encoding: string)->Token:
        pass
