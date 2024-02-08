import csv
import string

from src.importer_factory import createImporter


class Spine:
    def __init__(self, header, importer):
        self.header = header  # **mens, **kern, etc...
        self.processed_rows = []  # each row will contain just one item or an array of items
        self.unprocessed_rows = []  # each row will contain just one item or an array of items
        self.importer = importer
        self.subspines = 1  # 0 for terminated subspines

    def size(self):
        return len(self.processed_rows)

    def addRow(self):
        if self.subspines != 0: # if not terminated
            self.processed_rows.append([])
            self.unprocessed_rows.append([])

    def addToken(self, unprocessed_token, processed_token):
        if not unprocessed_token:
            raise Exception('Trying to add a None unprocessed token')

        if not processed_token:
            raise Exception('Trying to add a None processed token')

        row = len(self.processed_rows)-1
        if len(self.processed_rows[row]) >= self.subspines:
            raise Exception(
                f'There are already {len(self.processed_rows[row])} subspines, and this spine should have at most {self.subspines}')
        self.processed_rows[row].append(processed_token)
        self.unprocessed_rows[row].append(unprocessed_token)

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
            row = len(self.processed_rows)-1
            return len(self.processed_rows[row]) >= self.subspines

    def getRowContent(self, row, content_array) -> string:
        if row < 0:
            raise Exception(f'Negative row {row}')
        if row >= len(content_array):
            raise Exception(f'Row {row} out of bounds {len(content_array)}')

        result = ''
        for subspine in content_array[row]:
            if len(result) > 0:
                result += '\t'
            result += subspine

        return result

    def getProcessedRow(self, row: int) -> string:
        return self.getRowContent(row, self.processed_rows)

    def getUnprocessedRow(self, row: int) -> string:
        return self.getRowContent(row, self.unprocessed_rows)


class HumdrumImporter:
    HEADERS = {"**mens", "**kern", "**text", "**harm", "**mxhm", "**root", "**dyn", "**dynam", "**fing"}

    def __init__(self):
        self.spines = []
        self.current_spine_index = 0

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
                            extended_header = '**e' + column[2:] # remove the **, and append the e
                            spine.addRow()
                            spine.addToken(column, extended_header)
                            self.spines.append(spine)
                        else:
                            try:
                                current_spine = self.getNextSpine()
                            except ValueError:
                                raise Exception(f'Cannot get next spine at row {row_number}: {ValueError}')
                            processed_token = current_spine.importer.doImport(column)
                            current_spine.addToken(column, processed_token)

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

    def doExportProcessed(self) -> string:
        return self.doExport(True)

    def doExportUnprocessed(self) -> string:
        return self.doExport(False)

    def doExport(self, use_processed: bool) -> string:
        result = ''
        max_rows = max(spine.size() for spine in self.spines)
        for i in range(max_rows):
            first_col = True
            for spine in self.spines:
                if i < spine.size():
                    if first_col:
                        first_col = False
                    else:
                        result += '\t'

                    if use_processed:
                        content = spine.getProcessedRow(i)
                    else:
                        content = spine.getUnprocessedRow(i)

                    result += content
            result += '\n'

        return result
