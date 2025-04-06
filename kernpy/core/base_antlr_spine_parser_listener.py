from .generated.kernSpineParserListener import kernSpineParserListener
from .generated.kernSpineParser import kernSpineParser
from .tokens import BarToken

class BaseANTLRSpineParserListener(kernSpineParserListener):
    def __init__(self):
        self.token = None

    def exitBarline(self, ctx: kernSpineParser.BarlineContext):
        txt_without_number = ''
        if ctx.EQUAL(0) and ctx.EQUAL(1):
            txt_without_number = '=='
        elif ctx.EQUAL(0):
            txt_without_number = '='
        if ctx.barLineType():
            txt_without_number += ctx.barLineType().getText()
        if ctx.fermata():
            txt_without_number += ctx.fermata().getText()

        # correct wrong encodings
        if txt_without_number == ':!:':
            txt_without_number = ':|!|:'
        elif txt_without_number == ':|!|:':
            txt_without_number = ':|!|:'

        self.token = BarToken(txt_without_number)
        self.token.hidden = "-" in ctx.getText()  # hidden

