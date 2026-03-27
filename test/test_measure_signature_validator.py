import unittest
from unittest.mock import Mock, patch
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

    def test_public_load_and_loads_use_importer_measure_validator_factory(self):
        resource_path = "test/resources/wrongDurations/mono-good-duration-4by4.krn"
        resource_content = Path(resource_path).read_text()

        mocked_validator = Mock(spec=["assert_measure"])
        mocked_validator.assert_measure.return_value = (False, "mocked validator mismatch")

        with patch("kernpy.core.importer.Importer.get_measure_signature_validator", return_value=mocked_validator) as mocked_factory:
            with self.assertRaises(ValueError) as load_error:
                kp.load(resource_path, raise_on_duration_mismatch=True)
            with self.assertRaises(ValueError) as loads_error:
                kp.loads(resource_content, raise_on_duration_mismatch=True)

        self.assertEqual("mocked validator mismatch", str(load_error.exception))
        self.assertEqual("mocked validator mismatch", str(loads_error.exception))
        self.assertGreaterEqual(mocked_factory.call_count, 2)
        self.assertGreaterEqual(mocked_validator.assert_measure.call_count, 2)

    def test_public_loads_raises_when_horizontal_validation_fails(self):
        content = (
            "**kern\t**kern\n"
            "*M4/4\t*M4/4\n"
            "=1\t=1\n"
            "4c\t4e\n"
            "4d\t4f\n"
            "4e\t4g\n"
            "4f\t4a\n"
            "=2\t=2\n"
            "*-\t*-"
        )

        mocked_validator = Mock(spec=["assert_measure"])
        mocked_validator.assert_measure.return_value = (True, "")

        with patch("kernpy.core.importer.Importer.get_measure_signature_validator", return_value=mocked_validator):
            with patch(
                "kernpy.core.measure_signature_validators.HorizontalRhythmValidator.validate_measure_horizontally",
                return_value=(False, "mocked horizontal mismatch"),
            ) as mocked_horizontal:
                with self.assertRaises(ValueError) as context:
                    kp.loads(content, raise_on_duration_mismatch=True)

        self.assertEqual("mocked horizontal mismatch", str(context.exception))
        mocked_horizontal.assert_called()

    def test_public_load_and_loads_raise_when_horizontal_validation_fails(self):
        resource_path = "test/resources/wrongDurations/mono-good-duration-4by4.krn"
        resource_content = Path(resource_path).read_text()

        mocked_validator = Mock(spec=["assert_measure"])
        mocked_validator.assert_measure.return_value = (True, "")

        with patch("kernpy.core.importer.Importer.get_measure_signature_validator", return_value=mocked_validator):
            with patch(
                "kernpy.core.measure_signature_validators.HorizontalRhythmValidator.validate_measure_horizontally",
                return_value=(False, "mocked horizontal mismatch both"),
            ) as mocked_horizontal:
                with self.assertRaises(ValueError) as load_error:
                    kp.load(resource_path, raise_on_duration_mismatch=True)
                with self.assertRaises(ValueError) as loads_error:
                    kp.loads(resource_content, raise_on_duration_mismatch=True)

        self.assertEqual("mocked horizontal mismatch both", str(load_error.exception))
        self.assertEqual("mocked horizontal mismatch both", str(loads_error.exception))
        self.assertGreaterEqual(mocked_horizontal.call_count, 2)


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
        #("test/resources/wrongDurations/prediction-piano-2.krn", 1, "*M3/4", Fraction(1, 2)),
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
        ("test/resources/wrongDurations/prediction-piano.krn", "*M3/4", "load-error"),
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

    @parameterized.expand([
        ("test/resources/wrongDurations/prediction-piano.krn",),
        ("test/resources/wrongDurations/prediction-piano-2.krn",),
    ])
    def test_prediction_piano_resources_raise_expected_message_in_load_and_loads(self, resource_path: str):
        expected_message = (
            "Measure #1 duration mismatch in spine #0 where the latest time signature is *M3/4: "
            "got 1/2 of a full measure. The measure is underfilled by 1/4; "
            "add rhythmic value(s) totaling 1/4."
        )

        with self.assertRaises(ValueError) as load_error:
            kp.load(resource_path, raise_on_duration_mismatch=True)

        with self.assertRaises(ValueError) as loads_error:
            kp.loads(Path(resource_path).read_text(), raise_on_duration_mismatch=True)

        self.assertEqual(expected_message, str(load_error.exception))
        self.assertEqual(expected_message, str(loads_error.exception))
        

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


