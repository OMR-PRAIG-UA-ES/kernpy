import string

from antlr4 import *

from src.generated.kern.kernParserListener import kernParserListener
from src.generated.kern.kernLexer import kernLexer
from src.generated.kern.kernParser import kernParser
import logging


# TODO Añadir modos para que pueda trabajar con spines text
class Kern2EkernListener(kernParserListener):
    SEPARATOR = '·'

    def __init__(self, output):
        self.output = output
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

    def enterStart(self, ctx: kernParser.StartContext):
        logging.info('Parsing started')

    def exitStart(self, ctx: kernParser.StartContext):
        logging.info('Parsing finished')

    def exitHeader(self, ctx: kernParser.HeaderContext):
        self.writeLine()

    def enterHeader(self, ctx:kernParser.HeaderContext):
        self.initLine()

    def exitHeaderField(self, ctx: kernParser.HeaderFieldContext):
        self.addTab()
        self.writeContext(ctx)

    def enterRecord(self, ctx:kernParser.RecordContext):
        self.initLine()

    def enterField(self, ctx:kernParser.FieldContext):
        self.addTab()

    def exitRecord(self, ctx: kernParser.RecordContext):
        self.writeLine()

    def exitSpineOperation(self, ctx: kernParser.SpineOperationContext):
        self.writeContext(ctx)

    def exitPlaceHolder(self, ctx: kernParser.PlaceHolderContext):
        self.writeContext(ctx)

    # used for rests and notes
    def process_decorations(self, ctx: ParserRuleContext):
        # in order to standardize the order of note decorators, we map the different properties to their class names
        decorations = {}

        for child in ctx.getChildren():
            if not isinstance(child, kernParser.PitchContext) and not isinstance(child, kernParser.DurationContext):
                # all decorations have just a child
                if child.getChildCount() != 1:
                    raise Exception('Only 1 decoration child expected, and found ' + child.getChildren().len() + ', check the grammar')
                clazz = type(child.getChild(0))
                decoration_type = clazz.__name__
                if decoration_type in decorations:
                    logging.warning(f'The decoration {decoration_type} is duplicated') # TODO Dar información de línea, columna - ¿lanzamos excepción? - hay algunas que sí pueden estar duplicadas? Barrados?
                decorations[decoration_type] = child.getText()
        for key in sorted(decorations.keys()):
            self.writeSeparator()
            self.writeText(decorations[key])

    def exitNote(self, ctx:kernParser.NoteContext):
        if ctx.duration():
            self.writeContext(ctx.duration())
            self.writeSeparator()
        self.writeContext(ctx.pitch())
        self.process_decorations(ctx)

#TODO Recordar cuando aparece la posición del silencio en modo pitch


# It converts a humdrum file (**kern or **mens) to a ekern (extended kern) file (i.e. a kern with all components of
# each token divided into subtokens and separated by a · character)
class Kern2EkernConverter:
    def doConvertFile(self, input, output):
        logging.info(f'Converting filename {input}')
        input_stream = FileStream(input)
        lexer = kernLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = kernParser(token_stream)
        tree = parser.start()

        with open(output, 'w', buffering=4096) as outputFile:
            logging.info(f'Converting filename {input} to {output}')
            listener = Kern2EkernListener(outputFile)
            walker = ParseTreeWalker();
            walker.walk(listener, tree);
