import requests
from PIL import Image
from io import BytesIO
import os

from src.generated.kern.kernLexer import kernLexer
from src.generated.kern.kernParser import kernParser
from src.kern_2_ekern import KernListener
from antlr4 import *

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


class BoundingBox:
    def __init__(self, x, y, w, h):
        self.fromX = x
        self.fromY = y
        self.toX = x + w
        self.toY = y + h
        self.fromBar = None
        self.toBar = None

    def w(self):
        return self.toX - self.fromX

    def h(self):
        return self.toY - self.fromY

    def extend(self, bounding_box):
        self.fromX = min(self.fromX, bounding_box.from_x)
        self.fromY = min(self.fromY, bounding_box.from_y)
        self.toX = max(self.toX, bounding_box.to_x)
        self.toY = max(self.toY, bounding_box.to_y)

    def __str__(self):
        return f'(x={self.fromX}, y={self.fromY}, w={self.w()}, h={self.h()}), from bar {self.fromBar}, to bar {self.toBar}'

    def xywh(self):
        return f'{self.fromX},{self.fromY},{self.w()},{self.h()}'


class Kern2EkernListenerWithDownload(KernListener):

    def __init__(self, output):
        KernListener.__init__(self, output)
        self.mapPageLabelIIIFIds = None
        self.lastBoundingBox = None
        self.pageBoundingBoxes = {}
        self.lastBarNumber = None

    def exitEveryRule(self, ctx: ParserRuleContext):
        super().exitEveryRule(ctx)
        #print(f'Exit rule {ctx.getText()}')

    def exitMetacomment(self, ctx: kernParser.MetacommentContext):
        # we implement it this way instead of having explicit rules for the metacomments to simplify the grammar
        iiifTag = "!!!IIIF:"
        if ctx.getText().startswith(iiifTag):
            url = ctx.getText()[len(iiifTag):].strip()
            print(f'Reading IIIF manifest from {url}')
            self.mapPageLabelIIIFIds = get_image_urls(url)
            #print(self.mapPageLabelIIIFIds)

    def exitBarline(self, ctx: kernParser.BarlineContext):
        super().exitBarline(ctx)
        if ctx.number():
            self.lastBarNumber = ctx.number().getText()

    def exitXywh(self, ctx: kernParser.XywhContext):
        self.lastBoundingBox = BoundingBox(int(ctx.x().getText()), int(ctx.y().getText()), int(ctx.w().getText()),
                                           int(ctx.h().getText()))

    def exitBoundingBox(self, ctx: kernParser.BoundingBoxContext):
        page = ctx.pageNumber().getText()
        last_page_bb = self.pageBoundingBoxes.get(page)
        if last_page_bb is not None:
            print(f'Extending page {page}')
            last_page_bb.extend(self.lastBoundingBox)
            last_page_bb.toBar = self.lastBarNumber
        else:
            print(f'Adding {page}')
            if self.lastBarNumber is None:
                self.lastBarNumber = 0
            self.lastBoundingBox.from_bar = self.lastBarNumber
            self.lastBoundingBox.to_bar = self.lastBarNumber
            self.pageBoundingBoxes[page] = self.lastBoundingBox
        # TODO measures en cada uno


def download_and_save_page_images(_output_path, map_page_label_iiif_ids, page_bounding_boxes):
    print(f'Bounding boxes {page_bounding_boxes}')
    images_folder = os.path.join(_output_path, 'images')
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    for page_label, bounding_box in page_bounding_boxes.items():
        page_iiif_id = map_page_label_iiif_ids.get(page_label)
        if page_iiif_id is not None:
            print(f"Page: {page_label}, Bounding box: {bounding_box}, ID: {page_iiif_id}")
            url = f'{page_iiif_id}/{bounding_box.xywh()}/full/0/default.jpg'
            print(url)
            image_path = os.path.join(images_folder, page_label + ".jpg")
            download_and_save_image(url, image_path)
        else:
            raise Exception(f'Cannot find IIIF id for page with label "{page_label}"')


def convert_and_download_file(input_kern, _output_path):
    print(f'Converting filename {input_kern}')
    input_stream = FileStream(input_kern, 'UTF-8')
    lexer = kernLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = kernParser(token_stream)
    tree = parser.start()

    output_kern = os.path.join(_output_path, 'score.krn')

    with open(output_kern, 'w', buffering=4096) as outputFile:
        print(f'Converting filename {input} to {output_kern}')
        listener = Kern2EkernListenerWithDownload(outputFile)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        download_and_save_page_images(_output_path, listener.mapPageLabelIIIFIds, listener.pageBoundingBoxes)


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


if __name__ == "__main__":
    # Replace for the path where the kern files are found
    print("RECUERDA DEJAR TODO!!!!!!!!! - MENS?")
    #input_path = "/Users/drizo/githubs/humdrum-polish-scores/pl-wn/"
    input_path = "/Users/drizo/cmg/omr/datasets/humdrum-polish-scores/pruebas/input"
    output_path = "/Users/drizo/cmg/omr/datasets/humdrum-polish-scores/pruebas/output"

    kern_with_bboxes = search_files_with_string(input_path, 'xywh')
    for kern in kern_with_bboxes:
        filename = remove_extension(kern)
        kern_path = os.path.join(input_path, kern)
        output_kern_path = os.path.join(output_path, filename)
        if not os.path.exists(output_kern_path):
            os.makedirs(output_kern_path)

        convert_and_download_file(kern_path, output_kern_path)
