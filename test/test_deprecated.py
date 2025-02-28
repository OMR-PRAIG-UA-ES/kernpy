import kernpy as kp

from pathlib import Path
import unittest


class TestDeprecated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.basic, _ = kp.loads('**kern\n2e\n4f\n*-')

    def test_deprecated_get_spine_types(self):
        with self.assertWarns(DeprecationWarning):
            kp.get_spine_types(self.basic)

    def test_deprecated_store_graph(self):
        with self.assertWarns(DeprecationWarning):
            kp.store_graph(self.basic, Path('/tmp/a'))

    def test_deprecated_store(self):
        with self.assertWarns(DeprecationWarning):
            kp.store(self.basic, Path('/tmp/a'), options=kp.ExportOptions())

    def test_deprecated_export(self):
        with self.assertWarns(DeprecationWarning):
            kp.export(self.basic, options=kp.ExportOptions())

    def test_deprecated_read(self):
        with self.assertWarns(DeprecationWarning):
            kp.read('resource_dir/legacy/chor001.krn')

    def test_deprecated_create(self):
        with self.assertWarns(DeprecationWarning):
            kp.create('**kern\n2e\n4f\n*-')

    #def test_deprecated_argument(self):
    #    with self.assertWarns(DeprecationWarning):
    #        example_function(new_param=10, old_param=5)

    #def test_deprecated_class(self):
    #    with self.assertWarns(DeprecationWarning):
    #        instance = OldClass()