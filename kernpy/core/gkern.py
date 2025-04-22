"""

This module is responsible for generating the Graphic **kern encoding.

The Graphic **kern encoding (**gkern) is an agnostify **kern encoding. It keeps the original **kern encoding structure \
but replaces the pitches with its graphic representation. So the E pitch in G Clef will use the same graphic \
representation as the C pitch in C in 1st Clef or the A in F in 4th Clef.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict

from .tokens import (
    GRAPHIC_TOKEN_SEPARATOR, ClefToken, Token, TokenCategory
)

from .transposer import (
    transpose,
    Direction,
    distance,
    agnostic_distance,
    transpose_agnostics,
    transpose_encoding_to_agnostic,
    transpose_agnostic_to_encoding,
)

from .pitch_models import (
    AgnosticPitch,
    pitches,
)

class Alteration(Enum):
    """
    Enum for the alteration of a pitch.
    """
    NONE = 0
    SHARP = 1
    FLAT = -1
    DOUBLE_SHARP = 2
    DOUBLE_FLAT = -2
    TRIPLE_SHARP = 3
    TRIPLE_FLAT = -3
    HALF_SHARP = 0.5
    HALF_FLAT = -0.5
    QUARTER_SHARP = 0.25
    QUARTER_FLAT = -0.25

    def __str__(self) -> str:
        return self.name


class PositionInStaff:
    LINE_CHARACTER = 'L'
    SPACE_CHARACTER = 'S'

    def __init__(self, line_space: int):
        """
        Initializes the PositionInStaff object.

        Args:
            line_space (int): 0 for bottom line, -1 for space under bottom line, 1 for space above bottom line. \
             Increments by 1 for each line or space.

        """
        self.line_space = line_space

    @classmethod
    def from_line(cls, line: int) -> PositionInStaff:
        """
        Creates a PositionInStaff object from a line number.

        Args:
            line (int): The line number. line 1 is bottom line, 2 is the 1st line from bottom, 0 is the bottom ledger line

        Returns:
            PositionInStaff: The PositionInStaff object. 0 for the bottom line, 2 for the 1st line from bottom, -1 for the bottom ledger line, etc.
        """
        return cls((line - 1) * 2)

    @classmethod
    def from_space(cls, space: int) -> PositionInStaff:
        """
        Creates a PositionInStaff object from a space number.

        Args:
            space (int): The space number. space 1 is bottom space, 2

        Returns:
            PositionInStaff: The PositionInStaff object.
        """
        return cls((space) * 2 - 1)

    @classmethod
    def from_encoded(cls, encoded: str) -> PositionInStaff:
        """
        Creates a PositionInStaff object from an encoded string.

        Args:
            encoded (str): The encoded string.

        Returns:
            PositionInStaff: The PositionInStaff object.
        """
        if encoded.startswith(cls.LINE_CHARACTER):
            line = int(encoded[1:])  # Extract the line number
            return cls.from_line(line)
        elif encoded.startswith(cls.SPACE_CHARACTER):
            space = int(encoded[1:])  # Extract the space number
            return cls.from_space(space)
        else:
            raise ValueError(f""
                             f"Invalid encoded string: {encoded}. "
                             f"Expected to start with '{cls.LINE_CHARACTER}' or '{cls.SPACE_CHARACTER} at the beginning.")


    def line(self):
        """
        Returns the line number of the position in staff.
        """
        return self.line_space // 2 + 1


    def space(self):
        """
        Returns the space number of the position in staff.
        """
        return (self.line_space - 1) // 2 + 1


    def is_line(self) -> bool:
        """
        Returns True if the position is a line, False otherwise. If is not a line, it is a space, and vice versa.
        """
        return self.line_space % 2 == 0

    def move(self, line_space_difference: int) -> PositionInStaff:
        """
        Returns a new PositionInStaff object with the position moved by the given number of lines or spaces.

        Args:
            line_space_difference (int): The number of lines or spaces to move.

        Returns:
            PositionInStaff: The new PositionInStaff object.
        """
        return PositionInStaff(self.line_space + line_space_difference)

    def position_below(self) -> PositionInStaff:
        """
        Returns the position below the current position.
        """
        return self.move(-2)

    def position_above(self) -> PositionInStaff:
        """
        Returns the position above the current position.
        """
        return self.move(2)



    def __str__(self) -> str:
        """
        Returns the string representation of the position in staff.
        """
        if self.is_line():
            return f"{self.LINE_CHARACTER}{int(self.line())}"
        else:
            return f"{self.SPACE_CHARACTER}{int(self.space())}"

    def __repr__(self) -> str:
        """
        Returns the string representation of the PositionInStaff object.
        """
        return f"PositionInStaff(line_space={self.line_space}), {self.__str__()}"

    def __eq__(self, other) -> bool:
        """
        Compares two PositionInStaff objects.
        """
        if not isinstance(other, PositionInStaff):
            return False
        return self.line_space == other.line_space

    def __ne__(self, other) -> bool:
        """
        Compares two PositionInStaff objects.
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """
        Returns the hash of the PositionInStaff object.
        """
        return hash(self.line_space)

    def __lt__(self, other) -> bool:
        """
        Compares two PositionInStaff objects.
        """
        if not isinstance(other, PositionInStaff):
            return NotImplemented
        return self.line_space < other.line_space


