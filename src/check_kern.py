from antlr4 import *
from antlr4.error import ErrorListener

from src.generated.kern.kernLexer import kernLexer
from src.generated.kern.kernParser import kernParser
import logging

# This file checks that the provided kern file is correct according to the **kern grammar.
class MyErrorListener(ErrorListener.ErrorListener):
    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        logging.warning(f"Syntax error in symbol {offending_symbol} at line {line}:{column}: {msg}")

def do_check(stream):
    lexer = kernLexer(stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(MyErrorListener())
    token_stream = CommonTokenStream(lexer)
    parser = kernParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener())
    tree = parser.start()
    return tree is not None and parser.getNumberOfSyntaxErrors() == 0


def check_file(input_file):
    '''
    It checks that a given file is correct according our **kern grammar
    :param input_file: Path ot the file to be checked
    :return: True if correct
    '''
    logging.info(f'Importing filename {input_file}')
    input_stream = FileStream(input_file)
    correct = do_check(input_stream)
    return correct


def check_string(input_string):
    '''
    It checks that a given string is correct according our **kern grammar
    :param input_string: String to be checked
    :return: True if correct
    '''
    logging.info(f'Importing string {input_string}')
    input_stream = InputStream(input_string)
    do_check(input_stream)
    correct = do_check(input_stream)
    return correct

