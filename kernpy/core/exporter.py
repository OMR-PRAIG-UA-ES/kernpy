from __future__ import annotations

from copy import deepcopy
from enum import Enum
from typing import Optional
from collections.abc import Sequence
from abc import ABC, abstractmethod

from kernpy.core import Document, SpineOperationToken, HeaderToken, Importer, TokenCategory, InstrumentToken, \
    TOKEN_SEPARATOR, DECORATION_SEPARATOR, Token, NoteRestToken, HEADERS, BEKERN_CATEGORIES, ComplexToken
from kernpy.core.tokenizers import Encoding, TokenizerFactory, Tokenizer



class ExportOptions:
    """
    `ExportOptions` class.

    Store the options to export a **kern file.
    """

    def __init__(
            self,
            spine_types: [] = None,
            token_categories: [] = None,
            from_measure: int = None,
            to_measure: int = None,
            kern_type: Encoding = Encoding.normalizedKern,
            instruments: [] = None,
            show_measure_numbers: bool = False,
            spine_ids: [int] = None
    ):
        """
        Create a new ExportOptions object.

        Args:
            spine_types (Iterable): **kern, **mens, etc...
            token_categories (Iterable): TokenCategory
            from_measure (int): The measure to start exporting. When None, the exporter will start from the beginning of the file. The first measure is 1
            to_measure (int): The measure to end exporting. When None, the exporter will end at the end of the file.
            kern_type (Encoding): The type of the kern file to export.
            instruments (Iterable): The instruments to export. When None, all the instruments will be exported.
            show_measure_numbers (Bool): Show the measure numbers in the exported file.
            spine_ids (Iterable): The ids of the spines to export. When None, all the spines will be exported. Spines ids start from 0 and they are increased by 1.

        Example:
            >>> import kernpy

            Create the importer and read the file
            >>> hi = Importer()
            >>> document = hi.import_file('file.krn')
            >>> exporter = Exporter()

            Export the file with the specified options
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
            >>> exported_data = exporter.export_string(document, options)

            Export only the lyrics
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=[TokenCategory.LYRICS])
            >>> exported_data = exporter.export_string(document, options)

            Export the comments
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=[TokenCategory.LINE_COMMENTS, TokenCategory.FIELD_COMMENTS])
            >>> exported_data = exporter.export_string(document, options)

            Export using the eKern version
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES, kern_type=Encoding.eKern)
            >>> exported_data = exporter.export_string(document, options)

        """
        self.spine_types = spine_types if spine_types is not None else deepcopy(HEADERS)
        self.from_measure = from_measure
        self.to_measure = to_measure
        self.token_categories = token_categories if token_categories is not None else [c for c in TokenCategory]
        self.kern_type = kern_type
        self.instruments = instruments
        self.show_measure_numbers = show_measure_numbers
        self.spine_ids = spine_ids  # When exporting, if spine_ids=None all the spines will be exported.

    def __eq__(self, other: 'ExportOptions') -> bool:
        """
        Compare two ExportOptions objects.

        Args:
            other: The other ExportOptions object to compare.

        Returns (bool):
            True if the objects are equal, False otherwise.

        Examples:
            >>> options1 = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
            >>> options2 = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
            >>> options1 == options2
            True

            >>> options3 = ExportOptions(spine_types=['**kern', '**harm'], token_categories=BEKERN_CATEGORIES)
            >>> options1 == options3
            False
        """
        return self.spine_types == other.spine_types and \
            self.token_categories == other.token_categories and \
            self.from_measure == other.from_measure and \
            self.to_measure == other.to_measure and \
            self.kern_type == other.kern_type and \
            self.instruments == other.instruments and \
            self.show_measure_numbers == other.show_measure_numbers and \
            self.spine_ids == other.spine_ids

    def __ne__(self, other: 'ExportOptions') -> bool:
        """
        Compare two ExportOptions objects.

        Args:
            other (ExportOptions): The other ExportOptions object to compare.

        Returns (bool):
            True if the objects are not equal, False otherwise.

        Examples:
            >>> options1 = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
            >>> options2 = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
            >>> options1 != options2
            False

            >>> options3 = ExportOptions(spine_types=['**kern', '**harm'], token_categories=BEKERN_CATEGORIES)
            >>> options1 != options3
            True
        """
        return not self.__eq__(other)

    @classmethod
    def default(cls):
        return cls(
            spine_types=deepcopy(HEADERS),
            token_categories=[c for c in TokenCategory],
            from_measure=None,
            to_measure=None,
            kern_type=Encoding.normalizedKern,
            instruments=None,
            show_measure_numbers=False,
            spine_ids=None
        )


