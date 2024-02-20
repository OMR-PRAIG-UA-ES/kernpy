from antlr4 import *
from src.generated.kern.kernParserVisitor import kernParserVisitor
from src.generated.kern.kernLexer import kernLexer
from src.generated.kern.kernParser import kernParser
import logging


# TODO Añadir modos para que pueda trabajar con spines text
# TODO - pasar lo leído a una matriz / grafo
class HumdrumImporterVisitor(kernParserVisitor):
    def __init__(self):
        pass

    def visitStart(self, ctx: kernParser.StartContext):
        logging.debug('Visit start ')
        return self.visitChildren(ctx)

    def visitRecord(self, ctx: kernParser.RecordContext):
        logging.debug('Visit record')
        return self.visitChildren(ctx)

    def visitFields(self, ctx: kernParser.FieldsContext):
        logging.debug('Visit fields')
        return self.visitChildren(ctx)

    def visitField(self, ctx: kernParser.FieldContext):
        logging.debug('Visit field')
        return self.visitChildren(ctx)

    def visitGraphicalToken(self, ctx: kernParser.GraphicalTokenContext):
        logging.debug('Visit graphical token')
        return self.visitChildren(ctx)

    def visitClef(self, ctx: kernParser.ClefContext):
        logging.debug('Visit clef')
        return self.visitChildren(ctx)

    def visitNote(self, ctx: kernParser.NoteContext):
        logging.debug('Visit note')
        return self.visitChildren(ctx)

    def visitDuration(self, ctx: kernParser.DurationContext):
        logging.debug('Visit duration')

    def visitDiatonicPitchAndOctave(self, ctx: kernParser.DiatonicPitchAndOctaveContext):
        logging.debug('Visit pitch and octave')


class HumdrumImporter:
    def doImportFile(self, input):
        logging.info(f'Importing filename {input}')
        input_stream = FileStream(input)
        lexer = kernLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = kernParser(token_stream)
        tree = parser.start()
        visitor = HumdrumImporterVisitor()
        visitor.visit(tree)
