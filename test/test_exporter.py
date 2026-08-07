import os
import unittest

import kernpy as kp


class ExporterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read the basic score document once before all tests
        cls.doc_organ_4_voices, _ = kp.read('test/resources/legacy/chor048.krn')
        cls.doc_piano, _ = kp.read('test/resources/mozart/concerto-piano-12-allegro.krn')

    def _run_HeaderTokenGenerator_new_generalized(self, input_token, export_type, expected):
        """Private helper method to run individual test cases."""
        token = kp.HeaderToken(input_token, 0)
        result = kp.HeaderTokenGenerator.new(token=token, type=export_type).encoding
        self.assertEqual(
            result, expected,
            f"Failed for input: {input_token}, export_type: {export_type}, expected: {expected}, got: {result}"
        )

    def exported_filtering_by_category(self, doc, include, exclude, expected_path):
        # Arrange
        with open(expected_path, 'r') as f:
            expected_content = f.read()

        # Act
        real_content = kp.dumps(doc, include=include, exclude=exclude)

        # Assert
        self.assertEqual(expected_content, real_content)


    def test_get_spine_types_1(self):
        spine_types = kp.spine_types(self.doc_organ_4_voices)
        self.assertEqual(['**kern', '**kern', '**kern', '**kern', '**root', '**harm'], spine_types)

    def test_get_spine_types_2(self):
        spine_types = kp.get_spine_types(self.doc_organ_4_voices, spine_types=None)
        self.assertEqual(['**kern', '**kern', '**kern', '**kern', '**root', '**harm'], spine_types)

    def test_get_spine_types_3(self):
        spine_types = kp.get_spine_types(self.doc_organ_4_voices, spine_types=['**kern'])
        self.assertEqual(['**kern', '**kern', '**kern', '**kern'], spine_types)

    def test_get_spine_types_4(self):
        spine_types = kp.get_spine_types(self.doc_organ_4_voices, spine_types=['**root'])
        self.assertEqual(['**root'], spine_types)

    def test_get_spine_types_5(self):
        spine_types = kp.get_spine_types(self.doc_organ_4_voices, spine_types=['**harm'])
        self.assertEqual(['**harm'], spine_types)

    def test_get_spine_types_6(self):
        spine_types = kp.get_spine_types(self.doc_organ_4_voices, spine_types=['**not-exists'])
        self.assertEqual([], spine_types)

    def test_get_spine_types_7(self):
        spine_types = kp.get_spine_types(self.doc_organ_4_voices, spine_types=[])
        self.assertEqual([], spine_types)

    def test_exporter_spine_id_left_hand(self):
        with open('test/resources/mozart/concerto-piano-12-allegro-left-hand.krn', 'r') as f:
            expected_content = f.read()
        real_content = kp.dumps(self.doc_piano, spine_ids=[0])
        print(f"Real content:\n{real_content}\nExpected content:\n{expected_content}")
        self.assertEqual(expected_content, real_content)

    def test_exporter_spine_id_right_hand(self):
        with open('test/resources/mozart/concerto-piano-12-allegro-right-hand.krn', 'r') as f:
            expected_content = f.read()
        real_content = kp.dumps(self.doc_piano, spine_ids=[1])
        self.assertEqual(expected_content, real_content)

    def test_exporter_spines_id_mix_kern_dyn_spines(self):
        with open('test/resources/mozart/concerto-piano-12-allegro-right-hand-and-dyn.krn', 'r') as f:
            expected_content = f.read()
        real_content = kp.dumps(self.doc_piano,
                                 spine_ids=[0, 2])  # TODO: Solve export error: error in line 15 of the exported file. No tiene nada que ver con la funcionalidad de exportar por spines. Sino con exportar todo en general.
        self.assertEqual(expected_content, real_content)

    def test_basic_kern_to_ekern(self):
        input_path = 'test/resources/legacy/kern2ekern.krn'
        expected_path = 'test/resources/legacy/kern2ekern.ekrn'

        with open(expected_path, 'r') as f:
            expected_content = f.read()

        doc, _ = kp.load(input_path)
        real_content = kp.dumps(doc, encoding=kp.Encoding.eKern, include=kp.BEKERN_CATEGORIES)

        self.assertEqual(expected_content, real_content,
                         f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}")

    def test_check_categories_are_exported(self):
        data = self.doc_organ_4_voices.frequencies([kp.TokenCategory.CORE])
        for k, v in data.items():
            print(f"{k}: {v}")

    def test_should_export_with_all(self):
        self.exported_filtering_by_category(
            doc=self.doc_piano,
            include={t for t in kp.TokenCategory},
            exclude=None,
            expected_path='test/resources/categories/concerto-piano-12-allegro_with_all.krn'
        )

    def test_should_export_without_barlines(self):
        self.exported_filtering_by_category(
            doc=self.doc_piano,
            include={t for t in kp.TokenCategory},
            exclude={kp.TokenCategory.BARLINES},
            expected_path='test/resources/categories/concerto-piano-12-allegro_without_barlines.krn'
        )

    def test_should_export_without_only_signatures(self):
        self.exported_filtering_by_category(
            doc=self.doc_piano,
            include={kp.TokenCategory.SIGNATURES},
            exclude=None,
            expected_path='test/resources/categories/concerto-piano-12-allegro_without_only_signatures.krn'
        )

    def test_should_export_without_harmony(self):
        self.exported_filtering_by_category(
            doc=self.doc_organ_4_voices,
            include={t for t in kp.TokenCategory},
            exclude={kp.TokenCategory.HARMONY},
            expected_path='test/resources/categories/concerto-piano-12-allegro_without_harmony.krn'
        )

    def test_only_export_kern_and_harm_spines(self):
        with open('test/resources/spines/concerto-piano-12-allegro_only_kern_and_harm.krn', 'r') as f:
            expected_content = f.read()

        real_content = kp.dumps(self.doc_organ_4_voices, spine_types=['**kern', '**harm'])

        self.assertEqual(expected_content, real_content,
                         f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}")

    def test_exporter_HeaderTokenGenerator_new(self):
        self._run_HeaderTokenGenerator_new_generalized("**kern", kp.Encoding.eKern, "**ekern")
        self._run_HeaderTokenGenerator_new_generalized("**kern", kp.Encoding.normalizedKern, "**kern")
        self._run_HeaderTokenGenerator_new_generalized("**kern", kp.Encoding.bKern, "**bkern")
        self._run_HeaderTokenGenerator_new_generalized("**kern", kp.Encoding.bEkern, "**bekern")






