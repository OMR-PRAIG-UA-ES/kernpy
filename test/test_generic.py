import os
import unittest
import logging
import sys

import kernpy

class GenericTestCase(unittest.TestCase):
    def test_read_export_easy(self):
        # Arrange
        expected_ekrn = 'resource_dir/legacy/base_tuplet.ekrn'
        current_krn = 'resource_dir/legacy/base_tuplet.krn'
        with open(expected_ekrn, 'r') as f:
            expected_content = f.read()

        # Act
        doc = kernpy.read(current_krn)
        options = kernpy.ExportOptions(kern_type=kernpy.KernTypeExporter.eKern)
        real_content = kernpy.export(doc, options)

        # Assert
        self.assertEqual(expected_content, real_content, f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}")


    def test_test(self):
        doc = kernpy.read('resource_dir/legacy/chor048.krn')
        print(doc)
        for i in range (doc.get_first_measure(), doc.measures_count() + 1):
            options = kernpy.ExportOptions(from_measure=i, to_measure=i)
            content = kernpy.export(doc, options)
            print(content)

        for i in range(10):
            print(i)
