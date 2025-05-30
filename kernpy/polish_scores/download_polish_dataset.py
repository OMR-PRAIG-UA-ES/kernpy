import sys

import requests
from PIL import Image
from io import BytesIO
import os
import json
from typing import List, Optional

from kernpy import ExportOptions, BEKERN_CATEGORIES, Importer, Exporter, Document, Encoding, read


# This script creates the Polish dataset from the kern files.
# It downloads both the systems and full pages
DEFAULT_IIIF_ID = '/full/full/0/default.jpg'

LOG_FILENAME = 'polish_index.json'


def get_image_urls(_manifest_url):
    # It returns the URL of pages tagged with a page number
    # It returns a map with the page label as key, and the URL as
    response = requests.get(_manifest_url)
    manifest_data = response.json()
    result = {}

    # The corpus contains two kinds of IIIF manifests
    if 'sequences' in manifest_data:
        for sequence in manifest_data['sequences']:
            for canvas in sequence['canvases']:
                image_id = canvas['images'][0]['resource']['service']['@id']
                page_label = canvas['label'] if 'label' in canvas else None
                result[page_label] = image_id
    else:
        items = manifest_data.get('items', [])
        for item in items:
            pl = item.get('label').get('pl')
            if pl:
                page_label = pl[0]
                if page_label != '[]':
                    image_id = item.get('items')[0].get('items')[0].get('id', '')
                    if image_id.endswith(DEFAULT_IIIF_ID):
                        image_id = image_id[:-len(DEFAULT_IIIF_ID)]
                    result[page_label] = image_id

    # print(f'Items: ', len(items))

    return result


def download_and_save_image(url, save_path):
    try:
        # Make a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses

        # Open the image using Pillow
        image = Image.open(BytesIO(response.content))

        # Save the image to the specified path
        image.save(save_path, format='JPEG')

        print(f"Image downloaded and saved to: {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def factory_get_kern_type_exporter(kern_type: str) -> Encoding:
    """
    Factory method to get the Encoding

    Args:
        kern_type (str): the type of kern exporter. It can be 'krn' or 'ekrn'

    Returns:
        Encoding: the Encoding instance
    """
    if kern_type == 'krn':
        return Encoding.normalizedKern
    elif kern_type == 'ekrn':
        return Encoding.eKern
    else:
        raise Exception(f'Unknown export kern type: {kern_type}')


def extract_and_save_measures(document, from_measure, to_measure, krn_path, exporter_kern_type='ekrn'):
    exporter_kern_type = factory_get_kern_type_exporter(exporter_kern_type)
    export_options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES, kern_type=exporter_kern_type)
    export_options.from_measure = from_measure
    export_options.to_measure = to_measure
    exporter = Exporter()
    exported_ekern = exporter.export_string(document, export_options)
    with open(krn_path, "w") as f:
        f.write(exported_ekern)


def download_and_save_page_images(document, _output_path, map_page_label_iiif_ids, page_bounding_boxes, log_filename, exporter_kern_type='ekrn'):
    print(f'Bounding boxes {page_bounding_boxes}')

    for page_label, bounding_box_measure in page_bounding_boxes.items():
        page_iiif_id = map_page_label_iiif_ids.get(page_label)
        if page_iiif_id is None and page_label.startswith('#'):  # sometimes it's wrongly tagged without the #
            page_iiif_id = map_page_label_iiif_ids.get(page_label[1:])

        if page_iiif_id is not None:
            bounding_box = bounding_box_measure.bounding_box
            print(f"Page: {page_label}, "
                  f"Bounding box: {bounding_box}, "
                  f"ID: {page_iiif_id}, "
                  f"from bar {bounding_box_measure.from_measure}, "
                  f"to bar {bounding_box_measure.to_measure}")
            url = os.path.join(page_iiif_id, bounding_box.xywh(), 'full', '0', 'default.jpg')
            print(url)
            image_path = os.path.join(_output_path, page_label + ".jpg")
            download_and_save_image(url, image_path)
            krn_path = os.path.join(_output_path, page_label + f'.{exporter_kern_type}')
            extract_and_save_measures(document, bounding_box_measure.from_measure, bounding_box_measure.to_measure - 1,
                                      krn_path, exporter_kern_type=exporter_kern_type)
            add_log(document, krn_path, log_filename=log_filename)
        else:
            raise Exception(f'Cannot find IIIF id for page with label "{page_label}"')


