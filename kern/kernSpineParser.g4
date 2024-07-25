/*
This grammar is used in mOOsicae and kernpy. It must be kept synchronised
Changes (please, add here the authors and date of each change):

@author: David Rizo (drizo@dlsi.ua.es) Feb, 2024.
It parses just a token inside a **kern spine
*/
parser grammar kernSpineParser;

options { tokenVocab=kernSpineLexer;} // use tokens from kernSpineLexer.g4

start: field;

field
    :
    notes_rests_chords
    |
    structural
    |
    contextual
    |
    barline
    |
    empty
    |
    visualTandemInterpretation
    |
    nonVisualTandemInterpretation
    |
    boundingBox
    ;

notes_rests_chords: note | rest | chord;

structural: staff;
// those that must be maintained if the file is divided into segments
contextual:
    signatures
    |
    otherContextual
    ;

signatures: clef | timeSignature | meterSymbol | keyCancel | keySignature;

otherContextual: octaveShift
                     |
                     key
                     |
                     metronome;

empty: nullInterpretation | placeHolder;


rest: restDecoration* duration? restChar_r // duration not used in some grace notes (rests)
    restDecoration*;

restChar_r: CHAR_r CHAR_r?;

restDecoration: (slurStart | graceNote | staffChange | restPosition | fermata | editorialIntervention | slurEnd | // slur sometimes found
    staccato | // staccato found in a rest in beethoven/quartets/quartet14-5.krn
    phrase |
    augmentationDot |
    stem // even it does not make sense, it has appeared sometimes, we'l discard it in the code
    CHAR_j);

// We allow the chordSpace to be null for allowing invalid outputs of the OMR
// Rests are allowed to be in chords for cases such as bach/wtc/wtc1f06.krn:
// !! Four-voice material to the end:
//2.D	8r 8r	8r 8r	2.dd
chord: (note | rest) (chordSpace (note | rest))+;


// The correct orderEntities of notes is: beforeNote duration name staffChange afterNote, however, if changes in some encodings - as it does not work, we use noteDecorations? for any decoration in any position
note:
    noteDecoration* // TODO Regla semantica (boolean) para que no se repitan
    duration? // grace notes can be specified without durations
    noteDecoration*
    diatonicPitchAndOctave
    noteDecoration*
    alteration?
    //name
    noteDecoration*;
    // TODO in aferNote staffChange? // it must be placed immediately after the name+accidental tokens. This is because they also can modify the beam, as well as articulation, slur and tie positions


// those ones that are not engraved
nonVisualTandemInterpretation:
    timebase
    |
    solo
    |
    accomp
    |
    strophe
    |
    part
    |
    group
    |
    instrument
    |
    instrumentTitle
    |
    transposition
    |
    sections
    |
    pianoHand
    |
    ossia //TODO bach/wtc/wtc1f01.krn
    ;

    boundingBox: TANDEM_BOUNDING_BOX MINUS pageNumber COLON xywh;

    xywh: x COMMA y COMMA w COMMA h;
    x: number;
    y: number;
    w: number;
    h: number;
    pageNumber: ~':'*; // anything until the ':'



// those ones that are engraved
visualTandemInterpretation:
    dynamics_position // TODO: what is it for?
    |
    tandemCue
    |
    tandemTremolo
    |
    rscale
    |
    pedal
    |
    ela // sometimes found
    |
    tandemTuplet // sometimes found
    |
    TANDEM_TSTART | TANDEM_TEND // sometimes found
    ;


/* ----- LEAF RULES ----- */

associatedIDS: number (COMMA associatedIDS)*; // used for agnostic IDS in semantic mens

placeHolder: DOT;

octaveShift: OCTAVE_SHIFT;

pianoHand: TANDEM_LEFT_HAND | TANDEM_RIGHT_HAND;

tandemTuplet: TANDEM_TUPLET_START | TANDEM_TUPLET_END;

tandemCue: TANDEM_CUE_START | TANDEM_CUE_END;

tandemTremolo: TANDEM_TREMOLO_START | TANDEM_TREMOLO_END;

ossia: TANDEM_SIC | TANDEM_OSSIA | TANDEM_FIN | TANDEM_SMINUS;

rscale: TANDEM_RSCALE COLON number (SLASH number)?;

pedal: TANDEM_PEDAL_START | TANDEM_PEDAL_END;

ela: TANDEM_ELA;

dynamics_position: TANDEM_ABOVE | TANDEM_BELOW | TANDEM_CENTERED; //TODO It is not rendered in VHV

sections: TANDEM_SECTION
    (
        (NO_REPEAT? LEFT_BRACKET sectionNames RIGHT_BRACKET)
        |
        (sectionName)
    );

