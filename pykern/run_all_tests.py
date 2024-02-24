import unittest
import os


def run_tests():
    """
    Run all tests in the test directory.

    !IMPORTANT: Run this script from the root directory of the project:
    ```bash
    make tests
    ```
    or

    ```bash
    python pykern/run_all_tests.py
    ```

    """
    working_dir = "./pykern/test"
    os.chdir(working_dir)
    loader = unittest.TestLoader()
    suite = loader.discover('.')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    # In command line: python -m unittest -v test/test_humdrum_importer.py
    # In IDEs, configure working directory to "test"


if __name__ == '__main__':
    run_tests()
