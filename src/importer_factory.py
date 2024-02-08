import string

from src.dyn_importer import DynSpineImporter
from src.dynam_spine_importer import DynamSpineImporter
from src.fing_spine_importer import FingSpineImporter
from src.harm_spine_importer import HarmSpineImporter
from src.kern_spine_importer import KernSpineImporter
from src.mens_spine_importer import MensSpineImporter
from src.mhxm_spine_importer import MxhmSpineImporter
from src.root_importer import RootSpineImporter
from src.spine_importer import SpineImporter
from src.text_spine_importer import TextSpineImporter


def createImporter(spine_type: string) -> SpineImporter:
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
        raise ValueError(f"Invalid object type: {spine_type}")
