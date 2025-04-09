from __future__ import annotations

from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .spine_importer import SpineImporter
from .tokens import SimpleToken, TokenCategory, Token
from .kern_spine_importer import KernSpineImporter, KernSpineListener
from .dynam_spine_importer import DynamSpineImporter


class DynSpineImporter(SpineImporter):
    def import_listener(self) -> BaseANTLRSpineParserListener:
        return KernSpineListener()

    def import_token(self, encoding: str) -> Token:
        # TODO: Find out differences between **dyn vs **dynam and change this class. Using the same dor both for now.
        dynam_importer = DynamSpineImporter()
        return dynam_importer.import_token(encoding)



