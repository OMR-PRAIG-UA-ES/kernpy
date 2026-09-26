from __future__ import annotations

from typing import Optional

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, BailErrorStrategy, PredictionMode

from .base_antlr_spine_parser_listener import BaseANTLRSpineParserListener
from .generated.kernMensSpineLexer import kernMensSpineLexer
from .generated.kernMensSpineParser import kernMensSpineParser
from .spine_importer import SpineImporter
from .tokens import SimpleToken, Subtoken, TokenCategory


class MensSpineListener(BaseANTLRSpineParserListener):
    """
    Builds kernpy tokens from the combined **kern/**mens grammar (``kern/kernMensSpine*.g4``).

    That grammar is mOOsicae's, vendored verbatim, so both libraries read **mens alike. It shares the
    **kern rules with ``kernSpine*.g4`` and adds the mensural layer, where ``duration`` is either a
    mensural duration (figure, perfection, coloration, dot) or a modern one.
    """

    def exitDuration(self, ctx: kernMensSpineParser.DurationContext):
        mensural = ctx.mensuralDuration()
        if mensural is not None:
            # One subtoken, as written: the figure and what qualifies it, in the grammar's order,
            # p/i/I (perfect, imperfect, imperfect by alteration), ~ (coloured), . or : (augmentation
            # or division dot). Split, the exporter would sort the parts and write ':s' for 's:'.
            self.duration_subtokens = [Subtoken(mensural.getText(), TokenCategory.DURATION)]
            return
        modern = ctx.modernDuration()
        self.duration_subtokens = [Subtoken(modern.modernFigure().getText(), TokenCategory.DURATION)]
        for _ in modern.augmentationDot():
            self.duration_subtokens.append(Subtoken(".", TokenCategory.DURATION))
        if modern.graceNote():
            self.duration_subtokens.append(Subtoken(modern.graceNote().getText(), TokenCategory.DURATION))
        if modern.appoggiatura():
            self.duration_subtokens.append(Subtoken(modern.appoggiatura().getText(), TokenCategory.DURATION))

    def exitNote(self, ctx: kernMensSpineParser.NoteContext):
        # The combined grammar takes ligature, tie, slur, phrase and stem marks as a PREFIX of the note
        # (`<S~a`, `[sB`), outside noteDecoration; keep them as decorations, as **kern keeps its own.
        prefixes = (
            kernMensSpineParser.LigatureTieStartContext,
            kernMensSpineParser.SlurStartContext,
            kernMensSpineParser.SlurEndContext,
            kernMensSpineParser.PhraseContext,
            kernMensSpineParser.StemContext,
        )
        for child in ctx.getChildren():
            if isinstance(child, prefixes):
                self._add_decoration(Subtoken(child.getText(), TokenCategory.DECORATION))
        super().exitNote(ctx)

    def exitCustos(self, ctx: kernMensSpineParser.CustosContext):
        self.token = SimpleToken(ctx.getText(), TokenCategory.ENGRAVED_SYMBOLS)

    def exitSignumCongruentiae(self, ctx: kernMensSpineParser.SignumCongruentiaeContext):
        self.token = SimpleToken(ctx.getText(), TokenCategory.ENGRAVED_SYMBOLS)

    def exitLayout(self, ctx: kernMensSpineParser.LayoutContext):
        self.token = SimpleToken(ctx.getText(), TokenCategory.LINE_BREAK)

    def exitMultirest(self, ctx: kernMensSpineParser.MultirestContext):
        self.addNoteRest(ctx, [Subtoken(ctx.getText(), TokenCategory.REST)])


class MensSpineImporter(SpineImporter):
    """Imports **mens spines with the combined **kern/**mens grammar shared with mOOsicae."""

    def __init__(self, verbose: Optional[bool] = False):
        super().__init__(verbose=verbose)

    def import_listener(self) -> BaseANTLRSpineParserListener:
        return MensSpineListener()

    def import_token(self, encoding: str):
        self._raise_error_if_wrong_input(encoding)
        self.error_listener.errors = []

        lexer = kernMensSpineLexer(InputStream(encoding))
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)
        stream = CommonTokenStream(lexer)
        parser = kernMensSpineParser(stream)
        parser._interp.predictionMode = PredictionMode.SLL  # it improves a lot the parsing
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        parser.errHandler = BailErrorStrategy()
        tree = parser.start()
        listener = MensSpineListener()
        ParseTreeWalker().walk(listener, tree)
        if self.error_listener.getNumberErrorsFound() > 0:
            raise ValueError(str(self.error_listener).strip())
        return listener.token
