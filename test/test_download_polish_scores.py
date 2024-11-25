# Run from the root project (the 'test' parent folder): python3 -m unittest test/test_importer.py
# or from the IDE
import os
import unittest
import logging
import sys
import tempfile
from PIL import Image


from kernpy.polish_scores.download_polish_dataset import convert_and_download_file

logger = logging.getLogger()
logger.level = logging.INFO  # change it DEBUG to trace errors
logger.addHandler(logging.StreamHandler(sys.stdout))


class DownloadPolishScoresTestCase(unittest.TestCase):
    def check_image_sizes_equal(self, image_path1, image_path2):
        try:
            # Open the images
            image1 = Image.open(image_path1)
            image2 = Image.open(image_path2)

            # Get the sizes of the images
            size1 = image1.size
            size2 = image2.size

            # Check if the sizes are equal
            self.assertEqual(size1, size2)
        except IOError:
            raise Exception("Unable to load one or both images")

    def checkEqualFiles(self, file1, file2):
        with open(file1, 'r') as file1, open(file2, 'r') as file2:
            content1 = file1.read()
            content2 = file2.read()
            self.assertEqual(content1, content2)

    @unittest.skip("This test is too slow. Maybe we should mock the download. Comment this line to run the test")
    def test_convert_and_download_file(self):
        temp_dir = tempfile.mkdtemp()
        input_folder = 'resource_dir/polish/test1'
        log_file = os.path.join(temp_dir, 'polish_index.json')
        logging.info(f'Writing DownloadPolishScoresTestCase test to folder {temp_dir}')
        convert_and_download_file(input_folder + '/pl-wn--mus-iii-118-771--003_badarzewska-tekla--mazurka-brillante.krn', temp_dir, log_file)
        for i in range(9, 11):
            self.checkEqualFiles(input_folder + f'/pages/{i}.ekrn', temp_dir + f'/{i}.ekrn')
            self.check_image_sizes_equal(input_folder + f'/pages/{i}.jpg', temp_dir + f'/{i}.jpg')

    def test_polish_package_import(self):
        from kernpy.polish_scores import download_polish_scores
        self.assertIsNotNone(download_polish_scores)


if __name__ == '__main__':
    unittest.main()
