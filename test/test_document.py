import os
import unittest
import logging
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import json

import kernpy as kp


class DocumentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read the basic score document once before all tests
        cls.doc_organ_4_voices, _ = kp.read('resource_dir/legacy/chor048.krn')
        cls.doc_piano, _ = kp.read('resource_dir/mozart/concerto-piano-12-allegro.krn')

    def all_tokens_have_the_correct_category(self, doc: kp.Document, category: kp.TokenCategory):
        tokens = doc.get_all_tokens(filter_by_categories=[category])
        for token in tokens:
            self.assertEqual(category, token.category)

    @unittest.skip
    def test_document_self_concat(self):
        # Arrange
        doc_a, _ = kp.read('resource_dir/legacy/base_tuplet.krn')
        doc_b, _ = kp.read('resource_dir/legacy/base_tuplet_longer.krn')

        doc_concat = kp.Document.to_concat(doc_a, doc_b)
        kp.store_graph(doc_concat, '/tmp/graph_concat.dot')
        kp.store_graph(doc_a, '/tmp/graph_a.dot')
        kp.store_graph(doc_b, '/tmp/graph_b.dot')

        # compare
        ...

    @unittest.skip("TODO: Not implemented yet")
    def test_document_append_spines(self):
        doc, _ = kp.read('resource_dir/legacy/base_tuplet.krn')
        doc.append_spines(spines=['4e\t4f\t4g\t4a\n4b\t4c\t4d\t4e\n*_\t*_\t*_\t*_\n'])

        pass

    @unittest.skip("TODO: Not implemented yet")
    def test_document_get_voices(self):
        doc, _ = kp.read('resource_dir/legacy/chor048.krn')

        voices = doc.get_voices()
        self.assertEqual(['!sax', '!piano', '!bass'], voices)

        voices = doc.get_voices(clean=True)
        self.assertEqual(['sax', 'piano', 'bass'], voices)

    def test_document_get_header_nodes(self):
        input_kern_file = 'resource_dir/mozart/divertimento-quartet.krn'
        doc, err = kp.read(input_kern_file)
        headers_nodes = doc.get_header_nodes()

        self.assertEqual(8, len(headers_nodes))
        for node in headers_nodes:
            self.assertIsInstance(node, kp.core.HeaderToken)
        self.assertListEqual(
            ['**kern', '**dynam', '**kern', '**dynam', '**kern', '**dynam', '**kern', '**dynam'],
            [t.encoding for t in headers_nodes])

    def test_document_get_all_spines_ids(self):
        input_kern_file = 'resource_dir/mozart/divertimento-quartet.krn'

        doc, err = kp.read(input_kern_file)
        spines_ids = doc.get_spine_ids()
        self.assertListEqual(
            [0, 1, 2, 3, 4, 5, 6, 7],
            spines_ids)

    def test_document_maximum_recursion_depth_exceeded_in_tree_traversal_dfs(self):
        doc, err = kp.read('resource_dir/samples/score_with_dividing_two_spines.krn')
        tokens = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.CORE])

        # optimize this dfs implementation for not exceeding maximum recursion depth
        # use memoization to speed up the process
        # use queues
        self.assertTrue(len(tokens) > 0)

    def test_frequencies(self):
        with open('resource_dir/metadata/frequency.json', 'r') as f:
            expected_frequencies = json.load(f)

        doc, err = kp.read('resource_dir/legacy/chor001.krn')
        real_frequencies = doc.frequencies()

        self.assertDictEqual(expected_frequencies, real_frequencies)

    def test_document_split(self):
        doc, err = kp.read('resource_dir/legacy/chor001.krn')
        docs = doc.split()

        for i, new_doc in enumerate(docs):
            kp.store_graph(new_doc, f'/tmp/test_{i}.dot')
            kp.store(new_doc, f'/tmp/test_{i}.krn', kp.ExportOptions())
        self.assertEqual(4, len(docs))

    def test_has_categories_when_export(self):
        data: dict = self.doc_piano.frequencies({t for t in kp.TokenCategory} - {kp.TokenCategory.BARLINES})
        for k, v in data.items():
            print(f"{k}: {v}")

    def test_should_not_detect_barlines_tokens_with_non_barlines_category_0(self):
        frequencies = self.doc_organ_4_voices.frequencies()
        self.assertEqual(kp.TokenCategory.BARLINES.name, frequencies['=']['category'])

    def test_should_not_detect_barlines_tokens_with_non_barlines_category_1(self):
        frequencies = self.doc_organ_4_voices.frequencies()
        with self.assertRaises(KeyError):
            self.assertEqual(kp.TokenCategory.BARLINES.name, frequencies['=1-']['category'])
            self.assertEqual(kp.TokenCategory.BARLINES.name, frequencies['=2']['category'])
            self.assertEqual(kp.TokenCategory.BARLINES.name, frequencies['=3']['category'])
            self.assertEqual(kp.TokenCategory.BARLINES.name, frequencies['=4']['category'])
            ...

    def test_should_not_detect_barlines_tokens_with_non_barlines_category_2(self):
        frequencies = self.doc_organ_4_voices.frequencies()
        self.assertEqual(kp.TokenCategory.BARLINES.name, frequencies['====']['category'])

    def test_should_not_detect_barlines_tokens_with_non_barlines_category_3(self):
        frequencies = self.doc_piano.frequencies()
        self.assertEqual(kp.TokenCategory.BARLINES.name, frequencies['==:|!']['category'])

    def test_should_not_detect_barlines_tokens_with_non_barlines_category_4(self):
        frequencies = self.doc_piano.frequencies()
        with self.assertRaises(KeyError):
            self.assertEqual(kp.TokenCategory.BARLINES.name, frequencies['=94:|!|:']['category'])

    def test_all_tokens_have_correct_category_get_all_tokens_core(self):
        self.all_tokens_have_the_correct_category(self.doc_organ_4_voices, kp.TokenCategory.CORE)

    def test_all_tokens_have_correct_category_get_all_tokens_barlines(self):
        self.all_tokens_have_the_correct_category(self.doc_organ_4_voices, kp.TokenCategory.BARLINES)

    def test_all_tokens_have_correct_category_get_all_tokens_dynamics(self):
        self.all_tokens_have_the_correct_category(self.doc_organ_4_voices, kp.TokenCategory.DYNAMICS)

    def test_all_tokens_have_correct_category_get_all_tokens_signatures(self):
        self.all_tokens_have_the_correct_category(self.doc_organ_4_voices, kp.TokenCategory.SIGNATURES)

    def test_all_tokens_have_correct_category_get_all_tokens_fingering(self):
        self.all_tokens_have_the_correct_category(self.doc_organ_4_voices, kp.TokenCategory.FINGERING)

    def test_all_tokens_have_correct_category_get_all_tokens_lyrics(self):
        self.all_tokens_have_the_correct_category(self.doc_organ_4_voices, kp.TokenCategory.LYRICS)

    def test_all_tokens_have_correct_category_get_all_tokens_lines_comments(self):
        self.all_tokens_have_the_correct_category(self.doc_organ_4_voices, kp.TokenCategory.LINE_COMMENTS)

    def test_all_tokens_have_correct_category_get_all_tokens_field_comments(self):
        self.all_tokens_have_the_correct_category(self.doc_organ_4_voices, kp.TokenCategory.FIELD_COMMENTS)

    def test_match_same_document_reference(self):
        self.assertTrue(self.doc_organ_4_voices.match(self.doc_organ_4_voices, self.doc_organ_4_voices))

    def test_match_different_document_reference(self):
        self.assertFalse(self.doc_organ_4_voices.match(self.doc_organ_4_voices, self.doc_piano))

    def test_match_different_references_same_content(self):
        doc_1, _ = kp.loads('**kern\n=1\n=2\n=3\n=4\n*-\n')
        doc_2, _ = kp.loads('**kern\n=1\n=2\n=3\n=4\n*-\n')

        self.assertTrue(kp.Document.match(doc_1, doc_2))

    def test_match_different_references_different_content(self):
        doc_1, _ = kp.loads('**kern\n=1\n=2\n=3\n=4\n*-\n')
        doc_2, _ = kp.loads('**kern\t**kern\n=1\t=1\n=2\t=2\n=3\t=3\n=4\t=4\n*-\t*-\n')

        self.assertFalse(kp.Document.match(doc_1, doc_2))

    def test_match_same_kern_different_others_default_option(self):
        doc_1, _ = kp.loads('**kern\n=1\n=2\n=3\n=4\n*-\n')
        doc_2, _ = kp.loads('**kern\t**dynam\n=1\tpp\n=2\tpp\n=3\tpp\n=4\tpp\n*-\t*-\n')

        self.assertFalse(kp.Document.match(doc_1, doc_2))

    def test_match_same_kern_different_others_default_only_core(self):
        doc_1, _ = kp.loads('**kern\n=1\n=2\n=3\n=4\n*-\n')
        doc_2, _ = kp.loads('**kern\t**dynam\n=1\tpp\n=2\tpp\n=3\tpp\n=4\tpp\n*-\t*-\n')

        self.assertFalse(kp.Document.match(doc_1, doc_2, check_core_spines_only=False))

    def test_match_same_kern_different_others_default_check_all_core(self):
        doc_1, _ = kp.loads('**kern\n=1\n=2\n=3\n=4\n*-\n')
        doc_2, _ = kp.loads('**kern\t**dynam\n=1\tpp\n=2\tpp\n=3\tpp\n=4\tpp\n*-\t*-\n')

        self.assertTrue(kp.Document.match(doc_1, doc_2, check_core_spines_only=True))

    def test_add_document(self):
        doc_1, _ = kp.loads('**kern\n=1\n=2\n=3\n=4\n*-\n')
        doc_2, _ = kp.loads('**kern\n=5\n=6\n=7\n=8\n*-\n')

        expected_result = '**kern\n=\n=\n=\n=\n=\n=\n=\n=\n*-\n'

        doc_1.add(doc_2)
        real_result = kp.dumps(doc_1)
        self.assertEqual(expected_result, real_result)

    def test_document_to_transposed_easy(self):
        doc, err = kp.load('resource_dir/legacy/base_tuplet_longer.krn')
        with open(Path('resource_dir/legacy/base_tuplet_longer_plus_octave.krn')) as f:
            expected_content = f.read()

        doc_transposed = doc.to_transposed('octave', 'up')

        real_content = kp.dumps(doc_transposed)

        self.assertEqual(expected_content, real_content)