class DiatonicPitch:
    def __init__(self, diatonic_pitch: str) -> None:
        if diatonic_pitch not in pitches:
            raise ValueError(f"Invalid diatonic pitch: {diatonic_pitch}. "
                             f"Expected one of {pitches}.")
        self.encoding = diatonic_pitch

    def __str__(self) -> str:
        return self.encoding


class PitchPositionReferenceSystem:
    def __init__(self, base_pitch: AgnosticPitch):
        """
        Initializes the PitchPositionReferenceSystem object.
        Args:
            base_pitch (AgnosticPitch): The AgnosticPitch in the first line of the Staff. \
             The AgnosticPitch object that serves as the reference point for the system.
        """
        self.base_pitch = base_pitch

    def compute_position(self, pitch: AgnosticPitch) -> PositionInStaff:
        """
        Computes the position in staff for the given pitch.
        Args:
            pitch (AgnosticPitch): The AgnosticPitch object to compute the position for.
        Returns:
            PositionInStaff: The PositionInStaff object representing the computed position.
        """
        # map A–G to 0–6
        LETTER_TO_INDEX = {'C': 0, 'D': 1, 'E': 2,
                           'F': 3, 'G': 4, 'A': 5, 'B': 6}

        # strip off any '+' or '-' accidentals, then grab the letter
        def letter(p: AgnosticPitch) -> str:
            name = p.name.replace('+', '').replace('-', '')
            return AgnosticPitch(name, p.octave).name

        base_letter_idx = LETTER_TO_INDEX[letter(self.base_pitch)]
        target_letter_idx = LETTER_TO_INDEX[letter(pitch)]

        # "octave difference × 7" plus the letter‐index difference
        diatonic_steps = (pitch.octave - self.base_pitch.octave) * 7 \
                         + (target_letter_idx - base_letter_idx)

        # that many "lines or spaces" above (or below) the reference line
        return PositionInStaff(diatonic_steps)




# TARGET: Retrieve agnostic encoding from semantic encoding
# INPUT: Pitch (Semantic) + Clef (Semantic)
# OUTPUT: PositionInStaff (Agnostic)

# CLEF has
# 1. bottom line equivalent to C4
# - C in 1st clef: 1st line is F2 == F
# - C in 2nd clef: 1st line is D2 == D
# - C in 3rd clef: 1st line is B2 == BB
# - C in 4th clef: 1st line is G2 == GG
# - G clef: 1st line is E4 == e
# - F in 3rd clef: 1st line is B2 == BB
# - F in 4th clef: 1st line is G2 == GG