def empty_row(row):
    for col in row:
        if col != '.' and col != '' and col != '*':
            return False
    return True


class HeaderTokenGenerator:
    """
    HeaderTokenGenerator class.

    This class is used to translate the HeaderTokens to the specific tokenizer format.
    """
    @classmethod
    def new(cls, *, token: HeaderToken, type: Encoding):
        """
        Create a new HeaderTokenGenerator object. Only accepts stardized Humdrum **kern encodings. 

        Args:
            token (HeaderToken): The HeaderToken to be translated.
            type (Encoding): The tokenizer to be used.

        Examples:
            >>> header = HeaderToken('**kern', 0)
            >>> header.encoding
            '**kern'
            >>> new_header = HeaderTokenGenerator.new(token=header, type=Encoding.eKern)
            >>> new_header.encoding
            '**ekern'
        """
        new_encoding = f'**{type.prefix()}{token.encoding[2:]}'
        new_token = HeaderToken(new_encoding, token.spine_id)

        return new_token




class Exporter:
    def export_string(self, document: Document, options: ExportOptions) -> str:
        self.export_options_validator(document, options)

        rows = []

        if options.to_measure is not None and options.to_measure < len(document.measure_start_tree_stages):

            if options.to_measure < len(document.measure_start_tree_stages) - 1:
                to_stage = document.measure_start_tree_stages[
                    options.to_measure]  # take the barlines from the next coming measure
            else:
                to_stage = len(document.tree.stages) - 1  # all stages
        else:
            to_stage = len(document.tree.stages) - 1  # all stages

        if options.from_measure:
            # In case of beginning not from the first measure, we recover the spine creation and the headers
            # Traversed in reverse order to only include the active spines at the given measure...
            from_stage = document.measure_start_tree_stages[options.from_measure - 1]
            next_nodes = document.tree.stages[from_stage]
            while next_nodes and len(next_nodes) > 0 and next_nodes[0] != document.tree.root:
                row = []
                new_next_nodes = []
                non_place_holder_in_row = False
                spine_operation_row = False
                for node in next_nodes:
                    if isinstance(node.token, SpineOperationToken):
                        spine_operation_row = True
                        break

                for node in next_nodes:
                    content = ''
                    if isinstance(node.token, HeaderToken) and node.token.encoding in options.spine_types:
                        content = self.export_token(node.token, options)
                        non_place_holder_in_row = True
                    elif spine_operation_row:
                        # either if it is the split operator that has been cancelled, or the join one
                        if isinstance(node.token, SpineOperationToken) and (node.token.is_cancelled_at(
                                from_stage) or node.last_spine_operator_node and node.last_spine_operator_node.token.cancelled_at_stage == node.stage):
                            content = '*'
                        else:
                            content = self.export_token(node.token, options)
                            non_place_holder_in_row = True
                    if content:
                        row.append(content)
                    new_next_nodes.append(node.parent)
                next_nodes = new_next_nodes
                if non_place_holder_in_row:  # if the row contains just place holders due to an ommitted place holder, don't add it
                    rows.insert(0, row)

            # now, export the signatures
            node_signatures = None
            for node in document.tree.stages[from_stage]:
                node_signature_rows = []
                for signature_node in node.last_signature_nodes.nodes.values():
                    if not self.is_signature_cancelled(signature_node, node, from_stage, to_stage):
                        node_signature_rows.append(self.export_token(signature_node.token, options))
                if len(node_signature_rows) > 0:
                    if not node_signatures:
                        node_signatures = []  # an array for each spine
                    else:
                        if len(node_signatures[0]) != len(node_signature_rows):
                            raise Exception(f'Node signature mismatch: multiple spines with signatures at measure {len(rows)}')  # TODO better message
                    node_signatures.append(node_signature_rows)

            if node_signatures:
                for irow in range(len(node_signatures[0])):  # all spines have the same number of rows
                    row = []
                    for icol in range(len(node_signatures)):  #len(node_signatures) = number of spines
                        row.append(node_signatures[icol][irow])
                    rows.append(row)

        else:
            from_stage = 0
            rows = []

        #if not node.token.category == TokenCategory.LINE_COMMENTS and not node.token.category == TokenCategory.FIELD_COMMENTS:
        for stage in range(from_stage, to_stage + 1):  # to_stage included
            row = []
            for node in document.tree.stages[stage]:
                self.append_row(document=document, node=node, options=options, row=row)

            if len(row) > 0:
                rows.append(row)

        # now, add the spine terminate row
        if options.to_measure is not None and len(rows) > 0 and rows[len(rows) - 1][
            0] != '*-':  # if the terminate is not added yet
            spine_count = len(rows[len(rows) - 1])
            row = []
            for i in range(spine_count):
                row.append('*-')
            rows.append(row)

        result = ""
        for row in rows:
            if not empty_row(row):
                result += '\t'.join(row) + '\n'
        return result

    def compute_header_type(self, node) -> Optional[HeaderToken]:
        """
        Compute the header type of the node.

        Args:
            node (Node): The node to compute.

        Returns (Optional[Token]): The header type `Node`object. None if the current node is the header.

        """
        if isinstance(node.token, HeaderToken):
            header_type = node.token
        elif node.header_node:
            header_type = node.header_node.token
        else:
            header_type = None
        return header_type

    def export_token(self, token: Token, options: ExportOptions) -> str:
        if isinstance(token, HeaderToken):
            new_token = HeaderTokenGenerator.new(token=token, type=options.kern_type)
        else:
            new_token = token
        return (TokenizerFactory
                .create(options.kern_type.value, token_categories=options.token_categories)
                .tokenize(new_token))

    def append_row(self, document: Document, node, options: ExportOptions, row: list) -> bool:
        """
        Append a row to the row list if the node accomplishes the requirements.
        Args:
            document (Document): The document with the spines.
            node (Node): The node to append.
            options (ExportOptions): The export options to filter the token.
            row (list): The row to append.

        Returns (bool): True if the row was appended. False if the row was not appended.
        """
        header_type = self.compute_header_type(node)

        if (header_type is not None
                and header_type.encoding in options.spine_types
                and not node.token.hidden
                and (isinstance(node.token, ComplexToken) or node.token.category in options.token_categories)
                and (options.spine_ids is None or header_type.spine_id in options.spine_ids)
        # If None, all the spines will be exported. TODO: put all the spines as spine_ids = None
        ):
            row.append(self.export_token(node.token, options))
            return True

        return False

    def get_spine_types(self, document: Document, spine_types: list = None):
        """
        Get the spine types from the document.

        Args:
            document (Document): The document with the spines.
            spine_types (list): The spine types to export. If None, all the spine types will be exported.

        Returns: A list with the spine types.

        Examples:
            >>> exporter = Exporter()
            >>> exporter.get_spine_types(document)
            ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
            >>> exporter.get_spine_types(document, None)
            ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
            >>> exporter.get_spine_types(document, ['**kern'])
            ['**kern', '**kern', '**kern', '**kern']
            >>> exporter.get_spine_types(document, ['**kern', '**root'])
            ['**kern', '**kern', '**kern', '**kern', '**root']
            >>> exporter.get_spine_types(document, ['**kern', '**root', '**harm'])
            ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
            >>> exporter.get_spine_types(document, [])
            []
        """
        if spine_types is not None and len(spine_types) == 0:
            return []

        options = ExportOptions(spine_types=spine_types, token_categories=[TokenCategory.HEADER])
        content = self.export_string(document, options)

        # Remove all after the first line: **kern, **mens, etc... are always in the first row
        lines = content.split('\n')
        first_line = lines[0:1]
        tokens = first_line[0].split('\t')

        return tokens if tokens not in [[], ['']] else []


    @classmethod
    def export_options_validator(cls, document: Document, options: ExportOptions) -> None:
        """
        Validate the export options. Raise an exception if the options are invalid.

        Args:
            document: `Document` - The document to export.
            options: `ExportOptions` - The options to export the document.

        Returns: None

        Example:
            >>> export_options_validator(document, options)
            ValueError: option from_measure must be >=0 but -1 was found.
            >>> export_options_validator(document, options2)
            None
        """
        if options.from_measure is not None and options.from_measure < 0:
            raise ValueError(f'option from_measure must be >=0 but {options.from_measure} was found. ')
        if options.to_measure is not None and options.to_measure > len(document.measure_start_tree_stages):
            # "TODO: DAVID, check options.to_measure bounds. len(document.measure_start_tree_stages) or len(document.measure_start_tree_stages) - 1"
            raise ValueError(
                f'option to_measure must be <= {len(document.measure_start_tree_stages)} but {options.to_measure} was found. ')
        if options.to_measure is not None and options.from_measure is not None and options.to_measure < options.from_measure:
            raise ValueError(
                f'option to_measure must be >= from_measure but {options.to_measure} < {options.from_measure} was found. ')

    def is_signature_cancelled(self, signature_node, node, from_stage, to_stage) -> bool:
        if node.token.__class__ == signature_node.token.__class__:
            return True
        elif isinstance(node.token, NoteRestToken):
            return False
        elif from_stage < to_stage:
            for child in node.children:
                if self.is_signature_cancelled(signature_node, child, from_stage + 1, to_stage):
                    return True
            return False


