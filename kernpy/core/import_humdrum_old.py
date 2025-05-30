import csv
import string
import logging
from collections.abc import Iterable
from enum import Enum

from .importer_factory import createImporter
from .tokens import HeaderToken, SpineOperationToken, TokenCategory, BoundingBoxToken, KeySignatureToken, \
    TimeSignatureToken, MeterSymbolToken, ClefToken, BarToken, MetacommentToken, ErrorToken, FieldCommentToken, \
    BEKERN_CATEGORIES, TOKEN_SEPARATOR, DECORATION_SEPARATOR


class Encoding(Enum):  # TODO: Eventually, polymorphism will be used to export different types of kern files
    """
    Options for exporting a kern file.

    Example:
        # Create the importer
        >>> hi = HumdrumImporter()

        # Read the file
        >>> hi.import_file('file.krn')

        # Export the file
        >>> options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES, kernType=Encoding.normalizedKern)
        >>> exported = hi.doExport(options)

    """
    unprocessed = 0
    eKern = 1
    normalizedKern = 2


class ExportOptions:
    def __init__(self, spine_types=None, token_categories=None, from_measure: int = None, to_measure: int = None, kern_type: Encoding = Encoding.normalizedKern, instruments=None):
        """
        Create a new ExportOptions object.

        Args:
            spine_types (Iterable): **kern, **mens, etc...
            token_categories (Iterable): TokenCategory
            from_measure (int): The measure to start exporting. When None, the exporter will start from the beginning of the file.
            to_measure (int): The measure to end exporting. When None, the exporter will end at the end of the file.
            kern_type (Encoding): The type of the kern file to export.
            instruments (Iterable): The instruments to export. When None, all the instruments will be exported.


        Example:
            >>> from kernpy import HumdrumImporter, ExportOptions

            Create the importer and read the file
            >>> hi = HumdrumImporter()
            >>> hi.import_file('file.krn')

            Export the file with the specified options
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
            >>> exported_data = hi.doExport(options)

            Export only the lyirics
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=[TokenCategory.LYRICS])
            >>> exported_data = hi.doExport(options)

            Export the comments
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=[TokenCategory.LINE_COMMENTS, TokenCategory.FIELD_COMMENTS])
            >>> exported_data = hi.doExport(options)

            Export using the eKern version
            >>> options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES, kern_type=Encoding.eKern)
            >>> exported_data = hi.doExport(options)

        """
        self.spine_types = spine_types or []
        self.from_measure = from_measure
        self.to_measure = to_measure
        self.token_categories = token_categories or []
        self.kern_type = kern_type
        self.instruments = instruments or []


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

    def __len__(self):
        return self.size()

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

    def addToken(self, token):
        if not token:
            raise Exception('Trying to add a empty token')

        row = len(self.rows) - 1
        if not isinstance(token, MetacommentToken) and len(self.rows[row]) >= self.importing_subspines:
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

    def getRowContent(self, row, kern_type: Encoding, token_categories: Iterable) -> string:
        self.checkRowIndex(row)

        result = ''
        for subspine in self.rows[row]:
            if subspine.category == TokenCategory.STRUCTURAL or subspine.category in token_categories:
                if len(result) > 0:
                    result += '\t'
                if kern_type == Encoding.unprocessed:
                    result += subspine.encoding
                elif kern_type in {Encoding.eKern, Encoding.normalizedKern}:
                    if subspine.hidden:
                        exp = '.'
                    else:
                        exp = subspine.export()
                        if kern_type == Encoding.normalizedKern:
                            exp = get_kern_from_ekern(exp)
                    if not exp:
                        raise Exception(f'Subspine {subspine.encoding} is exported as None')
                    result += exp
                else:
                    raise ValueError(f'Unknown kern type {kern_type}.\nView {help(Encoding)} ')

        return result


