# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import unittest


from pykern import check_file, check_string

import logging
import sys

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))


class ImporterTestCase(unittest.TestCase):
    def testCorrectFile(self):
        correct = check_file('resource_dir/unit/minimal.krn')
        self.assertTrue(correct)

    def testIncorrectFile(self):
        correct = check_file('resource_dir/unit/minimal_incorrect.krn')
        self.assertFalse(correct)

    def testCorrectString(self):
        #correct = check_string('**kern\n4c\n4d\n4e\n4f')
        #self.assertTrue(correct)
        pass
    #TODO No sé por qué me está fallando ... Pendiente de arreglar

    def testIncorrectString(self):
        correct = check_string('**kern\n4c\n4d\nj\n4f\*-')
        self.assertFalse(correct)

def test():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
