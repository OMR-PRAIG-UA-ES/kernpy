import os
import random
import multiprocessing
import sys
from tqdm import tqdm

from kernpy import HumdrumImporter, ExportOptions, BEKERN_CATEGORIES, KernTypeExporter

DEFAULT_MEAN = 4.0
DEFAULT_STD_DEV = 0.0
ABSOLUTE_PATHS_KEYWORDS = ['user', 'home']
BAD_PATH_ERROR_MESSAGE = f'\tUsing absolute paths is not recommended.\n' \
                         f'\tThe input file will be used as a template for the output files. \n' \
                         f'\tUse relative paths to avoid overwriting the input file.\n' \
                         f'\tUse relative paths to avoid exposing private information.\n' \
                         f'\tAvoid using: {ABSOLUTE_PATHS_KEYWORDS}\n'


def create_fragments_from_kern(input_kern_file: str, output_directory: str, measure_length: int,
                               offset: int, log_file: str, verbose: int = 1, num_processes: int = None) -> None:
    """
    Create a bunch of little kern files from a single kern file.

    Args:
        log_file:
        input_kern_file:
        output_directory:
        measure_length:
        offset:
        verbose:
        num_processes:

    Returns:
        None

    Examples:
        ...

    """
    if any(keyword in input_kern_file for keyword in ABSOLUTE_PATHS_KEYWORDS):
        raise ValueError(BAD_PATH_ERROR_MESSAGE)

    fg = FragmentGenerator(offset=offset, verbose=verbose, num_processes=num_processes, log_file=log_file)
    fg.create_fragments_from_file(input_kern_file=input_kern_file,
                                  output_directory=output_directory,
                                  measure_length=measure_length)


def create_fragments_from_directory(input_directory: str, output_directory: str, log_file: str,
                                    check_file_extension: bool = True, offset: int = 0,
                                    verbose: int = 1, num_processes: int = None,
                                    mean: float = DEFAULT_MEAN, std_dev: float = DEFAULT_STD_DEV) -> None:
    """
    Create a bunch of little kern files from a directory of kern files.

    Args:
        log_file:
        input_directory:
        output_directory:
        check_file_extension:
        offset:
        verbose:
        num_processes:
        mean:
        std_dev:

    Returns:
        None

    Examples:
        ...

    """
    if any(keyword in input_directory for keyword in ABSOLUTE_PATHS_KEYWORDS):
        raise ValueError(BAD_PATH_ERROR_MESSAGE)
    if mean is None:
        mean = DEFAULT_MEAN
    if std_dev is None:
        std_dev = DEFAULT_STD_DEV
    if check_file_extension is None:
        check_file_extension = True

    fg = FragmentGenerator(offset=offset, verbose=verbose, num_processes=num_processes, log_file=log_file,
                           mean=mean, std_dev=std_dev)
    fg.create_fragments_from_directory(input_directory=input_directory,
                                       output_directory=output_directory,
                                       check_file_extension=check_file_extension)


class FragmentGenerator:
    def __init__(self, log_file: str, offset=None, verbose=1, num_processes=None, mean=DEFAULT_MEAN,
                 std_dev=DEFAULT_STD_DEV):
        if offset is None or offset < 1:
            raise ValueError('offset must be greater than 0')
        if mean is None or mean < 1:
            raise ValueError('mean must be greater than 0')

        self.log_file = str(log_file)
        self.offset = int(offset)
        self.verbose = int(verbose)
        self.num_processes = num_processes
        self.mean = float(mean)
        self.std_dev = float(std_dev)

    def create_fragments_from_directory(self, input_directory: str, output_directory: str,
                                        check_file_extension=True) -> None:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Get all files in the input directory
        clean_input_files = []
        for root, dirs, files in os.walk(input_directory):
            for file in files:
                if not check_file_extension or file.endswith('.krn'):
                    clean_input_files.append(os.path.join(root, file))

        # Get the measure length for each file
        measures = self.measures_normal_distribution(clean_input_files)

        # Create tasks
        tasks = [(clean_input_files[i], output_directory, measures[i]) for i in range(len(clean_input_files))]

        # Process tasks: single process or multiprocessing
        if self.num_processes is None or self.num_processes <= 1:
            for task in tqdm(tasks, desc='Creating fragments'):
                self.create_fragments_from_file(*task)
        else:
            with multiprocessing.Pool(processes=self.num_processes) as pool:
                list(tqdm(pool.imap_unordered(self.create_fragment_task_wrapper, tasks),
                          total=len(tasks), desc='Creating fragments'))

    def create_fragment_task_wrapper(self, args):
        try:
            if self.verbose < 2:
                # Redirect stdout and stderr
                sys.stdout = open(os.devnull, 'w')
                sys.stderr = open(os.devnull, 'w')

            self.create_fragments_from_file(*args)
        except Exception as e:
            self.add_log(str(e) + str(e), False)
            if self.verbose >= 2:
                print(f"Error processing {args}: {e}", file=sys.stderr)
        finally:
            # Reset stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    def create_fragments_from_file(self, input_kern_file: str, output_directory: str, measure_length: int,
                                   find_only_1_spine_scores=False) -> None:
        if self.verbose >= 2:
            print(f"Processing {input_kern_file} into {output_directory} using measure_length={measure_length}")

        importer = HumdrumImporter()
        importer.doImportFile(input_kern_file)

        # check if there is only 1 spine if required
        if find_only_1_spine_scores and len(importer.spines) != 1:
            self.add_log(f'{input_kern_file}->More than 1 spine', False)
            return

        options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)

        # Create folder for the current file
        current_folder = FragmentGenerator.get_output_filename_directory(input_kern_file, output_directory)
        if self.verbose >= 2:
            print(f'Creating folder: {current_folder}')
        os.makedirs(current_folder, exist_ok=True)

        print("WARNING: Check options.from_measure=1. Raise exception if 1 or 0", file=sys.stderr) # TODO: Change importer interface. 0-1 boundaries
        for i in range(1, importer.last_measure_number, self.offset):
            current_kern_file = os.path.join(current_folder, f'from-{i}-to-{i + measure_length}.krn')
            options.from_measure = i
            options.to_measure = i + measure_length

            # Check if the measures options are within the range of the file
            if options.to_measure is None or options.from_measure is None:
                continue
            if options.to_measure > importer.last_measure_number:
                break

            exported = importer.doExport(KernTypeExporter.normalizedKern, options)
            FragmentGenerator.store_kern_file(current_kern_file, exported)
        self.add_log(f'{input_kern_file}#{current_folder}', True)

    def add_log(self, msg: str, is_correct: bool) -> None:
        SEPARATOR = ','
        NON_SEPARATOR = ';'
        status = 'OK' if is_correct else 'ERROR'
        with open(self.log_file, 'a') as f:
            f.write(f'{msg.replace(SEPARATOR, NON_SEPARATOR)}{SEPARATOR}{status}\n')

    @staticmethod
    def get_output_filename_directory(input_kern_file: str, output_directory: str) -> str:
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
