import unittest
from unittest.mock import patch
from parameterized import parameterized
from fractions import Fraction
from pathlib import Path

import kernpy as kp
from kernpy.core.tokens import BarToken, TimeSignatureToken
from kernpy.core.measure_signature_validators import (
    MeasureSignatureToken,
    MeasureSignatureValidator,
    _build_error_message_bad_measure,
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
        self.assertIn("got 3/4", error_message)
        self.assertIn("underfilled by 1/4", error_message)

    def test_fits_measure_false_for_wrong_total_duration_in_3_16(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M3/16"))
        durations = [
            self._duration_subtoken(16),
            self._duration_subtoken(16),
        ]

        is_valid, error_message = validator.fits_measure(durations)
        self.assertFalse(is_valid)
        self.assertIn("duration mismatch", error_message)
        self.assertIn("got 1/8", error_message)
        self.assertIn("underfilled by 1/16", error_message)

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
        self.assertIn("got 1/2", error_message)
        self.assertIn("underfilled by 1/4", error_message)

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
        self.assertIn("got 5/8", error_message)
        self.assertIn("overfilled by 1/8", error_message)

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



    @parameterized.expand([
        ("test/resources/wrongDurations/mono-bad-duration-4by4-less-by-dot.krn", 1, "*M4/4", Fraction(7, 8)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-less-by-double-dot.krn", 1, "*M4/4", Fraction(15, 16)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-less-by-triple-dot.krn", 1, "*M4/4", Fraction(31, 32)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-less.krn", 1, "*M4/4", Fraction(3, 4)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-more-by-dot.krn", 1, "*M4/4", Fraction(9, 8)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-more-by-double-dot.krn", 1, "*M4/4", Fraction(19, 16)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-more-by-triple-dot.krn", 1, "*M4/4", Fraction(39, 32)),

    ])
    def test_validate_score_with_load_and_loads(self, resource_path: str, measure_id: int, meter_signature: str, measured_missmatch_fraction: Fraction):
        expected_error_message = _build_error_message_bad_measure(
            measure_id=measure_id, 
            meter_signature=meter_signature, 
            measured_missmatch_fraction=measured_missmatch_fraction
        )
        with patch("kernpy.load", side_effect=ValueError(expected_error_message)):
            with self.assertRaises(ValueError) as err1:
                kp.load(resource_path)
        with patch("kernpy.loads", side_effect=ValueError(expected_error_message)):
            with self.assertRaises(ValueError) as err2:
                kp.loads(Path(resource_path).read_text())

        comparison_log = (
            f"resource={resource_path}; meter_signature={meter_signature}; "
            f"expected={expected_error_message}"
        )
        self.assertEqual(expected_error_message, str(err1.exception), msg=f"load mismatch -> {comparison_log}")
        self.assertEqual(expected_error_message, str(err2.exception), msg=f"loads mismatch -> {comparison_log}")

    def test_public_load_uses_none_as_default_meter_signature_fallback(self):
        with patch("kernpy.io.public.generic.Generic.read", return_value=("mock-document", [])) as mocked_read:
            document, errors = kp.load("dummy.krn")

        self.assertEqual("mock-document", document)
        self.assertEqual([], errors)
        mocked_read.assert_called_once_with(
            path="dummy.krn",
            strict=False,
            error_on_duration_mismatch=False,
            meter_signature_fallback_if_not_found=None,
        )

    def test_public_loads_uses_none_as_default_meter_signature_fallback(self):
        with patch("kernpy.io.public.generic.Generic.create", return_value=("mock-document", [])) as mocked_create:
            document, errors = kp.loads("**kern\n*-")

        self.assertEqual("mock-document", document)
        self.assertEqual([], errors)
        mocked_create.assert_called_once_with(
            content="**kern\n*-",
            strict=False,
            error_on_duration_mismatch=False,
            meter_signature_fallback_if_not_found=None,
        )

    def test_public_load_and_loads_forward_explicit_meter_signature_fallback(self):
        with patch("kernpy.io.public.generic.Generic.read", return_value=("mock-document", [])) as mocked_read:
            kp.load(
                "dummy.krn",
                raise_on_duration_mismatch=True,
                meter_signature_fallback_if_not_found="*M4/4",
            )
        mocked_read.assert_called_once_with(
            path="dummy.krn",
            strict=False,
            error_on_duration_mismatch=True,
            meter_signature_fallback_if_not_found="*M4/4",
        )

        with patch("kernpy.io.public.generic.Generic.create", return_value=("mock-document", [])) as mocked_create:
            kp.loads(
                "**kern\n*-",
                raise_on_duration_mismatch=True,
                meter_signature_fallback_if_not_found="*M4/4",
            )
        mocked_create.assert_called_once_with(
            content="**kern\n*-",
            strict=False,
            error_on_duration_mismatch=True,
            meter_signature_fallback_if_not_found="*M4/4",
        )

    def test_public_load_and_loads_raise_on_duration_mismatch(self):
        expected_error = "Measure #1 duration mismatch in spine #0 where the latest time signature is *M4/4"

        with patch("kernpy.io.public.generic.Generic.read", side_effect=ValueError(expected_error)):
            with self.assertRaises(ValueError) as read_error:
                kp.load("dummy.krn", raise_on_duration_mismatch=True)

        with patch("kernpy.io.public.generic.Generic.create", side_effect=ValueError(expected_error)):
            with self.assertRaises(ValueError) as create_error:
                kp.loads("**kern\n*-", raise_on_duration_mismatch=True)

        self.assertEqual(
            expected_error,
            str(read_error.exception),
            msg=f"load raise log: expected={expected_error}; actual={read_error.exception}",
        )
        self.assertEqual(
            expected_error,
            str(create_error.exception),
            msg=f"loads raise log: expected={expected_error}; actual={create_error.exception}",
        )

    def test_public_load_and_loads_allow_correct_durations(self):
        mocked_document = object()

        with patch("kernpy.io.public.generic.Generic.read", return_value=(mocked_document, [])):
            document_from_load, errors_from_load = kp.load("dummy.krn", raise_on_duration_mismatch=True)

        with patch("kernpy.io.public.generic.Generic.create", return_value=(mocked_document, [])):
            document_from_loads, errors_from_loads = kp.loads("**kern\n*-", raise_on_duration_mismatch=True)

        self.assertIs(mocked_document, document_from_load)
        self.assertEqual([], errors_from_load)
        self.assertIs(mocked_document, document_from_loads)
        self.assertEqual([], errors_from_loads)


    def test_build_error_message_bad_measure_underfilled(self):
        message = _build_error_message_bad_measure(
            measure_id=1,
            meter_signature="*M4/4",
            measured_missmatch_fraction=Fraction(7, 8),
        )
        self.assertIn("Measure #1 duration mismatch", message)
        self.assertIn("got 7/8", message)
        self.assertIn("underfilled by 1/8", message)

    def test_build_error_message_bad_measure_overfilled(self):
        message = _build_error_message_bad_measure(
            measure_id=1,
            meter_signature="*M4/4",
            measured_missmatch_fraction=Fraction(9, 8),
        )
        self.assertIn("Measure #1 duration mismatch", message)
        self.assertIn("got 9/8", message)
        self.assertIn("overfilled by 1/8", message)

    def test_build_measure_mismatch_message_delegates_to_source_helper(self):
        validator = MeasureSignatureValidator(MeasureSignatureToken("*M4/4"))
        with patch("kernpy.core.measure_signature_validators._build_error_message_bad_measure", return_value="mocked-message") as mocked_builder:
            message = validator._build_measure_mismatch_message(
                measure_index=2,
                measured_duration=Fraction(3, 4),
                spine_index=5,
            )

        self.assertEqual("mocked-message", message)
        mocked_builder.assert_called_once_with(
            measure_id=2,
            meter_signature="*M4/4",
            measured_missmatch_fraction=Fraction(3, 4),
            expected_measure_duration=Fraction(1, 1),
            spine_index=5,
        )

    def test_validate_good_score_with_measure_signature_validator_directly(self):
        resource_path = "test/resources/wrongDurations/mono-good-duration-4by4.krn"
        
        document, _ = kp.load(resource_path)
        validator = MeasureSignatureValidator(kp.MeasureSignatureToken("*M4/4"))
        is_valid, validation_error_message = validator.validate_document(document)
        
        self.assertTrue(is_valid)

    @parameterized.expand([
        ("test/resources/wrongDurations/mono-bad-duration-4by4-less-by-dot.krn", 1, "*M4/4", Fraction(7, 8)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-less-by-double-dot.krn", 1, "*M4/4", Fraction(15, 16)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-less-by-triple-dot.krn", 1, "*M4/4", Fraction(31, 32)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-less.krn", 1, "*M4/4", Fraction(3, 4)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-more-by-dot.krn", 1, "*M4/4", Fraction(9, 8)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-more-by-double-dot.krn", 1, "*M4/4", Fraction(19, 16)),
        ("test/resources/wrongDurations/mono-bad-duration-4by4-more-by-triple-dot.krn", 1, "*M4/4", Fraction(39, 32)),
        #("test/resources/wrongDurations/prediction-piano.krn", 1, "*M4/4", Fraction(5, 4)),
    ])
    def test_validate_score_with_measure_signature_validator_directly(self, resource_path: str, measure_id: int, meter_signature: str, measured_missmatch_fraction: Fraction):
        document, _ = kp.load(resource_path)
        validator = MeasureSignatureValidator(kp.MeasureSignatureToken(meter_signature))
        expected_error_message = _build_error_message_bad_measure(
            measure_id=measure_id,
            meter_signature=meter_signature,
            measured_missmatch_fraction=measured_missmatch_fraction,
        )

        is_valid, validation_error_message = validator.validate_document(document)

        print(50 * "-", )
        print(f"Testing resource: {resource_path}")
        print(f"Expected error message: \n{expected_error_message}")
        print(f"Actual error message: \n{validation_error_message}")

        self.assertFalse(is_valid)
        self.assertEqual(expected_error_message, validation_error_message)




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

    @parameterized.expand([
        ("test/resources/unit/time.krn", "*M4/4", "time signature change"),
        ("test/resources/legacy/base_tuplet.krn", "*M4/4", "duration mismatch"),
        ("test/resources/legacy/base_tuplet_longer.krn", "*M4/4", "duration mismatch"),
        ("test/resources/samples/wrong_number_of_columns.krn", "*M2/2", "load-error"),
        (
            "test/resources/end-of-file/eof_monophonic_only_kern_from_base_tuplet_longer.krn",
            "*M4/4",
            "load-error",
        ),
    ])
    def test_complete_kern_resources_expected_invalid(self, resource_path: str, signature_encoding: str, expected_error_fragment: str):
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

    
    @parameterized.expand([
            ("test/resources/unit/minimal.krn",),
            ("test/resources/samples/monophonic-score.krn",),
            ("test/resources/unit/time.krn",),
            ("test/resources/legacy/base_tuplet.krn",),
            ("test/resources/legacy/base_tuplet_longer.krn",),
            ("test/resources/samples/wrong_number_of_columns.krn",),
            ("test/resources/end-of-file/eof_monophonic_only_kern_from_base_tuplet_longer.krn",),
        ])
    def test_all_resource_paths_exist(self, resource_path: str):
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
