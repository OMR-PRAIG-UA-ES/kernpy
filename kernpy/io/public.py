"""
Public API for KernPy.

The main functions for handling the input and output of **kern files are provided here.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Any, Union, Tuple, Sequence

from kernpy import Encoding
from kernpy.core import (
    Document, Importer, Exporter, ExportOptions, GraphvizExporter,
    generic,
    TokenCategoryHierarchyMapper)


def load(fp: Union[str, Path], *, raise_on_errors: Optional[bool] = False, **kwargs) -> (Document, List[str]):
    """
    Load a Document object from a Humdrum **kern file-like object.

    Args:
        fp (Union[str, Path]): A path-like object representing a **kern file.
        raise_on_errors (Optional[bool], optional): If True, raise an exception if any grammar error is detected\
            during parsing.

    Returns ((Document, List[str])): A tuple containing the Document object and a list of messages representing \
        grammar errors detected during parsing. If the list is empty,\
        the parsing did not detect any errors.

    Raises:
        ValueError: If the Humdrum **kern representation could not be parsed.

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.load('BWV565.krn')
        >>> if len(errors) > 0:
        >>>     print(f"Grammar didn't recognize the following errors: {errors}")
        ['Error: Invalid **kern spine: 1', 'Error: Invalid **kern spine: 2']
        >>>     # Anyway, we can use the Document
        >>>     print(document)
        >>> else:
        >>>     print(document)
        <kernpy.core.document.Document object at 0x7f8b3b7b3d90>
    """
    return generic.Generic.read(
        path=fp,
        strict=raise_on_errors,
    )


def loads(s, *, raise_on_errors: Optional[bool] = False, **kwargs) -> (Document, List[str]):
    """
    Load a Document object from a string encoded in Humdrum **kern.

    Args:
        s (str): A string containing a **kern file.
        raise_on_errors (Optional[bool], optional): If True, raise an exception if any grammar error is detected\
            during parsing.

    Returns ((Document, List[str])): A tuple containing the Document object and a list of messages representing \
        grammar errors detected during parsing. If the list is empty,\
        the parsing did not detect any errors.

    Raises:
        ValueError: If the Humdrum **kern representation could not be parsed.

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.loads('**kern\n*clefG2\n=1\n4c\n4d\n4e\n4f\n')
        >>> if len(errors) > 0:
        >>>     print(f"Grammar didn't recognize the following errors: {errors}")
        ['Error: Invalid **kern spine: 1']
        >>>     # Anyway, we can use the Document
        >>>     print(document)
        >>> else:
        >>>     print(document)
        <kernpy.core.document.Document object at 0x7f8b3b7b3d90>
    """
    return generic.Generic.create(
        content=s,
        strict=raise_on_errors,
    )


def dump(document: Document, fp: Union[str, Path], *,
         spine_types: [] = None,
         include: [] = None,
         exclude: [] = None,
         from_measure: int = None,
         to_measure: int = None,
         tokenizer: Encoding = None,
         instruments: [] = None,
         show_measure_numbers: bool = None,
         spine_ids: [int] = None
         ) -> None:
    """

    Args:
        document (Document): The Document object to write to the file.
        fp (Union[str, Path]): The file path to write the Document object.
        spine_types (Iterable): **kern, **mens, etc...
        include (Iterable): The token categories to include in the exported file. When None, all the token categories will be exported.
        exclude (Iterable): The token categories to exclude from the exported file. When None, no token categories will be excluded.
        from_measure (int): The measure to start exporting. When None, the exporter will start from the beginning of the file. The first measure is 1
        to_measure (int): The measure to end exporting. When None, the exporter will end at the end of the file.
        tokenizer (Encoding): The type of the **kern file to export.
        instruments (Iterable): The instruments to export. If None, all the instruments will be exported.
        show_measure_numbers (Bool): Show the measure numbers in the exported file.
        spine_ids (Iterable): The ids of the spines to export. When None, all the spines will be exported. \
            Spines ids start from 0, and they are increased by 1 for each spine to the right.


    Returns (None): None

    Raises:
        ValueError: If the document could not be exported.

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.load('BWV565.krn')
        >>> kp.dump(document, 'BWV565_normalized.krn')
        None
        >>> # File 'BWV565_normalized.krn' will be created with the normalized **kern representation.
    """
    # Create an ExportOptions instance with only user-modified arguments
    options = generic.Generic.parse_options_to_ExportOptions(
        spine_types=spine_types,
        include=include,
        exclude=exclude,
        from_measure=from_measure,
        to_measure=to_measure,
        kern_type=tokenizer,
        instruments=instruments,
        show_measure_numbers=show_measure_numbers,
        spine_ids=spine_ids
    )

    return generic.Generic.store(
        document=document,
        path=fp,
        options=options
    )


def dumps(document: Document, *,
          spine_types: [] = None,
          include: [] = None,
          exclude: [] = None,
          from_measure: int = None,
          to_measure: int = None,
          tokenizer: Encoding = None,
          instruments: [] = None,
          show_measure_numbers: bool = None,
          spine_ids: [int] = None
          ) -> str:
    """

    Args:
        document (Document): The Document object to write to the file.
        fp (Union[str, Path]): The file path to write the Document object.
        spine_types (Iterable): **kern, **mens, etc...
        include (Iterable): The token categories to include in the exported file. When None, all the token categories will be exported.
        exclude (Iterable): The token categories to exclude from the exported file. When None, no token categories will be excluded.
        from_measure (int): The measure to start exporting. When None, the exporter will start from the beginning of the file. The first measure is 1
        to_measure (int): The measure to end exporting. When None, the exporter will end at the end of the file.
        tokenizer (Encoding): The type of the **kern file to export.
        instruments (Iterable): The instruments to export. If None, all the instruments will be exported.
        show_measure_numbers (Bool): Show the measure numbers in the exported file.
        spine_ids (Iterable): The ids of the spines to export. When None, all the spines will be exported. \
            Spines ids start from 0, and they are increased by 1 for each spine to the right.


    Returns (None): None

    Raises:
        ValueError: If the document could not be exported.

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.load('score.krn')
        >>> kp.dumps(document)
        '**kern\n*clefG2\n=1\n4c\n4d\n4e\n4f\n*-'
    """
    # Create an ExportOptions instance with only user-modified arguments
    options = generic.Generic.parse_options_to_ExportOptions(
        spine_types=spine_types,
        include=include,
        exclude=exclude,
        from_measure=from_measure,
        to_measure=to_measure,
        kern_type=tokenizer,
        instruments=instruments,
        show_measure_numbers=show_measure_numbers,
        spine_ids=spine_ids
    )

    return generic.Generic.export(
        document=document,
        options=options
    )


def graph(document: Document, fp: Optional[Union[str, Path]]) -> None:
    """
    Create a graph representation of a Document object using Graphviz. Save the graph as a .dot file or indicate the\
     output file path or stream. If the output file path is None, the function will return the graphviz content as a\
        string to the standard output.

    Use the Graphviz software to convert the .dot file to an image.


    Args:
        document (Document): The Document object to export as a graphviz file.
        fp (Optional[Union[str, Path]]): The file path to write the graphviz file. If None, the function will return the\
            graphviz content as a string to the standard output.

    Returns (None): None

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.load('score.krn')
        >>> kp.graph(document, 'score.dot')
        None
        >>> # File 'score.dot' will be created with the graphviz representation of the Document object.
        >>> kp.graph(document, None)
        'digraph G { ... }'
    """
    return generic.Generic.store_graph(
        document=document,
        path=fp
    )


def concat(
        contents: List[str],
        *,
        separator: Optional[str] = '\n',
) -> Tuple[Document, List[Tuple[int, int]]]:
    """
    Concatenate multiple **kern fragments into a single Document object. \
     All the fragments should be presented in order. Each fragment does not need to be a complete **kern file. \

    Warnings:
        Processing a large number of files in a row may take some time.
         This method performs as many `kp.read` operations as there are fragments to concatenate.
    Args:
        contents (Sequence[str]): List of **kern strings
        separator (Optional[str]): Separator string to separate the **kern fragments. Default is '\n' (newline).

    Returns (Tuple[Document, List[Tuple[int, int]]]): Document object and \
      and a List of Pairs (Tuple[int, int]) representing the measure fragment indexes of the concatenated document.

    Examples:
        >>> import kernpy as kp
        >>> contents = ['**kern\n4e\n4f\n4g\n*-\n', '4a\n4b\n4c\n*-\n=\n', '4d\n4e\n4f\n*-\n']
        >>> document, indexes = kp.concat(contents)
        >>> indexes
        [(0, 3), (3, 6), (6, 9)]
        >>> document, indexes = kp.concat(contents, separator='\n')
        >>> indexes
        [(0, 3), (3, 6), (6, 9)]
        >>> document, indexes = kp.concat(contents, separator='')
        >>> indexes
        [(0, 3), (3, 6), (6, 9)]
        >>> for start, end in indexes:
        >>>     print(kp.dumps(document, from_measure=start, to_measure=end)))
    """
    return generic.Generic.concat(
        contents=contents,
        separator=separator,
    )


def merge(
        contents: List[str],
        *,
        raise_on_errors: Optional[bool] = False,
) -> Tuple[Document, List[Tuple[int, int]]]:
    """
    Merge multiple **kern fragments into a single **kern string. \
     All the fragments should be presented in order. Each fragment does not need to be a complete **kern file. \

    Warnings:
        Processing a large number of files in a row may take some time.
         This method performs as many `kp.read` operations as there are fragments to concatenate.
    Args:
        contents (Sequence[str]): List of **kern strings
        raise_on_errors (Optional[bool], optional): If True, raise an exception if any grammar error is detected\
            during parsing.

    Returns (Tuple[Document, List[Tuple[int, int]]]): Document object and \
      and a List of Pairs (Tuple[int, int]) representing the measure fragment indexes of the concatenated document.

    Examples:
        >>> import kernpy as kp
        >>> contents = ['**kern\n4e\n4f\n4g\n*-\n*-', '**kern\n4a\n4b\n4c\n*-\n=\n*-', '**kern\n4d\n4e\n4f\n*-\n*-']
        >>> document, indexes = kp.concat(contents)
        >>> indexes
        [(0, 3), (3, 6), (6, 9)]
        >>> document, indexes = kp.concat(contents, separator='\n')
        >>> indexes
        [(0, 3), (3, 6), (6, 9)]
        >>> document, indexes = kp.concat(contents, separator='')
        >>> indexes
        [(0, 3), (3, 6), (6, 9)]
        >>> for start, end in indexes:
        >>>     print(kp.dumps(document, from_measure=start, to_measure=end)))
    """
    return generic.Generic.merge(
        contents=contents,
        strict=raise_on_errors
    )


def spine_types(
        document: Document,
        headers: Optional[Sequence[str]] = None
) -> List[str]:
    """
    Get the spines of a Document object.

    Args:
        document (Document): Document object to get spines from
        headers (Optional[Sequence[str]]): List of spine types to get. If None, all spines are returned. Using a \
         header will return all the spines of that type.

    Returns (List[str]): List of spines

    Examples:
        >>> import kernpy as kp
        >>> document, _ = kp.read('path/to/file.krn')
        >>> kp.spine_types(document)
        ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
        >>> kp.spine_types(document, None)
        ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
        >>> kp.spine_types(document, headers=None)
        ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
        >>> kp.spine_types(document, headers=['**kern'])
        ['**kern', '**kern', '**kern', '**kern']
        >>> kp.spine_types(document, headers=['**kern', '**root'])
        ['**kern', '**kern', '**kern', '**kern', '**root']
        >>> kp.spine_types(document, headers=['**kern', '**root', '**harm'])
        ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
        >>> kp.spine_types(document, headers=[])
        []
    """
    return generic.Generic.get_spine_types(
        document=document,
        spine_types=headers
    )




