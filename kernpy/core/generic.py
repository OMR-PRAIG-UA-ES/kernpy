import os


def ekern_to_krn(input_file, output_file) -> None:
    """
    Convert one .ekrn file to .krn file.

    Args:
        input_file: The path to the input directory
        output_file: A boolean value to indicate whether the conversion should be recursive

    Returns:
        None
    """
    with open(input_file, 'r') as file:
        content = file.read()

    content = content.replace("ekern", "kern")
    content = content.replace("·", "")

    with open(output_file, 'w') as file:
        file.write(content)


def kern_to_ekern(input_file, output_file) -> None:
    """
    Convert one .krn file to .ekrn file

    Args:
        input_file: The path to the input directory
        output_file: A boolean value to indicate whether the conversion should be recursive

    Returns:
        None
    """
    raise NotImplementedError("Not implemented yet")


