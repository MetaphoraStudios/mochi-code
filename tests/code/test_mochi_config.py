"""Test the mochi_config module."""

import pathlib
import tempfile
import json
from unittest import TestCase
from mochi_code.code import ProjectDetailsWithDependencies

from mochi_code.code.mochi_config import (PROJECT_DETAILS_FILE_NAME,
                                          create_config, load_project_details,
                                          search_mochi_config, MOCHI_DIR_NAME,
                                          save_project_details)


class TestSearchMochiConfig(TestCase):
    """Test the search_mochi_config function."""

    def setUp(self) -> None:
        # Create a temporary folder as root
        self._root_dir = tempfile.TemporaryDirectory()
        self._root_path = pathlib.Path(self._root_dir.name)

    def tearDown(self) -> None:
        self._root_dir.cleanup()

    def test_raises_if_start_path_is_a_file(self) -> None:
        """Test that the function raises a ValueError if the start path is a
        file."""
        file_path = self._root_path / "file"
        file_path.touch()

        with self.assertRaises(ValueError):
            search_mochi_config(file_path, self._root_path)

    def test_starting_at_root_not_found(self) -> None:
        """Test that the function returns None when starting at the root and
        there isn't a mochi config."""
        self.assertIsNone(search_mochi_config(self._root_path, self._root_path))

    def test_starting_at_root_found(self) -> None:
        """Test that the function returns root path when starting at the root
        and there is a mochi config."""
        mochi_path = self._root_path / MOCHI_DIR_NAME
        mochi_path.mkdir()

        self.assertEqual(search_mochi_config(self._root_path, self._root_path),
                         mochi_path)

    def test_finds_in_parent(self) -> None:
        """Test that the function returns the parent path when there is a mochi
        config in the parent."""
        subfolder_path = self._root_path / "subfolder"
        subfolder_path.mkdir()
        mochi_path = subfolder_path / MOCHI_DIR_NAME
        mochi_path.mkdir()
        children_path = subfolder_path / "child1/child2"
        children_path.mkdir(parents=True)

        self.assertEqual(search_mochi_config(children_path, self._root_path),
                         mochi_path)

    def test_finds_starting_within_mochi_config(self) -> None:
        """Test that the function returns the parent if it starts from within
        the config path."""
        subfolder_path = self._root_path / "subfolder"
        subfolder_path.mkdir()
        mochi_path = subfolder_path / MOCHI_DIR_NAME
        mochi_path.mkdir()

        self.assertEqual(search_mochi_config(mochi_path, self._root_path),
                         mochi_path)

    def test_finds_in_self(self) -> None:
        """Test that the function returns the current path when there is a mochi
        config in the current path."""
        subfolder_path = self._root_path / "subfolder"
        subfolder_path.mkdir()
        mochi_path = subfolder_path / MOCHI_DIR_NAME
        mochi_path.mkdir()

        self.assertEqual(search_mochi_config(subfolder_path, self._root_path),
                         mochi_path)

    def test_not_found_across_dir_tree(self) -> None:
        """Test that the function returns None when there is no mochi config
        across the directory tree."""
        subfolder_path = self._root_path / "subfolder"
        subfolder_path.mkdir()
        children_path = subfolder_path / "child1/child2/child3"
        children_path.mkdir(parents=True)

        self.assertIsNone(search_mochi_config(children_path, self._root_path))

    def test_global_root_works(self) -> None:
        """Test that the function works when the root is the global root."""
        self.assertIsNone(
            search_mochi_config(pathlib.Path(self._root_path.root)))


