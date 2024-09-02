"""
Public API for KernPy.

The main functions for handling the input and output of **kern files are provided here.
"""

from typing import List, Optional
from collections.abc import Sequence
from overloading import overload

from kernpy import KernTypeExporter
from kernpy.core import Importer, Document, Exporter, ExportOptions, GraphvizExporter
from kernpy.core._io import _write


class Generic:
    """
    Generic class.

    This class provides support to the public API for KernPy.

    The main functions implementation are provided here.
    """

    @classmethod
    def read(
            cls,
            path: str,
            strict: Optional[bool] = False
    ) -> (Document, List[str]):
        """

        Args:
            path:
            strict:

        Returns:

        """
        importer = Importer()
        document = importer.import_file(path)
        errors = importer.errors

        if strict and len(errors) > 0:
            raise Exception(importer.get_error_messages())

        return document, errors

    @classmethod
    def create(
            cls,
            content: str,
            strict: Optional[bool] = False
    ) -> (Document, List[str]):
        """

        Args:
            content:
            strict:

        Returns:

        """
        importer = Importer()
        document = importer.import_string(content)
        errors = importer.errors

        if strict and len(errors) > 0:
            raise Exception(importer.get_error_messages())

        return document, errors

    @classmethod
    def export(
            cls,
            document: Document,
            options: ExportOptions
    ) -> str:
        """

        Args:
            document:
            options:

        Returns:

        """
        exporter = Exporter()
        return exporter.export_string(document, options)

    @classmethod
    def store(
            cls,
            document: Document,
            path: str,
            options: ExportOptions
    ) -> None:
        """

        Args:
            document:
            path:
            options:

        Returns:
        """
        content = cls.export(document, options)
        _write(path, content)

    @classmethod
    def store_graph(
            cls,
            document: Document,
            path: str
    ) -> None:
        """

        Args:
            document:
            path:

        Returns:
        """
        graph_exporter = GraphvizExporter()
        graph_exporter.export_to_dot(document.tree, path)

    @classmethod
    def get_spine_types(
            cls,
            document: Document,
            spine_types: Optional[Sequence[str]] = None
    ) -> List[str]:
        """

        Args:
            document:
            spine_types:

        Returns:

        """
        exporter = Exporter()
        return exporter.get_spine_types(document, spine_types)

    @classmethod
    def concat(
            cls,
            contents: Sequence[str],
            options: Optional[ExportOptions] = None,
            strict: Optional[bool] = False
    ) -> str:
        """

        Args:
            contents:
            options:
            strict:

        Returns:

        """
        if len(contents) < 2:
            raise ValueError(f"Concatenation action requires at least two documents to concatenate."
                             f"But {len(contents)} was given.")

        doc_a, err_a = cls.create(contents[0], strict=strict)
        for i, content in enumerate(contents[1:]):
            doc_b, err_b = cls.create(content, strict=strict)

            if strict and (len(err_a) > 0 or len(err_b) > 0):
                raise Exception(f"Errors were found during the creation of the documents "
                                f"while using the strict=True option. "
                                f"Description: concatenating: {err_a if len(err_a) > 0 else err_b}")

            doc_a.add_document(doc_b)
        return cls.export(
            document=doc_a,
            options=options
        )


def read(
        path: str,
        strict: Optional[bool] = False
) -> (Document, List[str]):
    """
    Read a Humdrum **kern file.

    Args:
        path (str): File path to read
        strict (Optional[bool]): If True, raise an error if the **kern file has any errors. Otherwise, return a list of errors.

    Returns (Document, List[str]): Document object and list of error messages. Empty list if no errors.

    Examples:
        >>> import kernpy as kp
        >>> document, _ = kp.read('path/to/file.krn')

        >>> document, errors = kp.read('path/to/file.krn')
        >>> if len(errors) > 0:
        >>>     print(errors)
        ['Error: Invalid **kern spine: 1', 'Error: Invalid **kern spine: 2']
    """
    return Generic.read(
        path=path,
        strict=strict
    )


def create(
        content: str,
        strict=False
) -> (Document, []):
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
    return Generic.create(
        content=content,
        strict=strict
    )

@overload
def export(
        document: Document,
        options: ExportOptions
) -> str:
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
    return Generic.export(
        document=document,
        options=options
    )

@overload
def export(
        document: Document,
        spine_types: Optional[Sequence[str]] = None,
        token_categories: Optional[Sequence[str]] = None,
        from_measure: Optional[int] = None,
        to_measure: Optional[int] = None,
        kern_type: Optional[KernTypeExporter] = None,
        instruments: Optional[Sequence[str]] = None,
        show_measure_numbers: Optional[bool] = None
) -> str:
    """
    Export a Document object to a string.

    Args:
        document (Document): Document object to store
        spine_types (Iterable): **kern, **mens, etc...
        token_categories (Iterable): TokenCategory
        from_measure (int): The measure to start exporting. When None, the exporter will start from the beginning of the file. The first measure is 1
        to_measure (int): The measure to end exporting. When None, the exporter will end at the end of the file.
        kern_type (KernTypeExporter): The type of the kern file to export.
        instruments (Iterable): The instruments to export. When None, all the instruments will be exported.
        show_measure_numbers (Bool): Show the measure numbers in the exported file.

    Returns (str): Content of the exported file

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.read('path/to/file.krn')
        >>> content = kp.export(
            document, ['**kern'],
            kp.BEKERN_CATEGORIES,
            1,
            3,
            kp.KernTypeExporter.eKern,
            ['Piano', 'Trumpet'])

    """


