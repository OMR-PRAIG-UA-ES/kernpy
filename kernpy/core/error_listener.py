from typing import Optional

from antlr4.error.ErrorListener import ConsoleErrorListener


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
    def __init__(self, *, verbose: Optional[bool] = False):
        """
        ErrorListener constructor.
        Args:
            verbose (bool): If True, the error messages will be printed to the console using \
            the `ConsoleErrorListener` interface.
        """
        super().__init__()
        self.errors = []
        self.verbose = verbose

    def syntaxError(self, recognizer, offendingSymbol, line, charPositionInLine, msg, e):
        if self.verbose:
            self.syntaxError(recognizer, offendingSymbol, line, charPositionInLine, msg, e)

        self.errors.append(ParseError(offendingSymbol, charPositionInLine, msg, e))

    def getNumberErrorsFound(self):
        return len(self.errors)

    def __str__(self):
        sb = ""
        for error in self.errors:
            sb += str(error) + "\n"
        return sb