"""Test the project prompts."""
import pathlib
from unittest import TestCase
from unittest.mock import MagicMock, patch

from mochi_code.code.mochi_config import get_config_path
from mochi_code.code import ProjectDetailsWithDependencies
from mochi_code.prompts.project_prompts import get_project_prompt


class TestGetProjectPrompt(TestCase):
    """Test the run_init_command function."""

    @patch("mochi_code.prompts.project_prompts.load_project_details")
    @patch("mochi_code.prompts.project_prompts.search_mochi_config")
    def test_it_returns_a_prompt(
        self,
        mock_search: MagicMock,
        mock_load: MagicMock,
    ) -> None:
        """Test that the function raises if the project is already initialized.
        """
        mock_search.return_value = get_config_path(pathlib.Path("/some/"))
        mock_load.return_value = ProjectDetailsWithDependencies(
            language="python",
            config_file="mochi.toml",
            package_manager="pip",
            dependencies=["numpy", "pandas"])

        prompt = get_project_prompt(pathlib.Path("/some/path"))

        self.assertIsNotNone(prompt)
        self.assertIn("python", prompt or "")
        self.assertIn("numpy", prompt or "")
        self.assertIn("pandas", prompt or "")
        self.assertIn("pip", prompt or "")
        self.assertNotIn("mochi.toml", prompt or "")

    @patch("mochi_code.prompts.project_prompts.load_project_details")
    @patch("mochi_code.prompts.project_prompts.search_mochi_config")
    def test_it_returns_none_if_no_config(
        self,
        mock_search: MagicMock,
        mock_load: MagicMock,
    ) -> None:
        """Test that the function raises if the project is already initialized.
        """
        # We're keeping the details here to double check it passes for the right
        # reasons.
        mock_search.return_value = None
        mock_load.return_value = ProjectDetailsWithDependencies(
            language="python",
            config_file="mochi.toml",
            package_manager="pip",
            dependencies=["numpy", "pandas"])

        prompt = get_project_prompt(pathlib.Path("/some/path"))

        self.assertIsNone(prompt)
