"""The init command. This command is used to initialize Mochi for a new 
project."""

import argparse
import pathlib
from typing import Optional


def setup_init_arguments(parser: argparse.ArgumentParser) -> None:
    """Setup the arguments for the init command.

    Args:
        parser (argparse.ArgumentParser): The parser to add the arguments to.
    """
    # Nothing to do here yet.


def run_init_command(args: argparse.Namespace) -> None:
    """Run the init command with the provided arguments."""
    # Arguments should be validated by the parser.
    init()


def init() -> None:
    """Run the init command."""
    raise NotImplementedError()


def _get_existing_mochi_config(
        path: pathlib.Path) -> Optional[pathlib.PurePath]:
    """Get the existing mochi config file if it exists.
    This will search up the directory tree from the provided path until it finds
    a mochi config file or reaches the root directory.

    Args:
        path (pathlib.Path): The path to start searching from.

    Returns:
        Optional[pathlib.PurePath]: The path to the mochi config file or None if
            it does not exist.
    """
    current_path = path
    root_path = pathlib.Path.root

    while current_path != root_path and not _has_mochi_config(current_path):
        current_path = current_path.parent

    return current_path if _has_mochi_config(current_path) else None


def _has_mochi_config(path: pathlib.Path) -> bool:
    """Return True if the path contains a mochi config, False otherwise."""
    return (path / ".mochi").exists()
