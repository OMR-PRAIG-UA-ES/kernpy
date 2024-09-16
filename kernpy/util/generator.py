import os
import random
import multiprocessing
import sys
from typing import Optional, List
from abc import ABC, abstractmethod

from tqdm import tqdm

from kernpy.core.exporter import ExportOptions, BEKERN_CATEGORIES, Exporter, KernTypeExporter
from kernpy.core.importer import Importer
from .. import read, store
from ..core._io import find_all_files

DEFAULT_MEAN = 4.0
DEFAULT_STD_DEV = 0.0


def create_fragments_from_kern(
        input_kern_file: str,
        output_directory: str,
        measure_length: int,
        offset: int,
        log_file: str,
        verbose: int = 1,
        num_processes: int = None,
        export_options: Optional[ExportOptions] = None,
) -> None:
    """
    Create a bunch of little kern files from a single kern file.

    Args:
        log_file: The log file to store the results
        input_kern_file (object): The input kern file
        output_directory: The output directory where the fragments will be stored
        measure_length: The number of measures of the fragments
        offset: The number of measures between fragments.\
            If offset is 1, and measure_length is 4, the fragments will be: 1-4, 2-5, 3-6, 4-7, ...
            If the offset is 2, and measure_length is 4, the fragments will be: 1-4, 3-6, 5-8, 7-10, ...
            If the offset is 4, and measure_length is 4, the fragments will be: 1-4, 5-8, 9-12, 13-16, ...
        verbose: The verbosity level
        num_processes: The number of processes to use for parallel processing.\
            If None, or num_processes <= 1, the processing will be done in a single process.
        export_options(Optional[ExportOptions]): The export options
    Returns:
        None

    Examples:
        # Basic execution
        >>> create_fragments_from_kern('input.krn', 'output_directory', measure_length=4)

        # Parallel processing
        >>> create_fragments_from_kern('input.krn', 'output_directory', measure_length=4, offset=4, log_file='log.txt', verbose=1, num_processes=8)
        >>> create_fragments_from_kern('input.krn', 'output_directory', measure_length=4, offset=4, log_file='log.txt', verbose=1, num_processes=8)

        # Single process
        >>> create_fragments_from_kern('input.krn', 'output_directory', measure_length=4, offset=4, log_file='log.txt', verbose=1)
        >>> create_fragments_from_kern('input.krn', 'output_directory', measure_length=4, offset=4, log_file='log.txt', verbose=1, num_processes=None)


    """
    fg = FragmentGenerator(
        offset=offset,
        verbose=verbose,
        num_processes=num_processes,
        log_file=log_file,
        export_options=export_options, )
    fg.create_fragments_from_file(
        input_kern_file=input_kern_file,
        output_directory=output_directory,
        measure_length=measure_length)


