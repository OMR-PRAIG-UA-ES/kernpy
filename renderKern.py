import os
import sys

import numpy as np
import multiprocessing
from tqdm import tqdm

import verovio
from cairosvg import svg2png
import cv2

### GLOBAL VARIABLES ###
PROCESSES_PARALLEL = 8
input_dir = ''


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


def render_image(args) -> None:
    """
    Render the image for the given importer and save it in the given folder
    :param args: A tuple containing, input_file, and progress_queue
    """
    input_file, progress_queue = args
    try:
        # Redirect stdout and stderr
        #sys.stdout = open(os.devnull, 'w')
        #sys.stderr = open(os.devnull, 'w')

        new_file_path_png = input_file.replace('.krn', '.png')
        print(f'Creating file: {new_file_path_png}')

        # Create a verovio toolkit instance
        vtk = verovio.toolkit()

        # Load the file
        vtk.loadFile(input_file)

        # Render the file
        svg_content = vtk.renderToSVG()
        svg_content = svg_content.replace("overflow=\"inherit\"", "overflow=\"visible\"")

        # Convert the SVG to PNG
        png_content = svg2png(bytestring=svg_content, background_color='white')
        png_data = np.frombuffer(png_content, np.uint8)
        png_img = cv2.imdecode(png_data, cv2.IMREAD_UNCHANGED)

        # Save the PNG
        cv2.imwrite(new_file_path_png, png_img)

        # Update progress
        progress_queue.put(1)

        add_log(input_file, True)
    except Exception as e:
        add_log(f'{input_file}->{e}', False)
    finally:
        pass
        # Restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def generate_rendered_images(input_dir: str, _log_file: str) -> None:
    """
    Generate the rendered images for the given images in the input directory.

    :param input_dir: The input directory
    :param _log_file: The log file
    """
    global log_file

    log_file = _log_file

    # Input files
    clean_input_files = []
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.endswith('.krn'):
                clean_input_files.append(os.path.join(root, f))

    print(clean_input_files)
    # Tasks
    tasks = list(zip(clean_input_files,))

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
                pool.imap_unordered(render_image, [(task + (progress_queue,)) for task in tasks]),
                total=total_tasks, desc='Rendering images'):
            pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: python {sys.argv[0]} <input_dir> <log_file>')
        sys.exit(1)

    generate_rendered_images(sys.argv[1], sys.argv[2])
