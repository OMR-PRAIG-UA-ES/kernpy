import unittest
import os


def run_tests():
    """"
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

    # Por línea de comandos: python -m unittest -v test/test_humdrum_importer.py
    # Pero configurando el working directory a "test"


if __name__ == '__main__':
    run_tests()