def get_kern_from_ekern(ekern_content: str) -> str:
    """
    Read the content of a **ekern file and return the **kern content.

    Args:
        ekern_content: The content of the **ekern file.
    Returns:
        The content of the **kern file.

    Example:
        ```python
        # Read **ekern file
        ekern_file = 'path/to/file.ekrn'
        with open(ekern_file, 'r') as file:
            ekern_content = file.read()

        # Get **kern content
        kern_content = get_kern_from_ekern(ekern_content)
        with open('path/to/file.krn', 'w') as file:
            file.write(kern_content)

        ```
    """
    content = ekern_content.replace("**ekern", "**kern")  # TODO Constante según las cabeceras
    content = content.replace(TOKEN_SEPARATOR, "")
    content = content.replace(DECORATION_SEPARATOR, "")

    return content


def ekern_to_krn(
        input_file: str,
        output_file: str
) -> None:
    """
    Convert one .ekrn file to .krn file.

    Args:
        input_file (str): Filepath to the input **ekern
        output_file (str): Filepath to the output **kern
    Returns:
        None

    Example:
        # Convert .ekrn to .krn
        >>> ekern_to_krn('path/to/file.ekrn', 'path/to/file.krn')

        # Convert a list of .ekrn files to .krn files
        ```python
        ekrn_files = your_modue.get_files()

        # Use the wrapper to avoid stopping the process if an error occurs
        def ekern_to_krn_wrapper(ekern_file, kern_file):
            try:
                ekern_to_krn(ekrn_files, output_folder)
            except Exception as e:
                print(f'Error:{e}')

        # Convert all the files
        for ekern_file in ekrn_files:
            output_file = ekern_file.replace('.ekrn', '.krn')
            ekern_to_krn_wrapper(ekern_file, output_file)
        ```
    """
    with open(input_file, 'r') as file:
        content = file.read()

    kern_content = get_kern_from_ekern(content)

    with open(output_file, 'w') as file:
        file.write(kern_content)


