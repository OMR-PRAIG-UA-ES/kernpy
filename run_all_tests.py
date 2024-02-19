import unittest
import os


def run_tests():
    working_dir = "test"
    os.chdir(working_dir)
    loader = unittest.TestLoader()
    suite = loader.discover('.')
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)



    # Por línea de comandos: python -m unittest -v test/test_humdrum_importer.py
    # Pero configurando el working directory a "test"


if __name__ == '__main__':
    run_tests()
