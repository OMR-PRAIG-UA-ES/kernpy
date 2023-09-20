/*
@author: David Rizo (drizo@dlsi.ua.es) Oct, 2020.
*/
lexer grammar kernLexer;

@lexer::header {
}


//Non context free grammar needs semantic predicates to handle text and harm spines
@lexer::members {
}

SPACE: ' ';
TAB: '\t'; // incSpine changes mode depending on the spine type
EOL : '\r'?'\n';


fragment ASTERISK_FRAGMENT : '*';
EXCLAMATION : '!';

MENS: ASTERISK_FRAGMENT ASTERISK_FRAGMENT 'mens';
KERN: ASTERISK_FRAGMENT ASTERISK_FRAGMENT 'kern';
TEXT: ASTERISK_FRAGMENT ASTERISK_FRAGMENT 'text';
HARM: ASTERISK_FRAGMENT ASTERISK_FRAGMENT 'harm';
MXHM: ASTERISK_FRAGMENT ASTERISK_FRAGMENT 'mxhm';
ROOT: ASTERISK_FRAGMENT ASTERISK_FRAGMENT 'root';
DYN: ASTERISK_FRAGMENT ASTERISK_FRAGMENT 'dyn';
DYNAM: ASTERISK_FRAGMENT ASTERISK_FRAGMENT 'dynam';

TANDEM_LIG_START: ASTERISK_FRAGMENT 'lig';
TANDEM_LIG_END: ASTERISK_FRAGMENT 'Xlig';
TANDEM_COL_START: ASTERISK_FRAGMENT 'col';
TANDEM_COL_END: ASTERISK_FRAGMENT 'Xcol';
TANDEM_PART: ASTERISK_FRAGMENT 'part';
//2020 fragment TANDEM_INSTRUMENT: ASTERISK_FRAGMENT CHAR_I;
// TANDEM_INSTRUMENT: ASTERISK_FRAGMENT CHAR_I;
TANDEM_STAFF: ASTERISK_FRAGMENT 'staff';
TANDEM_TRANSPOSITION: ASTERISK_FRAGMENT CHAR_I? 'Tr';
TANDEM_CLEF: ASTERISK_FRAGMENT 'clef';
TANDEM_CUSTOS: ASTERISK_FRAGMENT 'custos';
TANDEM_KEY_SIGNATURE: ASTERISK_FRAGMENT 'k';
//TANDEM_KEY: ASTERISK_FRAGMENT 'K';
TANDEM_MET: ASTERISK_FRAGMENT 'met';
METRONOME: ASTERISK_FRAGMENT 'MM';
TANDEM_SECTION: ASTERISK_FRAGMENT '>';
NO_REPEAT: 'norep';
TANDEM_LEFT_HAND: ASTERISK_FRAGMENT 'lh';
TANDEM_RIGHT_HAND: ASTERISK_FRAGMENT 'rh';
TANDEM_ABOVE: ASTERISK_FRAGMENT 'above';
TANDEM_BELOW: ASTERISK_FRAGMENT 'below' (COLON? [0-9])?; // sometimes we've found below:2 and below2
TANDEM_CENTERED: ASTERISK_FRAGMENT 'centered';
TANDEM_PEDAL_START: ASTERISK_FRAGMENT 'ped' ASTERISK_FRAGMENT?; // sometimes found *ped*
TANDEM_PEDAL_END: ASTERISK_FRAGMENT 'Xped';
TANDEM_TUPLET_START: ASTERISK_FRAGMENT 'tuplet'; // sometimes found
TANDEM_TUPLET_END: ASTERISK_FRAGMENT 'Xtuplet'; // sometimes found
TANDEM_CUE_START: ASTERISK_FRAGMENT 'cue'; // sometimes found
TANDEM_CUE_END: ASTERISK_FRAGMENT 'Xcue'; // sometimes found
TANDEM_TREMOLO_START: ASTERISK_FRAGMENT 'tremolo'; // sometimes found
TANDEM_TREMOLO_END: ASTERISK_FRAGMENT 'Xtremolo'; // sometimes found
TANDEM_TSTART: ASTERISK_FRAGMENT 'tstart'; // sometimes found
TANDEM_TEND: ASTERISK_FRAGMENT 'tend'; // sometimes found
TANDEM_RSCALE: ASTERISK_FRAGMENT 'rscale';
TANDEM_TIMESIGNATURE: ASTERISK_FRAGMENT 'M';
TANDEM_BEGIN_PLAIN_CHANT: ASTERISK_FRAGMENT 'bpc';
TANDEM_END_PLAIN_CHANT: ASTERISK_FRAGMENT 'epc';
LAYOUT: EXCLAMATION 'LO:' RAW_TEXT;

OCTAVE_SHIFT: ASTERISK_FRAGMENT 'X'?'8'[vb]+'a';

