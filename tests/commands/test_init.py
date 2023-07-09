"""Test the init command."""

import argparse
import pathlib
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock, patch

from mochi_code.code.mochi_config import MOCHI_DIR_NAME
from mochi_code.commands.exceptions import MochiCannotContinue
from mochi_code.commands.init import run_init_command, init, ProjectDetails


class TestRunInitCommand(TestCase):
    """Test the run_init_command function."""

    @patch("mochi_code.commands.init.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    @patch("mochi_code.commands.init.pathlib.Path.cwd")
    @patch("mochi_code.commands.init._get_project_details")
    def test_it_raises_if_already_initialized(
        self,
        mock_project_details: MagicMock,
        mock_cwd: MagicMock,
        mock_init: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        """Test that the function raises if the project is already initialized.
        """
        start_path = pathlib.Path("/some/path")

        mock_project_details.return_value = ProjectDetails(
            language="python",
            config_file="pyproject.toml",
            package_manager="poetry")
        mock_cwd.return_value = start_path
        mock_init.return_value = None
        mock_search.return_value = start_path / MOCHI_DIR_NAME

        error_pattern = rf".*'{start_path}'."
        with self.assertRaisesRegex(MochiCannotContinue, error_pattern):
            run_init_command(argparse.Namespace(force=False))
        mock_search.assert_called_once()
        mock_init.assert_not_called()

    @patch("mochi_code.commands.init.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    @patch("mochi_code.commands.init.pathlib.Path.cwd")
    @patch("mochi_code.commands.init._get_project_details")
    def test_it_forces_config_creation(
        self,
        mock_project_details: MagicMock,
        mock_cwd: MagicMock,
        mock_init: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        """Test that the function does not raise with the force argument.
        """
        start_path = pathlib.Path("/some/path")

        mock_project_details.return_value = ProjectDetails(
            language="python",
            config_file="pyproject.toml",
            package_manager="poetry")
        mock_cwd.return_value = start_path
        mock_init.return_value = None
        mock_search.return_value = start_path.parent / MOCHI_DIR_NAME

        run_init_command(argparse.Namespace(force=True))
        mock_init.assert_called_once()

    @patch("mochi_code.commands.init.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    @patch("mochi_code.commands.init.pathlib.Path.cwd")
    @patch("mochi_code.commands.init._get_project_details")
    def test_it_does_not_override_existing(
        self,
        mock_project_details: MagicMock,
        mock_cwd: MagicMock,
        mock_init: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        """Test that the function does not create a new config if one already
        exists on the current path."""
        start_path = pathlib.Path("/some/path")

        mock_project_details.return_value = ProjectDetails(
            language="python",
            config_file="pyproject.toml",
            package_manager="poetry")
        mock_cwd.return_value = start_path
        mock_init.return_value = None
        mock_search.return_value = start_path / MOCHI_DIR_NAME

        run_init_command(argparse.Namespace(force=True))
        mock_init.assert_not_called()

    @patch("mochi_code.commands.init.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    @patch("mochi_code.commands.init.pathlib.Path.cwd")
    @patch("mochi_code.commands.init._get_project_details")
    def test_it_calls_init(self, mock_project_details: MagicMock,
                           mock_cwd: MagicMock, mock_init: MagicMock,
                           search_mock: MagicMock) -> None:
        """Test that the function calls init with the project path."""
        start_path = pathlib.Path(tempfile.TemporaryDirectory().name)

        mock_project_details.return_value = ProjectDetails(
            language="python",
            config_file="pyproject.toml",
            package_manager="poetry")
        search_mock.return_value = None
        mock_init.return_value = None
        mock_cwd.return_value = start_path

        run_init_command(argparse.Namespace(force=False))

        assert mock_init.call_count == 1
        mock_init.assert_called_once_with(start_path)


class TestInit(TestCase):
    """Test the init function."""

    def setUp(self) -> None:
        # Create a temporary folder as root
        self._root_dir = tempfile.TemporaryDirectory()
        self._root_path = pathlib.Path(self._root_dir.name)
        self._mochi_path = self._root_path / MOCHI_DIR_NAME

    def tearDown(self) -> None:
        self._root_dir.cleanup()

    def test_it_creates_new_config(self) -> None:
        """Test that the function creates a new config if one didn't exist."""
        assert not self._mochi_path.exists()
        init(self._root_path)
        assert self._mochi_path.exists()