@overload
def store(
        document: Document,
        path: str,
        options: ExportOptions
) -> None:
    """
    Store a Document object to a file.

    Args:
        document (Document): Document object to store
        path (str): File path to store
        options (ExportOptions): Export options

    Returns: None

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.read('path/to/file.krn')
        >>> options = kp.ExportOptions()
        >>> kp.store(document, 'path/to/store.krn', options)

    """
    Generic.store(
        document=document,
        path=path,
        options=options
    )


@overload
def store(
        document: Document,
        path: str,
        spine_types: Optional[Sequence[str]] = None,
        token_categories: Optional[Sequence[str]] = None,
        from_measure: Optional[int] = None,
        to_measure: Optional[int] = None,
        kern_type: Optional[KernTypeExporter] = None,
        instruments: Optional[Sequence[str]] = None,
        show_measure_numbers: Optional[bool] = None
) -> None:
    """
    Args:
        document (Document): Document object to store
        path (str): File path to store
        spine_types (Iterable): **kern, **mens, etc...
        token_categories (Iterable): TokenCategory
        from_measure (int): The measure to start exporting. When None, the exporter will start from the beginning of the file. The first measure is 1
        to_measure (int): The measure to end exporting. When None, the exporter will end at the end of the file.
        kern_type (KernTypeExporter): The type of the kern file to export.
        instruments (Iterable): The instruments to export. When None, all the instruments will be exported.
        show_measure_numbers (Bool): Show the measure numbers in the exported file.


    Returns: None

    """
    options = ExportOptions(
        spine_types=spine_types,
        token_categories=token_categories,
        from_measure=from_measure,
        to_measure=to_measure,
        kern_type=kern_type,
        instruments=instruments,
        show_measure_numbers=show_measure_numbers)
    return Generic.store(
        document=document,
        path=path,
        options=options
    )


def store_graph(
        document: Document,
        path: str
) -> None:
    """
    Create a graph representation of a Document object using Graphviz. Save the graph to a file.

    Args:
        document (Document): Document object to create graph from
        path (str): File path to save the graph

    Returns: None

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.read('path/to/file.krn')
        >>> kp.store_graph(document, 'path/to/graph.dot')
    """
    return Generic.store_graph(
        document=document,
        path=path
    )


def get_spine_types(
        document: Document,
        spine_types: Optional[Sequence[str]] = None
) -> List[str]:
    """
    Get the spines of a Document object.

    Args:
        document (Document): Document object to get spines from
        spine_types (Optional[Sequence[str]]): List of spine types to get. If None, all spines are returned.

    Returns (List[str]): List of spines

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
    return Generic.get_spine_types(
        document=document,
        spine_types=spine_types
    )


@overload
def concat(
        content_a: str,
        content_b: str,
        options: ExportOptions,
        strict: Optional[bool] = False
) -> str:
    """
    Concatenate two **kern strings.

    Args:
        content_a (str): First **kern string
        content_b (str): Second **kern string
        options (ExportOptions): Export options for the concatenated string
        strict (Optional[bool]): If True, raise an error if the concatenated string exceeds the maximum length. If False, truncate the concatenated string to the maximum length.

    Returns: Concatenated **kern string

    Examples:
        >>> import kernpy as kp
        >>> content_a = '**kern\n4e\n4f\n4g\n*-\n'
        >>> content_b = '**kern\n4a\n4b\n4c\n*-\n'
        >>> kp.concat(content_a, content_b)
        '**kern\n4e\n4f\n4g\n*-\n**kern\n4a\n4b\n4c\n*-'
    """
    return Generic.concat(
        contents=[content_a, content_b],
        options=options,
        strict=strict
    )


@overload
def concat(
        contents: Sequence[str],
        options: ExportOptions,
        strict: Optional[bool] = False
) -> str:
    """
    Concatenate multiple **kern strings.

    Args:
        contents (Sequence[str]): List of **kern strings
        options (ExportOptions): Export options for the concatenated string
        strict (Optional[bool]): If True, raise an error if the concatenated string exceeds the maximum length. If False, truncate the concatenated string to the maximum length.

    Returns: Concatenated **kern string

    Examples:
        >>> import kernpy as kp
        >>> contents = ['**kern\n4e\n4f\n4g\n*-\n', '**kern\n4a\n4b\n4c\n*-\n']
        >>> kp.concat(contents)
        '**kern\n4e\n4f\n4g\n*-\n**kern\n4a\n4b\n4c\n*-'
    """
    return Generic.concat(
        contents=contents,
        options=options,
        strict=strict
    )
