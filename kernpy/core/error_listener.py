from typing import Optional

from antlr4.error.ErrorListener import ConsoleErrorListener


class ParseError:
    def __init__(self, offendingSymbol, line, charPositionInLine, msg, exception):
        self.offendingSymbol = offendingSymbol
        self.line = line
        self.charPositionInLine = charPositionInLine
        self.msg = msg
        self.exception = exception

    def __str__(self):
        symbol_text = None
        if self.offendingSymbol is not None:
            symbol_text = getattr(self.offendingSymbol, "text", None)
            if symbol_text is None:
                symbol_text = str(self.offendingSymbol)

        token_context = f" near '{symbol_text}'" if symbol_text else ""
        parser_context = f" (parser: {self.exception})" if self.exception else ""
        return (
            f"line {self.line}, column {self.charPositionInLine}{token_context}: "
            f"{self.msg}{parser_context}"
        )

    def getOffendingSymbol(self):
        return self.offendingSymbol

    def getCharPositionInLine(self):
        return self.charPositionInLine

    def getLine(self):
        return self.line

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
            super().syntaxError(recognizer, offendingSymbol, line, charPositionInLine, msg, e)

        self.errors.append(ParseError(offendingSymbol, line, charPositionInLine, msg, e))

    def getNumberErrorsFound(self):
        return len(self.errors)

    def __str__(self):
        sb = ""
        for error in self.errors:
            sb += str(error) + "\n"
        return sb