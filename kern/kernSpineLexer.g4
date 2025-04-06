/*
This grammar is used in mOOsicae and kernpy. It must be kept synchronised
Changes (please, add here the authors and date of each change):

@author: David Rizo (drizo@dlsi.ua.es) Feb, 2024.
It parses just a token inside a **kern spine
*/
lexer grammar kernSpineLexer;

fragment ASTERISK_FRAGMENT : '*';

TANDEM_KEYCANCEL: ASTERISK_FRAGMENT 'kcancel';
//TODO 8 mar 2024 - what it is for? TANDEM_COL_START: ASTERISK_FRAGMENT 'col';
//TODO 8 mar 2024 - what it is for?TANDEM_COL_END: ASTERISK_FRAGMENT 'Xcol';
TANDEM_PART: ASTERISK_FRAGMENT 'part';
TANDEM_GROUP: ASTERISK_FRAGMENT 'group'; // new March 2024
TANDEM_ACCOMP: ASTERISK_FRAGMENT 'accomp';
TANDEM_SOLO: ASTERISK_FRAGMENT 'solo';
TANDEM_STROPHE: ASTERISK_FRAGMENT 'strophe';
TANDEM_STAFF: ASTERISK_FRAGMENT 'staff';
TANDEM_TRANSPOSITION: ASTERISK_FRAGMENT CHAR_I? 'Tr';
TANDEM_CLEF: ASTERISK_FRAGMENT 'clef';
TANDEM_KEY_SIGNATURE: ASTERISK_FRAGMENT 'k';
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
TANDEM_ELA: ASTERISK_FRAGMENT 'ela'; // sometimes found *ela
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
TANDEM_SIC: ASTERISK_FRAGMENT 'S/sic'; // bach/wtc/wtc1f01.krn
TANDEM_OSSIA: ASTERISK_FRAGMENT 'S/ossia'; // bach/wtc/wtc1f01.krn
TANDEM_FIN: ASTERISK_FRAGMENT 'S/fin'; // bach/wtc/wtc1f01.krn
TANDEM_SMINUS: ASTERISK_FRAGMENT 'S-'; // bach/wtc/wtc1f01.krn TODO ???
TANDEM_TIMEBASE: ASTERISK_FRAGMENT 'tb';
TANDEM_BOUNDING_BOX: ASTERISK_FRAGMENT 'xywh';

OCTAVE_SHIFT: ASTERISK_FRAGMENT 'X'?'8'[vb]+'a';

EXCLAMATION: '!';
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
LEFT_CURLY_BRACES: '{';
RIGHT_CURLY_BRACES: '}';
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
QUESTION_MARK: '?';
SPACE: ' ';

// with pushMode, the lexer uses the rules below FREE_TEXT
INSTRUMENT_TITLE: '*mI' '"'? RAW_TEXT;
INSTRUMENT: '*I' '"'? RAW_TEXT;  // TODO: this only supports <<*Ipiano>> examples. But it should also support custom names using double quotes like <<*I"sax>>. Optional only at the beginning. Probably, do the same for INSTRUMENT_TITLE
fragment RAW_TEXT: ~([\t\n\r])+;
fragment RAW_TEXT_UNTIL_EOL: ~([\n\r])+; // !: or !| belong to bar lines
fragment RAW_TEXT_NOT_BARLINE: (~[!|=:;\t\n\r])~([\t\n\r])*; // !:, !; or !| belong to bar lines

