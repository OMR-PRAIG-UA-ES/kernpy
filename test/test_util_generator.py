import os
import unittest

import kernpy


class GenericTestCase(unittest.TestCase):

    @unittest.skip
    def C1_create_fragments_from_kern_when_input_kern_file_is_valid_and_execution_sequential(self):
        # Arrange
        input_kern_file = 'path/to/file.krn'
        output_directory = 'path/to/output'
        measure_length = 1
        offset = 1
        log_file = 'path/to/log'
        verbose = 1
        num_processes = None

        # Act
        kernpy.create_fragments_from_kern(
            input_kern_file=input_kern_file,
            output_directory=output_directory,
            measure_length=measure_length,
            offset=offset,
            log_file=log_file,
            verbose=verbose,
            num_processes=num_processes
        )
        # Assert
        self.assertTrue(True)

    @unittest.skip
    def C2_create_fragments_from_kern_when_input_kern_file_is_invalid_and_execution_parallel(self):
        # Arrange
        input_kern_file = 'resource_dir/to/file.krn'
        output_directory = 'resource_dir/path/to/output'
        measure_length = 1
        offset = 1
        log_file = 'path/to/log'
        verbose = 1
        num_processes = 1

        # Act
        kernpy.create_fragments_from_kern(
            input_kern_file=input_kern_file,
            output_directory=output_directory,
            measure_length=measure_length,
            offset=offset,
            log_file=log_file,
            verbose=verbose,
            num_processes=num_processes
        )
        # Assert
        self.assertTrue(True)

    @unittest.skip
    def C3_create_fragments_from_kern_when_easy_input_kern_file(self):
        # Arrange
        input_kern_file = 'resource_dir/to/file.krn'
        output_directory = 'resource_dir/path/to/output'
        measure_length = 1
        offset = 1
        log_file = 'path/to/log'
        verbose = 1
        num_processes = 1

        # Act
        kernpy.create_fragments_from_kern(
            input_kern_file=input_kern_file,
            output_directory=output_directory,
            measure_length=measure_length,
            offset=offset,
            log_file=log_file,
            verbose=verbose,
            num_processes=num_processes
        )
        # Assert
        self.assertTrue(True)

    @unittest.skip
    def C1_create_fragments_from_directory_when_input_directory_is_valid_and_execution_sequential(self):
        # Arrange
        input_directory = 'path/to/dir'
        output_directory = 'path/to/output'
        log_file = 'path/to/log'
        check_file_extension = True
        offset = 4
        verbose = 0
        num_processes = None
        mean = 4
        std_dev = 0

        # Act
        kernpy.create_fragments_from_directory(
            input_directory=input_directory,
            output_directory=output_directory,
            log_file=log_file,
            check_file_extension=check_file_extension,
            offset=offset,
            verbose=verbose,
            num_processes=num_processes,
            mean=mean,
            std_dev=std_dev
        )
        # Assert
        self.assertTrue(True)

    @unittest.skip
    def C2_create_fragments_from_directory_when_input_directory_is_invalid_and_execution_parallel(self):
        # Arrange
        input_directory = 'resource_dir/to/dir'
        output_directory = 'resource_dir/path/to/output'
        log_file = 'path/to/log'
        check_file_extension = True
        offset = 1
        verbose = 1
        num_processes = 1
        mean = 4
        std_dev = 1

        # Act
        kernpy.create_fragments_from_directory(
            input_directory=input_directory,
            output_directory=output_directory,
            log_file=log_file,
            check_file_extension=check_file_extension,
            offset=offset,
            verbose=verbose,
            num_processes=num_processes,
            mean=mean,
            std_dev=std_dev
        )
        # Assert
        self.assertTrue(True)