sectionNames: sectionName (COMMA sectionName)*;

// TODO
sectionName: (CHAR_A | CHAR_B | CHAR_C | CHAR_D | CHAR_E | CHAR_F | CHAR_G | CHAR_H | CHAR_I | CHAR_J | CHAR_K | CHAR_L |
    CHAR_M | CHAR_N | CHAR_O | CHAR_P | CHAR_Q | CHAR_R | CHAR_S | CHAR_T |
    CHAR_U | CHAR_V | CHAR_W | CHAR_X | CHAR_Y | CHAR_Z |
    CHAR_a | CHAR_b | CHAR_c | CHAR_d | CHAR_e | CHAR_f | CHAR_g | CHAR_h | CHAR_i | CHAR_j | CHAR_k | CHAR_l |
    CHAR_m | CHAR_n | CHAR_o | CHAR_p | CHAR_q | CHAR_r | CHAR_s | CHAR_t |
    CHAR_u | CHAR_v | CHAR_w | CHAR_x | CHAR_y | CHAR_z | SPACE // space for things like *>1st ending
    | number)+;

transposition: TANDEM_TRANSPOSITION CHAR_d MINUS? number CHAR_c MINUS? number;

instrument: INSTRUMENT;

instrumentTitle: INSTRUMENT_TITLE;

number: (DIGIT_0 | DIGIT_1 | DIGIT_2 | DIGIT_3 | DIGIT_4 | DIGIT_5 | DIGIT_6 | DIGIT_7 | DIGIT_8 | DIGIT_9)+;
lowerCasePitch: (CHAR_a | CHAR_b | CHAR_c | CHAR_d | CHAR_e | CHAR_f | CHAR_g); // we cannot use a generic rule because c is used both name and as common time symbol
upperCasePitch: (CHAR_A | CHAR_B | CHAR_C | CHAR_D | CHAR_E | CHAR_F | CHAR_G);

// e.g. f-
pitchClass: lowerCasePitch accidental;

accomp: TANDEM_ACCOMP; // found in bach/brandenburg/bwv1050c.krn
solo: TANDEM_SOLO;
strophe: TANDEM_STROPHE;

timebase: TANDEM_TIMEBASE number;
part: TANDEM_PART  number;
group: TANDEM_GROUP  number; // new March 2024

staff: TANDEM_STAFF
    PLUS? // sometimes found
    number (SLASH number)?;

// e.g. *clefG2
clef: TANDEM_CLEF  clefValue;

clefValue: clefSign clefOctave? clefLine?;
clefSign: CHAR_C | CHAR_F | CHAR_G | CHAR_P | CHAR_T;
clefLine: DIGIT_1 | DIGIT_2 | DIGIT_3 | DIGIT_4 | DIGIT_5;
clefOctave: CHAR_v CHAR_v? | CIRCUMFLEX CIRCUMFLEX?;

// e.g. *k[f#c#]
keySignature: TANDEM_KEY_SIGNATURE  LEFT_BRACKET keySignaturePitchClass* RIGHT_BRACKET keySignatureCancel?;
keySignaturePitchClass: pitchClass;
keySignatureCancel:  CHAR_X;
keyCancel: TANDEM_KEYCANCEL;

keyMode: (minorKey | majorKey | QUESTION_MARK); // *?: found in corelli/op1/op01n01c.krn
key: ASTERISK singleKey (SLASH singleKey)?; // found *C/a: in haydn/quartets/op54n2-03.krn
singleKey: keyMode keySignatureCancel? ((COLON modal?) | number?); // sometimes we've found a1, a3 (e.g. bwv1046g.krn)
minorKey: lowerCasePitch accidental?;
majorKey: upperCasePitch accidental?;
modal: dorian | phrygian | lydian | mixolydian | aeolian | ionian | locrian;

locrian: CHAR_l CHAR_o CHAR_c; //it could be used with literals, but this way we avoid possible ambiguities in bottom-up parsing

ionian: CHAR_i CHAR_o CHAR_n;

aeolian: CHAR_a CHAR_e CHAR_o;

mixolydian: CHAR_m CHAR_i CHAR_x;

lydian: CHAR_l CHAR_y CHAR_d;

phrygian: CHAR_p CHAR_h CHAR_r;

dorian: CHAR_d CHAR_o CHAR_r;

