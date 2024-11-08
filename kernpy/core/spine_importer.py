from __future__ import annotations

from abc import ABC, abstractmethod

from .tokens import Token


class SpineImporter(ABC):
    @abstractmethod
    def import_token(self, encoding: str) -> Token:
        pass
