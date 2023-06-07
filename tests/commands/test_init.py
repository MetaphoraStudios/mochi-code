"""Test the init command."""

import argparse
import pathlib
from unittest import TestCase
from unittest.mock import MagicMock, patch

from mochi_code.commands.exceptions import MochiCannotContinue
from mochi_code.commands.init import run_init_command


class TestSetupInitArguments(TestCase):
    """Test the setup_init_arguments function."""


class TestRunInitCommand(TestCase):
    """Test the run_init_command function."""

    @patch("mochi_code.code.mochi_config.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    def test_it_raises_if_already_initialized(self, search_mock: MagicMock,
                                              mock_init: MagicMock) -> None:
        """Test that the function raises if the project is already initialized.
        """
        test_path = pathlib.Path("/some/path")
        search_mock.return_value = test_path / ".mochi"
        mock_init.return_value = None

        with patch.object(pathlib.Path, "cwd",
                          lambda: pathlib.Path("/some/path")):
            error_pattern = rf".*'{test_path}'."
            with self.assertRaisesRegex(MochiCannotContinue, error_pattern):
                run_init_command(argparse.Namespace())

    def test_it_calls_init(self) -> None:
        """Test that the function calls init with the project path."""
        raise NotImplementedError()
