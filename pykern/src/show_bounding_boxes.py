# This script loads a kern file as tagged in the Polish Scores project
# (https://github.com/pl-wnifc/humdrum-polish-scores) and draws the given image with the annotated bounding boxes

from PIL import Image, ImageDraw


def rectangle(input_path, output_path, _rectangle):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    draw.rectangle(_rectangle, outline="red", width=10)
    image.save(output_path)


if __name__ == "__main__":
    # Specify the image path
    image_path = "/private/tmp/prueba/9.jpg"
    output_path = "/tmp/sal.jpg"

    # Set rectangle parameters
    x, y = 74, 94
    width, height = 2722, 1432
    #x, y = 61,1432
    #idth, height = 2606,699

    rectangle(image_path, output_path, (x, y, x + width, y + width))
