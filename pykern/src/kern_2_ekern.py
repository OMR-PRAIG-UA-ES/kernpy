import string
import csv

from antlr4 import *

from src.generated.kern.kernParserListener import kernParserListener
from src.generated.kern.kernParser import kernParser
import logging

from src.kern_lexer_with_spines import KernLexerWithSpines


# Each of the main spines defined in the header with **kern, **dyn, etc...
class KernMainSpine:
    def __init__(self, type):
        self.type = type
        # Each row contains another array. For single spines it will contain just one value, for split
        # spines, more than one
        self.rows = []
        self.current_size = 1  # when a spine is split, it will be increased, decreased when joined, etc...
        self.terminated = False

    def changeSize(self, modifier: int):
        value = self.current_size + modifier
        if value < 0:
            raise Exception(f'Negative spine size {value}')
        self.current_size = value

    def terminate(self):
        self.terminated = True


class KernMatrix:
    def __init__(self):
        self.spines = []  # array of KernMainSpine

    def addSpineType(self, spine_type: string):
        self.spine.append(KernMainSpine(spine_type))

    def addSpineOperation(self, operation):
        self.spines.append(KernSpineOperation(operation))

    def getMainSpine(self, index: int) -> KernMainSpine:
        if index < 0:
            raise Exception(f'Negative index {index}')
        if index >= len(self.spines):
            raise Exception(f'Index {index} out of bounds ({len(self.spines)})')
        return self.spines[index]


class KernItem:
    def __init__(self, content):
        self.content = content


class KernContextualItem(KernItem):  # key signatures, time signatures, clef changes
    def __init__(self, content):
        super().__init__(content)


class KernSpineOperation(KernItem):  # split, add, etc..
    def __init__(self, content):
        super().__init__(content)


class KernMatrixExporter:
    def __init__(self):
        self.line = None

    def initLine(self):
        self.line = ''

    def addTab(self):
        if self.line:
            self.line += '\t'

    def writeLine(self):
        if self.line:
            self.output.write(self.line)
            self.output.write('\n')

    def writeSeparator(self):
        self.line += self.SEPARATOR

    def writeContext(self, ctx: ParserRuleContext):
        self.line += ctx.getText()

    def writeText(self, text: string):
        self.line += text


# TODO Añadir modos para que pueda trabajar con spines text
class KernListener(kernParserListener):
    SEPARATOR = '·'

    def __init__(self):
        self.matrix = KernMatrix
        self.current_spine = 0
        self.first_chord_element = None
        self.in_chord = None

    def enterStart(self, ctx: kernParser.StartContext):
        logging.info('Parsing started')

    def exitStart(self, ctx: kernParser.StartContext):
        logging.info('Parsing finished')

    def exitHeaderField(self, ctx: kernParser.HeaderFieldContext):
        self.matrix.addSpineType(ctx.getText())

    def enterRecord(self, ctx: kernParser.RecordContext):
        self.current_spine = 0

    def enterField(self, ctx: kernParser.FieldContext):
        self.current_spine = self.current_spine + 1

    def exitField(self, ctx: kernParser.FieldContext):
        self.current_spine = self.current_spine + 1

    def exitSpineTerminator(self, ctx: kernParser.SpineTerminatorContext):
        self.matrix.getMainSpine(self.current_spine).terminate()

    def exitSpineAdd(self, ctx: kernParser.SpineAddContext):
        self.matrix.getMainSpine(self.current_spine).changeSize(1)

    def exitSpineSplit(self, ctx: kernParser.SpineSplitContext):
        self.matrix.getMainSpine(self.current_spine).changeSize(1)

    def exitSpineJoin(self, ctx: kernParser.SpineJoinContext):
        self.matrix.getMainSpine(self.current_spine).changeSize(-1)

    def exitSpineOperation(self, ctx: kernParser.SpineOperationContext):
        self.matrix.addSpineOperation(ctx.getText())
        self.current_spine = self.current_spine + 1

    # used for rests and notes
    def process_decorations(self, ctx: ParserRuleContext):
        # in order to standardize the order of note decorators, we map the different properties to their class names
        decorations = {}

        for child in ctx.getChildren():
            if not isinstance(child, kernParser.PitchContext) and not isinstance(child, kernParser.DurationContext) \
                    and not isinstance(child, kernParser.RestChar_rContext):
                # all decorations have just a child
                if child.getChildCount() != 1:
                    raise Exception('Only 1 decoration child expected, and found ' + child.getChildCount() + ', check '
                                                                                                             'the '
                                                                                                             'grammar')
                clazz = type(child.getChild(0))
                decoration_type = clazz.__name__
                if decoration_type in decorations:
                    logging.warning(
                        f'The decoration {decoration_type} is duplicated')  # TODO Dar información de línea, columna - ¿lanzamos excepción? - hay algunas que sí pueden estar duplicadas? Barrados?
                decorations[decoration_type] = child.getText()
        for key in sorted(decorations.keys()):
            self.writeSeparator()
            self.writeText(decorations[key])

    def exitNote(self, ctx: kernParser.NoteContext):
        if self.in_chord:
            self.addChordSeparator()

        if ctx.duration():
            self.writeContext(ctx.duration())
            self.writeSeparator()
        self.writeContext(ctx.pitch())
        self.process_decorations(ctx)

    def exitRest(self, ctx: kernParser.RestContext):
        if self.in_chord:
            self.addChordSeparator()

        self.writeText('r')
        if ctx.duration():
            self.writeContext(ctx.duration())
            self.writeSeparator()
        self.process_decorations(ctx)

    def enterChord(self, ctx: kernParser.ChordContext):
        self.in_chord = True
        self.first_chord_element = True

    def exitChord(self, ctx: kernParser.ChordContext):
        self.in_chord = False

    def addChordSeparator(self):
        if self.first_chord_element:
            self.first_chord_element = False
        else:
            self.writeText(' ')


# TODO Recordar cuando aparece la posición del silencio en modo pitch


# It converts a humdrum file (**kern or **mens) to a ekern (extended kern) file (i.e. a kern with all components of
# each token divided into subtokens and separated by a · character)
# TO-DO Poner opciones ----
class Kern2EkernConverter:
    def doConvertFile(self, input, output):
        logging.info(f'Converting filename {input}')
        input_stream = FileStream(input)
        lexer = KernLexerWithSpines(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = kernParser(token_stream)
        tree = parser.start()

        with open(output, 'w', buffering=4096) as outputFile:
            logging.info(f'Converting filename {input} to {output}')
            listener = KernListener(outputFile)
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
