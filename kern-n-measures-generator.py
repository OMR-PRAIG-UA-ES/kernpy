# It is a script utility to generate shorter ekern files from a given input directory.
# It is not a test script, but it is a script that uses the kernpy library as client code.
import os
import sys
import numpy as np
import multiprocessing
from tqdm import tqdm

import kernpy


### GLOBAL VARIABLES ###
PROCESSES_PARALLEL = 8
output_folder = '/tmp/output'
log_file = 'log.csv'
FIND_ONLY_1_SPINE_SCORES = False
MEASURE_LENGTH = 1


def add_log(msg: str, is_correct: bool) -> None:
    """
    Add a log message
    :param msg: The message
    :param is_correct: If the message is correct
    """
    global log_file
    SEPARATOR = ','
    status = 'OK' if is_correct else 'ERROR'
    with open(log_file, 'a') as f:
        f.write(f'{msg.replace(SEPARATOR, ";")}{SEPARATOR}{status}\n')


def create_fragments(args) -> None:
    """
    Create the fragments for the given importer and save them in the given folder
    :param args: A tuple containing, input_file, measure_length, and progress_queue
    """
    input_file, measure_length, progress_queue = args
    try:
        global output_folder

        # Redirect stdout and stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

        importer = kernpy.HumdrumImporter()
        importer.doImportFile(input_file)

        # find only 1 spine scores
        if FIND_ONLY_1_SPINE_SCORES:
            if len(importer.spines) != 1:
                add_log(f'{input_file}->More than 1 spine', False)
                return
        options = kernpy.ExportOptions(spine_types=['**kern'], token_categories=kernpy.BEKERN_CATEGORIES)

        # Create folder for the current file
        current_folder = os.path.join(output_folder, '/'.join(input_file.replace(".krn", "").split('/')[-2:]))
        #print(f'Creating folder: {current_folder}')
        os.makedirs(current_folder, exist_ok=True)

        for i in range(1, importer.last_measure_number, 1):
            current_kern_file = os.path.join(current_folder, f'from-{i}-to-{i+measure_length}.krn')
            #print(f'Processing: {current_ekern_file}')
            options.from_measure = i
            options.to_measure = i

            # Check if the measures are within the ranged of the file
            if options.to_measure is None or options.from_measure is None:
                continue

            if options.to_measure > importer.last_measure_number:
                break

            exported = importer.doExportNormalizedKern(options)

            with open(current_kern_file, 'w') as f:
                f.write(exported)

            # Update progress
            progress_queue.put(1)

        add_log(input_file, True)
    except Exception as e:
        add_log(f'{input_file}->{output_folder}->{e}', False)
    finally:
        pass
        # Restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def get_measures_normal_distribution(files: []) -> []:
    """
    Assign a measure length to each file in the list

    Use 4 as the mean and 1 as the standard deviation.

    :param files: The list of files. [str | path]
    :return: A list with the measure length for each file. [int]
    """
    mean = MEASURE_LENGTH
    std_dev = 0
    measures = np.random.normal(mean, std_dev, len(files)).astype(int)

    return list(measures)


def generate_fragment_files(input_dir: str, _output_dir: str, _log_file: str) -> None:
    """
    Generate new ekerns from the input directory.
    Use standard normal distribution to assign a measure length to each file.
    :param input_dir: The input directory
    :param _output_dir: The output directory
    :param _log_file: The log file
    """
    global output_folder, log_file
    output_folder = _output_dir
    log_file = _log_file

    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Input files
    clean_input_files = []
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.endswith('.krn'):
                clean_input_files.append(os.path.join(root, f))

    # Distribution of the measures
    measures = get_measures_normal_distribution(clean_input_files)

    # Tasks
    tasks = list(zip(clean_input_files, measures))

    # Shared progress queue
    manager = multiprocessing.Manager()
    progress_queue = manager.Queue()
    total_tasks = len(tasks)

    # Run the tasks
    # Sequential processing
    #for task in tqdm(tasks, desc='Creating fragments'):
    #    create_fragments(task + (progress_queue,))
    #    progress_queue.put(1)

    # Parallel processing
    with multiprocessing.Pool(processes=PROCESSES_PARALLEL) as pool:
        for _ in tqdm(
                pool.imap_unordered(create_fragments, [(task + (progress_queue,)) for task in tasks]),
                total=total_tasks, desc='Creating fragments'):
            pass


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'Usage: python {sys.argv[0]} <input_dir> <output_dir> <log_file>')
        sys.exit(1)

    generate_fragment_files(sys.argv[1], sys.argv[2], sys.argv[3])
