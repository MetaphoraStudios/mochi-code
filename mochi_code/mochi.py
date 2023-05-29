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
from typing import Any

from mochi_code.commands import setup_ask_command


CommandSetupType = Callable[
    [
        Any,
    ],
    tuple[str, argparse.ArgumentParser, Callable[[argparse.Namespace], None]],
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
            _run_command(command, args, command_parser)
            break
    else:
        root_parser.print_help()


def _run_command(
    command, args: argparse.Namespace, command_parser: argparse.ArgumentParser
):
    """Run the command and exit if an error occurred."""
    try:
        command(args)
    except Exception as error:  # pylint: disable=broad-except
        print(f"issue: {error}")
        command_parser.print_help()
        command_parser.exit(1)


if __name__ == "__main__":
    cli()
