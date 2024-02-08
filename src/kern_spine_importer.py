import logging
import string

from antlr4 import ParserRuleContext, InputStream, CommonTokenStream, ParseTreeWalker

from src.base_antlr_importer import BaseANTLRListenerImporter
from src.generated.kernSpineLexer import kernSpineLexer
from src.generated.kernSpineParser import kernSpineParser
from src.generated.kernSpineParserListener import kernSpineParserListener
from src.spine_importer import SpineImporter


class KernSpineListener(kernSpineParserListener):

    def __init__(self):
        self.SEPARATOR = '·'
        self.first_chord_element = None
        self.processed_token = None
        self.in_chord = False

    def enterStart(self, ctx: kernSpineParser.StartContext):
        self.processed_token = None

    def exitStart(self, ctx: kernSpineParser.StartContext):
        if not self.processed_token: # if not rule has processed it, generate the input itself
            self.processed_token = ctx.getText()

    def exitEveryRule(self, ctx: ParserRuleContext):
        super().exitEveryRule(ctx)

    def process_decorations(self, ctx: ParserRuleContext):
        # in order to standardize the order of note decorators, we map the different properties to their class names
        decorations = {}

        for child in ctx.getChildren():
            if not isinstance(child, kernSpineParser.PitchContext) and not isinstance(child,
                                                                                      kernSpineParser.DurationContext) \
                    and not isinstance(child, kernSpineParser.RestChar_rContext):
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

    def exitNote(self, ctx: kernSpineParser.NoteContext):
        if self.in_chord:
            self.addChordSeparator()

        if ctx.duration():
            self.writeContext(ctx.duration())
            self.writeSeparator()
        self.writeContext(ctx.pitch())
        self.process_decorations(ctx)

    def exitRest(self, ctx: kernSpineParser.RestContext):
        if self.in_chord:
            self.addChordSeparator()

        self.writeText('r')
        if ctx.duration():
            self.writeContext(ctx.duration())
            self.writeSeparator()
        self.process_decorations(ctx)

    def enterChord(self, ctx: kernSpineParser.ChordContext):
        self.in_chord = True
        self.first_chord_element = True

    def exitChord(self, ctx: kernSpineParser.ChordContext):
        self.in_chord = False

    def addChordSeparator(self):
        if self.first_chord_element:
            self.first_chord_element = False
        else:
            self.writeText(' ')

    def writeSeparator(self):
        if not self.processed_token:
            raise Exception('Cannot add a separator to an empty processed token')
        self.processed_token += self.SEPARATOR

    def writeContext(self, ctx: ParserRuleContext):
        self.writeText(ctx.getText())

    def writeText(self, text: string):
        if not self.processed_token:
            self.processed_token = text
        else:
            self.processed_token += text


class KernListenerImporter(BaseANTLRListenerImporter):

    def createListener(self):
        return KernSpineListener

    def createLexer(self, charStream):
        return kernSpineLexer(charStream)

    def createParser(self, tokenStream):
        return kernSpineParser(tokenStream)

    def startRule(self):
        return self.parser.start()


class KernSpineImporter(SpineImporter):
    def doImport(self, token: string):
        if not token:
            raise Exception('Input token is empty')
        #self.listenerImporter = KernListenerImporter(token) # TODO ¿Por qué no va esto?
        #self.listenerImporter.start()
        lexer = kernSpineLexer(InputStream(token))
        stream = CommonTokenStream(lexer)
        parser = kernSpineParser(stream)
        tree = parser.start()
        walker = ParseTreeWalker()
        listener = KernSpineListener()
        walker.walk(listener, tree)
        return listener.processed_token