# New abstraction:
# TARGET: PositionInStaff
# INPUT: Pitch (Semantic) + Reference System to the first line
# OUTPUT: PositionInStaff (Agnostic)
# Example:
# Input: Pitch (A4) + Reference System (Line 1 == E3) (Case of G Clef)
# >>> A4 is a 4th minor above E3   ¿How to calculate this?
# >>> a 4th minor is equivalent to the 2nd upper space
# >>> PositionInStaff.from_space(2)
# >>> PositionInStaff(?)

class Clef(ABC):
    """
    Abstract class representing a clef.
    """

    def __init__(self, diatonic_pitch: DiatonicPitch, on_line: int):
        """
        Initializes the Clef object.
        Args:
            diatonic_pitch (DiatonicPitch): The diatonic pitch of the clef (e.g., 'C', 'G', 'F'). This value is used as a decorator.
            on_line (int): The line number on which the clef is placed (1 for bottom line, 2 for 1st line from bottom, etc.). This value is used as a decorator.
        """
        self.diatonic_pitch = diatonic_pitch
        self.on_line = on_line

    @abstractmethod
    def bottom_line(self) -> AgnosticPitch:
        """
        Returns the pitch of the bottom line of the staff.
        """
        ...

    def name(self):
        """
        Returns the name of the clef.
        """
        return f"{self.diatonic_pitch} on line {self.on_line}"

    def reference_point(self) -> PitchPositionReferenceSystem:
        """
        Returns the reference point for the clef.
        """
        return PitchPositionReferenceSystem(self.bottom_line())

    def __str__(self) -> str:
        """
        Returns:
            str: The string representation of the clef.
        """
        return f'{self.diatonic_pitch.encoding.upper()} on the {self.on_line}{self._ordinal_suffix(self.on_line)} line'

    @staticmethod
    def _ordinal_suffix(number: int) -> str:
        """
        Returns the ordinal suffix for a given integer (e.g. 'st', 'nd', 'rd', 'th').

        Args:
            number (int): The number to get the suffix for.

        Returns:
            str: The ordinal suffix.
        """
        # 11, 12, 13 always take “th”
        if 11 <= (number % 100) <= 13:
            return 'th'
        # otherwise use last digit
        last = number % 10
        if last == 1:
            return 'st'
        elif last == 2:
            return 'nd'
        elif last == 3:
            return 'rd'
        else:
            return 'th'


class GClef(Clef):
    def __init__(self):
        """
        Initializes the G Clef object.
        """
        super().__init__(DiatonicPitch('G'), 2)

    def bottom_line(self) -> AgnosticPitch:
        """
        Returns the pitch of the bottom line of the staff.
        """
        return AgnosticPitch('E', 4)

class F3Clef(Clef):
    def __init__(self):
        """
        Initializes the F Clef object.
        """
        super().__init__(DiatonicPitch('F'), 3)

    def bottom_line(self) -> AgnosticPitch:
        """
        Returns the pitch of the bottom line of the staff.
        """
        return AgnosticPitch('B', 3)

class F4Clef(Clef):
    def __init__(self):
        """
        Initializes the F Clef object.
        """
        super().__init__(DiatonicPitch('F'), 4)

    def bottom_line(self) -> AgnosticPitch:
        """
        Returns the pitch of the bottom line of the staff.
        """
        return AgnosticPitch('G', 2)

class C1Clef(Clef):
    def __init__(self):
        """
        Initializes the C Clef object.
        """
        super().__init__(DiatonicPitch('C'), 1)

    def bottom_line(self) -> AgnosticPitch:
        """
        Returns the pitch of the bottom line of the staff.
        """
        return AgnosticPitch('C', 3)

class C2Clef(Clef):
    def __init__(self):
        """
        Initializes the C Clef object.
        """
        super().__init__(DiatonicPitch('A'), 2)

    def bottom_line(self) -> AgnosticPitch:
        """
        Returns the pitch of the bottom line of the staff.
        """
        return AgnosticPitch('A', 2)


