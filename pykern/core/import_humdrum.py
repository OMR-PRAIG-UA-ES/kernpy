import csv
import string
import logging

from .importer_factory import createImporter
from .tokens import HeaderToken, SpineOperationToken, TokenCategory, BoundingBoxToken, KeySignatureToken, \
    TimeSignatureToken, MeterSymbolToken, ClefToken, BarToken


class ExportOptions:
    def __init__(self, spine_types=[], token_categories=[], from_measure=None, to_measure=None):
        """
        :spine_types: **kern, **mens, etc...
        :token_types: TokenCategory
        """
        self.spine_types = spine_types
        self.from_measure = from_measure
        self.to_measure = to_measure
        self.token_categories = token_categories


class BoundingBoxMeasures:
    def __init__(self, bounding_box, from_measure, to_measure):
        self.from_measure = from_measure
        self.to_measure = to_measure
        self.bounding_box = bounding_box


class Spine:
    def __init__(self, spine_type, importer):
        self.spine_type = spine_type  # **mens, **kern, etc...
        self.rows = []  # each row will contain just one item or an array of items of type Token
        self.importer = importer
        self.importing_subspines = 1  # 0 for terminated subspines - used just for importing
        self.next_row_subspine_variation = 0  # when a spine operation is added or removed, the subspines number must be modified for the next row

    def size(self):
        return len(self.rows)

    def isTerminated(self):
        return self.importing_subspines > 0

    def getNumSubspines(self, row_number):
        if row_number < 0:
            raise Exception(f'Negative row number {row_number}')
        if row_number >= len(self.rows):
            raise Exception(f'Row number {row_number} out of bounds {len(self.rows)}')

        return len(self.rows[row_number])

    def addRow(self):
        if self.importing_subspines != 0:  # if not terminated
            self.rows.append([])
            if self.next_row_subspine_variation > 0:
                new_subspines = self.importing_subspines + self.next_row_subspine_variation
            elif self.next_row_subspine_variation < 0:
                new_subspines = self.importing_subspines + (
                            self.next_row_subspine_variation + 1)  # e.g. *v *v *v for three spines lead to 1 spine
            else:
                new_subspines = self.importing_subspines
            logging.debug(f'Adding row to spine, previous subspines={self.importing_subspines}, new={new_subspines}')
            self.importing_subspines = new_subspines
            self.next_row_subspine_variation = 0

    def addToken(self, encoding, token):
        if not encoding:
            raise Exception('Trying to add an empty encoding')

        if not token:
            raise Exception('Trying to add a empty token')

        row = len(self.rows) - 1
        if len(self.rows[row]) >= self.importing_subspines:
            raise Exception(
                f'There are already {len(self.rows[row])} subspines, and this spine should have at most {self.importing_subspines}')

        self.rows[row].append(token)

    def increaseSubspines(self):
        self.next_row_subspine_variation = self.next_row_subspine_variation + 1

    def decreaseSubspines(self):
        self.next_row_subspine_variation = self.next_row_subspine_variation - 1

    def terminate(self):
        self.importing_subspines = 0

    def isFullRow(self):
        if self.importing_subspines == 0:
            return True
        else:
            row = len(self.rows) - 1
            return len(self.rows[row]) >= self.importing_subspines

    def isContentOfType(self, row, clazz):
        self.checkRowIndex(row)
        for subspine in self.rows[row]:
            if isinstance(subspine, clazz):
                return True
        return False

    def checkRowIndex(self, row):
        if row < 0:
            raise Exception(f'Negative row {row}')
        if row >= len(self.rows):
            raise Exception(f'Row {row} out of bounds {len(self.rows)}')

    def getRowContent(self, row, just_encoding: bool, token_categories) -> string:
        self.checkRowIndex(row)

        result = ''
        for subspine in self.rows[row]:
            if subspine.category == TokenCategory.STRUCTURAL or subspine.category in token_categories:
                if len(result) > 0:
                    result += '\t'
                if just_encoding:
                    result += subspine.encoding
                else:
                    if subspine.hidden:
                        exp = '.'
                    else:
                        exp = subspine.export()
                    if not exp:
                        raise Exception(f'Subspine {subspine.encoding} is exported as None')
                    result += exp

        return result

    def getProcessedRow(self, row: int, token_categories) -> string:
        return self.getRowContent(row, False, token_categories)

    def getUnprocessedRow(self, row: int, token_categories) -> string:
        return self.getRowContent(row, True, token_categories)


