"""The init command. This command is used to initialize Mochi for a new 
project."""

import argparse
import pathlib

from mochi_code.code.mochi_config import create_config, search_mochi_config
from mochi_code.commands.exceptions import MochiCannotContinue


def setup_init_arguments(parser: argparse.ArgumentParser) -> None:
    """Setup the arguments for the init command.

    Args:
        parser (argparse.ArgumentParser): The parser to add the arguments to.
    """
    parser.add_argument("-f", "--force",
                        action="store_true",
                        help="Force creating the config, without overriding.")


def run_init_command(args: argparse.Namespace) -> None:
    """Run the init command with the provided arguments."""
    # Arguments should be validated by the parser.
    project_path = pathlib.Path.cwd()
    existing_root = search_mochi_config(project_path)

    if not args.force and existing_root is not None:
        raise MochiCannotContinue(
            f"🚫 Mochi is already initialized at '{existing_root.parent}'.")

    if existing_root is not None and existing_root.parent == project_path:
        print("😎 Mochi already exists in this folder, left intact.")
        return

    init(project_path)


def init(project_path: pathlib.Path) -> None:
    """Run the init command.
    
    Args:
        project_path (pathlib.Path): The path to the project to initialize (the
        config folder will be created here).
    """
    print(f"⚙️ Initializing mochi for project '{project_path}'.")
    create_config(project_path)
