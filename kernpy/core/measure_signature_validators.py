from __future__ import annotations

from fractions import Fraction
import re
from typing import Iterable, List, Sequence, Tuple, Union

from kernpy.core.document import Document
from kernpy.core.tokens import (
    BarToken,
    DurationClassical,
    NoteRestToken,
    Subtoken,
    TimeSignatureToken,
    TokenCategory,
)


class MeasureSignatureToken(TimeSignatureToken):
    """Semantic alias for measure-signature validation workflows."""


DurationToken = Union[DurationClassical, Subtoken, NoteRestToken, int, str]
FilteredScoreToken = Union[DurationToken, BarToken, TimeSignatureToken, MeasureSignatureToken]


def _build_error_message_bad_measure(
    *,
    measure_id: int | None,
    meter_signature: str,
    measured_missmatch_fraction: Fraction,
    expected_measure_duration: Fraction | None = None,
    spine_index: int | None = None,
) -> str:
    if expected_measure_duration is None:
        beats, beat_unit = meter_signature[2:].split("/")
        expected_measure_duration = Fraction(int(beats), int(beat_unit))

    duration_gap = abs(expected_measure_duration - measured_missmatch_fraction)

    if measured_missmatch_fraction < expected_measure_duration:
        direction_sentence = (
            f"The measure is underfilled by {duration_gap}; "
            f"add rhythmic value(s) totaling {duration_gap}."
        )
    else:
        direction_sentence = (
            f"The measure is overfilled by {duration_gap}; "
            f"remove or redistribute {duration_gap} of rhythmic duration."
        )

    measure_label = f"#{measure_id}" if measure_id is not None else "<unknown>"
    spine_label = f"#{spine_index}" if spine_index is not None else "<unknown>"

    return (
        f"Measure {measure_label} duration mismatch in spine {spine_label} "
        f"where the latest time signature is {meter_signature}: "
        f"got {measured_missmatch_fraction} of a full measure. {direction_sentence}"
    )