def create_fragments_from_directory(
        input_directory: str, output_directory: str,
        log_file: str,
        check_file_extension: bool = True,
        offset: int = 0,
        verbose: int = 1,
        num_processes: int = None,
        mean: float = DEFAULT_MEAN,
        std_dev: float = DEFAULT_STD_DEV,
        export_options: Optional[ExportOptions] = None
) -> None:
    """
    Create a bunch of little kern files from a directory of kern files.

    Args:
        export_options (Optional[ExportOptions]): The export options
        log_file: The log file to store the results
        input_directory: The input directory with the kern files
        output_directory: The output directory where the fragments will be stored
        check_file_extension: If True, only files with the extension '.krn' will be processed.\
         If False, all files will be processed, it could be more time-consuming.
        offset: The number of measures between fragments.\
            If offset is 1, and measure_length is 4, the fragments will be: 1-4, 2-5, 3-6, 4-7, ...
            If the offset is 2, and measure_length is 4, the fragments will be: 1-4, 3-6, 5-8, 7-10, ...
            If the offset is 4, and measure_length is 4, the fragments will be: 1-4, 5-8, 9-12, 13-16, ...
        verbose: The verbosity level
        num_processes: The number of processes to use for parallel processing.\
            If None, or num_processes <= 1, the processing will be done in a single process.
        mean: The mean of the normal distribution to generate the measure length of the new fragments
        std_dev: The standard deviation of the normal distribution to generate the measure length of the new fragments

    Returns:
        None

    Examples:

        # Basic execution
        >>> create_fragments_from_directory('input_directory', 'output_directory', log_file='log.txt')

        # Custom mean and std_dev
        >>> create_fragments_from_directory('input_directory', 'output_directory', log_file='log.txt', mean=5.2, std_dev=0.8)

        # Parallel processing
        >>> create_fragments_from_directory('input_directory', 'output_directory', log_file='log.txt', offset=4, verbose=1, num_processes=8)

        # Single process
        >>> create_fragments_from_directory('input_directory', 'output_directory', log_file='log.txt', offset=4, verbose=1)


    """
    if mean is None:
        mean = DEFAULT_MEAN
    if std_dev is None:
        std_dev = DEFAULT_STD_DEV
    if check_file_extension is None:
        check_file_extension = True

    fg = FragmentGenerator(
        offset=offset,
        verbose=verbose,
        num_processes=num_processes,
        log_file=log_file,
        mean=mean,
        std_dev=std_dev,
        export_options=export_options)
    fg.create_fragments_from_directory(
        input_directory=input_directory,
        output_directory=output_directory,
        check_file_extension=check_file_extension)


class FragmentGenerator:
    def __init__(
            self,
            log_file: str,
            offset: Optional[int] = None,
            verbose: int = 1,
            num_processes: Optional[int] = None,
            mean: float = DEFAULT_MEAN,
            std_dev: float = DEFAULT_STD_DEV,
            export_options: Optional[ExportOptions] = None
    ):
        if offset is None or offset < 1:
            raise ValueError('offset must be greater than 0')

        self.log_file = str(log_file)
        self.offset = int(offset)
        self.verbose = int(verbose)
        self.num_processes = num_processes
        self.mean = float(mean)
        self.std_dev = float(std_dev)
        self.export_options = export_options

    def create_fragments_from_directory(
            self,
            input_directory: str,
            output_directory: str,
            check_file_extension: Optional[bool] = True
    ) -> None:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)

        # Get all files in the input directory
        all_files = find_all_files(input_directory, '.krn') if check_file_extension \
            else find_all_files(input_directory, None)

        # Get the measure length for each file
        measures: List[int] = self.measures_normal_distribution(all_files)

        # Process tasks: single process or multiprocessing
        runner = FGRunnerFactory.create(
            fragment_generator=self,
            files=all_files,
            output_directory=output_directory,
            measures_length=measures,
            num_processes=self.num_processes
        )
        runner.run()

    def create_fragments_from_file(
            self,
            input_kern_file: str,
            output_directory: str,
            measure_length: int,
            export_options: Optional[ExportOptions] = None,
    ) -> None:
        if self.verbose >= 2:
            print(f"Processing {input_kern_file} into {output_directory} using measure_length={measure_length}")

        doc, err = read(input_kern_file)

        options = export_options if export_options is not None \
            else ExportOptions(spine_types=['**kern'],
                               token_categories=BEKERN_CATEGORIES,
                               kern_type=KernTypeExporter.normalizedKern)

        # Create folder for the current file
        current_folder = FragmentGenerator.get_output_filename_directory(input_kern_file, output_directory)
        os.makedirs(current_folder, exist_ok=True)

        for i in range(doc.get_first_measure(), doc.measures_count() + 1, self.offset):
            current_kern_file = os.path.join(current_folder, f'from-{i}-to-{i + measure_length}.krn')
            options.from_measure = i
            options.to_measure = i + measure_length

            # Check if the measures options are within the range of the file
            if options.to_measure is None or options.from_measure is None:
                continue
            if options.to_measure > doc.get_first_measure():
                break

            store(doc, current_kern_file, options)
        self.add_log(f'Created {input_kern_file} from file {input_kern_file}', True)

    def add_log(self, msg: str, is_correct: bool) -> None:
        SEPARATOR = ','
        NON_SEPARATOR = ';'
        status = 'OK' if is_correct else 'ERROR'
        with open(self.log_file, 'a') as f:
            f.write(f'{msg.replace(SEPARATOR, NON_SEPARATOR)}{SEPARATOR}{status}\n')

    @staticmethod
    def get_output_filename_directory(input_kern_file: str, output_directory: str) -> str:
        # Remove file extension
        input_kern_file = os.path.splitext(input_kern_file)[0]

        # Separate the file in parts
        tokens_input_kern_file = os.path.normpath(input_kern_file).split(os.sep)
        tokens_output_directory = os.path.normpath(output_directory).split(os.sep)

        # Remove relative paths parts
        clean_tokens_input_kern_file = [token for token in tokens_input_kern_file if all([token != '.', token != '..'])]
        clean_tokens_output_directory = [token for token in tokens_output_directory]  # Do not remove relative paths

        # Generate the output directory
        clean_input_kern_file = os.path.join(*clean_tokens_input_kern_file)
        clean_output_directory = os.path.join(*clean_tokens_output_directory)

        # Generate the output directory
        generated_output_directory = os.path.join(clean_output_directory, clean_input_kern_file)
        return generated_output_directory

    def measures_normal_distribution(self, files: list) -> list:
        return [int(round(random.gauss(self.mean, self.std_dev))) for _ in files]

    @staticmethod
    def store_kern_file(current_kern_file: str, exported: str) -> None:
        with open(current_kern_file, 'w') as f:
            f.write(exported)


