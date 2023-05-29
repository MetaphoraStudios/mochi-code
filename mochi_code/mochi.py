"""This file sets up the mochi subcommands, validates cli user input and calls
out to the subcommands.

Subcommands are setup by adding a setup function to the commands list, which
will add the sub parsers but also return the command function to run when the
user calls the subcommand.

The setup function tells the cli what subcommand name to match, what parser to
use and what function to call when the subcommand is called.
"""

import argparse
from typing import Callable

from mochi_code.commands import setup_ask_command


CommandSetupType = Callable[
    [
        argparse._SubParsersAction[argparse.ArgumentParser],
    ],
    tuple[str, argparse.ArgumentParser, Callable],
]

# commands includes a list of setup functions for each command.
# The setup function is responsible for adding the expected arguments for the
# command.
commands: list[CommandSetupType] = [setup_ask_command]


def cli():
    """Setup the cli environment and run the selected subcommand."""
    root_parser = argparse.ArgumentParser(prog="mochi")
    subparsers = root_parser.add_subparsers(title="subcommands", dest="subcommand")

    command_parsers = [
        parser for setup in commands if (parser := setup(subparsers)) is not None
    ]

    args = root_parser.parse_args()

    for command_name, command_parser, command in command_parsers:
        if args.subcommand == command_name:
            command(command_parser)
            break
    else:
        root_parser.print_help()


if __name__ == "__main__":
    cli()
