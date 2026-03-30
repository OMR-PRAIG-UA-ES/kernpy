"""
Public API for KernPy.

The main functions for handling the input and output of **kern files are provided here.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Any, Union, Tuple
from collections.abc import Sequence

from kernpy.core import Importer, Document, Exporter, ExportOptions, GraphvizExporter, TokenCategoryHierarchyMapper
from kernpy.core._io import _write
from kernpy.util.helpers import deprecated


class Generic:
    """
    Generic class.

    This class provides support to the public API for KernPy.

    The main functions implementation are provided here.
    """

    @classmethod
    def read(
            cls,
            path: Path,
            strict: Optional[bool] = False,
            error_on_duration_mismatch: bool = False,
            meter_signature_fallback_if_not_found: Optional[str] = None,
    ) -> (Document, List[str]):
        """

        Args:
            path:
            strict:

        Returns:

        """
        importer = Importer(
            error_on_duration_mismatch=error_on_duration_mismatch,
            meter_signature_fallback_if_not_found=meter_signature_fallback_if_not_found,
        )
        document = importer.import_file(path)
        errors = importer.errors

        if strict and len(errors) > 0:
            raise Exception(importer.get_error_messages())

        return document, errors

    @classmethod
    def create(
            cls,
            content: str,
            strict: Optional[bool] = False,
            error_on_duration_mismatch: bool = False,
            meter_signature_fallback_if_not_found: Optional[str] = None,
    ) -> (Document, List[str]):
        """

        Args:
            content:
            strict:

        Returns:

        """
        importer = Importer(
            error_on_duration_mismatch=error_on_duration_mismatch,
            meter_signature_fallback_if_not_found=meter_signature_fallback_if_not_found,
        )
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
            path: Path,
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
            path: Path
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
    def merge(
            cls,
            contents: Sequence[str],
            strict: Optional[bool] = False,
            raise_on_header_mismatch: bool = True,
            only_check_core_spines: bool = False,
    ) -> Tuple[Document, List[Tuple[int, int]]]:
        """

        Args:
            contents:
            strict:

        Returns:

        """
        return cls._merge_documents_via_filtered_roundtrip(
            contents=contents,
            strict=strict,
            raise_on_header_mismatch=raise_on_header_mismatch,
            only_check_core_spines=only_check_core_spines,
        )

    @classmethod
    def _validate_document_compatibility(
            cls,
            left: Document,
            right: Document,
            *,
            raise_on_header_mismatch: bool,
            only_check_core_spines: bool,
    ) -> bool:
        is_compatible = Document.match(
            left,
            right,
            check_core_spines_only=only_check_core_spines,
        )

        if not is_compatible and raise_on_header_mismatch:
            left_headers = [token.encoding for token in left.get_header_nodes()]
            right_headers = [token.encoding for token in right.get_header_nodes()]
            raise ValueError(
                f"Documents are not compatible for merge. "
                f"Headers do not match with only_check_core_spines={only_check_core_spines}. "
                f"left: {left_headers}, right: {right_headers}."
            )

        return is_compatible

    @classmethod
    def _merge_documents_via_add(
            cls,
            contents: Sequence[str],
            strict: Optional[bool] = False,
            raise_on_header_mismatch: bool = True,
            only_check_core_spines: bool = False,
    ) -> Tuple[Document, List[Tuple[int, int]]]:
        if len(contents) < 2:
            raise ValueError(
                f"Merge action requires at least two documents to merge. "
                f"But {len(contents)} was given."
            )

        documents = []
        indexes = []
        low_index = 0

        for content in contents:
            doc, _ = cls.create(content, strict=strict)
            documents.append(doc)

            high_index = low_index + doc.measures_count()
            indexes.append((low_index, high_index))
            low_index = high_index + 1

        merged_document = documents[0].clone()

        for doc in documents[1:]:
            cls._validate_document_compatibility(
                merged_document,
                doc,
                raise_on_header_mismatch=raise_on_header_mismatch,
                only_check_core_spines=only_check_core_spines,
            )

            merged_document.add(
                doc,
                check_core_spines_only=only_check_core_spines,
            )

        return merged_document, indexes

    @classmethod
    def _merge_documents_via_filtered_roundtrip(
            cls,
            contents: Sequence[str],
            strict: Optional[bool] = False,
            raise_on_header_mismatch: bool = True,
            only_check_core_spines: bool = False,
            include=None,
            exclude=None,
    ) -> Tuple[Document, List[Tuple[int, int]]]:
        if len(contents) < 2:
            raise ValueError(
                f"Merge action requires at least two documents to merge. "
                f"But {len(contents)} was given."
            )

        docs = []
        indexes = []
        low_index = 0

        for content in contents:
            doc, _ = cls.create(content, strict=strict)
            docs.append(doc)

            high_index = low_index + doc.measures_count()
            indexes.append((low_index, high_index))
            low_index = high_index + 1

        for doc in docs[1:]:
            cls._validate_document_compatibility(
                docs[0],
                doc,
                raise_on_header_mismatch=raise_on_header_mismatch,
                only_check_core_spines=only_check_core_spines,
            )

        options = cls.parse_options_to_ExportOptions(include=include, exclude=exclude)
        exported_contents = [cls.export(doc, options) for doc in docs]

        merged_content = exported_contents[0]
        for content in exported_contents[1:]:
            left_rows = merged_content.splitlines()
            right_rows = content.splitlines()
            merged_content = "\n".join(left_rows[:-1] + right_rows[1:]) + "\n"

        merged_document, _ = cls.create(merged_content, strict=strict)
        return merged_document, indexes

    @classmethod
    def concat(
            cls,
            contents: Sequence[str],
            separator: Optional[str] = None
    ) -> Tuple[Document, List[Tuple[int, int]]]:
        """

        Args:
            contents:
            separator:

        Returns:

        """
        # Raw kern content
        if separator is None:
            separator = '\n'

        if len(contents) == 0:
            raise ValueError("No contents to merge. At least one content is required.")

        raw_kern = ''
        document = None
        indexes = []
        low_index = 0
        high_index = 0

        # Merge all fragments
        for content in contents:
            raw_kern += separator + content
            document, _ = create(raw_kern)
            high_index = document.measures_count()
            indexes.append((low_index, high_index))

            low_index = high_index + 1  # Next fragment start is the previous fragment end + 1

        if document is None:
            raise Exception("Failed to merge the contents. The document is None.")

        return document, indexes

    @classmethod
    def parse_options_to_ExportOptions(
            cls,
            **kwargs: Any
    ) -> ExportOptions:
        """

        Args:
            **kwargs:

        Returns:

        """
        options = ExportOptions.default()

        # Compute the valid token categories
        options.token_categories = TokenCategoryHierarchyMapper.valid(
            include=kwargs.get('include', None),
            exclude=kwargs.get('exclude', None)
        )

        # Use kwargs to update the ExportOptions object
        for key, value in kwargs.items():
            if key in ['include', 'exclude', 'token_categories']:  # Skip these keys: generated manually
                continue

            if value is not None:
                setattr(options, key, value)

        return options


@deprecated("Use 'load' instead.")
def read(
        path: Union[str, Path],
        strict: Optional[bool] = False
) -> (Document, List[str]):
    """
    Read a Humdrum **kern file.

    Args:
        path (Union[str, Path]): File path to read
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
        path=Path(path),
        strict=strict
    )


@deprecated("Use 'loads' instead.")
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


@deprecated("Use 'dumps' instead.")
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


@deprecated("Use 'dump' instead.")
def store(
        document: Document,
        path: Union[str, Path],
        options: ExportOptions
) -> None:
    """
    Store a Document object to a file.

    Args:
        document (Document): Document object to store
        path (Union[str, Path]): File path to store
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
        path=Path(path),
        options=options
    )


@deprecated("Use 'graph' instead.")
def store_graph(
        document: Document,
        path: Union[str, Path]
) -> None:
    """
    Create a graph representation of a Document object using Graphviz. Save the graph to a file.

    Args:
        document (Document): Document object to create graph from
        path (str): File path to save the graph

    Returns (None): None

    Examples:
        >>> import kernpy as kp
        >>> document, errors = kp.read('path/to/file.krn')
        >>> kp.store_graph(document, 'path/to/graph.dot')
    """
    return Generic.store_graph(
        document=document,
        path=Path(path)
    )


@deprecated("Use 'spine_types' instead.")
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
