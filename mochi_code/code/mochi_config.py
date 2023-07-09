"""Module for handling mochi config files."""

import pathlib
from typing import Optional

from mochi_code.code import ProjectDetails

MOCHI_DIR_NAME = ".mochi"


def search_mochi_config(
        start_path: pathlib.Path,
        root_path: Optional[pathlib.Path] = None) -> Optional[pathlib.PurePath]:
    """Find the existing mochi config file if it exists.
    
    This will search up the directory tree from the provided path until it finds
    a mochi config file or reaches the root directory.

    Args:
        start_path (pathlib.Path): The path to start searching from.
        root_path (Optional[pathlib.Path], optional): The root path to stop.

    Returns:
        Optional[pathlib.PurePath]: The path to the mochi config dir or None if
            it does not exist.
    """

    def is_root(path: pathlib.Path) -> bool:
        return path in [path.parent, root_path]

    current_path = start_path
    if current_path.is_file():
        raise ValueError("Cannot search for mochi config in a file.")

    mochi_path = current_path / MOCHI_DIR_NAME

    while not is_root(current_path) and not mochi_path.exists():
        current_path = current_path.parent
        mochi_path = current_path / MOCHI_DIR_NAME

    return mochi_path if mochi_path.exists() else None


def create_config(project_path: pathlib.Path,
                  project_details: ProjectDetails) -> pathlib.PurePath:
    """Create the mochi config file for the project.

    Args:
        project_path (pathlib.Path): The path to the project to initialize (the
        config folder will be created here).
        project_details (ProjectDetails): The details of the project to save in
        the config.

    Returns:
        pathlib.PurePath: The path to the mochi config dir.
    """
    if project_path.is_file():
        raise ValueError("Cannot create a mochi config in a file.")

    mochi_root = project_path / MOCHI_DIR_NAME
    mochi_root.mkdir(parents=True)

    project_details_path = mochi_root / "project_details.json"
    with open(project_details_path, "w",
              encoding="utf-8") as project_details_file:
        project_details_file.write(project_details.json())

    return mochi_root
