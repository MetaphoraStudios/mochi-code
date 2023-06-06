"""Test the init command."""

import pathlib
import tempfile
from unittest import TestCase
from unittest.mock import patch

from mochi_code.commands.init import _get_existing_mochi_config


class TestSetupInitArguments(TestCase):
    """Test the setup_init_arguments function."""


class TestRunInitCommand(TestCase):
    """Test the run_init_command function."""


class TestGetExistingMochiConfig(TestCase):
    """Test the _get_existing_mochi_config function."""

    def setUp(self) -> None:
        # Create a temporary folder as root
        self._root_dir = tempfile.TemporaryDirectory()
        root_path = pathlib.Path(self._root_dir.name)
        self._mock_path = patch.object(pathlib.Path, "root", root_path)
        self._mock_path.start()

    def tearDown(self) -> None:
        self._mock_path.stop()
        self._root_dir.cleanup()

    def test_starting_at_root_not_found(self) -> None:
        """Test that the function returns None when starting at the root and
        there isn't a mochi config."""
        root_path = pathlib.Path(self._root_dir.name)

        self.assertIsNone(_get_existing_mochi_config(root_path))

    def test_starting_at_root_found(self) -> None:
        """Test that the function returns root path when starting at the root
        and there is a mochi config."""
        root_path = pathlib.Path(self._root_dir.name)
        mochi_path = root_path / ".mochi"
        mochi_path.mkdir()

        self.assertEqual(_get_existing_mochi_config(root_path), root_path)

    def test_finds_in_parent(self) -> None:
        """Test that the function returns the parent path when there is a mochi
        config in the parent."""
        root_path = pathlib.Path(self._root_dir.name)
        subfolder_path = root_path / "subfolder"
        subfolder_path.mkdir()
        mochi_path = subfolder_path / ".mochi"
        mochi_path.mkdir()
        children_path = subfolder_path / "child1/child2"
        children_path.mkdir(parents=True)

        self.assertEqual(_get_existing_mochi_config(children_path),
                         subfolder_path)

    def test_finds_starting_within_mochi_config(self) -> None:
        """Test that the function returns the parent if it starts from within
        the .mochi path."""
        root_path = pathlib.Path(self._root_dir.name)
        subfolder_path = root_path / "subfolder"
        subfolder_path.mkdir()
        mochi_path = subfolder_path / ".mochi"
        mochi_path.mkdir()

        self.assertEqual(_get_existing_mochi_config(mochi_path), subfolder_path)

    def test_finds_in_self(self) -> None:
        """Test that the function returns the current path when there is a mochi
        config in the current path."""
        root_path = pathlib.Path(self._root_dir.name)
        subfolder_path = root_path / "subfolder"
        subfolder_path.mkdir()
        mochi_path = subfolder_path / ".mochi"
        mochi_path.mkdir()

        self.assertEqual(_get_existing_mochi_config(subfolder_path),
                         subfolder_path)

    def test_not_found_across_dir_tree(self) -> None:
        """Test that the function returns None when there is no mochi config
        across the directory tree."""
        root_path = pathlib.Path(self._root_dir.name)
        subfolder_path = root_path / "subfolder"
        subfolder_path.mkdir()
        children_path = subfolder_path / "child1/child2/child3"
        children_path.mkdir(parents=True)

        self.assertIsNone(_get_existing_mochi_config(children_path))
