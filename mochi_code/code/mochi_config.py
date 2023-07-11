"""Module for handling mochi config files."""

import pathlib
import json
from typing import Optional, TypeVar

from mochi_code.code import ProjectDetailsWithDependencies

MOCHI_DIR_NAME = ".mochi"
PROJECT_DETAILS_FILE_NAME = "project_details.json"

_PathT = TypeVar("_PathT", pathlib.Path, pathlib.PurePath)


def get_config_path(root_path: _PathT) -> _PathT:
    """Get the path to the mochi config directory.

    Args:
        root_path (_PathT): The root path to the project.

    Returns:
        _PathT: The path to the mochi config directory.
    """
    return root_path / MOCHI_DIR_NAME


def get_project_details_path(config_path: _PathT) -> _PathT:
    """Get the path to the project details file.

    Args:
        root_path (_PathT): The root path to the project.

    Returns:
        _PathT: The path to the project details file.
    """
    return config_path / PROJECT_DETAILS_FILE_NAME


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

    mochi_path = get_config_path(current_path)

    while not is_root(current_path) and not mochi_path.exists():
        current_path = current_path.parent
        mochi_path = get_config_path(current_path)

    return mochi_path if mochi_path.exists() else None


def create_config(
        project_path: pathlib.Path,
        project_details: ProjectDetailsWithDependencies) -> pathlib.PurePath:
    """Create the mochi config file for the project.

    Args:
        project_path (pathlib.Path): The path to the project to initialize (the
        config folder will be created here).
        project_details (ProjectDetailsWithDependencies): The details of the 
        project to save in the config.

    Returns:
        pathlib.PurePath: The path to the mochi config dir.
    """
    if project_path.is_file():
        raise ValueError("Cannot create a mochi config in a file.")

    mochi_root = get_config_path(project_path)
    mochi_root.mkdir(parents=True)

    project_details_path = get_project_details_path(mochi_root)
    save_project_details(project_details_path, project_details)

    return mochi_root


def save_project_details(
        project_details_path: _PathT,
        project_details: ProjectDetailsWithDependencies) -> None:
    """Save the project details to the mochi config file. This will overwrite!

    Args:
        project_details_path (_PathT): The path to the project details json 
        file.
        project_details (ProjectDetailsWithDependencies): The details of the 
        project to save in the config.
    """
    with open(project_details_path, "w",
              encoding="utf-8") as project_details_file:
        project_details_file.write(project_details.json())


def load_project_details(
        project_details_path: _PathT) -> ProjectDetailsWithDependencies:
    """Load the project details from the mochi config file.

    Args:
        project_details_path (_PathT): The path to the project details file.

    Returns:
        ProjectDetailsWithDependencies: The project details loaded from the 
        config.
    """
    with open(project_details_path, "r",
              encoding="utf-8") as project_details_file:
        return ProjectDetailsWithDependencies(**json.load(project_details_file))
