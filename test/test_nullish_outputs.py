import kernpy as kp

from pathlib import Path
import unittest


class TestNullishOutputs(unittest.TestCase):
    def test_lines_of_nullish_output_are_removed(self):
        doc, _err = kp.load(Path('resource_dir/nullish/nullish_0_input.krn'))
        with open(Path('resource_dir/nullish/nullish_0_expected_output.krn'), 'r') as f:
            expected_output = str(f.read())

        real_output = kp.dumps(doc)

        self.assertEqual(expected_output, real_output,
                         msg=f'Expected and real output differ:\nExpected:\n{expected_output}\n\nReal Output:\n{real_output}')


    def test_lines_of_signature_tokens_are_removed(self):
        doc, _err = kp.load(Path('resource_dir/nullish/nullish_0_input.krn'))
        with open(Path('resource_dir/nullish/nullish_2_expected_output.krn'), 'r') as f:
            expected_output = str(f.read())

        real_output = kp.dumps(doc, exclude=[kp.TokenCategory.SIGNATURES])

        self.assertEqual(expected_output, real_output,
                         msg=f'Expected and real output differ:\nExpected:\n{expected_output}\n\nReal Output:\n{real_output}')


    def test_lines_of_nullish_and_signature_tokens_are_removed_2(self):
        doc, _err = kp.load(Path('resource_dir/nullish/didone_60202.krn'))

        with open(Path('resource_dir/nullish/didone_60202_expected_output.krn'), 'r') as f:
            expected_output = f.read()

        real_output = kp.dumps(doc)

        self.assertEqual(expected_output, real_output,
                         msg=f'Expected and real output differ:\nExpected:\n{expected_output}\n\nReal Output:\n{real_output}')