PERCENT: '%';
AMPERSAND: '&';
AT: '@';
CHAR_A: 'A';
CHAR_B: 'B';
CHAR_C: 'C';
CHAR_D: 'D';
CHAR_E: 'E';
CHAR_F: 'F';
CHAR_G: 'G';
CHAR_H: 'H';
CHAR_I: 'I';
CHAR_J: 'J';
CHAR_K: 'K';
CHAR_L: 'L';
CHAR_M: 'M';
CHAR_N: 'N';
CHAR_O: 'O';
CHAR_P: 'P';
CHAR_Q: 'Q';
CHAR_R: 'R';
CHAR_S: 'S';
CHAR_T: 'T';
CHAR_U: 'U';
CHAR_V: 'V';
CHAR_W: 'W';
CHAR_X: 'X';
CHAR_Y: 'Y';
CHAR_Z: 'Z';
CHAR_a: 'a';
CHAR_b: 'b';
CHAR_c: 'c';
CHAR_d: 'd';
CHAR_e: 'e';
CHAR_f: 'f';
CHAR_g: 'g';
CHAR_h: 'h';
CHAR_i: 'i';
CHAR_j: 'j';
CHAR_k: 'k';
CHAR_l: 'l';
CHAR_m: 'm';
CHAR_n: 'n';
CHAR_o: 'o';
CHAR_p: 'p';
CHAR_q: 'q';
CHAR_r: 'r';
CHAR_s: 's';
CHAR_t: 't';
CHAR_u: 'u';
CHAR_v: 'v';
CHAR_w: 'w';
CHAR_x: 'x';
CHAR_y: 'y';
CHAR_z: 'z';

NON_ENGLISH: [áéíóúàèìòùÁÉÍÓÚÀÈÌÒÙñÑçÇ];

DIGIT_0: '0';
DIGIT_1: '1';
DIGIT_2: '2';
DIGIT_3: '3';
DIGIT_4: '4';
DIGIT_5: '5';
DIGIT_6: '6';
DIGIT_7: '7';
DIGIT_8: '8';
DIGIT_9: '9';

SPINE_TERMINATOR: ASTERISK_FRAGMENT MINUS;
SPINE_ADD: ASTERISK_FRAGMENT PLUS;
SPINE_SPLIT: ASTERISK_FRAGMENT CIRCUMFLEX;
SPINE_JOIN: ASTERISK_FRAGMENT CHAR_v;
ASTERISK: ASTERISK_FRAGMENT;

QUOTATION_MARK: '"';
APOSTROPHE: '\'';
LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';
OCTOTHORPE: '#';
PLUS: '+';
MINUS: '-';
EQUAL: '=';
DOT: '.';
PIPE: '|';
GRAVE_ACCENT: '`';
CIRCUMFLEX: '^';
TILDE: '~';
ANGLE_BRACKET_OPEN: '<';
ANGLE_BRACKET_CLOSE: '>';
SLASH: '/';
BACKSLASH: '\\';
UNDERSCORE: '_';
DOLLAR: '$';

LEFT_PARENTHESIS: '(';
RIGHT_PARENTHESIS: ')';
COLON: ':';
SEMICOLON: ';';
COMMA: ',';
SEP: '·'; // only used in SKM
QUESTION_MARK: '?';



// with pushMode, the lexer uses the rules below FREE_TEXT
INSTRUMENT: '*I' '"'? RAW_TEXT;
METACOMMENT: '!!' '!'?  RAW_TEXT_UNTIL_EOL?;
FIELDCOMMENT: '!' RAW_TEXT_NOT_BARLINE;
fragment RAW_TEXT: ~([\t\n\r])+;
fragment RAW_TEXT_UNTIL_EOL: ~([\n\r])+; // !: or !| belong to bar lines
fragment RAW_TEXT_NOT_BARLINE: (~[!|\t\n\r])~([\t\n\r])*; // !: or !| belong to bar lines

ANY: . ;


//2020 METADATACOMMENT: '!!!' RAW_TEXT;
//2020 FIELDCCOMMENT_EMPTY: EXCLAMATION;
//2020 FIELDCCOMMENT: EXCLAMATION RAW_TEXT;
//2020 INSTRUMENT: TANDEM_INSTRUMENT '"'? RAW_TEXT;

// | and ! to avoid confusing a comment with a bar line
// the ? is used to set the non greedy mode (https://github.com/antlr/antlr4/blob/master/doc/wildcard.md)
//2020 fragment RAW_TEXT: (~[\t\n\r!|])+;
//fragment RAW_TEXT: .*?;

// FIELD_TEXT: RAW_TEXT;


mode FREE_TEXT;
    FIELD_TEXT: ~[\t\n\r]+; // must reset mode here to let lexer recognize the tab or newline
//FREE_TEXT_TAB: '\t' {incSpine("free_text mode tab");}; // incSpine changes mode depending on the spine type
//FREE_TEXT_EOL : '\r'?'\n' {onEOL("free_text mode eol");};

