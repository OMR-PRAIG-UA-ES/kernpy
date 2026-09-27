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

    That grammar is mOOsicae's, vendored verbatim, so both libraries read **mens alike. A **mens cell is
    read from its own entry rule, ``startMens``: several letters mean something else in **kern (``L``,
    ``S``, ``M``, ``m``, ``X``, ``p``, ``i``, ``u``...), so the spine type decides, as in humlib.

    **mens does not fix the order of the signifiers in a token (``si~d``, ``s~id``, ``sa~``, ``aS``): the
    figure, its perfection mark (``p``, ``i``, ``I``, ``+`` altera), the coloration (``~``) and the dot
    (``.`` or ``:``) are collected wherever they are and written back as one duration subtoken in a fixed
    order, figure, perfection, coloration, dot (``s~id`` is exported ``si~d``), so the exporter never
    splits and sorts them (it would write ``:s`` for ``s:``).
    """

    def enterStartMens(self, ctx: kernMensSpineParser.StartMensContext):
        self.enterStart(ctx)

    def _reset_mensural_duration(self):
        self.mensural_figure = None
        self.mensural_perfection = ''
        self.mensural_coloured = ''
        self.mensural_dots = ''
        self.mensural_alterations = []

    def enterMensNote(self, ctx: kernMensSpineParser.MensNoteContext):
        self._reset_mensural_duration()

    def enterMensRest(self, ctx: kernMensSpineParser.MensRestContext):
        self._reset_mensural_duration()

    def exitMensuralFigure(self, ctx: kernMensSpineParser.MensuralFigureContext):
        self.mensural_figure = ctx.getText()

    def exitMensuralPerfection(self, ctx: kernMensSpineParser.MensuralPerfectionContext):
        self.mensural_perfection += ctx.getText()

    def exitColoured(self, ctx: kernMensSpineParser.ColouredContext):
        self.mensural_coloured = '~'

    def exitMensuralDot(self, ctx: kernMensSpineParser.MensuralDotContext):
        self.mensural_dots += ctx.getText()

    def _mensural_duration_subtokens(self):
        if self.mensural_figure is None:
            return []
        encoding = self.mensural_figure + self.mensural_perfection + self.mensural_coloured + self.mensural_dots
        return [Subtoken(encoding, TokenCategory.DURATION)]

    def exitMensAlteration(self, ctx: kernMensSpineParser.MensAlterationContext):
        self.mensural_alterations.append(Subtoken(ctx.getText(), TokenCategory.ALTERATION))

    def exitMensNoteDecoration(self, ctx: kernMensSpineParser.MensNoteDecorationContext):
        self._add_decoration(Subtoken(ctx.getText(), TokenCategory.DECORATION))

    def exitMensNoteSignifierAfterFigure(self, ctx: kernMensSpineParser.MensNoteSignifierAfterFigureContext):
        # Beams and the editorial mark are not mensNoteDecorations: after the figure `L` is a beam (`UaL`)
        # and `X` an editorial mark (`MbX#`); before it they are the longa and the maxima.
        if ctx.beam() is not None or ctx.editorialIntervention() is not None:
            self._add_decoration(Subtoken(ctx.getText(), TokenCategory.DECORATION))

    def exitMensNote(self, ctx: kernMensSpineParser.MensNoteContext):
        subtokens = self._mensural_duration_subtokens()
        subtokens.append(self.diatonic_pitch_and_octave_subtoken)
        subtokens.extend(self.mensural_alterations)
        self.addNoteRest(ctx, subtokens)

    def exitMensRest(self, ctx: kernMensSpineParser.MensRestContext):
        subtokens = self._mensural_duration_subtokens()
        subtokens.append(Subtoken('r', TokenCategory.REST))
        self.addNoteRest(ctx, subtokens)

    def enterMensChord(self, ctx: kernMensSpineParser.MensChordContext):
        self.enterChord(ctx)

    def exitMensChord(self, ctx: kernMensSpineParser.MensChordContext):
        self.exitChord(ctx)

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

        tree = self._parse(encoding, kernMensSpineLexer, kernMensSpineParser, 'startMens')
        listener = MensSpineListener()
        ParseTreeWalker().walk(listener, tree)
        if self.error_listener.getNumberErrorsFound() > 0:
            raise ValueError(str(self.error_listener).strip())
        return listener.token
