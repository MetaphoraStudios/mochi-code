"""Ask command module setup."""
from mochi_code.commands.init import run_init_command, setup_init_arguments
from mochi_code.commands.ask import run_ask_command, setup_ask_arguments

__all__ = [
    "setup_init_arguments", "run_init_command", "setup_ask_arguments",
    "run_ask_command"
]
