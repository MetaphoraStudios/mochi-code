"""Test the init command."""

import argparse
import pathlib
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock, patch

from mochi_code.commands.exceptions import MochiCannotContinue
from mochi_code.commands.init import run_init_command


class TestSetupInitArguments(TestCase):
    """Test the setup_init_arguments function."""


class TestRunInitCommand(TestCase):
    """Test the run_init_command function."""

    @patch("mochi_code.commands.init.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    @patch("mochi_code.commands.init.pathlib.Path.cwd")
    def test_it_raises_if_already_initialized(self, mock_cwd: MagicMock, mock_init: MagicMock,
                                              mock_search: MagicMock, ) -> None:
        """Test that the function raises if the project is already initialized.
        """
        start_path = pathlib.Path("/some/path")

        mock_cwd.return_value = start_path
        mock_init.return_value = None
        mock_search.return_value = start_path / ".mochi"

        error_pattern = rf".*'{start_path}'."
        with self.assertRaisesRegex(MochiCannotContinue, error_pattern):
            run_init_command(argparse.Namespace())
        mock_search.assert_called_once()

    @patch("mochi_code.commands.init.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    @patch("mochi_code.commands.init.pathlib.Path.cwd")
    def test_it_calls_init(self, mock_cwd: MagicMock, mock_init: MagicMock,
                           search_mock: MagicMock) -> None:
        """Test that the function calls init with the project path."""
        start_path = pathlib.Path(tempfile.TemporaryDirectory().name)

        search_mock.return_value = None
        mock_init.return_value = None
        mock_cwd.return_value = start_path

        run_init_command(argparse.Namespace())

        assert mock_init.call_count == 1
        mock_init.assert_called_once_with(start_path)
