# Generated from kernMensSpineParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .kernMensSpineParser import kernMensSpineParser
else:
    from kernMensSpineParser import kernMensSpineParser

# This class defines a complete generic visitor for a parse tree produced by kernMensSpineParser.

class kernMensSpineParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by kernMensSpineParser#start.
    def visitStart(self, ctx:kernMensSpineParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#field.
    def visitField(self, ctx:kernMensSpineParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#layout.
    def visitLayout(self, ctx:kernMensSpineParser.LayoutContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#lineBreak.
    def visitLineBreak(self, ctx:kernMensSpineParser.LineBreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#pageBreak.
    def visitPageBreak(self, ctx:kernMensSpineParser.PageBreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#notes_rests_chords.
    def visitNotes_rests_chords(self, ctx:kernMensSpineParser.Notes_rests_chordsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#structural.
    def visitStructural(self, ctx:kernMensSpineParser.StructuralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#contextual.
    def visitContextual(self, ctx:kernMensSpineParser.ContextualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#signatures.
    def visitSignatures(self, ctx:kernMensSpineParser.SignaturesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#otherContextual.
    def visitOtherContextual(self, ctx:kernMensSpineParser.OtherContextualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#empty.
    def visitEmpty(self, ctx:kernMensSpineParser.EmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#rest.
    def visitRest(self, ctx:kernMensSpineParser.RestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#restChar_r.
    def visitRestChar_r(self, ctx:kernMensSpineParser.RestChar_rContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#restDecoration.
    def visitRestDecoration(self, ctx:kernMensSpineParser.RestDecorationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#multirest.
    def visitMultirest(self, ctx:kernMensSpineParser.MultirestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#chord.
    def visitChord(self, ctx:kernMensSpineParser.ChordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#note.
    def visitNote(self, ctx:kernMensSpineParser.NoteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#nonVisualTandemInterpretation.
    def visitNonVisualTandemInterpretation(self, ctx:kernMensSpineParser.NonVisualTandemInterpretationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#boundingBox.
    def visitBoundingBox(self, ctx:kernMensSpineParser.BoundingBoxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#xywh.
    def visitXywh(self, ctx:kernMensSpineParser.XywhContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#x.
    def visitX(self, ctx:kernMensSpineParser.XContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#y.
    def visitY(self, ctx:kernMensSpineParser.YContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#w.
    def visitW(self, ctx:kernMensSpineParser.WContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#h.
    def visitH(self, ctx:kernMensSpineParser.HContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#pageNumber.
    def visitPageNumber(self, ctx:kernMensSpineParser.PageNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#visualTandemInterpretation.
    def visitVisualTandemInterpretation(self, ctx:kernMensSpineParser.VisualTandemInterpretationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#placeHolder.
    def visitPlaceHolder(self, ctx:kernMensSpineParser.PlaceHolderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#octaveShift.
    def visitOctaveShift(self, ctx:kernMensSpineParser.OctaveShiftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#pianoHand.
    def visitPianoHand(self, ctx:kernMensSpineParser.PianoHandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#tandemTuplet.
    def visitTandemTuplet(self, ctx:kernMensSpineParser.TandemTupletContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#tandemCue.
    def visitTandemCue(self, ctx:kernMensSpineParser.TandemCueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#tandemTremolo.
    def visitTandemTremolo(self, ctx:kernMensSpineParser.TandemTremoloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#ossia.
    def visitOssia(self, ctx:kernMensSpineParser.OssiaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#rscale.
    def visitRscale(self, ctx:kernMensSpineParser.RscaleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#pedal.
    def visitPedal(self, ctx:kernMensSpineParser.PedalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#ela.
    def visitEla(self, ctx:kernMensSpineParser.ElaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#dynamics_position.
    def visitDynamics_position(self, ctx:kernMensSpineParser.Dynamics_positionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#sections.
    def visitSections(self, ctx:kernMensSpineParser.SectionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#sectionNames.
    def visitSectionNames(self, ctx:kernMensSpineParser.SectionNamesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#sectionName.
    def visitSectionName(self, ctx:kernMensSpineParser.SectionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#transposition.
    def visitTransposition(self, ctx:kernMensSpineParser.TranspositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#instrument.
    def visitInstrument(self, ctx:kernMensSpineParser.InstrumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#instrumentTitle.
    def visitInstrumentTitle(self, ctx:kernMensSpineParser.InstrumentTitleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#number.
    def visitNumber(self, ctx:kernMensSpineParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#lowerCasePitch.
    def visitLowerCasePitch(self, ctx:kernMensSpineParser.LowerCasePitchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#upperCasePitch.
    def visitUpperCasePitch(self, ctx:kernMensSpineParser.UpperCasePitchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#pitchClass.
    def visitPitchClass(self, ctx:kernMensSpineParser.PitchClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#accomp.
    def visitAccomp(self, ctx:kernMensSpineParser.AccompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#solo.
    def visitSolo(self, ctx:kernMensSpineParser.SoloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#strophe.
    def visitStrophe(self, ctx:kernMensSpineParser.StropheContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#timebase.
    def visitTimebase(self, ctx:kernMensSpineParser.TimebaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#part.
    def visitPart(self, ctx:kernMensSpineParser.PartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#group.
    def visitGroup(self, ctx:kernMensSpineParser.GroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#staff.
    def visitStaff(self, ctx:kernMensSpineParser.StaffContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#clef.
    def visitClef(self, ctx:kernMensSpineParser.ClefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#clefValue.
    def visitClefValue(self, ctx:kernMensSpineParser.ClefValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#clefSign.
    def visitClefSign(self, ctx:kernMensSpineParser.ClefSignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#clefLine.
    def visitClefLine(self, ctx:kernMensSpineParser.ClefLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#clefOctave.
    def visitClefOctave(self, ctx:kernMensSpineParser.ClefOctaveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#keySignature.
    def visitKeySignature(self, ctx:kernMensSpineParser.KeySignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#keySignaturePitchClass.
    def visitKeySignaturePitchClass(self, ctx:kernMensSpineParser.KeySignaturePitchClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#keySignatureCancel.
    def visitKeySignatureCancel(self, ctx:kernMensSpineParser.KeySignatureCancelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#keyCancel.
    def visitKeyCancel(self, ctx:kernMensSpineParser.KeyCancelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#keyMode.
    def visitKeyMode(self, ctx:kernMensSpineParser.KeyModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#key.
    def visitKey(self, ctx:kernMensSpineParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#singleKey.
    def visitSingleKey(self, ctx:kernMensSpineParser.SingleKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#minorKey.
    def visitMinorKey(self, ctx:kernMensSpineParser.MinorKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#majorKey.
    def visitMajorKey(self, ctx:kernMensSpineParser.MajorKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#modal.
    def visitModal(self, ctx:kernMensSpineParser.ModalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#locrian.
    def visitLocrian(self, ctx:kernMensSpineParser.LocrianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#ionian.
    def visitIonian(self, ctx:kernMensSpineParser.IonianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#aeolian.
    def visitAeolian(self, ctx:kernMensSpineParser.AeolianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mixolydian.
    def visitMixolydian(self, ctx:kernMensSpineParser.MixolydianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#lydian.
    def visitLydian(self, ctx:kernMensSpineParser.LydianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#phrygian.
    def visitPhrygian(self, ctx:kernMensSpineParser.PhrygianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#dorian.
    def visitDorian(self, ctx:kernMensSpineParser.DorianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#timeSignature.
    def visitTimeSignature(self, ctx:kernMensSpineParser.TimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#numerator.
    def visitNumerator(self, ctx:kernMensSpineParser.NumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#denominator.
    def visitDenominator(self, ctx:kernMensSpineParser.DenominatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#standardTimeSignature.
    def visitStandardTimeSignature(self, ctx:kernMensSpineParser.StandardTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#additiveTimeSignature.
    def visitAdditiveTimeSignature(self, ctx:kernMensSpineParser.AdditiveTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mixedTimeSignature.
    def visitMixedTimeSignature(self, ctx:kernMensSpineParser.MixedTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#alternatingTimeSignature.
    def visitAlternatingTimeSignature(self, ctx:kernMensSpineParser.AlternatingTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#alternatingTimeSignatureItem.
    def visitAlternatingTimeSignatureItem(self, ctx:kernMensSpineParser.AlternatingTimeSignatureItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#interchangingTimeSignature.
    def visitInterchangingTimeSignature(self, ctx:kernMensSpineParser.InterchangingTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#meterSymbol.
    def visitMeterSymbol(self, ctx:kernMensSpineParser.MeterSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mensurationSpecification.
    def visitMensurationSpecification(self, ctx:kernMensSpineParser.MensurationSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#modernMeterSymbolSign.
    def visitModernMeterSymbolSign(self, ctx:kernMensSpineParser.ModernMeterSymbolSignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mensuration.
    def visitMensuration(self, ctx:kernMensSpineParser.MensurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#maximodus.
    def visitMaximodus(self, ctx:kernMensSpineParser.MaximodusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#modusMinor.
    def visitModusMinor(self, ctx:kernMensSpineParser.ModusMinorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#tempus.
    def visitTempus(self, ctx:kernMensSpineParser.TempusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#prolatio.
    def visitProlatio(self, ctx:kernMensSpineParser.ProlatioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#metronome.
    def visitMetronome(self, ctx:kernMensSpineParser.MetronomeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#nullInterpretation.
    def visitNullInterpretation(self, ctx:kernMensSpineParser.NullInterpretationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#barline.
    def visitBarline(self, ctx:kernMensSpineParser.BarlineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#barLineType.
    def visitBarLineType(self, ctx:kernMensSpineParser.BarLineTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#custos.
    def visitCustos(self, ctx:kernMensSpineParser.CustosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#restPosition.
    def visitRestPosition(self, ctx:kernMensSpineParser.RestPositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#restLinePosition.
    def visitRestLinePosition(self, ctx:kernMensSpineParser.RestLinePositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#duration.
    def visitDuration(self, ctx:kernMensSpineParser.DurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#modernDuration.
    def visitModernDuration(self, ctx:kernMensSpineParser.ModernDurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#modernFigure.
    def visitModernFigure(self, ctx:kernMensSpineParser.ModernFigureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#augmentationDot.
    def visitAugmentationDot(self, ctx:kernMensSpineParser.AugmentationDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#fermata.
    def visitFermata(self, ctx:kernMensSpineParser.FermataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mensuralDuration.
    def visitMensuralDuration(self, ctx:kernMensSpineParser.MensuralDurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mensuralDot.
    def visitMensuralDot(self, ctx:kernMensSpineParser.MensuralDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#coloured.
    def visitColoured(self, ctx:kernMensSpineParser.ColouredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mensuralFigure.
    def visitMensuralFigure(self, ctx:kernMensSpineParser.MensuralFigureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mensuralPerfection.
    def visitMensuralPerfection(self, ctx:kernMensSpineParser.MensuralPerfectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#divisionDot.
    def visitDivisionDot(self, ctx:kernMensSpineParser.DivisionDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#alteration.
    def visitAlteration(self, ctx:kernMensSpineParser.AlterationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#staffChange.
    def visitStaffChange(self, ctx:kernMensSpineParser.StaffChangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#chordSpace.
    def visitChordSpace(self, ctx:kernMensSpineParser.ChordSpaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#graceNote.
    def visitGraceNote(self, ctx:kernMensSpineParser.GraceNoteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#appoggiatura.
    def visitAppoggiatura(self, ctx:kernMensSpineParser.AppoggiaturaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#appoggiaturaMode.
    def visitAppoggiaturaMode(self, ctx:kernMensSpineParser.AppoggiaturaModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#ligatureTie.
    def visitLigatureTie(self, ctx:kernMensSpineParser.LigatureTieContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#noteDecoration.
    def visitNoteDecoration(self, ctx:kernMensSpineParser.NoteDecorationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#noteDecorationCharX.
    def visitNoteDecorationCharX(self, ctx:kernMensSpineParser.NoteDecorationCharXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#phrase.
    def visitPhrase(self, ctx:kernMensSpineParser.PhraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#diatonicPitchAndOctave.
    def visitDiatonicPitchAndOctave(self, ctx:kernMensSpineParser.DiatonicPitchAndOctaveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#trebleNotes.
    def visitTrebleNotes(self, ctx:kernMensSpineParser.TrebleNotesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#bassNotes.
    def visitBassNotes(self, ctx:kernMensSpineParser.BassNotesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#accidental.
    def visitAccidental(self, ctx:kernMensSpineParser.AccidentalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#alterationDisplay.
    def visitAlterationDisplay(self, ctx:kernMensSpineParser.AlterationDisplayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#turn.
    def visitTurn(self, ctx:kernMensSpineParser.TurnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#userAssignable.
    def visitUserAssignable(self, ctx:kernMensSpineParser.UserAssignableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#glissando.
    def visitGlissando(self, ctx:kernMensSpineParser.GlissandoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#articulation.
    def visitArticulation(self, ctx:kernMensSpineParser.ArticulationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#accent.
    def visitAccent(self, ctx:kernMensSpineParser.AccentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#tenuto.
    def visitTenuto(self, ctx:kernMensSpineParser.TenutoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#staccatissimo.
    def visitStaccatissimo(self, ctx:kernMensSpineParser.StaccatissimoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#pizzicato.
    def visitPizzicato(self, ctx:kernMensSpineParser.PizzicatoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#spiccato.
    def visitSpiccato(self, ctx:kernMensSpineParser.SpiccatoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#staccato.
    def visitStaccato(self, ctx:kernMensSpineParser.StaccatoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#editorialIntervention.
    def visitEditorialIntervention(self, ctx:kernMensSpineParser.EditorialInterventionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#slurStart.
    def visitSlurStart(self, ctx:kernMensSpineParser.SlurStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#ligatureTieStart.
    def visitLigatureTieStart(self, ctx:kernMensSpineParser.LigatureTieStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#tieContinue.
    def visitTieContinue(self, ctx:kernMensSpineParser.TieContinueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#ligatureTieEnd.
    def visitLigatureTieEnd(self, ctx:kernMensSpineParser.LigatureTieEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#slurEnd.
    def visitSlurEnd(self, ctx:kernMensSpineParser.SlurEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#barLineCrossedNoteStart.
    def visitBarLineCrossedNoteStart(self, ctx:kernMensSpineParser.BarLineCrossedNoteStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#barLineCrossedNoteEnd.
    def visitBarLineCrossedNoteEnd(self, ctx:kernMensSpineParser.BarLineCrossedNoteEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#stem.
    def visitStem(self, ctx:kernMensSpineParser.StemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#beam.
    def visitBeam(self, ctx:kernMensSpineParser.BeamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#mordent.
    def visitMordent(self, ctx:kernMensSpineParser.MordentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#trill.
    def visitTrill(self, ctx:kernMensSpineParser.TrillContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#footnote.
    def visitFootnote(self, ctx:kernMensSpineParser.FootnoteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernMensSpineParser#signumCongruentiae.
    def visitSignumCongruentiae(self, ctx:kernMensSpineParser.SignumCongruentiaeContext):
        return self.visitChildren(ctx)



del kernMensSpineParser