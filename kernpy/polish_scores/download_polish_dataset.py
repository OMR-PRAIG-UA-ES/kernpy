import requests
from PIL import Image
from io import BytesIO
import os
import json

from kernpy import HumdrumImporter, ExportOptions, BEKERN_CATEGORIES
import argparse

# This script creates the Polish dataset from the kern files.
# It downloads both the systems and full pages
DEFAULT_IIIF_ID = '/full/full/0/default.jpg'


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


def extract_and_save_measures(importer, from_measure, to_measure, krn_path):
    export_options = ExportOptions(spine_types=['**kern'], token_categories=BEKERN_CATEGORIES)
    export_options.from_measure = from_measure
    export_options.to_measure = to_measure
    exported_ekern = importer.doExportEKern(export_options)
    with open(krn_path, "w") as f:
        f.write(exported_ekern)


def download_and_save_page_images(importer, _output_path, map_page_label_iiif_ids, page_bounding_boxes):
    print(f'Bounding boxes {page_bounding_boxes}')

    for page_label, bounding_box_measure in page_bounding_boxes.items():
        page_iiif_id = map_page_label_iiif_ids.get(page_label)
        if page_iiif_id is None and page_label.startswith('#'):  # sometimes it's wrongly tagged without the #
            page_iiif_id = map_page_label_iiif_ids.get(page_label[1:])

        if page_iiif_id is not None:
            bounding_box = bounding_box_measure.bounding_box
            print(f"Page: {page_label}, Bounding box: {bounding_box}, ID: {page_iiif_id}, from bar {bounding_box_measure.from_measure}, to bar {bounding_box_measure.to_measure}")
            url = f'{page_iiif_id}/{bounding_box.xywh()}/full/0/default.jpg'
            print(url)
            image_path = os.path.join(_output_path, page_label + ".jpg")
            download_and_save_image(url, image_path)
            krn_path = os.path.join(_output_path, page_label + ".ekrn")
            extract_and_save_measures(importer, bounding_box_measure.from_measure, bounding_box_measure.to_measure - 1,
                                      krn_path)
            add_log(importer, krn_path)
        else:
            raise Exception(f'Cannot find IIIF id for page with label "{page_label}"')


def findIIIFIds(importer):
    iiifTag = "!!!IIIF:"
    for metacomment_token in importer.getMetacomments():
        if metacomment_token.startswith(iiifTag):
            url = metacomment_token[len(iiifTag):].strip()
            print(f'Reading IIIF manifest from {url}')
            return get_image_urls(url)
    raise Exception('Cannot find any IIIF metacomment')


def convert_and_download_file(input_kern, _output_path):
    print(f'Converting filename {input_kern}')
    importer = HumdrumImporter()
    importer.doImportFile(input_kern)
    if len(importer.errors):
        raise Exception(f'{input_kern} has errors {importer.getErrorMessages()}')
    map_page_label_IIIF_ids = findIIIFIds(importer)
    download_and_save_page_images(importer, _output_path, map_page_label_IIIF_ids, importer.page_bounding_boxes)


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


def add_log(importer: HumdrumImporter, path, log_filename='/tmp/polish_index.json') -> None:
    def get_instruments(line):
        return [word for word in line.split(' ') if not word.isnumeric()]

    info = {
        'path': path,
        'publication_date': importer.getMetacomments('PDT')[0] if importer.getMetacomments('PDT') else None,
        'iiif': importer.getMetacomments('IIIF')[0] if importer.getMetacomments('IIIF') else None,
        'n_measures': importer.last_bounding_box,
        'composer': importer.getMetacomments('COM')[0] if importer.getMetacomments('COM') else None,
        'compose_dates': importer.getMetacomments('CDT')[0] if importer.getMetacomments('CDT') else None,
        'tempo': importer.getMetacomments('OTL')[0] if importer.getMetacomments('OTL') else None,
        'piece_title': importer.getMetacomments('OPR')[0] if importer.getMetacomments('OPR') else None,
        'segment': importer.getMetacomments('SEGMENT')[0] if importer.getMetacomments('SEGMENT') else None,
        'n_voices': len(get_instruments(importer.getMetacomments('AIN')[0])) if importer.getMetacomments('AIN') else 0,
        'instruments': get_instruments(importer.getMetacomments('AIN')[0]) if importer.getMetacomments('AIN') else [],
        'unique_instruments': set(get_instruments(importer.getMetacomments('AIN')[0])) if importer.getMetacomments('AIN') else set(),
    }

    with open(log_filename, 'a') as f:
        json.dump(info, f)


def main(input_directory, output_directory) -> None:
    """
    Process the files in the input_directory and save the results in the output_directory.
    http requests are made to download the images.

    Args:
        input_directory: directory where the input files are found
        output_directory: directory where the output files are saved

    Returns:
        None

    Examples:
        >>> main('/kern_files', '/output_ekern')

    """
    print(f'Processing files in {input_directory} and saving to {output_directory}')
    kern_with_bboxes = search_files_with_string(input_directory, 'xywh')
    ok_files = []
    ko_files = []
    for kern in kern_with_bboxes:
        try:
            filename = remove_extension(kern)
            kern_path = os.path.join(input_directory, kern)
            output_kern_path = os.path.join(output_directory, filename)
            if not os.path.exists(output_kern_path):
                os.makedirs(output_kern_path)
            convert_and_download_file(kern_path, output_kern_path)
            ok_files.append(kern)
        except Exception as error:
            ko_files.append(kern)
            print(f'Errors in {kern}: {error}')

    print(f'----> OK files #{len(ok_files)}')
    print(f'----> KO files #{len(ko_files)}')
    print(ko_files)


if __name__ == "__main__":
    # Replace for the path where the kern files are found
    #input_path = "/Users/drizo/cmg/omr/datasets/humdrum-polish-scores/data-github"
    input_path = "/tmp/zzz"
    #input_path = "/Users/drizo/githubs/OMR-PRAIG-UA-ES/kernpy/test/resource_dir/polish/test2"
    output_path = '/Users/drizo/cmg/omr/datasets/humdrum-polish-scores/output/pl-wn'

    #TODO parser = argparse.ArgumentParser(description="Download Polish scores.")

    # Add arguments
    #TODO parser.add_argument("input_folder", type=str, help="Path to the input folder")
    #TODO parser.add_argument("output_folder", type=str, help="Path to the output folder")

    # Parse arguments
    #TODO args = parser.parse_args()
    #TODO input_path = args.input_folder
    #TODO output_path = args.output_folder

    kern_with_bboxes = search_files_with_string(input_path, 'xywh')
    ok_files = []
    ko_files = []
    for kern in kern_with_bboxes:
        try:
            filename = remove_extension(kern)
            kern_path = os.path.join(input_path, kern)
            output_kern_path = os.path.join(output_path, filename)
            if not os.path.exists(output_kern_path):
                os.makedirs(output_kern_path)
            convert_and_download_file(kern_path, output_kern_path)
            ok_files.append(kern)
        except Exception as error:
            ko_files.append(kern)
            print(f'Errors in {kern}: {error}')

    print(f'----> OK files #{len(ok_files)}')
    print(f'----> KO files #{len(ko_files)}')
    print(ko_files)