// e.g *M4/4
timeSignature: TANDEM_TIMESIGNATURE  (standardTimeSignature | additiveTimeSignature | mixedTimeSignature | alternatingTimeSignature | interchangingTimeSignature) ('%' '2')?; //TODO %2
numerator: number;
denominator: number;
standardTimeSignature: numerator SLASH denominator;
additiveTimeSignature: numerator (PLUS numerator)+ SLASH denominator;
mixedTimeSignature: standardTimeSignature (PLUS standardTimeSignature)+;
alternatingTimeSignature: alternatingTimeSignatureItem (COLON alternatingTimeSignatureItem)+;
alternatingTimeSignatureItem: standardTimeSignature (SEMICOLON number)?;
interchangingTimeSignature: standardTimeSignature PIPE standardTimeSignature;

// e.g. *met(c) *met(O|)
// Changed to accept r character to reverse the mensural symbol
//meterSymbol: TANDEM_MET LEFT_PARENTHESIS (modernMeterSymbolSign | mensuration) RIGHT_PARENTHESIS;
meterSymbol: (TANDEM_TIMESIGNATURE | TANDEM_MET)  LEFT_PARENTHESIS (modernMeterSymbolSign | mensuration) RIGHT_PARENTHESIS;
modernMeterSymbolSign: CHAR_c | CHAR_c PIPE;
//mensuration: CHAR_C (DIGIT2 | (CHAR_C PIPE) | DOT | CHAR_O DOT? (SLASH | PIPE)? DIGIT_3? | CHAR_C DIGIT_3 SLASH DIGIT_2 | CHAR_C PIPE DIGIT_3 SLASH DIGIT_2 | DIGIT_3); //TODO
mensuration: (CHAR_C | CHAR_O | DOT | PIPE | SLASH | DIGIT_2 | DIGIT_3 | CHAR_r)+; // now any combination, we should do it better ;) TODO: include CHAR_r for some mensural signs

metronome: METRONOME number ((DOT | MINUS) number)?;

nullInterpretation: ASTERISK; // a null interpretation (placeholder) will have just an ASTERISK_FRAGMENT


// e.g. == =-
//barline: EQUAL+ (NUMBER)? (COLON? barlineWidth? partialBarLine? COLON?) ; // COLON = repetition mark
barline: EQUAL EQUAL? // sometimes found == to denote system break
    number? (CHAR_a? CHAR_b?) //TODO repetitions?
    MINUS? // hidden
    barLineType?
    fermata?
    CHAR_j? // sometimes found
    DOT? // sometimes found
    footnote?; // sometimes found -- TODO should it be after any symbol?

//barlineWidth: (EXCLAMATION? PIPE EXCLAMATION?);

// e.g. !|:
barLineType:
    PIPE PIPE // double thin bar line
    |
    PIPE EXCLAMATION COLON? // sometimes found
    |
    PIPE COLON // left-repeat sometimes found
    |
    EXCLAMATION PIPE COLON // left-repeat
    |
    EQUAL? COLON PIPE EXCLAMATION // right-repeat -- sometimes we've found the structure ==:|!
    |
    COLON PIPE EXCLAMATION? PIPE COLON // left-right repeat (the exclamation should appear - corrected in parser)
    |
    COLON EXCLAMATION COLON // left-right repeat - wrong encoding (the exclamation should appear - corrected in parser)
    |
    COLON EXCLAMATION EXCLAMATION COLON
    |
    EQUAL // end bar line (the first equal is encoded in the skmBarLine rule)
    ;


//rest: duration CHAR_r CHAR_r? fermata? restLinePosition?;
restPosition: diatonicPitchAndOctave;
//restLinePosition: UNDERSCORE clefLine;

//duration: mensuralDuration | modernDuration;
duration: modernDuration augmentationDot* (graceNote | appoggiatura)?; // sometimes we've found a grace note between the duration and the name

fermata: SEMICOLON; // pause

modernDuration: number (PERCENT number)?; //TODO 40%3...

// p=perfect, i=imperfect, I=imperfect by alteratio
augmentationDot: DOT;


/*name: diatonicPitchAndOctave - lo quito porque creo que está repetido con noteDecorations
    graceNote?
    appoggiatura? 
    staffChange? 
    accent? 
    fermata? 
    trill? 
    alteration?
    CHAR_x?; // sometimes found*/

// e.g. 4e#j -> this is for accidental in brackets
alteration: accidental alterationDisplay?;


staffChange: ANGLE_BRACKET_OPEN | ANGLE_BRACKET_CLOSE;


chordSpace: SPACE?; // required for ekern translation

//TODO
// it may appear after or before the note
// sometimes the duration is found before or after the note
graceNote:
    //2024 duration? CHAR_q CHAR_q? duration?;
    CHAR_q CHAR_q?;

//TODO
// it may appear after or before the note
// sometimes the duration is found before or after the note
appoggiatura:
    //2024 duration? appoggiaturaMode duration?;
    appoggiaturaMode;

