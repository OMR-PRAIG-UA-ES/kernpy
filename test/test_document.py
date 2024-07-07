import os
import unittest
import logging
import sys
from tempfile import TemporaryDirectory

import kernpy
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
        doc, _ = kernpy.read('resource_dir/legacy/chor048.krn')

        voices = doc.get_voices()
        self.assertEqual(['!sax', '!piano', '!bass'], voices)

        voices = doc.get_voices(clean=True)
        self.assertEqual(['sax', 'piano', 'bass'], voices)

