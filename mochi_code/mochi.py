"""This file sets up the mochi subcommands, validates cli user input and calls
out to the subcommands.
It serves as a router to the different subcommands.
"""

import argparse
from typing import Callable

from mochi_code.commands import (run_ask_command, run_init_command,
                                 setup_ask_arguments, setup_init_arguments)

CommandType = Callable[[argparse.Namespace], None]


def cli():
    """Setup the cli environment and run the selected subcommand."""
    root_parser = argparse.ArgumentParser(prog="mochi")
    subparsers = root_parser.add_subparsers(title="subcommands",
                                            dest="subcommand")

    init_name = "init"
    init_parser = subparsers.add_parser(init_name,
                                        help="Initialize mochi for a project.")
    setup_init_arguments(init_parser)

    ask_name = "ask"
    ask_parser = subparsers.add_parser(ask_name,
                                       help="Ask a question to mochi.")
    setup_ask_arguments(ask_parser)

    args = root_parser.parse_args()

    if args.subcommand == init_name:
        _run_command(run_init_command, args, init_parser)
    elif args.subcommand == ask_name:
        _run_command(run_ask_command, args, ask_parser)
    else:
        print("Here will live the chat mode, but not yet...")
        root_parser.print_help()


def _run_command(
    command: CommandType,
    args: argparse.Namespace,
    command_parser: argparse.ArgumentParser,
):
    """Run the command and exit if an error occurred."""
    try:
        command(args)
    except Exception as error:  # pylint: disable=broad-except
        print(f"😭 an issue occurred running your command: {error}")
        command_parser.exit(1)


if __name__ == "__main__":
    cli()
