from __future__ import annotations

from abc import ABC, abstractmethod

from antlr4 import CommonTokenStream, ParseTreeWalker
from antlr4.InputStream import InputStream


class BaseANTLRImporter(ABC):
    def __init__(self, input_string):
        char_stream = InputStream(input_string)
        self.lexer = self.createLexer(char_stream)
        token_stream = CommonTokenStream(self.lexer)
        self.parser = self.createParser(token_stream)

    @abstractmethod
    def createLexer(self, charStream):
        pass

    @abstractmethod
    def createParser(self, tokenStream):
        pass

    @abstractmethod
    def startRule(self):
        pass


class BaseANTLRListenerImporter(BaseANTLRImporter):
    def __init__(self, input_string):
        super().__init__(input_string)
        self.listener = self.createListener()

    def start(self):
        tree = self.startRule()
        walker = ParseTreeWalker()
        walker.walk(self.listener, tree)
        #ParseTreeWalker.DEFAULT.walk(walker, tree)

    @abstractmethod
    def createListener(self):
        pass


class BaseANTLRVisitorImporter(BaseANTLRImporter):
    def __init__(self, input):
        super().__init__(input)
        self.visitor = self.createVisitor()

    def start(self):
        tree_context = self.startRule()
        self.visitStart(tree_context)

    @abstractmethod
    def createVisitor(self):
        pass

    @abstractmethod
    def visitStart(self, start_context):
        pass