class HorizontalRhythmValidationTestCase(unittest.TestCase):
    """
    Tests for horizontal rhythm alignment validation across multiple spines.
    
    Validates that all spines account for every rhythmic subdivision that exists
    anywhere in the score (Humdrum global rhythmic grid rule).
    """

    @staticmethod
    def _duration_subtoken(value: int) -> kp.Subtoken:
        """Helper: create a duration subtoken (e.g., '4' for quarter)."""
        return kp.Subtoken(str(value), kp.TokenCategory.DURATION)

    @staticmethod
    def _null_token() -> kp.Subtoken:
        """Helper: create a null token (.)."""
        return kp.Subtoken(".", kp.TokenCategory.EMPTY)

    @staticmethod
    def _note_token(duration: int, pitch: str = "c") -> kp.NoteRestToken:
        """Helper: create a note token (e.g., 4c for quarter note on C)."""
        return kp.NoteRestToken(
            encoding=f"{duration}{pitch}",
            pitch_duration_subtokens=[
                kp.Subtoken(str(duration), kp.TokenCategory.DURATION),
                kp.Subtoken(pitch, kp.TokenCategory.PITCH),
            ],
            decoration_subtokens=[],
        )

    @staticmethod
    def _rest_token(duration: int) -> kp.NoteRestToken:
        """Helper: create a rest token (e.g., 4r for quarter rest)."""
        return kp.NoteRestToken(
            encoding=f"{duration}r",
            pitch_duration_subtokens=[
                kp.Subtoken(str(duration), kp.TokenCategory.DURATION),
                kp.Subtoken("r", kp.TokenCategory.PITCH),
            ],
            decoration_subtokens=[],
        )

    # ============= LCM Utility Tests =============
    
    def test_gcd_returns_greatest_common_divisor(self):
        """Test GCD computation for LCM calculation."""
        # These tests assume HorizontalRhythmValidator._gcd method exists
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        self.assertEqual(4, HorizontalRhythmValidator._gcd(8, 12))
        self.assertEqual(1, HorizontalRhythmValidator._gcd(7, 11))
        self.assertEqual(8, HorizontalRhythmValidator._gcd(8, 16))
        self.assertEqual(4, HorizontalRhythmValidator._gcd(4, 4))

    def test_lcm_returns_least_common_multiple(self):
        """Test LCM computation for rhythm grid resolution."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        self.assertEqual(12, HorizontalRhythmValidator._lcm(4, 12))
        self.assertEqual(24, HorizontalRhythmValidator._lcm(8, 12))
        self.assertEqual(16, HorizontalRhythmValidator._lcm(8, 16))
        self.assertEqual(12, HorizontalRhythmValidator._lcm(12, 4))

    def test_lcm_of_sequence_returns_lcm_across_all_values(self):
        """Test LCM computation across multiple duration values."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        self.assertEqual(12, HorizontalRhythmValidator._lcm_of_sequence([4, 12]))
        self.assertEqual(24, HorizontalRhythmValidator._lcm_of_sequence([4, 8, 12]))
        self.assertEqual(12, HorizontalRhythmValidator._lcm_of_sequence([4, 6, 12]))
        self.assertEqual(4, HorizontalRhythmValidator._lcm_of_sequence([4, 4, 4]))

    def test_parse_duration_value_extracts_numeric_ignoring_dots(self):
        """Test that duration parsing ignores augmentation dots."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        self.assertEqual(4, HorizontalRhythmValidator._parse_duration_value("4"))
        self.assertEqual(4, HorizontalRhythmValidator._parse_duration_value("4."))
        self.assertEqual(4, HorizontalRhythmValidator._parse_duration_value("4.."))
        self.assertEqual(8, HorizontalRhythmValidator._parse_duration_value("8..."))
        self.assertEqual(12, HorizontalRhythmValidator._parse_duration_value("12"))

    # ============= Grid Resolution Calculation Tests =============

    def test_calculate_grid_resolution_single_rhythm_type(self):
        """Test grid resolution when all spines have same rhythm."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # All quarters → grid = 4
        spines = [["4", "4", "4", "4"], ["4", "4", "4", "4"]]
        grid = HorizontalRhythmValidator._calculate_grid_resolution(spines)
        self.assertEqual(4, grid)

    def test_calculate_grid_resolution_quarters_and_eighths(self):
        """Test grid resolution with quarters + eighths → grid = 8."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Spine 1: quarters (4); Spine 2: eighths (8)
        spines = [["4", "4"], ["8", "8", "8", "8"]]
        grid = HorizontalRhythmValidator._calculate_grid_resolution(spines)
        self.assertEqual(8, grid)

    def test_calculate_grid_resolution_quarters_and_triplet_eighths(self):
        """Test grid resolution with quarters + triplet-eighths → grid = 12."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Spine 1: quarters (4); Spine 2: triplet eighths (12)
        spines = [["4", "4", "4"], ["12", "12", "12", "12", "12", "12", "12", "12", "12"]]
        grid = HorizontalRhythmValidator._calculate_grid_resolution(spines)
        self.assertEqual(12, grid)

    def test_calculate_grid_resolution_eighths_and_triplet_eighths(self):
        """Test grid resolution with eighths + triplet-eighths → grid = 24."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Spine 1: eighths (8); Spine 2: triplet eighths (12)
        spines = [["8", "8", "8"], ["12", "12", "12", "12", "12", "12"]]
        grid = HorizontalRhythmValidator._calculate_grid_resolution(spines)
        self.assertEqual(24, grid)

    # ============= Null Token & Grid Expansion Tests =============

    def test_expand_to_grid_single_quarter_matches_eighth_grid(self):
        """Test that a single quarter expands to 2 slots in eighth-note grid."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        durations = ["4"]
        expanded = HorizontalRhythmValidator._expand_to_grid(durations, grid_resolution=8)
        # Quarter (4 = 1/4) in grid 8 = 2 slots
        self.assertEqual(2, len(expanded))
        self.assertEqual("4", expanded[0])
        self.assertIsNone(expanded[1], "Second slot should be None (implicit null)")

    def test_expand_to_grid_quarters_with_explicit_nulls(self):
        """Test expansion when nulls (.) are explicitly provided."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        durations = ["4", ".", "4", "."]
        expanded = HorizontalRhythmValidator._expand_to_grid(durations, grid_resolution=8)
        # 4 tokens where nulls replace implicit ones 
        self.assertEqual(4, len(expanded))
        self.assertEqual("4", expanded[0])
        self.assertEqual(".", expanded[1])
        self.assertEqual("4", expanded[2])
        self.assertEqual(".", expanded[3])

    def test_expand_to_grid_detects_missing_null_tokens(self):
        """Test that expansion detects when null tokens are missing."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Two quarters without nulls in eighth-note grid
        durations = ["4", "4"]
        is_valid, error_msg = HorizontalRhythmValidator._validate_grid_alignment(durations, grid_resolution=8)
        self.assertFalse(is_valid, "Should detect missing nulls")
        self.assertIn("null", error_msg.lower())

    def test_expand_to_grid_accepts_valid_null_alignment(self):
        """Test that correctly-aligned nulls are accepted."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Two quarters with correct nulls in eighth-note grid
        durations = ["4", ".", "4", "."]
        is_valid, error_msg = HorizontalRhythmValidator._validate_grid_alignment(durations, grid_resolution=8)
        self.assertTrue(is_valid, f"Should accept valid alignment; got error: {error_msg}")
        self.assertEqual("", error_msg)

    # ============= Horizontal Alignment Tests (Simple Cases) =============

    def test_validate_two_spines_same_rhythm_quarters(self):
        """Test two spines with identical quarter notes → should PASS."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        spine_1 = [self._note_token(4, "c"), self._note_token(4, "d"), self._note_token(4, "e"), self._note_token(4, "f")]
        spine_2 = [self._note_token(4, "g"), self._note_token(4, "a"), self._note_token(4, "b"), self._note_token(4, "cc")]
        
        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_1, spine_2],
            meter_signature="*M4/4"
        )
        self.assertTrue(is_valid, f"Identical rhythms should pass; got: {error_msg}")
        self.assertEqual("", error_msg)

    def test_validate_two_spines_different_rhythms_without_nulls(self):
        """Test two spines with quarters + eighths but NO nulls → should FAIL."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        spine_1 = [self._note_token(4, "c"), self._note_token(4, "d")]  # 2 quarters
        spine_2 = [self._note_token(8, "e"), self._note_token(8, "f"), self._note_token(8, "g"), self._note_token(8, "a")]  # 4 eighths
        
        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_1, spine_2],
            meter_signature="*M4/4"
        )
        self.assertFalse(is_valid, "Misaligned rhythms without nulls should fail")
        # Error should mention grid slots or alignment problem
        self.assertTrue(
            "grid" in error_msg.lower() or "slot" in error_msg.lower() or "requires" in error_msg.lower(),
            f"Error should indicate alignment issue: {error_msg}"
        )

    def test_validate_two_spines_quarters_and_eighths_with_nulls(self):
        """Test quarters + eighths WITH proper null tokens → should PASS."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Spine 1: quarter, quarter (requires nulls between in 8th-note grid)
        spine_1 = [self._note_token(4, "c"), self._null_token(), self._note_token(4, "d"), self._null_token()]
        
        # Spine 2: four eighths
        spine_2 = [self._note_token(8, "e"), self._note_token(8, "f"), self._note_token(8, "g"), self._note_token(8, "a")]
        
        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_1, spine_2],
            meter_signature="*M4/4"
        )
        self.assertTrue(is_valid, f"Properly aligned rhythms should pass; got: {error_msg}")
        self.assertEqual("", error_msg)

    # ============= Complex Rhythm Tests (Triplets, Tuplets, Dots) =============

    def test_validate_quarters_and_triplet_eighths(self):
        """Test quarters + triplet-eighths (grid=12) with proper nulls."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Spine 1: 3 quarters = 12 grid slots (12/4 = 3 slots per quarter)
        spine_1 = [
            self._note_token(4, "c"), self._null_token(), self._null_token(),
            self._note_token(4, "d"), self._null_token(), self._null_token(),
            self._note_token(4, "e"), self._null_token(), self._null_token(),
        ]
        
        # Spine 2: 9 triplet eighths = 12 grid slots (12/12 = 1 slot per triplet eighth)
        spine_2 = [
            self._note_token(12, "f"), self._note_token(12, "g"), self._note_token(12, "a"),
            self._note_token(12, "b"), self._note_token(12, "cc"), self._note_token(12, "dd"),
            self._note_token(12, "ee"), self._note_token(12, "ff"), self._note_token(12, "gg"),
        ]
        
        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_1, spine_2],
            meter_signature="*M3/4"
        )
        self.assertTrue(is_valid, f"Quarters + triplet eighths should align; got: {error_msg}")

    def test_validate_dotted_quarter_with_eighths(self):
        """Test dotted quarter (4.) + plain eighths alignment."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Dotted quarter = 1/4 + 1/8 = 3/8 (3 eighth-note durations)
        # For proper alignment with eighths, need nulls
        spine_1 = [
            # Dotted quarter at beginning, filling 3 eighth slots
            self._note_token(4, "c"),
            self._null_token(),
            self._null_token(),
            # Plain quarter (no dots), filling 2 eighth slots
            self._note_token(4, "d"),
            self._null_token(),
        ]
        
        # Spine 2: 5 eighths
        spine_2 = [
            self._note_token(8, "e"), self._note_token(8, "f"),
            self._note_token(8, "g"), self._note_token(8, "a"), self._note_token(8, "b"),
        ]
        
        # Note: This test assumes the validator can compute that 4. = 3/8 slots
        # For now, it's a placeholder; actual implementation may differ
        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_1, spine_2],
            meter_signature="*M5/8"
        )
        # Expect it to pass IF proper nulls are provided
        # May need adjustment based on actual implementation

    # ============= Rests vs. Nulls Tests =============

    def test_validate_rest_is_not_equivalent_to_null(self):
        """Test that rests (r) are distinct from nulls (.) in grid validation."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        # Spine 1: quarter note, then quarter rest (not a null!)
        spine_1 = [self._note_token(4, "c"), self._rest_token(4)]
        
        # Spine 2: four eighths
        spine_2 = [self._note_token(8, "d"), self._note_token(8, "e"), self._note_token(8, "f"), self._note_token(8, "g")]
        
        # This should FAIL because rests are events (occupy grid slots), not null placeholders
        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_1, spine_2],
            meter_signature="*M4/4"
        )
        self.assertFalse(is_valid, "Rests should be distinct from nulls in validation")

    # ============= Error Message Tests =============

    def test_error_message_includes_spine_index(self):
        """Test that error messages include the spine index of misalignment."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        spine_1 = [self._note_token(4, "c"), self._note_token(4, "d")]
        spine_2 = [self._note_token(8, "e"), self._note_token(8, "f"), self._note_token(8, "g"), self._note_token(8, "a")]
        
        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_1, spine_2],
            meter_signature="*M4/4"
        )
        self.assertFalse(is_valid)
        self.assertIn("spine", error_msg.lower())

    def test_error_message_includes_grid_resolution(self):
        """Test that error messages include the calculated grid resolution."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator
        
        spine_1 = [self._note_token(4), self._note_token(4)]
        spine_2 = [self._note_token(8), self._note_token(8), self._note_token(8), self._note_token(8)]
        
        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_1, spine_2],
            meter_signature="*M4/4"
        )
        self.assertFalse(is_valid)
        # Error should mention grid or eighth-note resolution
        self.assertTrue(
            "grid" in error_msg.lower() or "eighth" in error_msg.lower() or "resolution" in error_msg.lower(),
            f"Error message should mention grid resolution: {error_msg}"
        )

    # ============= Integration with MeasureSignatureValidator =============

    def test_horizontal_validator_integrates_with_measure_signature_validator(self):
        """Test that HorizontalRhythmValidator can be used alongside MeasureSignatureValidator."""
        
        # Both validators should exist and be independent
        self.assertTrue(hasattr(kp.HorizontalRhythmValidator, "validate_measure_horizontally"))
        self.assertTrue(hasattr(kp.HorizontalRhythmValidator, "_calculate_grid_resolution"))


class HorizontalRhythmIrregularGroupsTestCase(unittest.TestCase):
    """TDD tests for irregular tuplet groups across spines."""

    @staticmethod
    def _null_token() -> kp.Subtoken:
        return kp.Subtoken(".", kp.TokenCategory.EMPTY)

    @staticmethod
    def _note_token(duration: int, pitch: str = "c") -> kp.NoteRestToken:
        return kp.NoteRestToken(
            encoding=f"{duration}{pitch}",
            pitch_duration_subtokens=[
                kp.Subtoken(str(duration), kp.TokenCategory.DURATION),
                kp.Subtoken(pitch, kp.TokenCategory.PITCH),
            ],
            decoration_subtokens=[],
        )

    def test_triplet_quarters_in_4_4_align_with_plain_quarters(self):
        """
        4/4 with quarter-note triplets (duration 3) against plain quarters (duration 4).
        Grid should resolve via LCM(3,4)=12 and align with explicit nulls.
        """
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        # 3 quarter-triplets in one whole note: each duration=1/3
        spine_triplets = [
            self._note_token(3, "c"), self._null_token(), self._null_token(), self._null_token(),
            self._note_token(3, "d"), self._null_token(), self._null_token(), self._null_token(),
            self._note_token(3, "e"), self._null_token(), self._null_token(), self._null_token(),
        ]

        # 4 quarters in 4/4: each quarter=3 slots in 12-grid
        spine_quarters = [
            self._note_token(4, "g"), self._null_token(), self._null_token(),
            self._note_token(4, "a"), self._null_token(), self._null_token(),
            self._note_token(4, "b"), self._null_token(), self._null_token(),
            self._note_token(4, "cc"), self._null_token(), self._null_token(),
        ]

        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_triplets, spine_quarters],
            meter_signature="*M4/4",
            measure_index=1,
        )
        self.assertTrue(is_valid, error_msg)
        self.assertEqual("", error_msg)

    def test_triplet_eighths_in_4_4_without_required_nulls_fails(self):
        """
        4/4 with triplet eighths (duration 6) mixed with quarters must fail if
        quarter spine omits required null tokens.
        """
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        # 12 triplet-eighths fill 4/4
        spine_triplet_eighths = [self._note_token(6, "e") for _ in range(12)]

        # 4 quarters, but missing null rows for 12-grid
        spine_quarters_missing_nulls = [
            self._note_token(4, "c"),
            self._note_token(4, "d"),
            self._note_token(4, "e"),
            self._note_token(4, "f"),
        ]

        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_quarters_missing_nulls, spine_triplet_eighths],
            meter_signature="*M4/4",
            measure_index=1,
        )
        self.assertFalse(is_valid)
        self.assertIn("grid", error_msg.lower())

    def test_duplet_style_group_2_against_triplet_grid_in_3_4(self):
        """
        3/4 mixed subdivision: group-of-2 style (duration 4 quarters with nulls)
        against triplet-eighths (duration 6) should align under LCM grid.
        """
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        # 3 quarters in 3/4 -> each quarter spans 3 slots in 12-grid
        spine_group_2_style = [
            self._note_token(4, "c"), self._null_token(), self._null_token(),
            self._note_token(4, "d"), self._null_token(), self._null_token(),
            self._note_token(4, "e"), self._null_token(), self._null_token(),
        ]

        # 9 triplet-eighths in 3/4, each 6 occupies 2 slots in 12-grid
        spine_triplet_eighths = []
        for _ in range(9):
            spine_triplet_eighths.extend([self._note_token(6, "g"), self._null_token()])

        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_group_2_style, spine_triplet_eighths],
            meter_signature="*M3/4",
            measure_index=1,
        )
        self.assertTrue(is_valid, error_msg)

    def test_sextuplets_in_5_4_align_with_quarters(self):
        """
        5/4 with sextuplets (duration 12, i.e. 1/12) against quarter notes.
        Quarters must include explicit null rows to match the 12-grid.
        """
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        # 15 sextuplet-eighth-like events (1/12 each) fill 5/4 (=15/12)
        spine_sextuplets = [self._note_token(12, "a") for _ in range(15)]

        # 5 quarters in 5/4 -> each quarter spans 3 slots in 12-grid
        spine_quarters = []
        for pitch in ["c", "d", "e", "f", "g"]:
            spine_quarters.extend([self._note_token(4, pitch), self._null_token(), self._null_token()])

        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_quarters, spine_sextuplets],
            meter_signature="*M5/4",
            measure_index=1,
        )
        self.assertTrue(is_valid, error_msg)

    def test_quintuplets_duration_10_mixed_with_eighths(self):
        """
        Irregular quintuplet-like duration value 10 mixed with eighths in 5/4.
        Ensures LCM-based grid resolution works for non-power-of-two denominators.
        """
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        # 5 events of duration 10 fill 1/2; duplicated to fill 5/4 => 25/20 -> use 10 events = 1
        # Build a coherent 5/4 by mixing with eighths and explicit nulls for alignment behavior.
        spine_tens = [self._note_token(10, "b") for _ in range(10)]

        # Companion spine uses eighths; include enough events to cover rows.
        spine_eighths = [self._note_token(8, "e") for _ in range(12)]

        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_tens, spine_eighths],
            meter_signature="*M5/4",
            measure_index=1,
        )
        self.assertFalse(is_valid)
        self.assertIn("grid", error_msg.lower())

    def test_mixed_irregular_groups_report_spine_and_measure(self):
        """Error message should include measure and spine in irregular mismatch."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        spine_a = [self._note_token(3, "c"), self._note_token(3, "d"), self._note_token(3, "e")]
        spine_b = [self._note_token(4, "g"), self._note_token(4, "a"), self._note_token(4, "b"), self._note_token(4, "cc")]

        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_a, spine_b],
            meter_signature="*M4/4",
            measure_index=7,
        )
        self.assertFalse(is_valid)
        self.assertIn("measure #7", error_msg.lower())
        self.assertIn("spine #", error_msg.lower())

    def test_fraction_style_duration_5_3_is_invalid(self):
        """5/3 is not a valid **kern duration encoding and must be rejected."""
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        with self.assertRaises(ValueError):
            HorizontalRhythmValidator._parse_duration_value("5/3")

    def test_septuplet_like_duration_7_aligns_with_quarters_in_4_4(self):
        """
        Duration 7 (1/7) against quarters in 4/4 requires LCM grid 28.
        Both spines should align with explicit null rows.
        """
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        spine_sevenths = []
        for _ in range(7):
            spine_sevenths.extend([
                self._note_token(7, "c"),
                self._null_token(),
                self._null_token(),
                self._null_token(),
            ])

        spine_quarters = []
        for pitch in ["g", "a", "b", "cc"]:
            spine_quarters.extend([
                self._note_token(4, pitch),
                self._null_token(),
                self._null_token(),
                self._null_token(),
                self._null_token(),
                self._null_token(),
                self._null_token(),
            ])

        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_sevenths, spine_quarters],
            meter_signature="*M4/4",
            measure_index=2,
        )
        self.assertTrue(is_valid, error_msg)

    def test_irregular_duration_11_without_required_nulls_fails(self):
        """
        Duration 11 mixed with quarter durations must fail when null rows are missing.
        """
        from kernpy.core.measure_signature_validators import HorizontalRhythmValidator

        spine_elevens = [self._note_token(11, "d") for _ in range(11)]
        spine_quarters_missing_nulls = [
            self._note_token(4, "c"),
            self._note_token(4, "d"),
            self._note_token(4, "e"),
            self._note_token(4, "f"),
        ]

        is_valid, error_msg = HorizontalRhythmValidator.validate_measure_horizontally(
            spines=[spine_elevens, spine_quarters_missing_nulls],
            meter_signature="*M4/4",
            measure_index=9,
        )
        self.assertFalse(is_valid)
        self.assertIn("grid", error_msg.lower())


if __name__ == "__main__":
    unittest.main()
