import os
import sys
import random

import numpy as np
import multiprocessing
from tqdm import tqdm

import verovio
from cairosvg import svg2png
import cv2

### GLOBAL VARIABLES ###
PROCESSES_PARALLEL = 8
input_dir = ''
log_file = ''


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


def find_image_cut(sample, margin_bot=40, margin_right=40):
    cut_height = None
    cut_width = None

    # Get the height and width of the image
    height, width = sample.shape[:2]

    # Iterate through the image array from the bottom to the top
    for y in range(height - 1, -1, -1):
        if [0, 0, 0] in sample[y]:
            cut_height = y + margin_bot
            break

    for x in range(width - 1, -1, -1):
        if [0, 0, 0] in sample[:, x]:
            cut_width = x + margin_right
            break

    # If no black pixel is found, return None
    return cut_height, cut_width


def rfloat(start, end):
    return round(random.uniform(start, end), 2)


def render_image(args) -> None:
    """
    Render the image for the given importer and save it in the given folder
    :param args: A tuple containing, input_file, and progress_queue
    """
    input_file, progress_queue = args
    try:
        input_file, progress_queue = args
        # Redirect stdout and stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

        # Create a verovio toolkit instance
        vtk = verovio.toolkit()

        # Set rendering options
        width = random.choice([2100, 3000])
        vtk.setOptions({
            "pageWidth": width,
            "footer": 'none',
            'barLineWidth': rfloat(0.3, 0.8),
            'beamMaxSlope': rfloat(10, 20),
            'staffLineWidth': rfloat(0.1, 0.3),
            'spacingStaff': rfloat(4, 12)
        })

        # Load the file
        vtk.loadFile(input_file)

        # Render the file to SVG
        svg_content = vtk.renderToSVG()
        svg_content = svg_content.replace("overflow=\"inherit\"", "overflow=\"visible\"")

        # Convert the SVG to PNG
        png_content = svg2png(bytestring=svg_content, background_color='white', dpi=300)
        png_data = np.frombuffer(png_content, np.uint8)
        png_img = cv2.imdecode(png_data, cv2.IMREAD_UNCHANGED)

        # Cut white boxes from the image
        cut_height, cut_width = find_image_cut(png_img)
        if cut_height is not None:
            png_img = png_img[:cut_height, :]
        if cut_width is not None:
            png_img = png_img[:, :cut_width]

        # Save the PNG
        new_file_path_png = input_file.replace('.krn', '.png')
        cv2.imwrite(new_file_path_png, png_img)

        # Update progress
        progress_queue.put(1)

        add_log(input_file, True)
    except Exception as e:
        # remove kern
        os.remove(input_file)
        add_log(f'{input_file}->{e}', False)
    finally:
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
    tasks = list(zip(clean_input_files, ))

    # Shared progress queue
    manager = multiprocessing.Manager()
    progress_queue = manager.Queue()
    total_tasks = len(tasks)

    print(f'Total tasks: {total_tasks}')
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
