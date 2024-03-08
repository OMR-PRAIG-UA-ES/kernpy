import requests
from PIL import Image
from io import BytesIO
import os


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


def get_image_urls(_manifest_url):
    # It returns the URL of pages tagged with a page number
    # It returns a map with the page label as key, and the URL as
    response = requests.get(_manifest_url)
    manifest_data = response.json()

    items = manifest_data.get('items', [])
    print(f'Items: ', len(items))

    for item in items:
        pl = item.get('label').get('pl')
        if pl:
            page_num = pl[0]
            if page_num != '[]':
                url = item.get('items')[0].get('items')[0].get('id', '')
                print(f'Page #{page_num}, {url}')
                #image_path = os.path.join(output_folder, page_num + '.jpg')
                #download_and_save_image(url, image_path)


if __name__ == "__main__":
    # Replace the manifest_url with the actual URL of your IIIF manifest
    manifest_url = "https://polona2.pl/iiif/item/MTk4NjI5Mw/manifest.json"
    get_image_urls(manifest_url)
