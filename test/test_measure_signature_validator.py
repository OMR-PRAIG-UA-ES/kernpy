import unittest
from pathlib import Path

import kernpy as kp
from kernpy.core.tokens import BarToken, TimeSignatureToken
from kernpy.core.measure_signature_validators import (
    MeasureSignatureToken,
    MeasureSignatureValidator,
)


class MeasureSignatureValidatorTestCase(unittest.TestCase):
    @staticmethod
    def _duration_subtoken(value: int) -> kp.Subtoken:
        return kp.Subtoken(str(value), kp.TokenCategory.DURATION)

    @staticmethod
    def _note_rest_duration(value: int) -> kp.NoteRestToken:
        return kp.NoteRestToken(
            encoding=f"{value}c",
            pitch_duration_subtokens=[
                kp.Subtoken(str(value), kp.TokenCategory.DURATION),
                kp.Subtoken("c", kp.TokenCategory.PITCH),
            ],
            decoration_subtokens=[],
        )

    @classmethod
    def _duration_subtokens(cls, values: list[int]) -> list[kp.Subtoken]:
        return [cls._duration_subtoken(v) for v in values]

    def test_constructor_accepts_measure_signature_token(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M4/4"))
        self.assertEqual("*M4/4", validator.measure_signature_token.encoding)

    def test_constructor_accepts_time_signature_token(self):
        validator = MeasureSignatureValidator(TimeSignatureToken("*M3/4"))
        self.assertEqual("*M3/4", validator.measure_signature_token.encoding)

    def test_constructor_raises_when_token_type_is_wrong(self):
        with self.assertRaises(ValueError) as context:
            MeasureSignatureValidator(BarToken("="))

        self.assertIn("MeasureSignatureValidator expects a MeasureSignatureToken or TimeSignatureToken", str(context.exception))

    def test_constructor_raises_when_signature_encoding_is_not_measure_signature(self):
        with self.assertRaises(ValueError) as context:
            MeasureSignatureValidator(MeasureSignatureToken("*clefG2"))

        self.assertIn("Expected a measure signature with the format '*M<beats>/<unit>'", str(context.exception))

    def test_fits_measure_true_for_4_4(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M4/4"))
        durations = [
            self._duration_subtoken(4),
            self._duration_subtoken(4),
            self._duration_subtoken(4),
            self._duration_subtoken(4),
        ]

        is_valid, error_message = validator.fits_measure(durations)
        self.assertTrue(is_valid)
        self.assertEqual("", error_message)

    def test_fits_measure_true_for_6_8(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M6/8"))
        durations = [self._duration_subtoken(8)] * 6

        is_valid, error_message = validator.fits_measure(durations)
        self.assertTrue(is_valid)
        self.assertEqual("", error_message)

    def test_fits_measure_true_for_3_2(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M3/2"))
        durations = [
            self._duration_subtoken(2),
            self._duration_subtoken(2),
            self._duration_subtoken(2),
        ]

        is_valid, error_message = validator.fits_measure(durations)
        self.assertTrue(is_valid)
        self.assertEqual("", error_message)

    def test_fits_measure_true_for_many_signatures(self):
        signature_cases = [
            ("*M2/8", [8, 8]),
            ("*M3/16", [16, 16, 16]),
            ("*M5/8", [8, 8, 8, 8, 8]),
            ("*M7/4", [4, 4, 4, 4, 4, 4, 4]),
            ("*M9/4", [4, 4, 4, 4, 4, 4, 4, 4, 4]),
            ("*M8/8", [8, 8, 8, 8, 8, 8, 8, 8]),
        ]

        for signature, duration_values in signature_cases:
            with self.subTest(signature=signature):
                validator = MeasureSignatureValidator(MeasureSignatureToken(signature))
                durations = [self._duration_subtoken(v) for v in duration_values]

                is_valid, error_message = validator.fits_measure(durations)
                self.assertTrue(is_valid)
                self.assertEqual("", error_message)

    def test_fits_measure_true_for_many_signatures_with_mixed_duration_values(self):
        # Same total duration per signature, but mixing rhythmic values inside each measure.
        signature_cases = [
            ("*M2/8", [8, 16, 16]),
            ("*M3/16", [16, 32, 32, 16]),
            ("*M5/8", [4, 8, 8, 8]),
            ("*M7/4", [1, 2, 4]),
            ("*M9/4", [1, 1, 4]),
            ("*M8/8", [2, 4, 8, 8]),
        ]

        for signature, duration_values in signature_cases:
            with self.subTest(signature=signature):
                validator = MeasureSignatureValidator(MeasureSignatureToken(signature))
                durations = self._duration_subtokens(duration_values)

                is_valid, error_message = validator.fits_measure(durations)
                self.assertTrue(is_valid)
                self.assertEqual("", error_message)

    def test_fits_measure_false_for_wrong_total_duration(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M4/4"))
        durations = [
            self._duration_subtoken(4),
            self._duration_subtoken(4),
            self._duration_subtoken(4),
        ]

        is_valid, error_message = validator.fits_measure(durations)
        self.assertFalse(is_valid)
        self.assertIn("duration mismatch", error_message)
        self.assertIn("expected 1", error_message)
        self.assertIn("got 3/4", error_message)

    def test_fits_measure_false_for_wrong_total_duration_in_3_16(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M3/16"))
        durations = [
            self._duration_subtoken(16),
            self._duration_subtoken(16),
        ]

        is_valid, error_message = validator.fits_measure(durations)
        self.assertFalse(is_valid)
        self.assertIn("duration mismatch", error_message)
        self.assertIn("expected 3/16", error_message)
        self.assertIn("got 1/8", error_message)

    def test_fits_measure_accepts_note_rest_tokens(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M2/4"))
        durations = [
            self._note_rest_duration(4),
            self._note_rest_duration(4),
        ]

        is_valid, error_message = validator.fits_measure(durations)
        self.assertTrue(is_valid)
        self.assertEqual("", error_message)

    def test_fits_measure_accepts_dotted_durations(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M11/16"))
        durations = [
            self._duration_subtoken(4),
            self._duration_subtoken('.'),
            self._duration_subtoken(8),
            self._duration_subtoken('.'),
            self._duration_subtoken(8),
        ]

        is_valid, error_message = validator.fits_measure(durations)
        self.assertTrue(is_valid)
        self.assertEqual("", error_message)

    def test_fits_measure_accepts_double_dotted_durations(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M11/16"))
        durations = [
            self._duration_subtoken(4),
            self._duration_subtoken('.'),
            self._duration_subtoken('.'),
            self._duration_subtoken(8),
            self._duration_subtoken('.'),
            self._duration_subtoken(16),
        ]

        is_valid, error_message = validator.fits_measure(durations)
        self.assertTrue(is_valid)
        self.assertEqual("", error_message)

    def test_assert_measure_returns_descriptive_underflow(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M3/4"))

        is_valid, error_message = validator.assert_measure(
            duration_tokens=[
                self._duration_subtoken(4),
                self._duration_subtoken(4),
            ],
            measure_index=2,
        )

        self.assertFalse(is_valid)
        self.assertIn("Measure #2 duration mismatch", error_message)
        self.assertIn("expected 3/4", error_message)
        self.assertIn("got 1/2", error_message)

    def test_assert_measure_returns_descriptive_overflow(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M2/4"))

        is_valid, error_message = validator.assert_measure(
            duration_tokens=[
                self._duration_subtoken(4),
                self._duration_subtoken(4),
                self._duration_subtoken(8),
            ],
            measure_index=1,
        )

        self.assertFalse(is_valid)
        self.assertIn("Measure #1 duration mismatch", error_message)
        self.assertIn("expected 1/2", error_message)
        self.assertIn("got 5/8", error_message)

    def test_assert_measure_returns_error_when_duration_token_is_invalid(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M4/4"))

        is_valid, error_message = validator.assert_measure([object()], measure_index=1)

        self.assertFalse(is_valid)
        self.assertIn("Unsupported duration token type at measure #1, position #1", error_message)

    def test_assert_measure_returns_error_for_non_integer_duration(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M4/4"))

        is_valid, error_message = validator.assert_measure(["invalid-duration"], measure_index=1)

        self.assertFalse(is_valid)
        self.assertIn("Duration value must be an integer", error_message)

    def test_assert_measure_returns_error_for_non_positive_duration(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M4/4"))

        is_valid, error_message = validator.assert_measure([0], measure_index=1)

        self.assertFalse(is_valid)
        self.assertIn("Duration value must be greater than zero", error_message)

    def test_validate_filtered_score_tokens_returns_true_when_all_measures_fit(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M2/4"))
        filtered_tokens = [
            self._duration_subtoken(4),
            self._duration_subtoken(4),
            BarToken("="),
            self._duration_subtoken(2),
            BarToken("="),
        ]

        is_valid, error_message = validator.validate_filtered_score_tokens(filtered_tokens)
        self.assertTrue(is_valid)
        self.assertEqual("", error_message)


class MeasureSignatureValidatorResourcesTestCase(unittest.TestCase):
    @staticmethod
    def _duration_subtoken(value: int) -> kp.Subtoken:
        return kp.Subtoken(str(value), kp.TokenCategory.DURATION)

    @staticmethod
    def _validate_resource(resource_path: str, signature_encoding: str) -> tuple[bool, str]:
        try:
            document, _ = kp.load(resource_path)
        except Exception as error:
            return False, f"load-error: {error}"

        validator = MeasureSignatureValidator(MeasureSignatureToken(signature_encoding))
        return validator.validate_document(document)

    def test_complete_kern_resources_expected_valid(self):
        valid_cases = [
            ("test/resources/unit/minimal.krn", "*M1/1"),
            ("test/resources/samples/monophonic-score.krn", "*M1/1"),
        ]

        for resource_path, signature_encoding in valid_cases:
            with self.subTest(resource=resource_path, signature=signature_encoding):
                is_valid, error_message = self._validate_resource(resource_path, signature_encoding)
                self.assertTrue(
                    is_valid,
                    msg=(
                        f"Expected valid measure layout for {resource_path} with {signature_encoding}, "
                        f"but got error: {error_message}"
                    ),
                )
                self.assertEqual("", error_message)

    def test_complete_kern_resources_expected_invalid(self):
        invalid_cases = [
            ("test/resources/unit/time.krn", "*M4/4", "time signature change"),
            ("test/resources/legacy/base_tuplet.krn", "*M4/4", "duration mismatch"),
            ("test/resources/legacy/base_tuplet_longer.krn", "*M4/4", "duration mismatch"),
            ("test/resources/samples/wrong_number_of_columns.krn", "*M2/2", "load-error"),
            (
                "test/resources/end-of-file/eof_monophonic_only_kern_from_base_tuplet_longer.krn",
                "*M4/4",
                "load-error",
            ),
        ]

        for resource_path, signature_encoding, expected_error_fragment in invalid_cases:
            with self.subTest(resource=resource_path, signature=signature_encoding):
                is_valid, error_message = self._validate_resource(resource_path, signature_encoding)
                self.assertFalse(
                    is_valid,
                    msg=(
                        f"Expected invalid measure layout for {resource_path} with {signature_encoding}, "
                        "but validation returned True."
                    ),
                )
                self.assertIn(expected_error_fragment, error_message)

    def test_all_resource_paths_exist(self):
        referenced_resources = [
            "test/resources/unit/minimal.krn",
            "test/resources/samples/monophonic-score.krn",
            "test/resources/unit/time.krn",
            "test/resources/legacy/base_tuplet.krn",
            "test/resources/legacy/base_tuplet_longer.krn",
            "test/resources/samples/wrong_number_of_columns.krn",
            "test/resources/end-of-file/eof_monophonic_only_kern_from_base_tuplet_longer.krn",
        ]

        for resource_path in referenced_resources:
            with self.subTest(resource=resource_path):
                self.assertTrue(Path(resource_path).exists())

    def test_validate_filtered_score_tokens_returns_descriptive_error_when_measure_fails(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M2/4"))
        filtered_tokens = [
            self._duration_subtoken(4),
            BarToken("="),
        ]

        is_valid, error_message = validator.validate_filtered_score_tokens(filtered_tokens)
        self.assertFalse(is_valid)
        self.assertIn("Measure #1 duration mismatch", error_message)

    def test_validate_filtered_score_tokens_returns_error_on_signature_change(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M4/4"))
        filtered_tokens = [
            self._duration_subtoken(4),
            self._duration_subtoken(4),
            TimeSignatureToken("*M3/4"),
            self._duration_subtoken(4),
            self._duration_subtoken(4),
        ]

        is_valid, error_message = validator.validate_filtered_score_tokens(filtered_tokens)
        self.assertFalse(is_valid)
        self.assertIn("time signature change", error_message)
        self.assertIn("*M3/4", error_message)

    def test_validate_filtered_score_tokens_returns_error_on_many_mixed_signatures(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M2/8"))
        filtered_tokens = [
            TimeSignatureToken("*M2/8"),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            BarToken("="),
            TimeSignatureToken("*M3/16"),
            self._duration_subtoken(16),
            self._duration_subtoken(16),
            self._duration_subtoken(16),
            BarToken("="),
            TimeSignatureToken("*M5/8"),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            BarToken("="),
        ]

        is_valid, error_message = validator.validate_filtered_score_tokens(filtered_tokens)
        self.assertFalse(is_valid)
        self.assertIn("time signature change", error_message)
        self.assertIn("*M3/16", error_message)

    def test_validate_filtered_score_tokens_returns_true_for_8_8_two_measures(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M8/8"))
        filtered_tokens = [
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            self._duration_subtoken(8),
            BarToken("="),
            self._duration_subtoken(4),
            self._duration_subtoken(4),
            self._duration_subtoken(4),
            self._duration_subtoken(4),
            BarToken("="),
        ]

        is_valid, error_message = validator.validate_filtered_score_tokens(filtered_tokens)
        self.assertTrue(is_valid)
        self.assertEqual("", error_message)


if __name__ == "__main__":
    unittest.main()
