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