// The appoggiatura note itself is designated by the upper-case letter P, whereas the subsequent note (whose notated duration has been shortened) is designated by the lower-case letter p
appoggiaturaMode: CHAR_p | CHAR_P;

ligatureTie:
    (ligatureTieStart | ligatureTieEnd | tieContinue) staffChange?;

noteDecoration:
    accent 
    | appoggiatura
    | articulation 
    | barLineCrossedNoteStart
    | barLineCrossedNoteEnd
    | beam
    | editorialIntervention
    | fermata
    | footnote
    | glissando   
    | graceNote
    | ligatureTie
    | mordent
    | augmentationDot // sometimes found TODO Verlo con la duración
    | phrase
    | slurStart
    | slurEnd  
    | staffChange 
    | stem
    | turn
    | trill
    | userAssignable
    | CHAR_N // sometimes found - user assignable?
    | CHAR_j // sometimes found - user assignable?
    | CHAR_X // sometimes found - it does nothing
    | CHAR_Z // sometimes found - user assignable?
    | CHAR_O // sometimes found - generic ornament
    | CHAR_l // sometimes found - ???
    | CHAR_V // sometimes found - ???
    | noteDecorationCharX // TODO?
    ;

noteDecorationCharX: CHAR_x CHAR_x?; // sometimes found - ???

phrase: LEFT_CURLY_BRACES | RIGHT_CURLY_BRACES; // see https://www.humdrum.org/Humdrum/guide03.html


diatonicPitchAndOctave:
    bassNotes // BASS
    |
    trebleNotes
	;

trebleNotes: lowerCasePitch+;
bassNotes: upperCasePitch+;

// e.g. 4c--
// Changed to accept triple bemol
accidental: OCTOTHORPE (OCTOTHORPE OCTOTHORPE?)? | MINUS (MINUS MINUS?)? | CHAR_n;

// x is show, xx is shows editorial
//alterationVisualMode: CHAR_x CHAR_x?;
alterationDisplay:
        CHAR_x // sometimes found - TODO for?
        |
        CHAR_X // cautionary accidental
        |
        CHAR_i // editorial accidental, it does not imply position
        |
        CHAR_I // accidental placed above the note
        |
        CHAR_j // bracket
        |
        CHAR_Z // parentheses
        |
        (CHAR_y CHAR_y?) | (CHAR_Y CHAR_Y?); // X = editorial intervention


turn: CHAR_S // regular turn
    |
    DOLLAR // wagnerian turn
    ;

userAssignable: CHAR_i;

glissando: COLON;


articulation:
    staccato | spiccato | pizzicato | staccatissimo | tenuto | accent
    ;

accent: CIRCUMFLEX;

tenuto: TILDE;

staccatissimo: GRAVE_ACCENT;

pizzicato: QUOTATION_MARK;

spiccato: CHAR_s;

staccato: APOSTROPHE;

editorialIntervention:
    (CHAR_y CHAR_y* AT?) // hidden //@ footnote comment? // if yy --> hidden, we've found even yyy
    |
    CHAR_X; // associated no a note

slurStart: AMPERSAND* LEFT_PARENTHESIS staffChange?; // ampersand for ellision - staffChange sometimes found
ligatureTieStart: ANGLE_BRACKET_OPEN | LEFT_BRACKET CHAR_y?; // y for hidden;
tieContinue: UNDERSCORE;
ligatureTieEnd: ANGLE_BRACKET_CLOSE | RIGHT_BRACKET;
slurEnd: AMPERSAND* RIGHT_PARENTHESIS; // ampersand for ellision
barLineCrossedNoteStart: CHAR_T;
barLineCrossedNoteEnd: CHAR_t;

// it can be found before or after the note with the same meaning
stem:
    SLASH  // STEM_UP
    |
    BACKSLASH // STEM_DOWN;
    ;

beam:
    (
        (CHAR_L //BEAM_START
        |
        CHAR_J// BEAM_END
        |
        CHAR_K // partial beam that extends to the right
        |
        CHAR_k // partial beam that extends to the left
        ) staffChange?
    ) // March 2024 we've removed the + for using lazy encoding and exporting later just one L or J
    ;


mordent:
    //LETTER_W
       CHAR_M | // MORDENT form accid upper, //TODO
       CHAR_m | // MORDENT form upper, //TODO
	   CHAR_W // MORDENT_INVERTED_TONE
	   CHAR_w? // MORDENT_INVERTED_TONE
	   |
       CHAR_w;
trill:
	 CHAR_T CHAR_T? // the second T denotes an extended trill (horizontal twisting line)
     |
     CHAR_t;

footnote: QUESTION_MARK+; //TODO -- ???