def findIIIFIds(document):
    iiifTag = "!!!IIIF:"
    for metacomment_token in document.get_metacomments():
        encoding = metacomment_token
        if encoding.startswith(iiifTag):
            url = encoding[len(iiifTag):].strip()
            print(f'Reading IIIF manifest from {url}')
            return get_image_urls(url)
    raise Exception('Cannot find any IIIF metacomment')


def is_valid_document(document, kern_spines_filter) -> bool:
    if kern_spines_filter is None:
        return True

    exporter = Exporter()
    kern_types = exporter.get_spine_types(document, spine_types=['**kern'])
    return len(kern_types) == int(kern_spines_filter)


def convert_and_download_file(input_kern, _output_path, log_filename, kern_spines_filter: int = None, exporter_kern_type='ekrn') -> None:
    document, errors = read(input_kern)
    if len(errors) > 0:
        print(f'ERRORS when kernpy.read:{input_kern} has errors {errors}\nContinue...', file=sys.stderr)
        raise Exception(f'ERRORS when kernpy.read: {input_kern}. Has errors: {errors}')

    if not is_valid_document(document, kern_spines_filter):
        return

    map_page_label_IIIF_ids = findIIIFIds(document)
    download_and_save_page_images(document, _output_path, map_page_label_IIIF_ids, document.page_bounding_boxes,
                                  log_filename=log_filename, exporter_kern_type=exporter_kern_type)


