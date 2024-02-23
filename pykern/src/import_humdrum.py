import csv
import string

from src.importer_factory import createImporter
from src.tokens import HeaderToken, SpineOperationToken, TokenCategory, BoundingBoxToken


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
        self.subspines = 1  # 0 for terminated subspines

    def size(self):
        return len(self.rows)

    def addRow(self):
        if self.subspines != 0: # if not terminated
            self.rows.append([])

    def addToken(self, encoding, token):
        if not encoding:
            raise Exception('Trying to add an empty encoding')

        if not token:
            raise Exception('Trying to add a empty token')

        row = len(self.rows)-1
        if len(self.rows[row]) >= self.subspines:
            raise Exception(
                f'There are already {len(self.rows[row])} subspines, and this spine should have at most {self.subspines}')

        self.rows[row].append(token)

    def increaseSubspines(self):
        self.subspines = self.subspines + 1

    def decreaseSubspines(self):
        self.subspines = self.subspines + 1

    def terminate(self):
        self.subspines = 0

    def isFullRow(self):
        if self.subspines == 0:
            return True
        else:
            row = len(self.rows)-1
            return len(self.rows[row]) >= self.subspines

    def getRowContent(self, row, just_encoding: bool, token_categories) -> string:
        if row < 0:
            raise Exception(f'Negative row {row}')
        if row >= len(self.rows):
            raise Exception(f'Row {row} out of bounds {len(self.rows)}')

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


class HumdrumImporter:
    HEADERS = {"**mens", "**kern", "**text", "**harm", "**mxhm", "**root", "**dyn", "**dynam", "**fing"}
    SPINE_OPERATIONS = {"*-", "*+", "*^", "*v"}

    def __init__(self):
        self.spines = []
        self.current_spine_index = 0
        #self.page_start_rows = []
        self.measure_start_rows = [] # starting from 1
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
                for column in row:
                    if not column.startswith("!!"):
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
                            except ValueError:
                                raise Exception(f'Cannot get next spine at row {row_number}: {ValueError}')

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
                                    raise Exception(f'No token generated for input {column}')
                                current_spine.addToken(column, token)
                                if token.category == TokenCategory.BARLINES or token.category == TokenCategory.CORE and len(self.measure_start_rows) == 0:
                                    is_barline = True
                                elif isinstance(token, BoundingBoxToken):
                                    self.handleBoundingBox(token)

                if is_barline:
                    self.measure_start_rows.append(row_number)
                    self.last_measure_number = len(self.measure_start_rows)
                    if self.last_bounding_box:
                        self.last_bounding_box.to_measure = self.last_measure_number
                row_number = row_number + 1

    def getSpine(self, index: int)->Spine:
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
            self.last_bounding_box = BoundingBoxMeasures(token.bounding_box, self.last_measure_number, self.last_measure_number)
            self.page_bounding_boxes[page_number] = self.last_bounding_box
        else:
            print(f'Extending page {page_number}')
            last_page_bb.bounding_box.extend(self.last_bounding_box.bounding_box)
            last_page_bb.to_measure = self.last_measure_number

    def doExport(self, use_processed: bool, options: ExportOptions) -> string:
        result = ''
        max_rows = max(spine.size() for spine in self.spines)
        for i in range(max_rows):
            row_result = ''
            empty = True
            for spine in self.spines:
                if spine.spine_type in options.spine_types:
                    if i < spine.size(): # required because the spine may be terminated
                        if len(row_result) > 0:
                            row_result += '\t'

                        if use_processed:
                            content = spine.getProcessedRow(i, options.token_categories)
                        else:
                            content = spine.getUnprocessedRow(i, options.token_categories)

                        if content and content != '.' and content != '*':
                            empty = False

                        row_result += content
            if not empty:
                result += row_result
                result += '\n'

        return result

