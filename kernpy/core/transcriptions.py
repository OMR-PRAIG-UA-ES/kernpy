from enum import Enum

class IM3Error(Exception):
    def __init__(self, message):
        super().__init__(message)


class Accidentals:
    INDEX_NUMBER = 0
    INDEX_NAME = 1

    TRIPLE_FLAT = -3, "bbb"
    DOUBLE_FLAT = -2, "bb"
    FLAT = -1, "b"
    NATURAL = 0, "n"
    SHARP = 1, "#"
    DOUBLE_SHARP = 2, "x"


    def __init__(self, alteration: int, name: str):
        self.alteration = alteration
        self.name = name

    def __str__(self):
        return "" if self.alteration == 0 else self.name

    @staticmethod
    def modify_to_accidentals(alteration: int):
        if alteration == -3:
            return Accidentals.TRIPLE_FLAT
        elif alteration == -2:
            return Accidentals.DOUBLE_FLAT
        elif alteration == -1:
            return Accidentals.FLAT
        elif alteration == 0:
            return Accidentals.NATURAL
        elif alteration == 1:
            return Accidentals.SHARP
        elif alteration == 2:
            return Accidentals.DOUBLE_SHARP
        else:
            raise ValueError(f"Invalid number of accidentals: <{alteration}>")

    @staticmethod
    def accidental_from_name(name: str):
        if name == Accidentals.TRIPLE_FLAT[Accidentals.INDEX_NAME]:
            return Accidentals.TRIPLE_FLAT[Accidentals.INDEX_NUMBER]
        elif name == Accidentals.DOUBLE_FLAT[Accidentals.INDEX_NAME]:
            return Accidentals.DOUBLE_FLAT[Accidentals.INDEX_NUMBER]
        elif name == Accidentals.FLAT[Accidentals.INDEX_NAME]:
            return Accidentals.FLAT[Accidentals.INDEX_NUMBER]
        elif name == Accidentals.NATURAL[Accidentals.INDEX_NAME]:
            return Accidentals.NATURAL[Accidentals.INDEX_NUMBER]
        elif name == Accidentals.SHARP[Accidentals.INDEX_NAME]:
            return Accidentals.SHARP[Accidentals.INDEX_NUMBER]
        elif name == Accidentals.DOUBLE_SHARP[Accidentals.INDEX_NAME]:
            return Accidentals.DOUBLE_SHARP[Accidentals.INDEX_NUMBER]
        else:
            raise IM3Error(f"Invalid accidental name: <{name}>")


class DiatonicPitch:
    INDEX_SEMITONES_FROM_C = 0
    INDEX_ORDER = 1

    C = 0, 0
    D = 2, 1
    E = 4, 2
    F = 5, 3
    G = 7, 4
    A = 9, 5
    B = 11, 6

    NAMES = 'CDEFGAB'

    def __init__(self, semitones_from_c: int, order: int):
        self.semitones_from_c = semitones_from_c

