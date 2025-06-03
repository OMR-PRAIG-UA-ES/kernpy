"""
This module contains the main function for the kernpy package.

Usage:
    python -m kernpy
"""

import argparse
import sys
from pathlib import Path

from kernpy import polish_scores, ekern_to_krn, kern_to_ekern


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="kernpy CLI tool")

    parser.add_argument('--verbose', type=int, default=1, help='Verbosity level')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--ekern2kern', action='store_true', help='Convert files from ekern to kern')
    group.add_argument('--kern2ekern', action='store_true', help='Convert files from kern to ekern')
    group.add_argument('--polish', action='store_true', help='Run Polish Exporter')
    group.add_argument('--generate_fragments', action='store_true', help='Generate Fragments')

    parser.add_argument('--input_path', type=str, help='Input file or directory')
    parser.add_argument('--output_path', type=str, help='Output file or directory')
    parser.add_argument('-r', '--recursive', action='store_true', help='Enable recursive directory processing')

    # Polish Exporter
    parser.add_argument('--input_directory', type=str, help='Polish: Input directory')
    parser.add_argument('--output_directory', type=str, help='Polish: Output directory')
    parser.add_argument('--instrument', type=str, help='Polish: Instrument name')
    parser.add_argument('--kern_type', type=str, help='Polish: "krn" or "ekrn"')
    parser.add_argument('--kern_spines_filter', type=str, help='Polish: Filter for number of kern spines')
    parser.add_argument('--remove_empty_dirs', action='store_true', help='Polish: Remove empty directories')


    return parser


def find_files(directory: Path, patterns: list[str], recursive: bool = False) -> list[Path]:
    files = []
    for pattern in patterns:
        if recursive:
            files.extend(directory.rglob(pattern))
        else:
            files.extend(directory.glob(pattern))
    return files


def handle_ekern2kern(args):
    input_path = Path(args.input_path)
    output_path = Path(args.output_path) if args.output_path else None

    if input_path.is_file():
        out = output_path or input_path.with_suffix(".krn")
        ekern_to_krn(str(input_path), str(out))
        if args.verbose:
            print(f"Converted: {input_path} → {out}")
        return

    files = find_files(input_path, ["*.ekrn", "*.ekern"], recursive=args.recursive)
    for file in files:
        out = file.with_suffix(".krn")
        try:
            ekern_to_krn(str(file), str(out))
            if args.verbose:
                print(f"Converted: {file} → {out}")
        except Exception as e:
            print(f"Error converting {file}: {e}", file=sys.stderr)


def handle_kern2ekern(args):
    input_path = Path(args.input_path)
    output_path = Path(args.output_path) if args.output_path else None

    if input_path.is_file():
        out = output_path or input_path.with_suffix(".ekrn")
        kern_to_ekern(str(input_path), str(out))
        if args.verbose:
            print(f"Converted: {input_path} → {out}")
        return

    files = find_files(input_path, ["*.krn", "*.kern"], recursive=args.recursive)
    for file in files:
        out = file.with_suffix(".ekrn")
        try:
            kern_to_ekern(str(file), str(out))
            if args.verbose:
                print(f"Converted: {file} → {out}")
        except Exception as e:
            print(f"Error converting {file}: {e}", file=sys.stderr)


def handle_polish_exporter(args):
    if args.verbose:
        print(f"Running Polish Exporter on {args.input_directory} → {args.output_directory}")

    polish_scores.download_polish_dataset.main(
        input_directory=args.input_directory,
        output_directory=args.output_directory,
        kern_spines_filter=args.kern_spines_filter,
        exporter_kern_type=args.kern_type,
        remove_empty_directories=args.remove_empty_dirs,
    )


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.verbose > 2:
        print("Arguments:")
        for key, val in vars(args).items():
            print(f"  {key}: {val}")

    if args.ekern2kern:
        handle_ekern2kern(args)
    elif args.kern2ekern:
        handle_kern2ekern(args)
    elif args.polish:
        handle_polish_exporter(args)


if __name__ == "__main__":
    main()