def kern_to_ekern(
        input_file: str,
        output_file: str
) -> None:
    """
    Convert one .krn file to .ekrn file

    Args:
        input_file (str): Filepath to the input **kern
        output_file (str): Filepath to the output **ekern

    Returns:
        None

    Example:
        # Convert .krn to .ekrn
        >>> kern_to_ekern('path/to/file.krn', 'path/to/file.ekrn')

        # Convert a list of .krn files to .ekrn files
        ```python
        krn_files = your_module.get_files()

        # Use the wrapper to avoid stopping the process if an error occurs
        def kern_to_ekern_wrapper(krn_file, ekern_file):
            try:
                kern_to_ekern(krn_file, ekern_file)
            except Exception as e:
                print(f'Error:{e}')

        # Convert all the files
        for krn_file in krn_files:
            output_file = krn_file.replace('.krn', '.ekrn')
            kern_to_ekern_wrapper(krn_file, output_file)
        ```

    """
    importer = Importer()
    document = importer.import_file(input_file)

    if len(importer.errors):
        raise Exception(f'ERROR: {input_file} has errors {importer.get_error_messages()}')

    export_options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES,
                                   kern_type=Encoding.eKern)
    exporter = Exporter()
    exported_ekern = exporter.export_string(document, export_options)

    with open(output_file, 'w') as file:
        file.write(exported_ekern)