class Signatures:
    def __init__(self, header_row, clef_row, key_signature_row, time_signature_row, meter_symbol_row):
        self.last_header_row = header_row
        self.last_clef_row = clef_row
        self.last_key_signature_row = key_signature_row
        self.last_time_signature_row = time_signature_row
        self.last_meter_symbol_row = meter_symbol_row


class HumdrumImporter:
    HEADERS = {"**mens", "**kern", "**text", "**harm", "**mxhm", "**root", "**dyn", "**dynam", "**fing"}
    SPINE_OPERATIONS = {"*-", "*+", "*^", "*v"}

    def __init__(self):
        self.spines = []
        self.current_spine_index = 0
        # self.page_start_rows = []
        self.measure_start_rows = []  # starting from 1. Rows after removing empty lines and line comments
        self.page_bounding_boxes = {}
        self.last_measure_number = None
        self.last_bounding_box = None

    def doImportFile(self, file_path: string):
        importers = {}
        header_row_number = None
        row_number = 1
        with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as file:
            reader = csv.reader(file, delimiter='\t')
            for row in reader:
                for spine in self.spines:
                    self.current_spine_index = 0
                    spine.addRow()
                is_barline = False
                if len(row) > 0 and not row[0].startswith("!!"):
                    for column in row:
                        if column in self.HEADERS:
                            if header_row_number is not None and header_row_number != row_number:
                                raise Exception(
                                    f"Several header rows not supported, there is a header row in #{header_row_number} and another in #{row_number} ")

                            header_row_number = row_number
                            importer = importers.get(column)
                            if not importer:
                                importer = createImporter(column)
                                importers[column] = importer
                            spine = Spine(column, importer)
                            token = HeaderToken(column)
                            spine.addRow()
                            spine.addToken(column, token)
                            self.spines.append(spine)
                        else:
                            try:
                                current_spine = self.getNextSpine()
                                logging.debug(
                                    f'Row #{row_number}, current spine #{self.current_spine_index} of size {current_spine.importing_subspines}, and importer {current_spine.importer}')
                            except Exception as e:
                                raise Exception(f'Cannot get next spine at row {row_number}: {e}')

                            if column in self.SPINE_OPERATIONS:
                                current_spine.addToken(column, SpineOperationToken(column))

                                if column == '*-':
                                    current_spine.terminate()
                                elif column == "*+" or column == "*^":
                                    current_spine.increaseSubspines()
                                elif column == "*v":
                                    current_spine.decreaseSubspines()
                            else:
                                token = current_spine.importer.doImport(column)
                                if not token:
                                    raise Exception(
                                        f'No token generated for input {column} in row number #{row_number} using importer {current_spine.importer}')
                                current_spine.addToken(column, token)
                                if token.category == TokenCategory.BARLINES or token.category == TokenCategory.CORE and len(
                                        self.measure_start_rows) == 0:
                                    is_barline = True
                                elif isinstance(token, BoundingBoxToken):
                                    self.handleBoundingBox(token)

                    if is_barline:
                        self.measure_start_rows.append(row_number)
                        self.last_measure_number = len(self.measure_start_rows)
                        if self.last_bounding_box:
                            self.last_bounding_box.to_measure = self.last_measure_number
                    row_number = row_number + 1

    def getSpine(self, index: int) -> Spine:
        if index < 0:
            raise Exception(f'Negative index {index}')
        elif index >= len(self.spines):
            raise Exception(f'Index {index} out of bounds for an array of {len(self.spines)} spines')
        return self.spines[index]

    def getNextSpine(self):
        spine = self.getSpine(self.current_spine_index)
        while spine.isFullRow() and self.current_spine_index < (len(self.spines) - 1):
            self.current_spine_index = self.current_spine_index + 1
            spine = self.getSpine(self.current_spine_index)

        if self.current_spine_index == len(self.spines):
            raise Exception('All spines are full, the spine divisions may be wrong')

        return spine

    def doExportProcessed(self, options: ExportOptions) -> string:
        return self.doExport(True, options)

    def doExportUnprocessed(self, options: ExportOptions) -> string:
        return self.doExport(False, options)

    def handleBoundingBox(self, token: BoundingBoxToken):
        page_number = token.page_number
        last_page_bb = self.page_bounding_boxes.get(page_number)
        if last_page_bb is None:
            print(f'Adding {page_number}')
            if self.last_measure_number is None:
                self.last_measure_number = 0
            self.last_bounding_box = BoundingBoxMeasures(token.bounding_box, self.last_measure_number,
                                                         self.last_measure_number)
            self.page_bounding_boxes[page_number] = self.last_bounding_box
        else:
            print(f'Extending page {page_number}')
            last_page_bb.bounding_box.extend(self.last_bounding_box.bounding_box)
            last_page_bb.to_measure = self.last_measure_number

    def getMaxRows(self):
        return max(spine.size() for spine in self.spines)

    def checkMeasure(self, measure_number):
        if measure_number < 1:
            raise Exception(f'The measure number must be >=1, and it is {measure_number}')

        max_measures = len(self.measure_start_rows)
        if measure_number > max_measures:
            raise Exception(f'The measure number must be <= {max_measures}, and it is {measure_number}')

    def doExport(self, use_processed: bool, options: ExportOptions) -> string:
        max_rows = self.getMaxRows()
        current_signature = Signatures(None, None, None, None, None)
        signatures_at_each_row = []
        row_contents = []

        for i in range(max_rows):
            row_result = ''
            empty = True
            for spine in self.spines:
                if spine.spine_type in options.spine_types:
                    if i < spine.size():  # required because the spine may be terminated
                        if len(row_result) > 0:
                            row_result += '\t'

                        if use_processed:
                            content = spine.getProcessedRow(i, options.token_categories)
                        else:
                            content = spine.getUnprocessedRow(i, options.token_categories)

                        if content and content != '.' and content != '*':
                            empty = False
                            if options.from_measure:  # if not, we don't need to compute this value
                                if spine.isContentOfType(i, HeaderToken):
                                    current_signature.last_header_row = i
                                elif spine.isContentOfType(i, ClefToken):
                                    current_signature.last_clef_row = i
                                elif spine.isContentOfType(i, KeySignatureToken):
                                    current_signature.last_key_signature_row = i
                                elif spine.isContentOfType(i, TimeSignatureToken):
                                    current_signature.last_time_signature_row = i
                                elif spine.isContentOfType(i, MeterSymbolToken):
                                    current_signature.last_meter_symbol_row = i

                        row_result += content
            if not empty:
                row_contents.append(row_result)
            else:
                row_contents.append(None)  # in order to maintain the indexes

            signatures_at_each_row.append(current_signature)

        # if last_header_row is None:
        #     raise Exception('No header row found')
        #
        # if last_clef_row is None:
        #     raise Exception('No clef row found')
        #
        # if last_time_signature_row is None and last_meter_symbol_row is None:
        #     raise Exception('No time signature or meter symbol row found')

        result = ''
        if not options.from_measure and not options.to_measure:
            for row_content in row_contents:
                if row_content:
                    result += row_content
                    result += '\n'
        else:
            if options.from_measure:
                self.checkMeasure(options.from_measure)
            else:
                options.from_measure = 1

            if options.to_measure:
                self.checkMeasure(options.to_measure)
            else:
                options.to_measure = len(self.measure_start_rows)

            from_row = self.measure_start_rows[options.from_measure-1]-1
            to_row = self.measure_start_rows[options.to_measure] # to the next one
            signature = signatures_at_each_row[from_row]

            # first, attach the signatures if not in the exported range
            result = self.addSignatureRowIfRequired(row_contents, result, from_row, signature.last_header_row)
            result = self.addSignatureRowIfRequired(row_contents, result, from_row, signature.last_clef_row)
            result = self.addSignatureRowIfRequired(row_contents, result, from_row, signature.last_key_signature_row)
            result = self.addSignatureRowIfRequired(row_contents, result, from_row, signature.last_time_signature_row)
            result = self.addSignatureRowIfRequired(row_contents, result, from_row, signature.last_meter_symbol_row)

            for row in range(from_row, to_row):
                row_content = row_contents[row]
                if row_content:
                    result += row_content
                    result += '\n'

            if to_row < max_rows:
                row_content = ''
                for spine in self.spines:
                    if spine.spine_type in options.spine_types and not spine.isTerminated():
                        if len(row_content) > 0:
                            row_content += '\t'
                        row_content += '*-'
                result += row_content
                result += '\n'
        return result

    def addSignatureRowIfRequired(self, row_contents, result, from_row, signature_row):
        if signature_row is not None and signature_row < from_row:
            srow = row_contents[signature_row]
            result += srow
            result += '\n'
        return result