'''
In Java:
public enum PitchClasses {
	C_DFLAT(DiatonicPitch.C, Accidentals.DOUBLE_FLAT,0),
	C_FLAT(DiatonicPitch.C, Accidentals.FLAT,1),
	C(DiatonicPitch.C, Accidentals.NATURAL,2),
	C_SHARP(DiatonicPitch.C, Accidentals.SHARP,3),
	C_DSHARP(DiatonicPitch.C, Accidentals.DOUBLE_SHARP,4),

	D_TFLAT(DiatonicPitch.D, Accidentals.TRIPLE_FLAT,5),
	D_DFLAT(DiatonicPitch.D, Accidentals.DOUBLE_FLAT,6),
	D_FLAT(DiatonicPitch.D, Accidentals.FLAT,7),
	D(DiatonicPitch.D, Accidentals.NATURAL,8),
	D_SHARP(DiatonicPitch.D, Accidentals.SHARP,9),
	D_DSHARP(DiatonicPitch.D, Accidentals.DOUBLE_SHARP,10),

	E_TFLAT(DiatonicPitch.E, Accidentals.TRIPLE_FLAT,11),
	E_DFLAT(DiatonicPitch.E, Accidentals.DOUBLE_FLAT,12),
	E_FLAT(DiatonicPitch.E, Accidentals.FLAT,13),
	E(DiatonicPitch.E, Accidentals.NATURAL,14),
	E_SHARP(DiatonicPitch.E, Accidentals.SHARP,15),
	E_DSHARP(DiatonicPitch.E, Accidentals.DOUBLE_SHARP,16),

	F_DFLAT(DiatonicPitch.F, Accidentals.DOUBLE_FLAT,17),
	F_FLAT(DiatonicPitch.F, Accidentals.FLAT,18),
	F(DiatonicPitch.F, Accidentals.NATURAL,19),
	F_SHARP(DiatonicPitch.F, Accidentals.SHARP,20),
	F_DSHARP(DiatonicPitch.F, Accidentals.DOUBLE_SHARP,21),
	
	G_DFLAT(DiatonicPitch.G, Accidentals.DOUBLE_FLAT,23),
	G_FLAT(DiatonicPitch.G, Accidentals.FLAT,24),
	G(DiatonicPitch.G, Accidentals.NATURAL,25),
	G_SHARP(DiatonicPitch.G, Accidentals.SHARP,26),
	G_DSHARP(DiatonicPitch.G, Accidentals.DOUBLE_SHARP,27),

	A_TFLAT(DiatonicPitch.A, Accidentals.TRIPLE_FLAT,28),
	A_DFLAT(DiatonicPitch.A, Accidentals.DOUBLE_FLAT,29),
	A_FLAT(DiatonicPitch.A, Accidentals.FLAT,30),
	A(DiatonicPitch.A, Accidentals.NATURAL,31),
	A_SHARP(DiatonicPitch.A, Accidentals.SHARP,32),
	A_DSHARP(DiatonicPitch.A, Accidentals.DOUBLE_SHARP,33),

	B_TFLAT(DiatonicPitch.B, Accidentals.TRIPLE_FLAT,34),
	B_DFLAT(DiatonicPitch.B, Accidentals.DOUBLE_FLAT,35),
	B_FLAT(DiatonicPitch.B, Accidentals.FLAT,36),
	B(DiatonicPitch.B, Accidentals.NATURAL,37),
	B_SHARP(DiatonicPitch.B, Accidentals.SHARP,38),
	B_DSHARP(DiatonicPitch.B, Accidentals.DOUBLE_SHARP,39);
	

'''
class PitchClasses:
    C_DFLAT

class PitchClass:
    pass

class ScientificPitch:
    C4 = ScientificPitch(pitch_class=PitchClasses.C.class, octave=4)

    def __init__(self, octave: int, pitch_class: PitchClass = None, pitch_classes: PitchClasses = None):
        if pitch_class is None and pitch_classes is None:
            raise ValueError("pitch_class or pitch_classes must be provided")
        if pitch_class is not None and pitch_classes is not None:
            raise ValueError("Only one of pitch_class or pitch_classes must be provided")

        if pitch_class is not None:
            self.pitch_class = pitch_class
        elif pitch_classes is not None:
            self.pitch_class = pitch_classes.get_pitch_class()
        else:
            raise ValueError("pitch_class or pitch_classes must be provided")

        self.octave = int(octave)

    def __eq__(self, other):
        if self is other:
            return True

        if not isinstance(other, ScientificPitch):
            return False

        if other is None:
            return False

        return self.pitch_class == other.pitch_class and self.octave == other.octave

class Base40:
    def __init__(self, sp: ScientificPitch):
        self.base_40_chroma: int = sp.pitch_class.base_40_chroma
        self.base_40: int = sp.octave * 40 + self.base_40_chroma

