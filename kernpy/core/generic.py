"""
Public API for KernPy.

The main functions for handling the input and output of **kern files are provided here.
"""

from kernpy.core import Importer, Document, Exporter, ExportOptions, GraphvizExporter
from kernpy.core.io import _write

def read(path) -> Document:
    """
    Read a Humdrum **kern file.

    Args:
        path: File path to read

    Returns: Document object

    Examples:
        >>> import kernpy as kp
        >>> document = kp.read('path/to/file.krn')

    """
    importer = Importer()
    document = importer.import_file(path)
    return document

def export(document: Document, options: ExportOptions) -> str:
    """
    Export a Document object to a string.

    Args:
        document: Document object to export
        options: Export options

    Returns: Exported string

    Examples:
        >>> import kernpy as kp
        >>> document = kp.read('path/to/file.krn')
        >>> options = kp.ExportOptions()
        >>> content = kp.export(document, options)
    """
    exporter = Exporter()
    return exporter.export_string(document, options)

def store(document: Document, path, options: ExportOptions) -> None:
    """
    Store a Document object to a file.

    Args:
        document: Document object to store
        path: File path to store
        options: Export options

    Returns: None

    Examples:
        >>> import kernpy as kp
        >>> document = kp.read('path/to/file.krn')
        >>> options = kp.ExportOptions()
        >>> kp.store(document, 'path/to/store.krn', options)

    """
    exporter = Exporter()
    content = exporter.export_string(document, options)
    _write(path, content)

def store_graph(document: Document, path) -> None:
    """
    Create a graph representation of a Document object using Graphviz. Save the graph to a file.

    Args:
        document: Document object to create graph from
        path: File path to save the graph

    Returns: None

    Examples:
        >>> import kernpy as kp
        >>> document = kp.read('path/to/file.krn')
        >>> kp.store_graph(document, 'path/to/graph.dot')
    """
    graph_exporter = GraphvizExporter()
    graph_exporter.export_to_dot(document.tree, path)

def get_spine_types(document: Document, spine_types: list = None) -> list:
    """
    Get the spines of a Document object.

    Args:
        document(Document): Document object to get spines from
        spine_types(list): List of spine types to get. If None, all spines are returned.

    Returns: List of spines

    Examples:
        >>> import kernpy as kp
        >>> document = kp.read('path/to/file.krn')
        >>> kp.get_spine_types(document)
        ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
        >>> kp.get_spine_types(document, None)
        ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
        >>> kp.get_spine_types(document, ['**kern'])
        ['**kern', '**kern', '**kern', '**kern']
        >>> kp.get_spine_types(document, ['**kern', '**root'])
        ['**kern', '**kern', '**kern', '**kern', '**root']
        >>> kp.get_spine_types(document, ['**kern', '**root', '**harm'])
        ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
        >>> kp.get_spine_types(document, [])
        []
    """
    exporter = Exporter()
    return exporter.get_spine_types(document)