class MeasureSignatureValidator:
    """Validate measure duration totals against one fixed measure signature."""

    _MEASURE_SIGNATURE_PATTERN = re.compile(r"^\*M(\d+)\/(\d+)$")

    def __init__(self, measure_signature_token: Union[MeasureSignatureToken, TimeSignatureToken]):
        if not isinstance(measure_signature_token, (MeasureSignatureToken, TimeSignatureToken)):
            raise ValueError(
                "MeasureSignatureValidator expects a MeasureSignatureToken or TimeSignatureToken, "
                f"but received {type(measure_signature_token).__name__}."
            )

        self.measure_signature_token = MeasureSignatureToken(measure_signature_token.encoding)
        self._beats, self._beat_unit = self._parse_measure_signature(self.measure_signature_token.encoding)
        self._expected_measure_duration = Fraction(self._beats, self._beat_unit)

    @property
    def expected_measure_duration(self) -> Fraction:
        return self._expected_measure_duration

    def fits_measure(
        self,
        duration_tokens: Sequence[DurationToken],
        *,
        spine_index: int | None = None,
    ) -> Tuple[bool, str]:
        measured_duration, error_message = self._compute_total_duration(duration_tokens, measure_index=None)
        if error_message:
            return False, error_message

        if measured_duration != self._expected_measure_duration:
            return False, self._build_measure_mismatch_message(
                measure_index=None,
                measured_duration=measured_duration,
                spine_index=spine_index,
            )

        return True, ""

    def assert_measure(
        self,
        duration_tokens: Sequence[DurationToken],
        measure_index: int | None = None,
        *,
        spine_index: int | None = None,
    ) -> Tuple[bool, str]:
        measured_duration, error_message = self._compute_total_duration(duration_tokens, measure_index=measure_index)
        if error_message:
            return False, error_message

        if measured_duration != self._expected_measure_duration:
            return False, self._build_measure_mismatch_message(
                measure_index=measure_index,
                measured_duration=measured_duration,
                spine_index=spine_index,
            )

        return True, ""

    def validate_filtered_score_tokens(self, filtered_tokens: Sequence[FilteredScoreToken]) -> Tuple[bool, str]:
        current_measure_tokens: List[DurationToken] = []
        current_measure_index = 1

        for position, token in enumerate(filtered_tokens, start=1):
            if isinstance(token, BarToken):
                if current_measure_tokens:
                    is_valid, error_message = self.assert_measure(
                        current_measure_tokens,
                        measure_index=current_measure_index,
                    )
                    if not is_valid:
                        return False, error_message
                    current_measure_tokens = []
                    current_measure_index += 1
                continue

            if isinstance(token, (MeasureSignatureToken, TimeSignatureToken)):
                if token.encoding != self.measure_signature_token.encoding:
                    return False, (
                        f"Found time signature change at filtered token position #{position}: "
                        f"'{token.encoding}' does not match validator signature "
                        f"'{self.measure_signature_token.encoding}'."
                    )
                continue

            current_measure_tokens.append(token)

        if current_measure_tokens:
            is_valid, error_message = self.assert_measure(
                current_measure_tokens,
                measure_index=current_measure_index,
            )
            if not is_valid:
                return False, error_message

        return True, ""

    def validate_document(self, document: Document) -> Tuple[bool, str]:
        filtered_tokens = self.filter_document_to_durations_and_measures(document)
        return self.validate_filtered_score_tokens(filtered_tokens)

    @staticmethod
    def filter_document_to_durations_and_measures(document: Document) -> List[FilteredScoreToken]:
        tokens = document.get_all_tokens(
            filter_by_categories=[
                TokenCategory.TIME_SIGNATURE,
                TokenCategory.BARLINES,
                TokenCategory.NOTE_REST,
            ]
        )

        filtered_tokens: List[FilteredScoreToken] = []
        for token in tokens:
            if isinstance(token, (TimeSignatureToken, MeasureSignatureToken, BarToken)):
                filtered_tokens.append(token)
                continue

            if isinstance(token, NoteRestToken):
                duration_subtokens = MeasureSignatureValidator._extract_rhythm_subtokens(token)
                filtered_tokens.extend(duration_subtokens)

        return filtered_tokens

    @staticmethod
    def _extract_rhythm_subtokens(note_rest_token: NoteRestToken) -> List[Subtoken]:
        duration_subtokens = [
            subtoken for subtoken in note_rest_token.pitch_duration_subtokens
            if subtoken.category == TokenCategory.DURATION
        ]
        dot_count = MeasureSignatureValidator._count_augmentation_dots(note_rest_token)
        dot_subtokens = [Subtoken(".", TokenCategory.DECORATION)] * dot_count
        return [*duration_subtokens, *dot_subtokens]

    @staticmethod
    def _count_augmentation_dots(note_rest_token: NoteRestToken) -> int:
        encoding = note_rest_token.encoding.strip()
        dot_count = 0
        for char in reversed(encoding):
            if char != ".":
                break
            dot_count += 1
        return dot_count

    @staticmethod
    def _is_duration_dot_subtoken(subtoken: Subtoken) -> bool:
        return subtoken.encoding.strip(".") == "" and len(subtoken.encoding) > 0

    @classmethod
    def _parse_measure_signature(cls, signature_encoding: str) -> tuple[int, int]:
        parsed = cls._MEASURE_SIGNATURE_PATTERN.match(signature_encoding)
        if not parsed:
            raise ValueError(
                "Expected a measure signature with the format '*M<beats>/<unit>', "
                f"but received '{signature_encoding}'."
            )

        beats = int(parsed.group(1))
        beat_unit = int(parsed.group(2))

        if beats <= 0 or beat_unit <= 0:
            raise ValueError(
                f"Invalid measure signature values in '{signature_encoding}': "
                "both beats and unit must be positive integers."
            )

        return beats, beat_unit

    def _compute_total_duration(
        self,
        duration_tokens: Sequence[DurationToken],
        measure_index: int | None,
    ) -> Tuple[Fraction, str]:
        total = Fraction(0, 1)
        index = 0
        while index < len(duration_tokens):
            token_position = index + 1
            duration_fraction, consumed_count, error_message = self._consume_duration_group_as_fraction(
                duration_tokens,
                index=index,
                measure_index=measure_index,
                token_position=token_position,
            )
            if error_message:
                return Fraction(0, 1), error_message
            total += duration_fraction
            index += consumed_count

        return total, ""

    @classmethod
    def _consume_duration_group_as_fraction(
        cls,
        duration_tokens: Sequence[DurationToken],
        *,
        index: int,
        measure_index: int | None,
        token_position: int,
    ) -> Tuple[Fraction, int, str]:
        token = duration_tokens[index]

        if isinstance(token, NoteRestToken):
            duration_subtokens = [
                subtoken for subtoken in token.pitch_duration_subtokens
                if subtoken.category == TokenCategory.DURATION
            ]
            if len(duration_subtokens) == 0:
                return Fraction(0, 1), 1, cls._format_positioned_error(
                    "NoteRestToken must contain at least one duration subtoken",
                    measure_index=measure_index,
                    token_position=token_position,
                )
            duration_values = [subtoken.encoding for subtoken in duration_subtokens]
            duration_fraction, error_message = cls._duration_group_values_to_fraction(
                duration_values,
                measure_index=measure_index,
                token_position=token_position,
            )
            return duration_fraction, 1, error_message

        token_value, error_message = cls._extract_duration_value(token)
        if error_message:
            return Fraction(0, 1), 1, cls._format_positioned_error(
                "Unsupported duration token type",
                measure_index=measure_index,
                token_position=token_position,
                details=f"type={type(token).__name__}",
            )

        if cls._is_dot_token_value(token_value):
            return Fraction(0, 1), 1, cls._format_positioned_error(
                "Duration dot found without a previous base duration",
                measure_index=measure_index,
                token_position=token_position,
            )

        duration_values: List[Union[int, str]] = [token_value]
        look_ahead_index = index + 1
        while look_ahead_index < len(duration_tokens):
            look_ahead_value, look_ahead_error = cls._extract_duration_value(duration_tokens[look_ahead_index])
            if look_ahead_error:
                break
            if not cls._is_dot_token_value(look_ahead_value):
                break
            duration_values.append(look_ahead_value)
            look_ahead_index += 1

        duration_fraction, error_message = cls._duration_group_values_to_fraction(
            duration_values,
            measure_index=measure_index,
            token_position=token_position,
        )
        return duration_fraction, len(duration_values), error_message

    @classmethod
    def _extract_duration_value(cls, duration_token: DurationToken) -> Tuple[Union[int, str, None], str]:
        if isinstance(duration_token, DurationClassical):
            return duration_token.duration, ""

        if isinstance(duration_token, Subtoken):
            if cls._is_dot_token_value(duration_token.encoding):
                return ".", ""
            if duration_token.category != TokenCategory.DURATION:
                return None, "Subtoken category must be DURATION"
            return duration_token.encoding, ""

        if isinstance(duration_token, (int, str)):
            return duration_token, ""

        return None, "Unsupported duration token type"

    @classmethod
    def _is_dot_token_value(cls, duration_value: Union[int, str]) -> bool:
        return isinstance(duration_value, str) and duration_value.strip() == "."

    @classmethod
    def _duration_group_values_to_fraction(
        cls,
        duration_values: Sequence[Union[int, str]],
        *,
        measure_index: int | None,
        token_position: int,
    ) -> Tuple[Fraction, str]:
        if len(duration_values) == 0:
            return Fraction(0, 1), cls._format_positioned_error(
                "Duration group cannot be empty",
                measure_index=measure_index,
                token_position=token_position,
            )

        base_duration, error_message = cls._duration_value_to_fraction(
            duration_values[0],
            measure_index=measure_index,
            token_position=token_position,
        )
        if error_message:
            return Fraction(0, 1), error_message

        total = base_duration
        increment = base_duration
        for dot_value in duration_values[1:]:
            if not cls._is_dot_token_value(dot_value):
                return Fraction(0, 1), cls._format_positioned_error(
                    "Only duration dots are allowed after a base duration",
                    measure_index=measure_index,
                    token_position=token_position,
                    details=f"value={dot_value}",
                )
            increment = increment / 2
            total += increment

        return total, ""

    @classmethod
    def _convert_duration_token_to_fraction(
        cls,
        duration_token: DurationToken,
        *,
        measure_index: int | None,
        token_position: int,
    ) -> Tuple[Fraction, str]:
        if isinstance(duration_token, DurationClassical):
            return cls._duration_value_to_fraction(
                duration_token.duration,
                measure_index=measure_index,
                token_position=token_position,
            )

        if isinstance(duration_token, Subtoken):
            if duration_token.category != TokenCategory.DURATION:
                return Fraction(0, 1), cls._format_positioned_error(
                    "Subtoken category must be DURATION",
                    measure_index=measure_index,
                    token_position=token_position,
                )
            return cls._duration_value_to_fraction(
                duration_token.encoding,
                measure_index=measure_index,
                token_position=token_position,
            )

        if isinstance(duration_token, NoteRestToken):
            duration_subtokens = [
                subtoken for subtoken in duration_token.pitch_duration_subtokens
                if subtoken.category == TokenCategory.DURATION
            ]
            if len(duration_subtokens) != 1:
                return Fraction(0, 1), cls._format_positioned_error(
                    "NoteRestToken must contain exactly one duration subtoken",
                    measure_index=measure_index,
                    token_position=token_position,
                )
            return cls._duration_value_to_fraction(
                duration_subtokens[0].encoding,
                measure_index=measure_index,
                token_position=token_position,
            )

        if isinstance(duration_token, (int, str)):
            return cls._duration_value_to_fraction(
                duration_token,
                measure_index=measure_index,
                token_position=token_position,
            )

        return Fraction(0, 1), cls._format_positioned_error(
            "Unsupported duration token type",
            measure_index=measure_index,
            token_position=token_position,
            details=f"type={type(duration_token).__name__}",
        )

    @classmethod
    def _duration_value_to_fraction(
        cls,
        raw_duration: Union[int, str],
        *,
        measure_index: int | None,
        token_position: int,
    ) -> Tuple[Fraction, str]:
        try:
            duration_value = int(raw_duration)
        except (TypeError, ValueError):
            return Fraction(0, 1), cls._format_positioned_error(
                "Duration value must be an integer",
                measure_index=measure_index,
                token_position=token_position,
                details=f"value={raw_duration}",
            )

        if duration_value <= 0:
            return Fraction(0, 1), cls._format_positioned_error(
                "Duration value must be greater than zero",
                measure_index=measure_index,
                token_position=token_position,
                details=f"value={duration_value}",
            )

        return Fraction(1, duration_value), ""

    def _build_measure_mismatch_message(
        self,
        *,
        measure_index: int | None,
        measured_duration: Fraction,
        spine_index: int | None = None,
    ) -> str:
        return _build_error_message_bad_measure(
            measure_id=measure_index,
            meter_signature=self.measure_signature_token.encoding,
            measured_missmatch_fraction=measured_duration,
            expected_measure_duration=self._expected_measure_duration,
            spine_index=spine_index,
        )

    @staticmethod
    def _format_positioned_error(
        message: str,
        *,
        measure_index: int | None,
        token_position: int,
        details: str | None = None,
    ) -> str:
        measure_label = f"#{measure_index}" if measure_index is not None else "<unknown>"
        suffix = f" ({details})" if details else ""
        return (
            f"{message} at measure {measure_label}, position #{token_position}{suffix}."
        )