class C3Clef(Clef):
    def __init__(self):
        """
        Initializes the C Clef object.
        """
        super().__init__(DiatonicPitch('C'), 3)

    def bottom_line(self) -> AgnosticPitch:
        """
        Returns the pitch of the bottom line of the staff.
        """
        return AgnosticPitch('B', 2)

class C4Clef(Clef):
    def __init__(self):
        """
        Initializes the C Clef object.
        """
        super().__init__(DiatonicPitch('C'), 4)

    def bottom_line(self) -> AgnosticPitch:
        """
        Returns the pitch of the bottom line of the staff.
        """
        return AgnosticPitch('D', 2)


class ClefFactory:
    CLEF_NAMES = { 'G', 'F', 'C' }
    @classmethod
    def create_clef(cls, encoding: str) -> Clef:
        """
        Creates a Clef object based on the given token.

        Clefs are encoded in interpretation tokens that start with a single * followed by the string clef and then the shape and line position of the clef. For example, a treble clef is *clefG2, with G meaning a G-clef, and 2 meaning that the clef is centered on the second line up from the bottom of the staff. The bass clef is *clefF4 since it is an F-clef on the fourth line of the staff.
        A vocal tenor clef is represented by *clefGv2, where the v means the music should be played an octave lower than the regular clef’s sounding pitches. Try creating a vocal tenor clef in the above interactive example. The v operator also works on the other clefs (but these sorts of clefs are very rare). Another rare clef is *clefG^2 which is the opposite of *clefGv2, where the music is written an octave lower than actually sounding pitch for the normal form of the clef. You can also try to create exotic two-octave clefs by doubling the ^^ and vv markers.

        Args:
            encoding (str): The encoding of the clef token.

        Returns:

        """
        encoding = encoding.replace('*clef', '')

        # at this point the encoding is like G2, F4,... or Gv2, F^4,... or G^^2, Fvv4,... or G^^...^^2, Fvvv4,...
        name = list(filter(lambda x: x in cls.CLEF_NAMES, encoding))[0]
        line = int(list(filter(lambda x: x.isdigit(), encoding))[0])
        decorators = ''.join(filter(lambda x: x in ['^', 'v'], encoding))

        if name not in cls.CLEF_NAMES:
            raise ValueError(f"Invalid clef name: {name}. Expected one of {cls.CLEF_NAMES}.")

        if name == 'G':
            return GClef()
        elif name == 'F':
            if line == 3:
                return F3Clef()
            elif line == 4:
                return F4Clef()
            else:
                raise ValueError(f"Invalid F clef line: {line}. Expected 3 or 4.")
        elif name == 'C':
            if line == 1:
                return C1Clef()
            elif line == 2:
                return C2Clef()
            elif line == 3:
                return C3Clef()
            elif line == 4:
                return C4Clef()
            else:
                raise ValueError(f"Invalid C clef line: {line}. Expected 1, 2, 3 or 4.")
        else:
            raise ValueError(f"Invalid clef name: {name}. Expected one of {cls.CLEF_NAMES}.")






class Staff:
    def position_in_staff(self, *, clef: Clef, pitch: AgnosticPitch) -> PositionInStaff:
        """
        Returns the position in staff for the given clef and pitch.
        """
        bottom_cleff_note_name = clef.bottom_line()



class GKernExporter:
    def __init__(self, clef: Clef):
        self.clef = clef

    def export(self, staff: Staff, pitch: AgnosticPitch) -> str:
        """
        Exports the given pitch to a graphic **kern encoding.
        """
        position = self.agnostic_position(staff, pitch)
        return f"{GRAPHIC_TOKEN_SEPARATOR}{str(position)}"

    def agnostic_position(self, staff: Staff, pitch: AgnosticPitch) -> PositionInStaff:
        """
        Returns the agnostic position in staff for the given pitch.
        """
        return staff.position_in_staff(clef=self.clef, pitch=pitch)



