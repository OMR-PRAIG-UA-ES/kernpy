"""
Public API for KernPy.

The main functions for handling the input and output of **kern files are provided here.
"""

from kernpy.core import Importer, Document, Exporter, ExportOptions, GraphvizExporter
from kernpy.core.io import _write


def read(path, strict=False) -> (Document, []):
    """
    Read a Humdrum **kern file.

    Args:
        path: File path to read
        strict: If True, raise an error if the **kern file has any errors. Otherwise, return a list of errors.

    Returns (Document, list): Document object and list of error messages. Empty list if no errors.

    Examples:
        >>> import kernpy as kp
        >>> document, _ = kp.read('path/to/file.krn')

        >>> document, errors = kp.read('path/to/file.krn')
        >>> if len(errors) > 0:
        >>>     print(errors)
        ['Error: Invalid **kern spine: 1', 'Error: Invalid **kern spine: 2']
    """
    importer = Importer()
    document = importer.import_file(path)
    errors = importer.errors

    if strict and len(errors) > 0:
        raise Exception(importer.get_error_messages())

    return document, errors


def create(content: str, strict=False) -> (Document, []):
    """
    Create a Document object from a string encoded in Humdrum **kern format.

    Args:
        content: String encoded in Humdrum **kern format
        strict: If True, raise an error if the **kern file has any errors. Otherwise, return a list of errors.

    Returns (Document, list): Document object and list of error messages. Empty list if no errors.

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.create('**kern\n4e\n4f\n4g\n*-\n')
        >>> if len(errors) > 0:
        >>>     print(errors)
        ['Error: Invalid **kern spine: 1', 'Error: Invalid **kern spine: 2']
    """
    importer = Importer()
    document = importer.import_string(content)
    errors = importer.errors

    if strict and len(errors) > 0:
        raise Exception(importer.get_error_messages())

    return document, errors


def export(document: Document, options: ExportOptions) -> str:
    """
    Export a Document object to a string.

    Args:
        document: Document object to export
        options: Export options

    Returns: Exported string

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.read('path/to/file.krn')
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
        >>> document, errors = kp.read('path/to/file.krn')
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
        >>> document, _ = kp.read('path/to/file.krn')
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
    return exporter.get_spine_types(document, spine_types=spine_types)


def concat(content_a: str, content_b: str, options: ExportOptions = None) -> str:
    """
    Concatenate two **kern strings.

    Args:
        content_a (str): First **kern string
        content_b (str): Second **kern string
        options (ExportOptions): Export options for the concatenated string

    Returns: Concatenated **kern string

    Examples:
        >>> import kernpy as kp
        >>> content_a = '**kern\n4e\n4f\n4g\n*-\n'
        >>> content_b = '**kern\n4a\n4b\n4c\n*-\n'
        >>> kp.concat(content_a, content_b)
        '**kern\n4e\n4f\n4g\n*-\n**kern\n4a\n4b\n4c\n*-'
    """
    importer = Importer()
    document_a = importer.import_string(content_a)
    document_b = importer.import_string(content_b)
    document_concat = Document.to_concat(document_a, document_b)
    exporter = Exporter()
    return exporter.export_string(document_concat, ExportOptions())
