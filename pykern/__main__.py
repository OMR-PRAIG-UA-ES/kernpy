import argparse
import sys

from pykern import polish_scores


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
    parser = argparse.ArgumentParser(description="pyKern")

    # Boolean option
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')

    # Integer option
    parser.add_argument('--num_iterations', type=int, default=10, help='Number of iterations')

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
    if args.polish:
        # TODO: Add instrument argument to download_polish_dataset.main
        if args.instrument:
            print("Instrument:", args.instrument)
        else:
            print("Instrument: Not specified")

        polish_scores.download_polish_dataset.main(args.input_directory, args.output_directory)


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Accessing the values of the options
    print(f"{50 * '*'}")
    for key, value in vars(args).items():
        print(key, value)
    print(f"{50 * '*'}\n")

    if args.polish:
        handle_polish_exporter(args)


if __name__ == "__main__":
    main()