class TestCreateConfig(TestCase):
    """Test the create_config function."""

    def setUp(self) -> None:
        # Create a temporary folder as root
        self._root_dir = tempfile.TemporaryDirectory()
        self._root_path = pathlib.Path(self._root_dir.name)
        self._project_details = ProjectDetailsWithDependencies(
            language="python",
            config_file="testing.yml",
            package_manager="pip",
            dependencies=["numpy", "pandas"])

    def tearDown(self) -> None:
        self._root_dir.cleanup()

    def test_creates_config(self) -> None:
        """Test that the function creates the mochi config folder."""
        mochi_path = self._root_path / MOCHI_DIR_NAME

        self.assertFalse(mochi_path.exists())

        config_path = create_config(self._root_path, self._project_details)

        self.assertTrue(mochi_path.exists())
        self.assertEqual(config_path, mochi_path)

    def test_raises_if_not_directory(self) -> None:
        """Test that the function raises a ValueError if the path is not a
        directory."""
        root_path = self._root_path / "file.txt"
        root_path.touch()

        with self.assertRaises(ValueError):
            create_config(root_path, self._project_details)

    def test_does_not_override_existing(self) -> None:
        """Test that the function does not override existing configs."""
        mochi_path = self._root_path / MOCHI_DIR_NAME
        mochi_path.mkdir()
        test_file_path = mochi_path / "test.txt"
        test_file_path.touch()

        assert test_file_path.exists()

        with self.assertRaises(FileExistsError):
            create_config(self._root_path, self._project_details)

        assert test_file_path.exists()

    def test_writes_project_details(self) -> None:
        """Test that the function writes the project details to the config
        file."""
        mochi_path = self._root_path / MOCHI_DIR_NAME

        self.assertFalse(mochi_path.exists())

        config_path = create_config(self._root_path, self._project_details)

        self.assertTrue(mochi_path.exists())
        self.assertEqual(config_path, mochi_path)

        with open(config_path / PROJECT_DETAILS_FILE_NAME,
                  encoding="utf-8") as config_file:
            project_details = json.load(config_file)

        self.assertEqual(project_details, self._project_details)


class TestSaveAndLoadProjectDetails(TestCase):
    """Test the save_project_details and load_project_details functions."""

    def setUp(self) -> None:
        # Create a temporary folder as root
        self._root_dir = tempfile.TemporaryDirectory()
        self._root_path = pathlib.Path(self._root_dir.name)
        self._project_details = ProjectDetailsWithDependencies(
            language="typescript",
            config_file="testing.json",
            package_manager="npm",
            dependencies=["react", "redux"])

    def tearDown(self) -> None:
        self._root_dir.cleanup()

    def test_loads_project_details(self) -> None:
        """Test that the function loads the project details from the config
        file."""
        mochi_path = self._root_path / MOCHI_DIR_NAME
        mochi_path.mkdir()
        project_details_path = mochi_path / PROJECT_DETAILS_FILE_NAME

        save_project_details(project_details_path, self._project_details)
        loaded_project_details = load_project_details(project_details_path)

        self.assertEqual(loaded_project_details, self._project_details)

        # Test that it actually updates the values
        new_project_details = ProjectDetailsWithDependencies(
            language="python",
            config_file="testing.yml",
            package_manager="pip",
            dependencies=["numpy", "pandas"])

        save_project_details(project_details_path, new_project_details)
        loaded_project_details = load_project_details(project_details_path)

        self.assertEqual(loaded_project_details, new_project_details)

    def test_raises_config_is_dir_when_saving(self) -> None:
        """Test that the function raises if the path is a folder."""
        with self.assertRaises(IsADirectoryError):
            save_project_details(self._root_path, self._project_details)

    def test_raises_if_no_config_folder_when_saving(self) -> None:
        """Test that the function raises if there is no config folder to save 
        to."""
        project_details_path = self._root_path / "invalid/project_details.json"
        with self.assertRaises(FileNotFoundError):
            save_project_details(project_details_path, self._project_details)

    def test_raises_if_no_config_when_loading(self) -> None:
        """Test that the function raises if there is no config file to load."""
        with self.assertRaises(IsADirectoryError):
            load_project_details(self._root_path)

        with self.assertRaises(FileNotFoundError):
            load_project_details(self._root_path /
                                 "invalid/project_details.json")
