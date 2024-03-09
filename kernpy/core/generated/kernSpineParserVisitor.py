# Generated from kernSpineParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .kernSpineParser import kernSpineParser
else:
    from kernSpineParser import kernSpineParser

# This class defines a complete generic visitor for a parse tree produced by kernSpineParser.

class kernSpineParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by kernSpineParser#start.
    def visitStart(self, ctx:kernSpineParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#field.
    def visitField(self, ctx:kernSpineParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#notes_rests_chords.
    def visitNotes_rests_chords(self, ctx:kernSpineParser.Notes_rests_chordsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#structural.
    def visitStructural(self, ctx:kernSpineParser.StructuralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#contextual.
    def visitContextual(self, ctx:kernSpineParser.ContextualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#signatures.
    def visitSignatures(self, ctx:kernSpineParser.SignaturesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#otherContextual.
    def visitOtherContextual(self, ctx:kernSpineParser.OtherContextualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#empty.
    def visitEmpty(self, ctx:kernSpineParser.EmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#rest.
    def visitRest(self, ctx:kernSpineParser.RestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#restChar_r.
    def visitRestChar_r(self, ctx:kernSpineParser.RestChar_rContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#restDecoration.
    def visitRestDecoration(self, ctx:kernSpineParser.RestDecorationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#chord.
    def visitChord(self, ctx:kernSpineParser.ChordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#note.
    def visitNote(self, ctx:kernSpineParser.NoteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#nonVisualTandemInterpretation.
    def visitNonVisualTandemInterpretation(self, ctx:kernSpineParser.NonVisualTandemInterpretationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#boundingBox.
    def visitBoundingBox(self, ctx:kernSpineParser.BoundingBoxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#xywh.
    def visitXywh(self, ctx:kernSpineParser.XywhContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#x.
    def visitX(self, ctx:kernSpineParser.XContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#y.
    def visitY(self, ctx:kernSpineParser.YContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#w.
    def visitW(self, ctx:kernSpineParser.WContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#h.
    def visitH(self, ctx:kernSpineParser.HContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#pageNumber.
    def visitPageNumber(self, ctx:kernSpineParser.PageNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#visualTandemInterpretation.
    def visitVisualTandemInterpretation(self, ctx:kernSpineParser.VisualTandemInterpretationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#associatedIDS.
    def visitAssociatedIDS(self, ctx:kernSpineParser.AssociatedIDSContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#placeHolder.
    def visitPlaceHolder(self, ctx:kernSpineParser.PlaceHolderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#octaveShift.
    def visitOctaveShift(self, ctx:kernSpineParser.OctaveShiftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#pianoHand.
    def visitPianoHand(self, ctx:kernSpineParser.PianoHandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#tandemTuplet.
    def visitTandemTuplet(self, ctx:kernSpineParser.TandemTupletContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#tandemCue.
    def visitTandemCue(self, ctx:kernSpineParser.TandemCueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#tandemTremolo.
    def visitTandemTremolo(self, ctx:kernSpineParser.TandemTremoloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#ossia.
    def visitOssia(self, ctx:kernSpineParser.OssiaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#rscale.
    def visitRscale(self, ctx:kernSpineParser.RscaleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#pedal.
    def visitPedal(self, ctx:kernSpineParser.PedalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#ela.
    def visitEla(self, ctx:kernSpineParser.ElaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#dynamics_position.
    def visitDynamics_position(self, ctx:kernSpineParser.Dynamics_positionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#sections.
    def visitSections(self, ctx:kernSpineParser.SectionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#sectionNames.
    def visitSectionNames(self, ctx:kernSpineParser.SectionNamesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#sectionName.
    def visitSectionName(self, ctx:kernSpineParser.SectionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#transposition.
    def visitTransposition(self, ctx:kernSpineParser.TranspositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#instrument.
    def visitInstrument(self, ctx:kernSpineParser.InstrumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#instrumentTitle.
    def visitInstrumentTitle(self, ctx:kernSpineParser.InstrumentTitleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#number.
    def visitNumber(self, ctx:kernSpineParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#lowerCasePitch.
    def visitLowerCasePitch(self, ctx:kernSpineParser.LowerCasePitchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#upperCasePitch.
    def visitUpperCasePitch(self, ctx:kernSpineParser.UpperCasePitchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#pitchClass.
    def visitPitchClass(self, ctx:kernSpineParser.PitchClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#accomp.
    def visitAccomp(self, ctx:kernSpineParser.AccompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#solo.
    def visitSolo(self, ctx:kernSpineParser.SoloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#strophe.
    def visitStrophe(self, ctx:kernSpineParser.StropheContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#timebase.
    def visitTimebase(self, ctx:kernSpineParser.TimebaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#part.
    def visitPart(self, ctx:kernSpineParser.PartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#group.
    def visitGroup(self, ctx:kernSpineParser.GroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#staff.
    def visitStaff(self, ctx:kernSpineParser.StaffContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#clef.
    def visitClef(self, ctx:kernSpineParser.ClefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#clefValue.
    def visitClefValue(self, ctx:kernSpineParser.ClefValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#clefSign.
    def visitClefSign(self, ctx:kernSpineParser.ClefSignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#clefLine.
    def visitClefLine(self, ctx:kernSpineParser.ClefLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#clefOctave.
    def visitClefOctave(self, ctx:kernSpineParser.ClefOctaveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#keySignature.
    def visitKeySignature(self, ctx:kernSpineParser.KeySignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#keySignaturePitchClass.
    def visitKeySignaturePitchClass(self, ctx:kernSpineParser.KeySignaturePitchClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#keySignatureCancel.
    def visitKeySignatureCancel(self, ctx:kernSpineParser.KeySignatureCancelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#keyCancel.
    def visitKeyCancel(self, ctx:kernSpineParser.KeyCancelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#keyMode.
    def visitKeyMode(self, ctx:kernSpineParser.KeyModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#key.
    def visitKey(self, ctx:kernSpineParser.KeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#singleKey.
    def visitSingleKey(self, ctx:kernSpineParser.SingleKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#minorKey.
    def visitMinorKey(self, ctx:kernSpineParser.MinorKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#majorKey.
    def visitMajorKey(self, ctx:kernSpineParser.MajorKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#modal.
    def visitModal(self, ctx:kernSpineParser.ModalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#locrian.
    def visitLocrian(self, ctx:kernSpineParser.LocrianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#ionian.
    def visitIonian(self, ctx:kernSpineParser.IonianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#aeolian.
    def visitAeolian(self, ctx:kernSpineParser.AeolianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#mixolydian.
    def visitMixolydian(self, ctx:kernSpineParser.MixolydianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#lydian.
    def visitLydian(self, ctx:kernSpineParser.LydianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#phrygian.
    def visitPhrygian(self, ctx:kernSpineParser.PhrygianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#dorian.
    def visitDorian(self, ctx:kernSpineParser.DorianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#timeSignature.
    def visitTimeSignature(self, ctx:kernSpineParser.TimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#numerator.
    def visitNumerator(self, ctx:kernSpineParser.NumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#denominator.
    def visitDenominator(self, ctx:kernSpineParser.DenominatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#standardTimeSignature.
    def visitStandardTimeSignature(self, ctx:kernSpineParser.StandardTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#additiveTimeSignature.
    def visitAdditiveTimeSignature(self, ctx:kernSpineParser.AdditiveTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#mixedTimeSignature.
    def visitMixedTimeSignature(self, ctx:kernSpineParser.MixedTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#alternatingTimeSignature.
    def visitAlternatingTimeSignature(self, ctx:kernSpineParser.AlternatingTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#alternatingTimeSignatureItem.
    def visitAlternatingTimeSignatureItem(self, ctx:kernSpineParser.AlternatingTimeSignatureItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#interchangingTimeSignature.
    def visitInterchangingTimeSignature(self, ctx:kernSpineParser.InterchangingTimeSignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#meterSymbol.
    def visitMeterSymbol(self, ctx:kernSpineParser.MeterSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#modernMeterSymbolSign.
    def visitModernMeterSymbolSign(self, ctx:kernSpineParser.ModernMeterSymbolSignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#mensuration.
    def visitMensuration(self, ctx:kernSpineParser.MensurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#metronome.
    def visitMetronome(self, ctx:kernSpineParser.MetronomeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#nullInterpretation.
    def visitNullInterpretation(self, ctx:kernSpineParser.NullInterpretationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#barline.
    def visitBarline(self, ctx:kernSpineParser.BarlineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#barLineType.
    def visitBarLineType(self, ctx:kernSpineParser.BarLineTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#restPosition.
    def visitRestPosition(self, ctx:kernSpineParser.RestPositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#duration.
    def visitDuration(self, ctx:kernSpineParser.DurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#fermata.
    def visitFermata(self, ctx:kernSpineParser.FermataContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#modernDuration.
    def visitModernDuration(self, ctx:kernSpineParser.ModernDurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#augmentationDot.
    def visitAugmentationDot(self, ctx:kernSpineParser.AugmentationDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#alteration.
    def visitAlteration(self, ctx:kernSpineParser.AlterationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#staffChange.
    def visitStaffChange(self, ctx:kernSpineParser.StaffChangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#chordSpace.
    def visitChordSpace(self, ctx:kernSpineParser.ChordSpaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#graceNote.
    def visitGraceNote(self, ctx:kernSpineParser.GraceNoteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#appoggiatura.
    def visitAppoggiatura(self, ctx:kernSpineParser.AppoggiaturaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#appoggiaturaMode.
    def visitAppoggiaturaMode(self, ctx:kernSpineParser.AppoggiaturaModeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#ligatureTie.
    def visitLigatureTie(self, ctx:kernSpineParser.LigatureTieContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#noteDecoration.
    def visitNoteDecoration(self, ctx:kernSpineParser.NoteDecorationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#noteDecorationCharX.
    def visitNoteDecorationCharX(self, ctx:kernSpineParser.NoteDecorationCharXContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#phrase.
    def visitPhrase(self, ctx:kernSpineParser.PhraseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#diatonicPitchAndOctave.
    def visitDiatonicPitchAndOctave(self, ctx:kernSpineParser.DiatonicPitchAndOctaveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#trebleNotes.
    def visitTrebleNotes(self, ctx:kernSpineParser.TrebleNotesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#bassNotes.
    def visitBassNotes(self, ctx:kernSpineParser.BassNotesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#accidental.
    def visitAccidental(self, ctx:kernSpineParser.AccidentalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#alterationDisplay.
    def visitAlterationDisplay(self, ctx:kernSpineParser.AlterationDisplayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#turn.
    def visitTurn(self, ctx:kernSpineParser.TurnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#userAssignable.
    def visitUserAssignable(self, ctx:kernSpineParser.UserAssignableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#glissando.
    def visitGlissando(self, ctx:kernSpineParser.GlissandoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#articulation.
    def visitArticulation(self, ctx:kernSpineParser.ArticulationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#accent.
    def visitAccent(self, ctx:kernSpineParser.AccentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#tenuto.
    def visitTenuto(self, ctx:kernSpineParser.TenutoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#staccatissimo.
    def visitStaccatissimo(self, ctx:kernSpineParser.StaccatissimoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#pizzicato.
    def visitPizzicato(self, ctx:kernSpineParser.PizzicatoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#spiccato.
    def visitSpiccato(self, ctx:kernSpineParser.SpiccatoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#staccato.
    def visitStaccato(self, ctx:kernSpineParser.StaccatoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#editorialIntervention.
    def visitEditorialIntervention(self, ctx:kernSpineParser.EditorialInterventionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#slurStart.
    def visitSlurStart(self, ctx:kernSpineParser.SlurStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#ligatureTieStart.
    def visitLigatureTieStart(self, ctx:kernSpineParser.LigatureTieStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#tieContinue.
    def visitTieContinue(self, ctx:kernSpineParser.TieContinueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#ligatureTieEnd.
    def visitLigatureTieEnd(self, ctx:kernSpineParser.LigatureTieEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#slurEnd.
    def visitSlurEnd(self, ctx:kernSpineParser.SlurEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#barLineCrossedNoteStart.
    def visitBarLineCrossedNoteStart(self, ctx:kernSpineParser.BarLineCrossedNoteStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#barLineCrossedNoteEnd.
    def visitBarLineCrossedNoteEnd(self, ctx:kernSpineParser.BarLineCrossedNoteEndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#stem.
    def visitStem(self, ctx:kernSpineParser.StemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#beam.
    def visitBeam(self, ctx:kernSpineParser.BeamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#mordent.
    def visitMordent(self, ctx:kernSpineParser.MordentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#trill.
    def visitTrill(self, ctx:kernSpineParser.TrillContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by kernSpineParser#footnote.
    def visitFootnote(self, ctx:kernSpineParser.FootnoteContext):
        return self.visitChildren(ctx)



del kernSpineParser