class CrossHeaderSpineMergeTestCase(unittest.TestCase):
    """Regression test: joining adjacent spines that descend from DIFFERENT
    same-type headers (e.g. a spine split from the 1st **kern merged with a
    spine split from the 2nd **kern) is legal Humdrum ("only spines of the
    same data type may be joined" — there is no same-header requirement).

    The importer used to refuse the collapse (it compared header-node IDENTITY
    instead of exclusive TYPE), which left the internal parent list one wider
    than the real column count. From the next row onward every column attached
    to the wrong parent chain, so spine-type-filtered exports kept the **dynam
    column (as '*', '.', '*-' cells) from the second consecutive merge row to
    the end of the file. Real-world case: KernScores Mozart sonata05-2.krn.
    """

    INPUT = (
        "**kern\t**kern\t**dynam\n"
        "*^\t*\t*\n"                 # -> [kern, kern, kern, dynam]
        "*\t*\t*^\t*\n"              # -> [kern, kern, kern, kern, dynam]
        "4c\t4d\t4e\t4f\tp\n"
        "*\t*v\t*v\t*\t*\n"          # merge cols 2,3 (cross-header) -> 4 spines
        "*v\t*v\t*\t*\n"             # merge cols 1,2 -> 3 spines
        "4g\t4a\t.\n"
        "*-\t*-\t*-\n"
    )

    def test_kern_only_export_drops_dynam_after_consecutive_cross_header_merges(self):
        doc, _ = kp.loads(self.INPUT)
        exported = kp.dumps(doc, spine_types=['**kern'])
        expected = (
            "**kern\t**kern\n"
            "*^\t*\n"
            "*\t*\t*^\n"
            "4c\t4d\t4e\t4f\n"
            "*\t*v\t*v\t*\n"
            "*v\t*v\t*\n"
            "4g\t4a\n"
            "*-\t*-\n"
        )
        self.assertEqual(expected, exported)

    def test_full_export_row_widths_follow_spine_arithmetic(self):
        doc, _ = kp.loads(self.INPUT)
        exported = kp.dumps(doc, spine_types=['**kern'])
        width = None
        for lineno, line in enumerate(exported.splitlines(), start=1):
            cells = line.split('\t')
            if width is None:
                self.assertTrue(all(c.startswith('**') for c in cells),
                                f"line {lineno}: expected header row, got {line!r}")
                width = len(cells)
                continue
            self.assertEqual(width, len(cells),
                             f"line {lineno}: {len(cells)} cells where spine "
                             f"arithmetic requires {width}: {line!r}")
            delta, merge_run = 0, 0
            for c in cells:
                if c == '*^':
                    delta += 1
                    merge_run = 0
                elif c == '*v':
                    if merge_run >= 1:
                        delta -= 1
                    merge_run += 1
                else:
                    merge_run = 0
            width += delta
