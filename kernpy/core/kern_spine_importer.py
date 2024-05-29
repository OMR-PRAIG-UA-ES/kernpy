import string

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy, \
    PredictionMode
from antlr4.error.ErrorListener import ConsoleErrorListener

from .base_antlr_importer import BaseANTLRListenerImporter
from .generated.kernSpineLexer import kernSpineLexer
from .generated.kernSpineParser import kernSpineParser
from .generated.kernSpineParserListener import kernSpineParserListener
from .spine_importer import SpineImporter
from .tokens import SimpleToken, TokenCategory, Subtoken, SubTokenCategory, ChordToken, BoundingBox, \
    BoundingBoxToken, ClefToken, KeySignatureToken, TimeSignatureToken, MeterSymbolToken, BarToken, NoteRestToken, \
    KeyToken, InstrumentToken


class KernSpineListener(kernSpineParserListener):

    def __init__(self):
        self.first_chord_element = None
        self.token = None
        self.chord_tokens = None
        self.duration_subtokens = []
        self.diatonic_pitch_and_octave_subtoken = None
        self.accidental_subtoken = None
        # self.decorations = {}  # in order to standardize the order of decorators, we map the different properties to their class names
        # We cannot order it using the class name because there are rules with subrules, such as ties, or articulations. We order it using the encoding itself
        self.decorations = []
        self.in_chord = False
        # self.page_start_rows = [] # TODO
        self.measure_start_rows = []
        self.last_bounding_box = None

    def enterStart(self, ctx: kernSpineParser.StartContext):
        self.token = None
        self.duration_subtokens = []
        self.diatonic_pitch_and_octave_subtoken = None
        self.accidental_subtoken = None
        # self.decorations = {}
        self.decorations = []

    # def process_decorations(self, ctx: ParserRuleContext):
    #     # in order to standardize the order of note decorators, we map the different properties to their class names
    #     decorations = {}
    #
    #     for child in ctx.getChildren():
    #         # all decorations have just a child
    #         if child.getChildCount() != 1:
    #             raise Exception('Only 1 decoration child expected, and found ' + child.getChildCount() + ', check '
    #                                                                                                      'the '
    #                                                                                                      'grammar')
    #         clazz = type(child.getChild(0))
    #         decoration_type = clazz.__name__
    #         if decoration_type in decorations:
    #             logging.warning(
    #                 f'The decoration {decoration_type} is duplicated')  # TODO Dar información de línea, columna - ¿lanzamos excepción? - hay algunas que sí pueden estar duplicadas? Barrados?
    #         decorations[decoration_type] = child.getText()
    #     for key in sorted(decorations.keys()):
    #         subtoken = Subtoken(decorations[key], SubTokenCategory.DECORATION)
    #         self.duration_subtoken.append(subtoken)

    def exitDuration(self, ctx: kernSpineParser.DurationContext):
        self.duration_subtokens = [Subtoken(ctx.modernDuration().getText(), SubTokenCategory.DURATION)]
        for i in range(len(ctx.augmentationDot())):
            self.duration_subtokens.append(Subtoken(".", SubTokenCategory.DURATION))

        if ctx.graceNote():
            self.duration_subtokens.append(Subtoken(ctx.graceNote().getText(), SubTokenCategory.DURATION))

        if ctx.appoggiatura():
            self.duration_subtokens.append(Subtoken(ctx.appoggiatura().getText(), SubTokenCategory.DURATION))

    def exitDiatonicPitchAndOctave(self, ctx: kernSpineParser.DiatonicPitchAndOctaveContext):
        self.diatonic_pitch_and_octave_subtoken = Subtoken(ctx.getText(), SubTokenCategory.PITCH)

    def exitNoteDecoration(self, ctx: kernSpineParser.NoteDecorationContext):
        # clazz = type(ctx.getChild(0))
        # decoration_type = clazz.__name__
        # if decoration_type in self.decorations:
        #    logging.warning(
        #        f'The decoration {decoration_type} is duplicated after reading {ctx.getText()}')  # TODO Dar información de línea, columna - ¿lanzamos excepción? - hay algunas que sí pueden estar duplicadas? Barrados?

        # self.decorations[decoration_type] = ctx.getText()
        # We cannot order it using the class name because there are rules with subrules, such as ties, or articulations. We order it using the encoding itself
        self.decorations.append(ctx.getText())

    def exitRestDecoration(self, ctx: kernSpineParser.NoteDecorationContext):
        # clazz = type(ctx.getChild(0))
        # decoration_type = clazz.__name__
        # if decoration_type in self.decorations:
        #    logging.warning(
        #        f'The decoration {decoration_type} is duplicated after reading {ctx.getText()}')  # TODO Dar información de línea, columna - ¿lanzamos excepción? - hay algunas que sí pueden estar duplicadas? Barrados?

        # self.decorations[decoration_type] = ctx.getText()
        # We cannot order it using the class name because there are rules with subrules, such as ties, or articulations. We order it using the encoding itself
        decoration = ctx.getText();
        if decoration != '/' and decoration != '\\':
            self.decorations.append(ctx.getText())

    def addNoteRest(self, ctx, pitchduration_subtokens):
        # subtoken = Subtoken(self.decorations[key], SubTokenCategory.DECORATION)
        token = NoteRestToken(ctx.getText(), pitchduration_subtokens, self.decorations)
        if self.in_chord:
            self.chord_tokens.append(token)
        else:
            self.token = token

    def exitNote(self, ctx: kernSpineParser.NoteContext):
        pitch_duration_tokens = []
        for duration_subtoken in self.duration_subtokens:
            pitch_duration_tokens.append(duration_subtoken)
        pitch_duration_tokens.append(self.diatonic_pitch_and_octave_subtoken)
        if ctx.alteration():
            pitch_duration_tokens.append(Subtoken(ctx.alteration().getText(), SubTokenCategory.PITCH))

        self.addNoteRest(ctx, pitch_duration_tokens)

    def exitRest(self, ctx: kernSpineParser.RestContext):
        pitch_duration_tokens = []
        for duration_subtoken in self.duration_subtokens:
            pitch_duration_tokens.append(duration_subtoken)
        pitch_duration_tokens.append(Subtoken('r', SubTokenCategory.PITCH))
        self.addNoteRest(ctx, pitch_duration_tokens)

    def enterChord(self, ctx: kernSpineParser.ChordContext):
        self.in_chord = True
        self.chord_tokens = []

    def exitChord(self, ctx: kernSpineParser.ChordContext):
        self.in_chord = False
        self.token = ChordToken(ctx.getText(), TokenCategory.CORE, self.chord_tokens)

    def exitBarline(self, ctx: kernSpineParser.BarlineContext):
        txt_without_number = ''
        if ctx.EQUAL(0) and ctx.EQUAL(1):
            txt_without_number = '=='
        elif ctx.EQUAL(0):
            txt_without_number = '='
        if ctx.barLineType():
            txt_without_number += ctx.barLineType().getText()
        if ctx.fermata():
            txt_without_number += ctx.fermata().getText()

        # correct wrong encodings
        if txt_without_number == ':!:':
            txt_without_number = ':|!|:'
        elif txt_without_number == ':|!|:':
            txt_without_number = ':|!|:'

        self.token = BarToken(txt_without_number)
        self.token.hidden = "-" in ctx.getText()  # hidden

    def exitEmpty(self, ctx: kernSpineParser.EmptyContext):
        self.token = SimpleToken(ctx.getText(), TokenCategory.EMPTY)

    def exitNonVisualTandemInterpretation(self, ctx: kernSpineParser.NonVisualTandemInterpretationContext):
        self.token = SimpleToken(ctx.getText(), TokenCategory.OTHER)

    def exitVisualTandemInterpretation(self, ctx: kernSpineParser.VisualTandemInterpretationContext):
        self.token = SimpleToken(ctx.getText(), TokenCategory.ENGRAVED_SYMBOLS)

    def exitOtherContextual(self, ctx: kernSpineParser.ContextualContext):
        self.token = SimpleToken(ctx.getText(), TokenCategory.OTHER_CONTEXTUAL)

    def exitClef(self, ctx: kernSpineParser.ClefContext):
        self.token = ClefToken(ctx.getText())

    def exitKeySignature(self, ctx: kernSpineParser.KeySignatureContext):
        self.token = KeySignatureToken(ctx.getText())

    def exitKeyCancel(self, ctx: kernSpineParser.KeyCancelContext):
        self.token = KeySignatureToken(ctx.getText())

    def exitKey(self, ctx: kernSpineParser.KeyContext):
        self.token = KeyToken(ctx.getText())

    def exitTimeSignature(self, ctx: kernSpineParser.TimeSignatureContext):
        self.token = TimeSignatureToken(ctx.getText())

    def exitMeterSymbol(self, ctx: kernSpineParser.MeterSymbolContext):
        self.token = MeterSymbolToken(ctx.getText())

    def exitStructural(self, ctx: kernSpineParser.StructuralContext):
        self.token = SimpleToken(ctx.getText(), TokenCategory.STRUCTURAL)

    def exitXywh(self, ctx: kernSpineParser.XywhContext):
        self.last_bounding_box = BoundingBox(int(ctx.x().getText()), int(ctx.y().getText()), int(ctx.w().getText()),
                                             int(ctx.h().getText()))

    def exitBoundingBox(self, ctx: kernSpineParser.BoundingBoxContext):
        page = ctx.pageNumber().getText()
        bbox = BoundingBox(int(ctx.xywh().x().getText()), int(ctx.xywh().y().getText()), int(ctx.xywh().w().getText()),
                           int(ctx.xywh().h().getText()))
        self.token = BoundingBoxToken(ctx.getText(), page, bbox)

    def exitInstrument(self, ctx: kernSpineParser.InstrumentContext):
        self.token = InstrumentToken(ctx.getText())


