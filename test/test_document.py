import os
import unittest
import logging
import sys
from tempfile import TemporaryDirectory
import json

import kernpy as kp


class DocumentTestCase(unittest.TestCase):
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
        real_frequencies = doc.frequencies(token_categories=None)

        self.assertEqual(expected_frequencies, real_frequencies)



