from __future__ import annotations
import sys

from .dyn_importer import DynSpineImporter
from .dynam_spine_importer import DynamSpineImporter
from .fing_spine_importer import FingSpineImporter
from .harm_spine_importer import HarmSpineImporter
from .kern_spine_importer import KernSpineImporter
from .mens_spine_importer import MensSpineImporter
from .mhxm_spine_importer import MxhmSpineImporter
from .root_spine_importer import RootSpineImporter
from .spine_importer import SpineImporter
from .text_spine_importer import TextSpineImporter
from .basic_spine_importer import BasicSpineImporter


def createImporter(spine_type: str) -> SpineImporter:
    if spine_type == '**mens':
        return MensSpineImporter()
    elif spine_type == '**kern':
        return KernSpineImporter()
    elif spine_type == '**text':
        return TextSpineImporter()
    elif spine_type == '**harm':
        return HarmSpineImporter()
    elif spine_type == '**mxhm':
        return MxhmSpineImporter()
    elif spine_type == '**root':
        return RootSpineImporter()
    elif spine_type == '**dyn':
        return DynSpineImporter()
    elif spine_type == '**dynam':
        return DynamSpineImporter()
    elif spine_type == '**fing':
        return FingSpineImporter()
    else:
        #print(f'Invalid spine header type found: {spine_type} '
        #      f'using a basic spine importer instead',
        #      file=sys.stderr)
        # TODO: Should we use a logger? Global variable for verbosity?

        return BasicSpineImporter()  # Only parse basic token categories

