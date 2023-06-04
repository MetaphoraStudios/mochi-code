"""The init command. This command is used to initialize Mochi for a new 
project."""

import argparse


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
