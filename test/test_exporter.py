import os
import unittest

import kernpy as kp


class ExporterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read the basic score document once before all tests
        cls.doc_organ_4_voices, _ = kp.read('resource_dir/legacy/chor048.krn')
        cls.doc_piano, _ = kp.read('resource_dir/mozart/concerto-piano-12-allegro.krn')

    def test_get_spine_types_1(self):
        spine_types = kp.get_spine_types(self.doc_organ_4_voices)
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
        options = kp.ExportOptions(
            spine_ids=[0]
        )

        with open('resource_dir/mozart/concerto-piano-12-allegro-left-hand.krn', 'r') as f:
            expected_content = f.read()
        real_content = kp.export(self.doc_piano, options)
        self.assertEqual(expected_content, real_content)

    def test_exporter_spine_id_right_hand(self):
        options = kp.ExportOptions(
            spine_ids=[1]
        )

        with open('resource_dir/mozart/concerto-piano-12-allegro-right-hand.krn', 'r') as f:
            expected_content = f.read()
        real_content = kp.export(self.doc_piano, options)
        self.assertEqual(expected_content, real_content)

    def test_exporter_spines_id_mix_kern_dyn_spines(self):
        options = kp.ExportOptions(
            spine_ids=[0, 2]
        )

        with open('resource_dir/mozart/concerto-piano-12-allegro-right-hand-and-dyn.krn', 'r') as f:
            expected_content = f.read()
        real_content = kp.export(self.doc_piano, options)  # TODO: Solve export error: error in line 15 of the exported file. No tiene nada que ver con la funcionalidad de exportar por spines. Sino con exportar todo en general.
        # kp.store(self.doc_piano, '/tmp/test_mix_spines_error.krn', options)  # for debug
        self.assertEqual(expected_content, real_content)

    def test_basic_kern_to_ekern(self):
        input_path = 'resource_dir/legacy/kern2ekern.krn'
        expected_path = 'resource_dir/legacy/kern2ekern.ekrn'

        with open(expected_path, 'r') as f:
            expected_content = f.read()

        doc, _ = kp.read(input_path)
        real_content = kp.export(doc, kp.ExportOptions(
            kern_type=kp.KernTypeExporter.eKern,
            token_categories=kp.BEKERN_CATEGORIES
        ))

        self.assertEqual(expected_content, real_content, f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}")
