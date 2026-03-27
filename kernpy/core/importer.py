from __future__ import annotations

import csv
import io
from copy import copy
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from kernpy.core.tokens import TokenCategory, SignatureToken, MetacommentToken, HeaderToken, SpineOperationToken, \
    FieldCommentToken, \
    BoundingBoxToken, SPINE_OPERATIONS, HEADERS, Token, TimeSignatureToken, NoteRestToken, Subtoken
from kernpy.core.document import Document, MultistageTree, BoundingBoxMeasures
from kernpy.core.importer_factory import createImporter
from kernpy.core.measure_signature_validators import MeasureSignatureValidator, HorizontalRhythmValidator

class Importer:
    """
    Importer class.

    Use this class to import the content from a file or a string to a `Document` object.
    """
    def __init__(
            self,
            *,
            error_on_duration_mismatch: bool = False,
            meter_signature_fallback_if_not_found: Optional[str] = None,
    ):
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

        self._tree = MultistageTree()
        self._document = Document(self._tree)
        self._importers = {}
        self._header_row_number = None
        self._row_number = 1
        self._tree_stage = 0
        self._next_stage_parents = None
        self._prev_stage_parents = None
        self._last_node_previous_to_header = self._tree.root
        self._terminated_spine_columns = {}
        self._error_on_duration_mismatch = error_on_duration_mismatch
        self._meter_signature_fallback_if_not_found = meter_signature_fallback_if_not_found
        self._current_measure_durations_by_column: Dict[int, List[Subtoken]] = {}
        self._current_measure_signature_by_column: Dict[int, str] = {}
        self._measure_duration_validation_memo: Dict[Tuple[str, Tuple[str, ...]], Tuple[bool, str]] = {}
        self._seen_first_barline = False
        # Horizontal rhythm validation: track token types per spine
        self._current_measure_tokens_by_column: Dict[int, List[Token | Subtoken]] = {}

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
        for row in reader:
            if len(row) <= 0:
                # Found an empty row, usually the last one. Ignore it.
                continue

            self._tree_stage = self._tree_stage + 1
            measure_start_stage = None
            if self._next_stage_parents:
                self._prev_stage_parents = copy(self._next_stage_parents)
            self._next_stage_parents = []

            if row[0].startswith("!!"):
                self._compute_metacomment_token(row[0].strip())
            else:
                for icolumn, column in enumerate(row):
                    if icolumn in self._terminated_spine_columns:
                        terminated_row = self._terminated_spine_columns[icolumn]
                        raise ValueError(
                            f'Token found in column #{icolumn} and row #{self._row_number} '
                            f'after an end-of-program token (*-) in row #{terminated_row}. '
                            f'Found {column}.'
                        )

                    if column.startswith("**"):
                        self._compute_header_token(icolumn, column)
                        # go to next row
                        continue

                    if column in SPINE_OPERATIONS:
                        self._compute_spine_operator_token(icolumn, column, row)
                    else:  # column is not a spine operation
                        if column.startswith("!"):
                            token = FieldCommentToken(column)
                        else:
                            if self._prev_stage_parents is None:
                                raise ValueError(f'Any spine header found in the column #{icolumn}. '
                                                 f'Expected a previous line with valid content. '
                                                 f'The token in column #{icolumn} and row #{self._row_number - 1}'
                                                 f' was not created correctly. Error detected in '
                                                 f'column #{icolumn} in row #{self._row_number}. '
                                                 f'Found {column}. ')
                            if icolumn >= len(self._prev_stage_parents):
                                # TODO: Try to fix the kern in runtime. Add options to public API
                                # continue  # ignore the column
                                raise ValueError(f'Wrong columns number in row {self._row_number}. '
                                                 f'The token in column #{icolumn} and row #{self._row_number}'
                                                 f' has more columns than expected in its row. '
                                                 f'Expected {len(self._prev_stage_parents)} columns '
                                                 f'but found {len(row)}.')
                            parent = self._prev_stage_parents[icolumn]
                            if not parent:
                                raise Exception(f'Cannot find a parent node for column #{icolumn} in row {self._row_number}')
                            if not parent.header_node:
                                raise Exception(f'Cannot find a header node for column #{icolumn} in row {self._row_number}')
                            importer = self._importers.get(parent.header_node.token.encoding)
                            if not importer:
                                raise Exception(f'Cannot find an importer for header {parent.header_node.token.encoding}')
                            try:
                                token = importer.import_token(column)
                            except Exception as error:
                                original_error = str(error).strip() or type(error).__name__
                                formatted_message = (
                                    f"Invalid token at row {self._row_number}, column {icolumn} (spine #{icolumn}): "
                                    f"'{column}'. Parsing detail: {original_error}"
                                )
                                self.errors.append(formatted_message)
                                raise ValueError(formatted_message) from error
                        if not token:
                            raise Exception(
                                f'No token generated for input {column} in row number #{self._row_number} using importer {importer}')

                        parent = self._prev_stage_parents[icolumn]
                        node = self._tree.add_node(self._tree_stage, parent, token, self.get_last_spine_operator(parent), parent.last_signature_nodes, parent.header_node)
                        self._next_stage_parents.append(node)

                        self._track_measure_validation_state(column_index=icolumn, token=token)

                        if token.category == TokenCategory.BARLINES:
                            measure_start_stage = self._tree_stage + 1
                            self._seen_first_barline = True
                        elif (
                            not self._seen_first_barline
                            and TokenCategory.is_child(child=token.category, parent=TokenCategory.CORE)
                            and len(self._document.measure_start_tree_stages) == 0
                        ):
                            # Scores without an opening barline still need a first measure start.
                            measure_start_stage = self._tree_stage
                        elif isinstance(token, BoundingBoxToken):
                            self.handle_bounding_box(self._document, token)
                        elif isinstance(token, SignatureToken):
                            node.last_signature_nodes.update(node)

                if measure_start_stage is not None:
                    self._document.measure_start_tree_stages.append(measure_start_stage)
                    self.last_measure_number = len(self._document.measure_start_tree_stages)
                    if self.last_bounding_box:
                        self.last_bounding_box.to_measure = self.last_measure_number
            self._row_number = self._row_number + 1

        last_stage_index = len(self._tree.stages) - 1
        self._document.measure_start_tree_stages = [
            stage for stage in self._document.measure_start_tree_stages
            if stage <= last_stage_index
        ]

        self._validate_pending_measures_at_end()
        return self._document

    def _track_measure_validation_state(self, column_index: int, token: Token):
        if not self._error_on_duration_mismatch:
            return

        if isinstance(token, TimeSignatureToken):
            self._current_measure_signature_by_column[column_index] = token.encoding
            return

        if token.category == TokenCategory.BARLINES:
            measure_index = len(self._document.measure_start_tree_stages)
            self._validate_measure_for_column(column_index=column_index, measure_index=measure_index)
            if self._is_last_column_in_row(column_index):
                self._validate_horizontal_measure_for_all_columns(measure_index=measure_index)
            return

        if isinstance(token, NoteRestToken):
            tokens = self._current_measure_tokens_by_column.setdefault(column_index, [])
            tokens.append(token)
            duration_subtokens = MeasureSignatureValidator._extract_rhythm_subtokens(token)
            if len(duration_subtokens) > 0:
                durations = self._current_measure_durations_by_column.setdefault(column_index, [])
                durations.extend(duration_subtokens)
            return

        if token.category == TokenCategory.EMPTY:
            tokens = self._current_measure_tokens_by_column.setdefault(column_index, [])
            tokens.append(Subtoken(".", TokenCategory.EMPTY))

    def _validate_pending_measures_at_end(self):
        if not self._error_on_duration_mismatch:
            return

        measure_index = len(self._document.measure_start_tree_stages)
        for column_index in list(self._current_measure_durations_by_column.keys()):
            self._validate_measure_for_column(column_index=column_index, measure_index=measure_index)
        self._validate_horizontal_measure_for_all_columns(measure_index=measure_index)

    def _validate_measure_for_column(self, *, column_index: int, measure_index: int):
        durations = self._current_measure_durations_by_column.get(column_index)
        if not durations:
            return

        signature_encoding = self._current_measure_signature_by_column.get(column_index)
        if signature_encoding is None:
            signature_encoding = self._meter_signature_fallback_if_not_found

        if signature_encoding is None:
            raise ValueError(
                f"No time signature available for column #{column_index} at measure #{measure_index}, "
                "and no fallback signature was provided."
            )

        duration_pattern = self._duration_pattern_from_subtokens(durations)
        memo_key = (signature_encoding, duration_pattern)
        result = self._measure_duration_validation_memo.get(memo_key)
        if result is None:
            validator = self.get_measure_signature_validator(signature_encoding)
            result = validator.assert_measure(
                durations,
                measure_index=measure_index,
                spine_index=column_index,
            )
            self._measure_duration_validation_memo[memo_key] = result

        is_valid, error_message = result
        if not is_valid:
            raise ValueError(error_message)

        self._current_measure_durations_by_column[column_index] = []

    def get_measure_signature_validator(self, signature_encoding: str) -> MeasureSignatureValidator:
        return MeasureSignatureValidator(TimeSignatureToken(signature_encoding))

    def _is_last_column_in_row(self, column_index: int) -> bool:
        if self._prev_stage_parents is None:
            return True
        return column_index == len(self._prev_stage_parents) - 1

    def _validate_horizontal_measure_for_all_columns(self, *, measure_index: int):
        if len(self._current_measure_tokens_by_column) == 0:
            return

        sorted_columns = sorted(self._current_measure_tokens_by_column.keys())
        spines_tokens: List[List[Token | Subtoken]] = []
        for column_index in sorted_columns:
            spines_tokens.append(self._current_measure_tokens_by_column.get(column_index, []))

        signature_encoding = None
        for column_index in sorted_columns:
            signature_encoding = self._current_measure_signature_by_column.get(column_index)
            if signature_encoding is not None:
                break
        if signature_encoding is None:
            signature_encoding = self._meter_signature_fallback_if_not_found

        if signature_encoding is None:
            raise ValueError(
                f"No time signature available for horizontal validation at measure #{measure_index}, "
                "and no fallback signature was provided."
            )

        is_valid, error_message = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=spines_tokens,
            meter_signature=signature_encoding,
            measure_index=measure_index,
        )
        if not is_valid:
            raise ValueError(error_message)

        for column_index in sorted_columns:
            self._current_measure_tokens_by_column[column_index] = []

    @staticmethod
    def _duration_pattern_from_subtokens(duration_subtokens: Sequence[Subtoken]) -> Tuple[str, ...]:
        return tuple(subtoken.encoding for subtoken in duration_subtokens)

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

    def import_file(self, file_path: Path) -> Document:
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
            >>> importer.import_file(Path('file.krn'))
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
            >>> importer.import_file(Path('file.krn'))    # file.krn has an error
            >>> print(importer.has_errors())
            True
            >>> importer.import_file(Path('file2.krn'))   # file2.krn has no errors
            >>> print(importer.has_errors())
            False
        """
        return len(self.errors) > 0

    def _compute_metacomment_token(self, raw_token: str):
        token = MetacommentToken(raw_token)
        if self._header_row_number is None:
            node = self._tree.add_node(self._tree_stage, self._last_node_previous_to_header, token, None, None, None)
            self._last_node_previous_to_header = node
        else:
            for parent in self._prev_stage_parents:
                node = self._tree.add_node(self._tree_stage, parent, token, self.get_last_spine_operator(parent), parent.last_signature_nodes, parent.header_node) # the same reference for all spines - TODO Recordar documentarlo
                self._next_stage_parents.append(node)

    def _compute_header_token(self, column_index: int, column_content: str):
        if self._header_row_number is not None and self._header_row_number != self._row_number:
            raise Exception(
                f"Several header rows not supported, there is a header row in #{self._header_row_number} and another in #{self._row_number} ")

            # it's a spine header
        self._document.header_stage = self._tree_stage
        importer = self._importers.get(column_content)
        if not importer:
            importer = createImporter(column_content)
            self._importers[column_content] = importer

        token = HeaderToken(column_content, spine_id=column_index)
        node = self._tree.add_node(self._tree_stage, self._last_node_previous_to_header, token, None, None)
        node.header_node = node # this value will be propagated
        self._next_stage_parents.append(node)
        self._terminated_spine_columns = {}

    def _compute_spine_operator_token(self, column_index: int, column_content: str, row: List[str]):
        token = SpineOperationToken(column_content)

        if column_index >= len(self._prev_stage_parents):
            raise Exception(f'Expected at least {column_index+1} parents in row {self._row_number}, but found {len(self._prev_stage_parents)}: {row}')

        parent = self._prev_stage_parents[column_index]
        node = self._tree.add_node(self._tree_stage, parent, token, self.get_last_spine_operator(parent), parent.last_signature_nodes, parent.header_node)

        if column_content == '*-':
            self._terminated_spine_columns[column_index] = self._row_number
            if node.last_spine_operator_node is not None:
                node.last_spine_operator_node.token.cancelled_at_stage = self._tree_stage
            pass # it's terminated, no continuation
        elif column_content == "*+" or column_content == "*^":
            self._next_stage_parents.append(node)
            self._next_stage_parents.append(node) # twice, the next stage two children will have this one as parent
        elif column_content == "*v":
            if node.last_spine_operator_node is not None:
                node.last_spine_operator_node.token.cancelled_at_stage = self._tree_stage

            if column_index == 0 or row[column_index-1] != '*v' or self._prev_stage_parents[column_index-1].header_node != self._prev_stage_parents[column_index].header_node: # don't collapse two different spines
                self._next_stage_parents.append(node) # just one spine each two
        else:
            raise Exception(f'Unknown spine operation in column #{column_content} and row #{self._row_number}')