def search_files_with_string(root_folder, target_string):
    matching_files = []

    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.krn'):
                file_path = os.path.join(foldername, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if target_string in content:
                            relative_path = os.path.relpath(file_path, root_folder)
                            matching_files.append(relative_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return matching_files


def remove_extension(file_name):
    # Using os.path.splitext to split the file name and extension
    base_name, _ = os.path.splitext(file_name)
    return base_name


def add_log(document: Document, path, log_filename) -> None:
    try:
        def get_instruments(line):
            words = line.split(' ')
            instruments = []
            for i in range(len(words)):
                if words[i].isnumeric():
                    instruments.extend([words[i + 1]] * int(words[i]))
            return instruments

        def get_publish_date(line):
            if line is None or line == '':
                return 0

            clean_line = [char for char in line if char.isnumeric()]
            return int(''.join(clean_line))

        def round_publication_year(original_composer_date):
            try:
                if original_composer_date is None:
                    return 0
                start_date, end_date = original_composer_date.split('-')

                start_year = int(start_date.split('/')[0])
                end_year = int(end_date.split('/')[0])

                RATIO = 0.7  # date where the composer was most active
                return int(start_year + (end_year - start_year) * RATIO)
            except Exception as e:
                return -1

        def round_publication_year_v2(original_composer_date):
            def flatten(xss):
                return [x for xs in xss for x in xs]

            try:
                items_date = original_composer_date.split('/')
                clean_items = [item.replace(' ', '') for item in items_date]
                clean_items = [item.replace('~', '') for item in clean_items]
                split_again = [item.split('-') for item in clean_items]
                flatten_items = flatten(split_again)
                useful_items = [item for item in flatten_items if item.isnumeric()]
                year_items = [int(item) for item in useful_items if len(item) == 4]
                return int(year_items[0]) if len(year_items) > 0 else -3
            except Exception as e:
                return -2

        info = {
            'path': path,
            'publication_date': get_publish_date(document.get_metacomments('PDT')[0]) if document.get_metacomments(
                'PDT') else None,
            'original_publication_date_tag': True,
            'iiif': document.get_metacomments('IIIF')[0] if document.get_metacomments('IIIF') else None,
            'n_measures': len(document.tree.stages),
            'composer': document.get_metacomments('COM')[0] if document.get_metacomments('COM') else None,
            'composer_dates': document.get_metacomments('CDT')[0] if document.get_metacomments('CDT') else None,
            'tempo': document.get_metacomments('OTL')[0] if document.get_metacomments('OTL') else None,
            'piece_title': document.get_metacomments('OPR')[0] if document.get_metacomments('OPR') else None,
            'segment': document.get_metacomments('SEGMENT')[0] if document.get_metacomments('SEGMENT') else None,
            'n_voices': len(get_instruments(document.get_metacomments('AIN')[0])) if document.get_metacomments(
                'AIN') else 0,
            'instruments': get_instruments(document.get_metacomments('AIN')[0]) if document.get_metacomments(
                'AIN') else [],
            'unique_instruments': [
                *set(get_instruments(document.get_metacomments('AIN')[0]))] if document.get_metacomments('AIN') else [],
        }

        if info['publication_date'] in (0, 1, -1, -2) or info['publication_date'] is None:
            info['publication_date'] = round_publication_year(info['composer_dates'])
            info['original_publication_date_tag'] = False

        if info['publication_date'] in (0, 1, -1, -2) or info['publication_date'] is None:
            info['publication_date'] = round_publication_year_v2(info['composer_dates'])
            info['original_publication_date_tag'] = False

        with open(log_filename, 'a') as f:
            json.dump(info, f)
            f.write('\n')
    except Exception as e:
        print(f"Error adding log:{path}:{e}")


def remove_empty_dirs(directory):
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            full_dir = os.path.join(root, dir)
            if not os.listdir(full_dir):
                os.rmdir(full_dir)


def store_error_log(filename, msg: dict):
    with open(filename, encoding='utf-8', mode='a') as f:
        f.write(f'{json.dumps(msg)}\n')


def main(
        input_directory: str,
        output_directory: str,
        remove_empty_directories: Optional[bool] = True,
        kern_spines_filter: Optional[int] = 2,
        exporter_kern_type: Optional[str] = 'ekern'
) -> None:
    """
    Process the files in the input_directory and save the results in the output_directory.
    http requests are made to download the images.

    Args:
        input_directory (str): directory where the input files are found
        output_directory (str): directory where the output files are saved
        remove_empty_directories (Optional[bool]): remove empty directories when finish processing the files
        kern_spines_filter (Optional[int]): Only process files with the number of **kern spines specified.\
            Use it to export 2-voice files. Default is 2.\
            Use None to process all files.
        exporter_kern_type (Optional[str]): the type of kern exporter. It can be 'krn' or 'ekrn'



    Returns:
        None

    Examples:
        >>> main('/kern_files', '/output_ekern')
        None

        >>> main('/kern_files', '/output_ekern', remove_empty_directories=False)
        None

        >>> main('/kern_files', '/output_ekern', kern_spines_filter=2, remove_empty_directories=False)
        None

        >>> main('/kern_files', '/output_ekern', kern_spines_filter=None, remove_empty_directories=False)
        None

        >>> main('/kern_files', '/output_ekern', exporter_kern_type='krn', remove_empty_directories=True)
        None

        >>> main('/kern_files', '/output_ekern', exporter_kern_type='ekrn', remove_empty_directories=True, kern_spines_filter=2)
        None

    """
    print(f'Processing files in {input_directory} and saving to {output_directory}')
    kern_with_bboxes = search_files_with_string(input_directory, 'xywh')
    ok_files = []
    ko_files = []
    log_file = os.path.join(output_directory, LOG_FILENAME)
    print(f"{25*'='}"
          f"\nProcessing {len(kern_with_bboxes)} files."
          f"\nLog will be saved in {log_file}."
          f"\n{25*'='}")
    for kern in kern_with_bboxes:
        try:
            filename = remove_extension(kern)
            kern_path = os.path.join(input_directory, kern)
            output_kern_path = os.path.join(output_directory, filename)
            if not os.path.exists(output_kern_path):
                os.makedirs(output_kern_path)
            convert_and_download_file(kern_path, output_kern_path, log_filename=log_file, kern_spines_filter=kern_spines_filter, exporter_kern_type=exporter_kern_type)
            ok_files.append(kern)
        except Exception as error:
            ko_files.append(kern)
            print(f'Errors in {kern}: {error}')
            store_error_log(os.path.join(output_directory, 'errors.json'), {'kern': kern, 'error': str(error)})

    if remove_empty_directories:
        remove_empty_dirs(output_directory)

    print(f'----> OK files #{len(ok_files)}')
    print(f'----> KO files #{len(ko_files)}')
    print(ko_files)


if __name__ == '__main__':
    print(f'Usage: python -m kernpy --polish --input_directory /path/to/input --output_directory /path/to/output')
    sys.exit(1)