class KernListenerImporter(BaseANTLRListenerImporter):

    def createListener(self):
        return KernSpineListener

    def createLexer(self, charStream):
        return kernSpineLexer(charStream)

    def createParser(self, tokenStream):
        return kernSpineParser(tokenStream)

    def startRule(self):
        return self.parser.start()


# TODO - hacerlo común...

class ParseError:
    def __init__(self, offendingSymbol, charPositionInLine, msg, exception):
        self.offendingSymbol = offendingSymbol
        self.charPositionInLine = charPositionInLine
        self.msg = msg
        self.exception = exception

    def __str__(self):
        return f"({self.charPositionInLine}): {self.msg}"

    def getOffendingSymbol(self):
        return self.offendingSymbol

    def getCharPositionInLine(self):
        return self.charPositionInLine

    def getMsg(self):
        return self.msg


class ErrorListener(ConsoleErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, charPositionInLine, msg, e):
        super().syntaxError(recognizer, offendingSymbol, line, charPositionInLine, msg, e)
        self.errors.append(ParseError(offendingSymbol, charPositionInLine, msg, e))

    def getNumberErrorsFound(self):
        return len(self.errors)

    def __str__(self):
        sb = ""
        for error in self.errors:
            sb += str(error) + "\n"
        return sb


class KernSpineImporter(SpineImporter):
    def import_token(self, token: string):
        if not token:
            raise Exception('Input token is empty')
        # self.listenerImporter = KernListenerImporter(token) # TODO ¿Por qué no va esto?
        # self.listenerImporter.start()
        error_listener = ErrorListener()
        lexer = kernSpineLexer(InputStream(token))
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        stream = CommonTokenStream(lexer)
        parser = kernSpineParser(stream)
        parser._interp.predictionMode = PredictionMode.SLL  # it improves a lot the parsing
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        parser.errHandler = BailErrorStrategy()
        tree = parser.start()
        walker = ParseTreeWalker()
        listener = KernSpineListener()
        walker.walk(listener, tree)
        if error_listener.getNumberErrorsFound() > 0:
            raise Exception(error_listener.errors)
        return listener.token
