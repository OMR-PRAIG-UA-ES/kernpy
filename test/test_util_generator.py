import os
import unittest
import tempfile

import kernpy as kp


class GenericTestCase(unittest.TestCase):

    def test_C1_create_fragments_from_kern_when_execution_sequential(self):
        # Arrange
        input_kern_file = 'resource_dir/fragments/input/sub/chor001.krn'
        expected_output_directory = 'resource_dir/fragments/output/chor001'
        real_output_directory = tempfile.mkdtemp(prefix='real_output_1')
        if real_output_directory.startswith('/'):
            real_output_directory = real_output_directory[1:]
        measure_length = 2
        offset = 1
        log_file = tempfile.mktemp()
        verbose = 1
        num_processes = None

        # Act
        kp.create_fragments_from_kern(
            input_kern_file=input_kern_file,
            output_directory=real_output_directory,
            measure_length=measure_length,
            offset=offset,
            log_file=log_file,
            verbose=verbose,
            num_processes=num_processes,
        )

        # Assert
        expected_files = [os.path.join(expected_output_directory, file) for file in
                          os.listdir(expected_output_directory)]
        real_files = [os.path.join(expected_output_directory, file) for file in
                      os.listdir(os.path.join(expected_output_directory))]
        expected_files.sort()
        real_files.sort()
        for expected_file, real_file in zip(expected_files, real_files):
            with open(real_file, 'r') as f1:
                real_content = f1.read()

            with open(expected_file, 'r') as f2:
                expected_content = f2.read()

            message = f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}"
            self.assertEqual(expected_content, real_content, message)

    def test_C2_create_fragments_from_kern_when_execution_parallel(self):
        # Arrange
        input_kern_file = 'resource_dir/fragments/input/sub/chor001.krn'
        expected_output_directory = 'resource_dir/fragments/output/chor001'
        real_output_directory = tempfile.mkdtemp(prefix='real_output_1')
        if real_output_directory.startswith('/'):
            real_output_directory = real_output_directory[1:]
        measure_length = 2
        offset = 1
        log_file = tempfile.mktemp(prefix='log')
        verbose = 1
        num_processes = 4

        # Act
        kp.create_fragments_from_kern(
            input_kern_file=input_kern_file,
            output_directory=real_output_directory,
            measure_length=measure_length,
            offset=offset,
            log_file=log_file,
            verbose=verbose,
            num_processes=num_processes,
        )

        # Assert
        expected_files = [os.path.join(expected_output_directory, file) for file in
                          os.listdir(expected_output_directory)]
        real_files = [os.path.join(expected_output_directory, file) for file in
                      os.listdir(os.path.join(expected_output_directory))]
        expected_files.sort()
        real_files.sort()
        for expected_file, real_file in zip(expected_files, real_files):
            with open(real_file, 'r') as f1:
                real_content = f1.read()

            with open(expected_file, 'r') as f2:
                expected_content = f2.read()

            message = f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}"
            self.assertEqual(expected_content, real_content, message)

    def test_C1_create_fragments_from_directory_when_execution_sequential(self):
        # Arrange
        input_directory = 'resource_dir/fragments/'
        expected_output_directory = 'resource_dir/fragments/output'
        real_output_directory = tempfile.mkdtemp(prefix='real_output_2')
        log_file = tempfile.mktemp(prefix='log')
        check_file_extension = True
        offset = 1
        verbose = 0
        num_processes = None
        mean = 4
        std_dev = 0

        # Act
        kp.create_fragments_from_directory(
            input_directory=input_directory,
            output_directory=real_output_directory,
            log_file=log_file,
            check_file_extension=check_file_extension,
            offset=offset,
            verbose=verbose,
            num_processes=num_processes,
            mean=mean,
            std_dev=std_dev
        )

        # Assert
        expected_files = [os.path.join(expected_output_directory, file) for file in os.listdir(input_directory)]
        real_files = [os.path.join(real_output_directory, file) for file in os.listdir(real_output_directory)]
        expected_files.sort()
        real_files.sort()
        for expected_file, real_file in zip(expected_files, real_files):
            with open(real_file, 'r') as f1:
                real_content = f1.read()

            with open(expected_file, 'r') as f2:
                expected_content = f2.read()

            message = f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}"
            self.assertEqual(expected_content, real_content, message)

    def test_C2_create_fragments_from_directory_when_execution_parallel(self):
        # Arrange
        input_directory = 'resource_dir/fragments/'
        expected_output_directory = 'resource_dir/fragments/output'
        real_output_directory = tempfile.mkdtemp(prefix='real_output_2')
        log_file = tempfile.mktemp(prefix='log')
        check_file_extension = True
        offset = 1
        verbose = 0
        num_processes = 4
        mean = 4
        std_dev = 0

        # Act
        kp.create_fragments_from_directory(
            input_directory=input_directory,
            output_directory=real_output_directory,
            log_file=log_file,
            check_file_extension=check_file_extension,
            offset=offset,
            verbose=verbose,
            num_processes=num_processes,
            mean=mean,
            std_dev=std_dev
        )

        # Assert
        expected_files = [os.path.join(expected_output_directory, file) for file in os.listdir(input_directory)]
        real_files = [os.path.join(real_output_directory, file) for file in os.listdir(real_output_directory)]
        expected_files.sort()
        real_files.sort()
        for expected_file, real_file in zip(expected_files, real_files):
            with open(real_file, 'r') as f1:
                real_content = f1.read()

            with open(expected_file, 'r') as f2:
                expected_content = f2.read()

            message = f"File content mismatch: \nExpected:\n{expected_content}\n{40 * '='}\nReal\n{real_content}"
            self.assertEqual(expected_content, real_content, message)

