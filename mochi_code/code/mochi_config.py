"""Module for handling mochi config files."""

import pathlib
from typing import Optional

CONFIG_DIR_NAME = ".mochi"


def search_mochi_config(start_path: pathlib.Path) -> Optional[pathlib.PurePath]:
    """Find the existing mochi config file if it exists.
    
    This will search up the directory tree from the provided path until it finds
    a mochi config file or reaches the root directory.

    Args:
        path (pathlib.Path): The path to start searching from.

    Returns:
        Optional[pathlib.PurePath]: The path to the mochi config file or None if
            it does not exist.
    """
    current_path = start_path
    mochi_path = (current_path / CONFIG_DIR_NAME)
    root_path = pathlib.Path.root

    while current_path != root_path and not mochi_path.exists():
        current_path = current_path.parent
        mochi_path = (current_path / CONFIG_DIR_NAME)

    return mochi_path if mochi_path.exists() else None
