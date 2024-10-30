import csv
import io
from copy import copy

from kernpy.core.tokens import TokenCategory, SignatureToken, MetacommentToken, HeaderToken, SpineOperationToken, \
    FieldCommentToken, ErrorToken, \
    BoundingBoxToken, SPINE_OPERATIONS, HEADERS
from kernpy.core.document import Document, MultistageTree, BoundingBoxMeasures


class Importer:
    """
    Importer class.

    Use this class to import the content from a file or a string to a `Document` object.
    """
    def __init__(self):
        """
        Create an instance of the importer.

        Raises:
            Exception: If the importer content is not a valid **kern file.

        Examples:
            # Create the importer
            >>> importer = Importer()

            # Import the content from a file
            >>> document = importer.import_file('file.krn')

            # Import the content from a string
            >>> document = importer.import_string("**kern\n*clefF4\nc4\n4d\n4e\n4f\n*-")
        """
        self.last_measure_number = None
        self.last_bounding_box = None
        self.errors = []

    @staticmethod
    def get_last_spine_operator(parent):
        if parent is None:
            return None
        elif isinstance(parent.token, SpineOperationToken):
            return parent
        else:
            return parent.last_spine_operator_node

    #TODO Documentar cómo propagamos los header_node y last_spine_operator_node...
    def run(self, reader) -> Document:
        tree = MultistageTree()
        document = Document(tree)
        importers = {}
        header_row_number = None
        row_number = 1
        tree_stage = 0
        next_stage_parents = None
        prev_stage_parents = None
        last_node_previous_to_header = tree.root
        for row in reader:
            if len(row) <= 0:
                # Found an empty row, usually the last one. Ignore it.
                continue

            tree_stage = tree_stage + 1
            is_barline = False
            if next_stage_parents:
                prev_stage_parents = copy(next_stage_parents)
            next_stage_parents = []

            if row[0].startswith("!!"):
                token = MetacommentToken(row[0].strip())
                if header_row_number is None:
                    # it has no header, so it creates the header
                    node = tree.add_node(tree_stage, last_node_previous_to_header, token, None, None, None)
                    last_node_previous_to_header = node
                else:
                    for parent in prev_stage_parents:
                        node = tree.add_node(tree_stage, parent, token, self.get_last_spine_operator(parent), parent.last_signature_nodes, parent.header_node) # the same reference for all spines - TODO Recordar documentarlo
                        next_stage_parents.append(node)
            else:
                for icolumn, column in enumerate(row):
                    if column in HEADERS:
                        if header_row_number is not None and header_row_number != row_number:
                            raise Exception(
                                f"Several header rows not supported, there is a header row in #{header_row_number} and another in #{row_number} ")

                        document.header_stage = tree_stage
                        importer = importers.get(column)
                        if not importer:
                            from kernpy.core.importer_factory import createImporter
                            importer = createImporter(column)
                            importers[column] = importer

                        token = HeaderToken(column, spine_id=icolumn)
                        node = tree.add_node(tree_stage, last_node_previous_to_header, token, None, None)
                        node.header_node = node # this value will be propagated
                        next_stage_parents.append(node)
                    else:
                        if column in SPINE_OPERATIONS:
                            token = SpineOperationToken(column)

                            if icolumn >= len(prev_stage_parents):
                                raise Exception(f'Expected at least {icolumn+1} parents in row {row_number}, but found {len(prev_stage_parents)}: {row}')

                            parent = prev_stage_parents[icolumn]
                            node = tree.add_node(tree_stage, parent, token, self.get_last_spine_operator(parent), parent.last_signature_nodes, parent.header_node)

                            if column == '*-':
                                if node.last_spine_operator_node is not None:
                                    node.last_spine_operator_node.token.cancelled_at_stage = tree_stage
                                pass # it's terminated, no continuation
                            elif column == "*+" or column == "*^":
                                next_stage_parents.append(node)
                                next_stage_parents.append(node) # twice, the next stage two children will have this one as parent
                            elif column == "*v":
                                if node.last_spine_operator_node is not None:
                                    node.last_spine_operator_node.token.cancelled_at_stage = tree_stage

                                if icolumn == 0 or row[icolumn-1] != '*v' or prev_stage_parents[icolumn-1].header_node != prev_stage_parents[icolumn].header_node: # don't collapse two different spines
                                    next_stage_parents.append(node) # just one spine each two
                            else:
                                raise Exception(f'Unknown spine operator {column}')
                        else:  # column is not a spine operation
                            if column.startswith("!"):
                                token = FieldCommentToken(column)
                            else:
                                if prev_stage_parents is None:
                                    raise ValueError(f'The token in column #{icolumn} and row #{row_number - 1}'
                                                     f' was not created correctly. Error detected in '
                                                     f'column #{icolumn} in row #{row_number}. '
                                                     f'Found {column.split(" ")[-1]}. ')
                                parent = prev_stage_parents[icolumn]
                                if not parent:
                                    raise Exception(f'Cannot find a parent node for column #{icolumn} in row {row_number}')
                                if not parent.header_node:
                                    raise Exception(f'Cannot find a header node for column #{icolumn} in row {row_number}')
                                importer = importers.get(parent.header_node.token.encoding)
                                if not importer:
                                    raise Exception(f'Cannot find an importer for header {parent.header_node.token.encoding}')
                                try:
                                    token = importer.import_token(column)
                                except Exception as error:
                                    token = ErrorToken(column, row_number, error)
                                    self.errors.append(token)
                            if not token:
                                raise Exception(
                                    f'No token generated for input {column} in row number #{row_number} using importer {importer}')

                            parent = prev_stage_parents[icolumn]
                            node = tree.add_node(tree_stage, parent, token, self.get_last_spine_operator(parent), parent.last_signature_nodes, parent.header_node)
                            next_stage_parents.append(node)

                            if token.category == TokenCategory.BARLINES or token.category == TokenCategory.CORE and len(
                                    document.measure_start_tree_stages) == 0:
                                is_barline = True
                            elif isinstance(token, BoundingBoxToken):
                                self.handle_bounding_box(document, token)
                            elif isinstance(token, SignatureToken):
                                node.last_signature_nodes.update(node)

                if is_barline:
                    document.measure_start_tree_stages.append(tree_stage)
                    self.last_measure_number = len(document.measure_start_tree_stages)
                    if self.last_bounding_box:
                        self.last_bounding_box.to_measure = self.last_measure_number
            row_number = row_number + 1
        return document

    def handle_bounding_box(self, document: Document, token: BoundingBoxToken):
        page_number = token.page_number
        last_page_bb = document.page_bounding_boxes.get(page_number)
        if last_page_bb is None:
            if self.last_measure_number is None:
                self.last_measure_number = 0
            self.last_bounding_box = BoundingBoxMeasures(token.bounding_box, self.last_measure_number,
                                                         self.last_measure_number)
            document.page_bounding_boxes[page_number] = self.last_bounding_box
        else:
            last_page_bb.bounding_box.extend(token.bounding_box)
            last_page_bb.to_measure = self.last_measure_number

    def import_file(self, file_path: str) -> Document:
        """
        Import the content from the importer to the file.
        Args:
            file_path: The path to the file.

        Returns:
            Document - The document with the imported content.

        Examples:
            # Create the importer and read the file
            >>> importer = Importer()
            >>> importer.import_file('file.krn')
        """
        with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as file:
            reader = csv.reader(file, delimiter='\t')
            return self.run(reader)

    def import_string(self, text: str) -> Document:
        """
        Import the content from the content of the score in string format.

        Args:
            text: The content of the score in string format.

        Returns:
            Document - The document with the imported content.

        Examples:
            # Create the importer and read the file
            >>> importer = Importer()
            >>> importer.import_string("**kern\n*clefF4\nc4\n4d\n4e\n4f\n*-")
            # Read the content from a file
            >>> with open('file.krn',  'r', newline='', encoding='utf-8', errors='ignore') as f: # We encourage you to use these open file options
            >>>     content = f.read()
            >>> importer.import_string(content)
            >>> document = importer.import_string(content)
        """
        lines = text.splitlines()
        reader = csv.reader(lines, delimiter='\t')
        return self.run(reader)

    def get_error_messages(self) -> str:
        """
        Get the error messages of the importer.

        Returns: str - The error messages split by a new line character.

        Examples:
            # Create the importer and read the file
            >>> importer = Importer()
            >>> importer.import_file('file.krn')
            >>> print(importer.get_error_messages())
            'Error: Invalid token in row 1'
        """
        result = ''
        for err in self.errors:
            result += str(err)
            result += '\n'
        return result

    def has_errors(self) -> bool:
        """
        Check if the importer has any errors.

        Returns: bool - True if the importer has errors, False otherwise.

        Examples:
            # Create the importer and read the file
            >>> importer = Importer()
            >>> importer.import_file('file.krn')    # file.krn has an error
            >>> print(importer.has_errors())
            True
            >>> importer.import_file('file2.krn')   # file2.krn has no errors
            >>> print(importer.has_errors())
            False
        """
        return len(self.errors) > 0
