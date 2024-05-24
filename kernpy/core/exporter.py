import string
from enum import Enum

from kernpy.core import Document, SpineOperationToken, HeaderToken, Importer, TokenCategory, InstrumentToken

BEKERN_CATEGORIES = [TokenCategory.STRUCTURAL, TokenCategory.CORE, TokenCategory.EMPTY, TokenCategory.SIGNATURES,
                     TokenCategory.BARLINES, TokenCategory.ENGRAVED_SYMBOLS]


class KernTypeExporter(Enum):  # TODO: Eventually, polymorphism will be used to export different types of kern files
    """
    Options for exporting a kern file.

    Example:
        # Create the importer
        >>> hi = Importer()

        # Read the file
        >>> document = hi.import_file('file.krn')

        # Export the file
        >>> options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES, kernType=KernTypeExporter.normalizedKern)
        >>> exporter = Exporter()
        >>> exported = exporter.export_string(options)

    """
    unprocessed = 0
    eKern = 1
    normalizedKern = 2


class ExportOptions:
    """
    `ExportOptions` class.

    Store the options to export a **kern file.
    """
    def __init__(self, spine_types=None, token_categories=None, from_measure: int = None, to_measure: int = None,
                 kern_type: KernTypeExporter = KernTypeExporter.normalizedKern, instruments=None):
        """
        Create a new ExportOptions object.

        Args:
            spine_types (Iterable): **kern, **mens, etc...
            token_categories (Iterable): TokenCategory
            from_measure (int): The measure to start exporting. When None, the exporter will start from the beginning of the file.
            to_measure (int): The measure to end exporting. When None, the exporter will end at the end of the file.
            kern_type (KernTypeExporter): The type of the kern file to export.
            instruments (Iterable): The instruments to export. When None, all the instruments will be exported.


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
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES, kern_type=KernTypeExporter.eKern)
            >>> exported_data = exporter.export_string(document, options)

        """
        self.spine_types = spine_types or []
        self.from_measure = from_measure
        self.to_measure = to_measure
        self.token_categories = token_categories or []
        self.kern_type = kern_type
        self.instruments = instruments or []


def empty_row(row):
    for col in row:
        if col != '.' and col != '' and col != '*':
            return False
    return True


class Exporter:
    def do_export_normalized_kern(self, document: Document, options: ExportOptions) -> string:
        options.kern_type = KernTypeExporter.normalizedKern
        return self.export_string(document, options)

    def do_export_ekern(self, document: Document, options: ExportOptions) -> string:
        options.kern_type = KernTypeExporter.eKern
        return self.export_string(document, options)

    def do_export_unprocessed(self, document: Document, options: ExportOptions) -> string:
        options.kern_type = KernTypeExporter.unprocessed
        return self.export_string(document, options)

    def export_string(self, document: Document, options: ExportOptions) -> string:
        Exporter.export_options_validator(document, options)

        rows = []
        if options.from_measure:
            # In case of beginning not from the first measure, we recover the spine creation and the headers
            # Traversed in reverse order to only include the active spines at the given measure...
            from_stage = document.measure_start_tree_stages[options.from_measure]
            next_nodes = document.tree.stages[from_stage]
            while next_nodes and len(next_nodes) > 0 and next_nodes[0] != document.tree.root:
                row = []
                new_next_nodes = []
                non_place_holder_in_row = False
                for node in next_nodes:
                    content = ''
                    if isinstance(node.token, HeaderToken):
                        content = node.token.export()
                        non_place_holder_in_row = True
                    elif isinstance(node.token, SpineOperationToken):
                        if node.token.is_cancelled_at(from_stage):
                            content = '*'
                        else:
                            content = node.token.export()
                            non_place_holder_in_row = True
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
                    node_signature_rows.append(signature_node.token.export())
                if not node_signatures:
                    node_signatures = []  # an array for each spine
                else:
                    if len(node_signatures[0]) != len(node_signature_rows):
                        raise Exception('Node signature mismatch')  # TODO better message
                    node_signature_rows.append(node_signature_rows)

            if node_signatures:
                row = []
                for irow in range(0, len(node_signatures[0])):  # all spines have the same number of rows
                    for icol in range(0, len(node_signatures)):  #len(node_signatures) = number of spines
                        row.append(node_signatures[icol][irow].token.export())
                rows.append(row)

        else:
            from_stage = 0
            rows = []

        if options.to_measure and len(document.measure_start_tree_stages) < options.from_measure:
            to_stage = document.measure_start_tree_stages[options.to_measure + 1]
        else:
            to_stage = len(document.tree.stages)  # all stages

        #if not node.token.category == TokenCategory.LINE_COMMENTS and not node.token.category == TokenCategory.FIELD_COMMENTS:
        for stage in range(from_stage, to_stage):
            row = []

            for node in document.tree.stages[stage]:
                if isinstance(node.token, HeaderToken):
                    header_type = node.token.encoding
                elif node.header_node:
                    header_type = node.header_node.token.encoding
                else:
                    header_type = None

                if header_type and header_type in options.spine_types and not node.token.hidden and \
                        (not options.token_categories or node.token.category in options.token_categories):
                    row.append(node.token.export())

            if len(row) > 0:
                rows.append(row)

        result = ""
        for row in rows:
            if not empty_row(row):
                result += '\t'.join(row) + '\n'
        return result

    @staticmethod
    def export_options_validator(document: Document, options: ExportOptions) -> None:
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

def get_kern_from_ekern(ekern_content: string) -> string:
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
    content = content.replace(kernpy.core.TOKEN_SEPARATOR, "")
    content = content.replace(kernpy.core.DECORATION_SEPARATOR, "")

    return content


def ekern_to_krn(input_file, output_file) -> None:
    """
    Convert one .ekrn file to .krn file.

    Args:
        input_file: Filepath to the input **ekern
        output_file: Filepath to the output **kern
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


def kern_to_ekern(input_file, output_file) -> None:
    """
    Convert one .krn file to .ekrn file

    Args:
        input_file: Filepath to the input **kern
        output_file: Filepath to the output **ekern

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
                                   kern_type=KernTypeExporter.eKern)
    exporter = Exporter()
    exported_ekern = exporter.export_string(document, export_options)

    with open(output_file, 'w') as file:
        file.write(exported_ekern)
