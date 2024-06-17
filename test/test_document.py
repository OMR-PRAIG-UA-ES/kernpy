import os
import unittest
import logging
import sys
from tempfile import TemporaryDirectory

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