class Runner(ABC):
    def __init__(
            self,
            fragment_generator: FragmentGenerator,
            files,
            output_directory: str,
            measures_length: List[int]
    ):
        self.fg = fragment_generator
        self.files = files
        self.output_directory = output_directory
        self.measures_length = measures_length

    @abstractmethod
    def run(self) -> None:
        pass


class SingleProcessRunner(Runner):
    def __init__(
            self,
            fragment_generator: FragmentGenerator,
            files: List[str],
            output_directory: str,
            measures_length: List[int]
    ):
        super().__init__(fragment_generator, files, output_directory, measures_length)

    def run(self) -> None:
        for i, file in enumerate(self.files):
            self.fg.create_fragments_from_file(
                file,
                self.output_directory,
                self.measures_length[i],
                self.fg.export_options)


class MultiProcessRunner(Runner):
    def __init__(
            self,
            fragment_generator: FragmentGenerator,
            files: List[str],
            output_directory: str,
            measures_length: List[int],
            num_processes: int
    ):
        super().__init__(fragment_generator, files, output_directory, measures_length)
        self.processes = int(num_processes)

    def run(self) -> None:
        with multiprocessing.Pool(processes=self.processes) as pool:
            list(tqdm(pool.imap_unordered(
                self.fg.create_fragments_from_file,
                [(file, self.output_directory, self.measures_length, self.fg.export_options) for file in self.files]),
                total=len(self.files), desc='Creating fragments'))


class FGRunnerFactory:
    @classmethod
    def create(
            cls,
            fragment_generator: FragmentGenerator,
            files: List[str],
            output_directory: str,
            measures_length: List[int],
            num_processes: Optional[int] = None) -> Runner:
        if num_processes is None or num_processes == 1:
            return SingleProcessRunner(
                fragment_generator=fragment_generator,
                files=files,
                output_directory=output_directory,
                measures_length=measures_length)
        else:
            return MultiProcessRunner(
                fragment_generator=fragment_generator,
                files=files,
                output_directory=output_directory,
                measures_length=measures_length,
                num_processes=num_processes)
