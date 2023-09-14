from antlr4 import *
from generated.kern.kernParserVisitor import kernParserVisitor
from generated.kern.kernLexer import kernLexer
from generated.kern.kernParser import kernParser


class ImporterVisitor(kernParserVisitor):
    def visitStart(self, ctx:kernParser.StartContext):
        return self.visitChildren(ctx)


class KernImporter:
    def doImportFile(self, filename):
        input_stream = FileStream(filename)
        lexer = kernLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = kernParser(token_stream)

        tree = parser.start()

        visitor = ImporterVisitor()
        result = visitor.visit(tree)

