from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union


def _write(path: Union[str, Path], content: str) -> None:
    """
    Store content in a file.

    Args:
        path (str): Path to the file.
        content (str): Content to be stored in the file.

    Returns: None

    """
    if not os.path.exists(os.path.dirname(Path(path).absolute())):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'w+') as f:
        f.write(content)


def find_all_files(
        path: Path,
        extension: Optional[str] = None) -> list:
    """
    Find all files with the given extension in the given directory.
    Args:
        path (str): Path to the directory where the files are located.
        extension (Optional[str]): Extension of the files to be found. If None, all files are returned.

    Returns (List[str]): List of paths to the found files.

    Examples:
        >>> find_all_files('/kern_files', 'krn')
        ...

        >>> find_all_files('/files' )
        ...
    """
    p = Path(path)
    if extension is None:
        return list(p.glob('**/*'))
    else:
        return list(p.glob(f'**/*.{extension}'))
