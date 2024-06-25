"""
This module contains the main function for the kernpy package.

Use the following command to run `kernpy` as a module:
```bash
python -m kernpy
```

"""

import argparse
import sys
import os

from kernpy import polish_scores, ekern_to_krn, kern_to_ekern, create_fragments_from_directory


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

    parser.add_argument('--verbose', default=1, help='Enable verbose mode')


    # ekern to kern
    kern_parser = parser.add_argument_group('Kern Parser options')
    kern_parser.add_argument('--ekern2kern', action='store_true', help='Convert file from ekern to kern. [-r]')
    kern_parser.add_argument('--kern2ekern', action='store_true', help='Convert file from kern to ekern. [-r]')

    if '--ekern2kern' in sys.argv:
        kern_parser.add_argument('--input_path', required=True, type=str,
                                 help='Input file or directory path. Employ -r to use recursive mode')
        kern_parser.add_argument('--output_path', required=False, type=str, help='Output file or directory path')
        kern_parser.add_argument('-r', '--recursive', required=False, action='store_true', help='Recursive mode')

    if '--kern2ekern' in sys.argv:
        kern_parser.add_argument('--input_path', required=True, type=str,
                                 help='Input file or directory path. Employ -r to use recursive mode')
        kern_parser.add_argument('--output_path', required=False, type=str, help='Output file or directory path')
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
        polish_args.add_argument('--kern_type', required=False, type=str, help='Kern type: "krn" or "ekrn"')
        polish_args.add_argument('--kern_spines_filter', required=False, type=str, help='How many kern spines scores will be exported. A number greater than 0', default=None)
        polish_args.add_argument('--remove_empty_dirs', required=False, action='store_true', help='Remove empty directories after exporting the scores', default=True)

    # Generate fragments
    # Create a group for optional arguments
    generate_fragments = parser.add_argument_group('Generate Fragments options')
    generate_fragments.add_argument('--generate_fragments', action='store_true', help='Enable Generate Fragments')
    if '--generate_fragments' in sys.argv:
        generate_fragments.add_argument('--input_directory', required=True, type=str, help='Input directory path')
        generate_fragments.add_argument('--output_directory', required=True, type=str, help='Output directory path')
        generate_fragments.add_argument('--log_file', required=True, type=str, help='Log file path')
        generate_fragments.add_argument('--check_file_extension', required=False, action='store_true', help='Check file extension', default=True)
        generate_fragments.add_argument('--offset', required=True, type=int, help='Offset', default=1)
        generate_fragments.add_argument('--num_processes', required=True, type=int, help='Number of processes')
        generate_fragments.add_argument('--mean', required=True, type=float, help='Mean')
        generate_fragments.add_argument('--std_dev', required=True, type=float, help='Standard deviation')

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

    polish_scores.download_polish_dataset.main(
        input_directory=args.input_directory,
        output_directory=args.output_directory,
        kern_spines_filter=args.kern_spines_filter,
        exporter_kern_type=args.kern_type,
        remove_empty_directories=args.remove_empty_dirs
    )


def handle_ekern2kern(args) -> None:
    """
    Handle the ekern2kern options.

    Args:
        args: The parsed arguments

    Returns:
        None
    """
    if not args.output_path:
        args.output_path = args.input_path.replace("ekrn", "krn")

    if not args.recursive:
        ekern_to_krn(args.input_path, args.output_path)
        if int(args.verbose) > 0:
            print(f"New kern generated in {args.output_path}")
        return

    # Recursive mode
    for root, dirs, files in os.walk(args.input_path):
        for directory in dirs:
            files = os.listdir(os.path.join(root, directory))
            for filename in files:
                if filename.endswith(".ekrn"):
                    if int(args.verbose) > 0:
                        print("New kern: ", os.path.join(root, directory, filename))
                    try:
                        ekern_to_krn(os.path.join(root, directory, filename),
                                     os.path.join(root, directory, filename.replace(".ekrn", ".krn")))
                    except Exception as e:
                        if int(args.verbose) > 0:
                            print(f"An error occurred converting:{filename}:{e}", file=sys.stderr)


def handle_kern2ekern(args) -> None:
    """
    Handle the kern2ekern options.

    Args:
        args: The parsed arguments

    Returns:
        None
    """
    if not args.output_path:
        args.output_path = args.input_path.replace("krn", "ekrn")

    if not args.recursive:
        kern_to_ekern(args.input_path, args.output_path)
        if int(args.verbose) > 0:
            print(f"New ekern generated in {args.output_path}")
        return

    # Recursive mode
    for root, dirs, files in os.walk(args.input_path):
        for directory in dirs:
            files = os.listdir(os.path.join(root, directory))
            for filename in files:
                if filename.endswith(".krn"):
                    if int(args.verbose) > 0:
                        print("New ekern: ", os.path.join(root, directory, filename))
                    try:
                        kern_to_ekern(os.path.join(root, directory, filename),
                                      os.path.join(root, directory, filename.replace(".krn", ".ekrn")))
                    except Exception as e:
                        if int(args.verbose) > 0:
                            print(f"An error occurred converting:{filename}:{e}", file=sys.stderr)


def handle_generate_fragments(args) -> None:
    """
    Handle the generate_fragments options.

    Args:
        args: The parsed arguments

    Returns:
        None
    """
    create_fragments_from_directory(args.input_directory, args.output_directory, args.log_file,
                                    check_file_extension=args.check_file_extension, offset=args.offset,
                                    verbose=args.verbose, num_processes=args.num_processes, mean=args.mean,
                                    std_dev=args.std_dev)


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Accessing the values of the options
    if int(args.verbose) > 2:
        print(f"All arguments: \n{50 * '*'}")
        for key, value in vars(args).items():
            print(key, value)
        print(f"{50 * '*'}\n")

    if args.polish:
        handle_polish_exporter(args)
    if args.ekern2kern:
        handle_ekern2kern(args)
    if args.kern2ekern:
        handle_kern2ekern(args)
    if args.generate_fragments:
        handle_generate_fragments(args)


if __name__ == "__main__":
    main()

