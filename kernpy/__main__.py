import argparse
import sys
import os

from kernpy import polish_scores, ekern_to_krn


# drizo: TODO ¿?


def create_parser() -> argparse.ArgumentParser:
    """
    Create a parser for the command line arguments.

    Examples:
        >>> parser = create_parser()
        >>> args = parser.parse_args()
        >>> print(args.verbose)


    Returns:
        argparse.ArgumentParser: The parser object
    """
    parser = argparse.ArgumentParser(description="kernpy")

    # Boolean option
    parser.add_argument('--verbose', default=1, help='Enable verbose mode')

    # Integer option
    parser.add_argument('--num_iterations', type=int, default=10, help='Number of iterations')

    # ekern to kern
    kern_parser = parser.add_argument_group('Kern Parser options')
    kern_parser.add_argument('--ekern2kern', action='store_true', help='ekern to kern one file')
    if '--ekern2kern' in sys.argv:
        kern_parser.add_argument('--input_path', required=True, type=str, help='Input file or directory path. Employ -r to use recursive mode')
        kern_parser.add_argument('-r', '--recursive', required=False, action='store_true', help='Recursive mode')

    # Polish operations
    # Create a group for optional arguments
    polish_args = parser.add_argument_group('Polish Exporter options')
    polish_args.add_argument('--polish', action='store_true', help='Enable Polish Exporter')
    # Add the required flags, but only if --polish exists
    if '--polish' in sys.argv:
        polish_args.add_argument('--input_directory', required=True, type=str, help='Input directory path')
        polish_args.add_argument('--output_directory', required=True, type=str, help='Output directory path')
        polish_args.add_argument('--instrument', required=False, type=str, help='Instrument name')

    return parser


def handle_polish_exporter(args) -> None:
    """
    Handle the Polish options.

    Args:
        args: The parsed arguments

    Returns:
        None
    """
    # TODO: Add instrument argument to download_polish_dataset.main
    if args.instrument:
        print("Instrument:", args.instrument)
    else:
        print("Instrument: Not specified")

    polish_scores.download_polish_dataset.main(args.input_directory, args.output_directory)


def handle_ekern2kern(args) -> None:
    """
    Handle the ekern2kern options.

    Args:
        args: The parsed arguments

    Returns:
        None
    """
    if not args.recursive:
        ekern_to_krn(args.input_path, args.input_path.replace("ekrn", "krn"))
        if int(args.verbose) > 0:
            print(f"New kern generated in {args.input_path.replace('ekrn', 'krn')}")
        return

    # Recursive mode
    for root, dirs, files in os.walk(args.input_path):
        for directory in dirs:
            files = os.listdir(os.path.join(root, directory))
            for filename in files:
                if filename.endswith(".ekrn"):
                    if int(args.verbose) > 0:
                        print("New kern: ", os.path.join(root, directory, filename))
                    ekern_to_krn(os.path.join(root, directory, filename),
                                 os.path.join(root, directory, filename.replace("ekrn", "krn")))


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Accessing the values of the options
    print(f"All arguments: \n{50 * '*'}")
    for key, value in vars(args).items():
        print(key, value)
    print(f"{50 * '*'}\n")

    if args.polish:
        handle_polish_exporter(args)
    if args.ekern2kern:
        handle_ekern2kern(args)


if __name__ == "__main__":
    main()