class HorizontalRhythmValidator:
    """
    Validate horizontal rhythm alignment across multiple spines.
    
    Implements Humdrum's global rhythmic grid rule: every spine must account for
    every rhythmic subdivision that exists anywhere in the measure across all spines.
    All spines must have exactly one token per grid row, using null tokens (.)
    for positions where a voice has no new attack.
    """

    @staticmethod
    def _gcd(a: int, b: int) -> int:
        """Compute greatest common divisor for LCM calculation."""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def _lcm(a: int, b: int) -> int:
        """Compute least common multiple of two duration values."""
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // HorizontalRhythmValidator._gcd(a, b)

    @classmethod
    def _lcm_of_sequence(cls, duration_values: List[int]) -> int:
        """Compute LCM across a sequence of duration values."""
        if not duration_values:
            return 0
        result = duration_values[0]
        for value in duration_values[1:]:
            result = cls._lcm(result, value)
        return result

    @staticmethod
    def _parse_duration_value(duration_encoding: str) -> int:
        """
        Extract numeric duration value, ignoring augmentation dots.
        
        Example: "4.." → 4; "12" → 12; "8..." → 8
        """
        # Strip leading/trailing whitespace and all trailing dots
        encoding = duration_encoding.strip().rstrip(".")
        try:
            return int(encoding)
        except ValueError:
            raise ValueError(f"Invalid duration encoding: {duration_encoding}")

    @classmethod
    def _calculate_grid_resolution(cls, spines: List[List[str]]) -> int:
        """
        Calculate the finest rhythmic subdivision (grid resolution) across all spines.
        
        Grid resolution = LCM of all duration denominators in the measure.
        
        Args:
            spines: List of spines, each spine is a list of duration strings
                   (e.g., ["4", ".", "4", "."] for spine 1)
        
        Returns:
            Grid resolution (smallest rhythmic unit in the measure)
        """
        all_durations = []
        
        for spine in spines:
            for duration_str in spine:
                # Skip null tokens entirely (they're not rhythmic events)
                if duration_str.strip() == ".":
                    continue
                try:
                    dur_value = cls._parse_duration_value(duration_str)
                    all_durations.append(dur_value)
                except ValueError:
                    # Invalid encoding; skip
                    continue
        
        if not all_durations:
            return 1  # Default to whole note if no valid durations found
        
        grid = cls._lcm_of_sequence(all_durations)
        return grid if grid > 0 else 1

    @classmethod
    def _expand_to_grid(
        cls,
        durations: List[str],
        grid_resolution: int,
    ) -> List[str | None]:
        """
        Expand a spine's duration list to match the grid resolution.
        
        For each real duration token, calculates how many grid slots it occupies.
        Adds implicit None (null) placeholders for unfilled slots.
        Explicit "." tokens are preserved and count toward filling slots.
        
        Args:
            durations: List of duration strings for one spine
            grid_resolution: The LCM grid resolution
        
        Returns:
            List of strings/None representing all grid slots used
        """
        expanded = []
        i = 0
        
        while i < len(durations):
            duration_str = durations[i].strip()
            
            if duration_str == ".":
                # Explicit null token - represents 1 slot
                expanded.append(".")
                i += 1
            else:
                # Real duration token
                try:
                    dur_value = cls._parse_duration_value(duration_str)
                    slots_needed = grid_resolution // dur_value
                    
                    # Add the note itself
                    expanded.append(duration_str)
                    slots_filled = 1
                    
                    # Look ahead for explicit nulls to fill remaining slots
                    j = i + 1
                    while j < len(durations) and durations[j].strip() == "." and slots_filled < slots_needed:
                        expanded.append(".")
                        slots_filled += 1
                        j += 1
                    
                    # Fill any remaining slots with implicit None
                    while slots_filled < slots_needed:
                        expanded.append(None)
                        slots_filled += 1
                    
                    i = j
                except ValueError:
                    # Invalid encoding - just add it
                    expanded.append(duration_str)
                    i += 1
        
        return expanded

    @classmethod
    def _validate_grid_alignment(
        cls,
        durations: List[str],
        grid_resolution: int,
    ) -> Tuple[bool, str]:
        """
        Validate that a spine's durations properly align to the grid.
        
        Each token occupies a certain number of grid slots based on its duration.
        Explicit null tokens (.) should mark continuation of previous events.
        
        Args:
            durations: List of duration strings for one spine
            grid_resolution: The grid resolution to validate against
        
        Returns:
            (is_valid, error_message)
        """
        # Calculate total grid slots needed vs. what's provided
        total_slots_needed = 0
        slots_filled = 0
        
        i = 0
        while i < len(durations):
            duration_str = durations[i].strip()
            
            if duration_str == ".":
                # Null token occupies 1 slot
                slots_filled += 1
                i += 1
            else:
                # Regular duration token
                try:
                    dur_value = cls._parse_duration_value(duration_str)
                    slots_for_this = grid_resolution // dur_value
                    
                    # Count how many nulls follow this token
                    nulls_after = 0
                    j = i + 1
                    while j < len(durations) and durations[j].strip() == ".":
                        nulls_after += 1
                        j += 1
                    
                    # This token + its following nulls should fill slots_for_this
                    total_filled_by_group = 1 + nulls_after
                    
                    if total_filled_by_group < slots_for_this:
                        return False, (
                            f"Duration '{duration_str}' requires {slots_for_this} grid slots "
                            f"but only {total_filled_by_group} tokens provided (1 note + {nulls_after} nulls)"
                        )
                    
                    slots_filled += total_filled_by_group
                    i = j
                except ValueError as e:
                    return False, f"Invalid duration: {duration_str} ({str(e)})"
        
        return True, ""

    @classmethod
    def validate_measure_horizontally(
        cls,
        spines: List[List[NoteRestToken | Subtoken]],
        meter_signature: str,
        measure_index: int | None = None,
    ) -> Tuple[bool, str]:
        """
        Validate horizontal rhythm alignment across multiple spines.
        
        Args:
            spines: List of spines, each spine is a list of note/rest/null tokens
            meter_signature: Time signature (e.g., "*M4/4")
            measure_index: Optional measure number for error messages
        
        Returns:
            (is_valid, error_message)
        """
        if not spines:
            return True, ""
        
        if len(spines) == 1:
            # Single spine always aligns with itself
            return True, ""
        
        # Extract duration values from each spine
        spine_durations: List[List[str]] = []
        for spine_idx, spine in enumerate(spines):
            durations = []
            for token in spine:
                if isinstance(token, Subtoken):
                    # Subtoken with category DURATION or EMPTY
                    if token.category == TokenCategory.DURATION:
                        durations.append(token.encoding)
                    elif token.category == TokenCategory.EMPTY:
                        durations.append(".")
                    else:
                        # Unexpected category
                        return False, (
                            f"Horizontal alignment error: unexpected token category "
                            f"{token.category} in spine #{spine_idx}"
                        )
                elif isinstance(token, NoteRestToken):
                    # Extract duration from NoteRestToken
                    duration_subtokens = [
                        st for st in token.pitch_duration_subtokens
                        if st.category == TokenCategory.DURATION
                    ]
                    if duration_subtokens:
                        durations.append(duration_subtokens[0].encoding)
                    else:
                        return False, (
                            f"Horizontal alignment error: NoteRestToken in spine #{spine_idx} "
                            f"has no duration subtoken"
                        )
                else:
                    return False, (
                        f"Horizontal alignment error: unsupported token type "
                        f"{type(token).__name__} in spine #{spine_idx}"
                    )
            spine_durations.append(durations)
        
        # Calculate grid resolution (LCM of all rhythmic values)
        grid_resolution = cls._calculate_grid_resolution(spine_durations)
        
        # Validate each spine aligns to the grid
        for spine_idx, durations in enumerate(spine_durations):
            is_valid, error_msg = cls._validate_grid_alignment(durations, grid_resolution)
            if not is_valid:
                measure_label = f"#{measure_index}" if measure_index is not None else "<unknown>"
                return False, (
                    f"Measure {measure_label}, spine #{spine_idx}: {error_msg} "
                    f"(grid resolution: {grid_resolution})"
                )
        
        return True, ""