class Signatures:
    def __init__(self, header_row, clef_row, key_signature_row, time_signature_row, meter_symbol_row):
        self.last_header_row = header_row
        self.last_clef_row = clef_row
        self.last_key_signature_row = key_signature_row
        self.last_time_signature_row = time_signature_row
        self.last_meter_symbol_row = meter_symbol_row

    def clone(self):
        return Signatures(self.last_header_row, self.last_clef_row, self.last_key_signature_row,
                          self.last_time_signature_row, self.last_meter_symbol_row)


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
        self.errors = []

    def getMetacomments(self, KeyComment: str = None, clean: bool = True):  # each metacomment is contained in all spines as a reference to the same object
        """
        Get the metacomments of the file.

        Args:
            KeyComment: The key of the metacomment. (optional).\
                If not specified, all the metacomments will be returned.
                If specified, all the content of the metacomment with the specified key will be returned.
            clean: If True, the metacomments will be returned applying a .strip(). Only valid if KeyComment is not None.

        Returns:
            A list with the metacomments.\
                if KeyComment is not None, a list be returned anyway. \
                If there are no metacomments with the specified key, an empty list will be returned.

        Example:
            >>> from kernpy import HumdrumImporter
            >>> importer = HumdrumImporter()

            # Read the file
            >>> importer.import_file('file.krn')

            # Get all the metacomments
            >>> all_metacomments = importer.getMetacomments()
            # ... modify the metacomments using your own logic

            # Get the metacomments with the key: get the composer:
            >>> composer = importer.getMetacomments(KeyComment='!!!COM')

            # check if your kern file format is compatible with the expected format. If it is not, do not clen it:
            >>> raw_compose = importer.getMetacomments(KeyComment='!!!COM', clean=False)

        """
        result = []
        for token in self.spines[0].rows:
            if isinstance(token[0], MetacommentToken):
                if clean:
                    result.append(token[0].encoding.strip())
                else:
                    result.append(token[0].encoding)

        if KeyComment is not None:
            clean_rows = [row.replace('!!!', '').replace('!!', '') for row in result]
            filtered_rows = [row for row in clean_rows if row.startswith(KeyComment)]
            valid_rows = [row.replace(KeyComment, '').strip()[2:] for row in filtered_rows] if clean else filtered_rows
            return valid_rows

        return result

    def doImport(self, reader):
        importers = {}
        header_row_number = None
        row_number = 1
        pending_metacomments = []  # those appearing before the headers
        for row in reader:
            for spine in self.spines:
                self.current_spine_index = 0
                spine.addRow()
            if len(row) > 0:  # the last one
                if row[0].startswith("!!"):
                    mt = MetacommentToken(row[0])
                    if len(self.spines) == 0:
                        pending_metacomments.append(mt)
                    else:
                        for spine in self.spines:
                            spine.addToken(mt)  # the same reference for all spines
                else:
                    is_barline = False
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
                            spine = Spine(column, importer) # TODO: Add instrument
                            for pending_metacomment in pending_metacomments:
                                spine.addRow()
                                spine.addToken(pending_metacomment)  # same reference for all spines

                            token = HeaderToken(column)
                            spine.addRow()
                            spine.addToken(token)
                            self.spines.append(spine)
                        else:
                            try:
                                current_spine = self.getNextSpine()
                                logging.debug(
                                    f'Row #{row_number}, current spine #{self.current_spine_index} of size {current_spine.importing_subspines}, and importer {current_spine.importer}')
                            except Exception as e:
                                raise Exception(
                                    f'Cannot get next spine at row {row_number}: {e} while reading row {row} ')

                            if column in self.SPINE_OPERATIONS:
                                current_spine.addToken(SpineOperationToken(column))

                                if column == '*-':
                                    current_spine.terminate()
                                elif column == "*+" or column == "*^":
                                    current_spine.increaseSubspines()
                                elif column == "*v":
                                    current_spine.decreaseSubspines()
                            else:
                                if column.startswith("!"):
                                    token = FieldCommentToken(column)
                                else:
                                    try:
                                        token = current_spine.importer.run(column)
                                    except Exception as error:
                                        token = ErrorToken(column, row_number, error)
                                        self.errors.append(token)
                                if not token:
                                    raise Exception(
                                        f'No token generated for input {column} in row number #{row_number} using importer {current_spine.importer}')
                                current_spine.addToken(token)
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

    def doImportFile(self, file_path: string):
        """
        Import the content from the importer to the file.
        Args:
            file_path: The path to the file.

        Returns:
            None

        Example:
            # Create the importer and read the file
            >>> hi = HumdrumImporter()
            >>> hi.import_file('file.krn')
        """
        with open(file_path, 'r', newline='', encoding='utf-8', errors='ignore') as file:
            reader = csv.reader(file, delimiter='\t')
            self.doImport(reader)

    def doImportString(self, text: string):
        lines = text.splitlines()
        reader = csv.reader(lines)
        self.doImport(reader)

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

    def doExportNormalizedKern(self, options: ExportOptions) -> string:
        options.kern_type = Encoding.normalizedKern
        return self.doExport(options)

    def doExportEKern(self, options: ExportOptions) -> string:
        options.kern_type = Encoding.eKern
        return self.doExport(options)

    def doExportUnprocessed(self, options: ExportOptions) -> string:
        options.kern_type = Encoding.unprocessed
        return self.doExport(options)

    def handleBoundingBox(self, token: BoundingBoxToken):
        page_number = token.page_number
        last_page_bb = self.page_bounding_boxes.get(page_number)
        if last_page_bb is None:
            # print(f'Adding {page_number}')
            if self.last_measure_number is None:
                self.last_measure_number = 0
            self.last_bounding_box = BoundingBoxMeasures(token.bounding_box, self.last_measure_number,
                                                         self.last_measure_number)
            self.page_bounding_boxes[page_number] = self.last_bounding_box
        else:
            # print(f'Extending page {page_number}')
            last_page_bb.bounding_box.extend(token.bounding_box)
            last_page_bb.to_measure = self.last_measure_number

    def getMaxRows(self):
        return max(spine.size() for spine in self.spines)

    def checkMeasure(self, measure_number):
        if measure_number < 0:
            raise Exception(f'The measure number must be >=1, and it is {measure_number}')

        max_measures = len(self.measure_start_rows)
        if measure_number > max_measures:
            raise Exception(f'The measure number must be <= {max_measures}, and it is {measure_number}')

    def doExport(self, options: ExportOptions) -> string:
        max_rows = self.getMaxRows()
        signatures_at_each_row = []
        row_contents = []

        if options.from_measure is not None and options.from_measure < 0:
            raise ValueError(f'option from_measure must be >=0 but {options.from_measure} was found. ')
        if options.to_measure is not None and options.to_measure > len(self.measure_start_rows):
            #"TODO: DAVID, check options.to_measure bounds. len(self.measure_start_rows) or len(self.measure_start_rows) - 1"
            raise ValueError(f'option to_measure must be <= {len(self.measure_start_rows)} but {options.to_measure} was found. ')
        if options.to_measure is not None and options.from_measure is not None and options.to_measure < options.from_measure:
            raise ValueError(f'option to_measure must be >= from_measure but {options.to_measure} < {options.from_measure} was found. ')

        last_signature = None
        for i in range(max_rows):
            row_result = ''
            if last_signature:
                current_signature = last_signature.clone()
            else:
                current_signature = Signatures(None, None, None, None, None)
            last_signature = current_signature
            empty = True
            for spine in self.spines:
                if spine.spine_type in options.spine_types:
                    if i < spine.size():  # required because the spine may be terminated
                        if len(row_result) > 0:
                            row_result += '\t'

                        content = spine.getRowContent(i, options.kern_type, options.token_categories)

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
        if options.from_measure is None and options.to_measure is None:
            for row_content in row_contents:
                if row_content:
                    result += row_content
                    result += '\n'
        else:
            if options.from_measure:
                self.checkMeasure(options.from_measure)
            else:
                options.from_measure = 0

            if options.to_measure:
                self.checkMeasure(options.to_measure)
            else:
                options.to_measure = len(self.measure_start_rows)

            from_row = self.measure_start_rows[options.from_measure - 1] - 1  # measures and rows are counted from 1
            if options.to_measure == len(self.measure_start_rows):
                to_row = self.measure_start_rows[options.to_measure - 1]
            else:
                to_row = self.measure_start_rows[options.to_measure]  # to the next one
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

    def getErrorMessages(self):
        result = ''
        for err in self.errors:
            result += str(err)
            result += '\n'
        return result

    def hasErrors(self):
        return len(self.errors) > 0

    def has_token(self, token_goal: str):
        """
        Check if the importer has a specific token.

        Args:
            token_goal: The token to check.

        Returns:
            True if the importer has the token, False otherwise.

        Example:
            # Create the importer
            >>> hi = HumdrumImporter()

            # Read the file
            >>> hi.import_file('file.krn')

            # Check if the importer has a specific token
            >>> has_f_4_clef = hi.has_token('*clefF4')
        """
        for spine in self.spines:
            for row in spine.rows:
                if any(token.encoding == token_goal for token in row):
                    return True

        return False

    def has_category(self, token_category_goal: TokenCategory):
        """
        Check if the importer has a specific token.

        Args:
            token_category_goal: The token category to check.
        Returns:
            True if the importer has the token category, False otherwise.

        Example:
            # Create the importer
            >>> hi = HumdrumImporter()

            # Read the file
            >>> hi.import_file('file.krn')

            # Check if the importer has a specific token
            >>> has_barlines = hi.has_category(TokenCategory.BARLINES)

        """
        for spine in self.spines:
            for row in spine.rows:
                for token in row:
                    if token.category == token_category_goal:
                        return True
        return False

    def get_all_tokens(self, apply_strip: bool = True, remove_measure_numbers: bool = False, filter_by_categories: Iterable = None) -> list:
        """
        Get all the tokens in the importer.

        Args:
            apply_strip: If True, the tokens will be stripped. False otherwise. Default is True.
            remove_measure_numbers: If True, the measure numbers will be removed. False otherwise. Default is False.
            filter_by_categories: An Iterable (like a list) with the categories to filter the tokens. Default is None.\
                Only the tokens with the categories in the list will be returned.


        Returns:
            A list with all the tokens in the importer.

        Example:
            # Create the importer
            >>> hi = HumdrumImporter()

            # Read the file
            >>> hi.import_file('file.krn')

            # Get all the tokens
            >>> all_tokens = hi.get_all_tokens()

            # Get all the tokens without measure numbers
            >>> all_tokens = hi.get_all_tokens(remove_measure_numbers=True)

            # Get all the tokens without measure numbers and filtered by categories
            >>> all_tokens = hi.get_all_tokens(remove_measure_numbers=True, filter_by_categories=[TokenCategory.BARLINES, TokenCategory.FINGERING, TokenCategory.CORE])

            # Get all tokens used in the bekern codification
            >>> all_tokens = hi.get_all_tokens(remove_measure_numbers=True, filter_by_categories=BEKERN_CATEGORIES)

        """
        MEASURE_START = '='
        DIGITS_TO_REMOVE = string.digits
        result = []
        for spine in self.spines:
            for row in spine.rows:
                for token in row:
                    if filter_by_categories is not None and token.category not in filter_by_categories:
                        continue

                    if remove_measure_numbers and token.encoding.startswith(MEASURE_START):
                        token.encoding = token.encoding.lstrip(DIGITS_TO_REMOVE)

                    if apply_strip:
                        token.encoding = token.encoding.strip()

                    result.append(token.encoding)

        return result

    def get_unique_tokens(self, apply_strip: bool = True, remove_measure_numbers: bool = False, filter_by_categories: Iterable = None) -> list:
        """
        Get the unique tokens in the importer.

        Args:
            apply_strip: If True, the tokens will be stripped. False otherwise. Default is True.
            remove_measure_numbers: If True, the measure numbers will be removed. False otherwise. Default is False.
            filter_by_categories: An Iterable (like a list) with the categories to filter the tokens. Default is None.\
                Only the tokens with the categories in the list will be returned.

        Returns:
            A list with the unique tokens in the importer.

        Example:
            # Create the importer
            >>> hi = HumdrumImporter()

            # Read the file
            >>> hi.import_file('file.krn')

            # Get the unique tokens
            >>> unique_tokens = hi.get_unique_tokens()

            # Get the unique tokens without measure numbers
            >>> unique_tokens = hi.get_unique_tokens(remove_measure_numbers=True)

            # Get the unique tokens without measure numbers and filtered by categories
            >>> unique_tokens = hi.get_unique_tokens(remove_measure_numbers=True, filter_by_categories=[TokenCategory.BARLINES, TokenCategory.KEYSIGNATURE, TokenCategory.CORE])

            # Get the unique tokens used in the bekern codification
            >>> unique_tokens = hi.get_all_tokens(remove_measure_numbers=True, filter_by_categories=BEKERN_CATEGORIES)

        """
        all_tokens = self.get_all_tokens(apply_strip=apply_strip, remove_measure_numbers=remove_measure_numbers, filter_by_categories=filter_by_categories)
        return list(set(all_tokens))

    def is_voice_in_tessitura(self, voice: int, tessitura: tuple) -> bool:
        """
        Check if a voice is in a tessitura.

        Args:
            voice: The voice to check.
            tessitura: A tuple with the tessitura. The first element is the lower limit, and the second element is the upper limit.

        Returns:
            True if the voice is in the tessitura, False otherwise.

        Example:
            # Create the importer
            >>> hi = HumdrumImporter()

            # Read the file
            >>> hi.import_file('file.krn')

            # Check if the voice 1 is in the tessitura (C4, G4)
            >>> is_in_tessitura = hi.is_voice_in_tessitura(1, ('c4', 'g4'))
        """
        raise NotImplementedError('This method is not implemented yet.')   # TODO: Implementar el método
        min_tessitura = tessitura[0].lower()
        max_tessitura = tessitura[1].lower()

        all_tokens = None
        for row in self.spines[voice].rows:
            all_tokens = [token.encoding.lower() for token in row if isinstance(token.category, SpineOperationToken)]   # TODO: Buscar la categoria que solo deje pasar notas

        for token in all_tokens:
            if token < min_tessitura or token > max_tessitura:
                return False

        return True

    def __len__(self):
        """
        Get the number of spines in the importer.
        """
        return len(self.spines)

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
    content = content.replace(TOKEN_SEPARATOR, "")
    content = content.replace(DECORATION_SEPARATOR, "")

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
    importer = HumdrumImporter()
    importer.doImportFile(input_file)

    if len(importer.errors):
        raise Exception(f'ERROR: {input_file} has errors {importer.getErrorMessages()}')

    export_options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES, kern_type=Encoding.eKern)
    exported_ekern = importer.doExport(export_options)

    with open(output_file, 'w') as file:
        file.write(exported_ekern)
