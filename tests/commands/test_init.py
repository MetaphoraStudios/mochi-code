"""Test the init command."""

import argparse
import pathlib
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock, patch

from mochi_code.code.mochi_config import MOCHI_DIR_NAME, load_project_details
from mochi_code.commands.exceptions import MochiCannotContinue
from mochi_code.commands.init import (ProjectDetails,
                                      ProjectDetailsWithDependencies, init,
                                      run_init_command)


class TestRunInitCommand(TestCase):
    """Test the run_init_command function."""

    @patch("mochi_code.commands.init.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    @patch("mochi_code.commands.init.pathlib.Path.cwd")
    def test_it_raises_if_already_initialized(
        self,
        mock_cwd: MagicMock,
        mock_init: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        """Test that the function raises if the project is already initialized.
        """
        start_path = pathlib.Path("/some/path")

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
    def test_it_forces_config_creation(
        self,
        mock_cwd: MagicMock,
        mock_init: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        """Test that the function does not raise with the force argument.
        """
        start_path = pathlib.Path("/some/path")

        mock_cwd.return_value = start_path
        mock_init.return_value = None
        mock_search.return_value = start_path.parent / MOCHI_DIR_NAME

        run_init_command(argparse.Namespace(force=True))
        mock_init.assert_called_once()

    @patch("mochi_code.commands.init.search_mochi_config")
    @patch("mochi_code.commands.init.init")
    @patch("mochi_code.commands.init.pathlib.Path.cwd")
    def test_it_does_not_override_existing(
        self,
        mock_cwd: MagicMock,
        mock_init: MagicMock,
        mock_search: MagicMock,
    ) -> None:
        """Test that the function does not create a new config if one already
        exists on the current path."""
        start_path = pathlib.Path("/some/path")

        mock_cwd.return_value = start_path
        mock_init.return_value = None
        mock_search.return_value = start_path / MOCHI_DIR_NAME

        run_init_command(argparse.Namespace(force=True))
        mock_init.assert_not_called()

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

    @patch("mochi_code.commands.init._get_dependencies_list")
    @patch("mochi_code.commands.init._get_project_details")
    def test_it_creates_new_config(self, mock_project_details: MagicMock,
                                   mock_dependencies_list: MagicMock) -> None:
        """Test that the function creates a new config if one didn't exist."""
        mock_project_details.return_value = ProjectDetails(
            language="python",
            config_file="pyproject.toml",
            package_manager="poetry",
        )
        mock_dependencies_list.return_value = ["mypy", "black"]

        self.assertFalse(self._mochi_path.exists())

        init(self._root_path)

        self.assertTrue(self._mochi_path.exists())
        mock_dependencies_list.assert_called_once_with(
            pathlib.Path(mock_project_details.return_value.config_file))

        loaded_project_details = load_project_details(self._mochi_path /
                                                      "project_details.json")

        expected_project_details = ProjectDetailsWithDependencies(
            **mock_project_details.return_value.dict(),
            dependencies=mock_dependencies_list.return_value,
        )
        self.assertEqual(loaded_project_details, expected_project_details)

    @patch("mochi_code.commands.init._get_dependencies_list")
    @patch("mochi_code.commands.init._get_project_details")
    def test_does_not_create_config_if_failed(
            self, mock_project_details: MagicMock,
            mock_dependencies_list: MagicMock) -> None:
        """Test that the function does not create a new config if it fails to
        gather the project details."""
        mock_project_details.side_effect = ValueError("Some error")

        self.assertFalse(self._mochi_path.exists())

        with self.assertRaises(ValueError):
            init(self._root_path)

        self.assertFalse(self._mochi_path.exists())
        mock_dependencies_list.assert_not_called()
