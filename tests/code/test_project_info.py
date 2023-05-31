"""Tests for the project_info module."""

import os
import tempfile
import unittest
from unittest import mock

from mochi_code.code.project_info import find_project_root


class FindProjectRootTests(unittest.TestCase):
    """Tests for the find_project_root function."""

    def setUp(self):
        # Create a temporary directory.
        self.test_dir = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.root_dir = self.test_dir.name
        self.test_file_name = "root.test"
        # A file we can use to check if we're in the project root.
        file_path = os.path.join(self.root_dir, self.test_file_name)
        with open(file_path, "w", encoding="utf-8"):
            pass

    def tearDown(self):
        # Clean up the temporary directory and files
        self.test_dir.cleanup()

    def test_asserts_max_depth(self):
        """Test that the function asserts the maximum depth.
        Added just to make sure we don't remove the assertion accidentally."""
        with self.assertRaises(AssertionError):
            find_project_root(self.root_dir,
                              max_depth=0,
                              is_root_heuristic=lambda _: False)

        with self.assertRaises(AssertionError):
            find_project_root(self.root_dir,
                              max_depth=-1,
                              is_root_heuristic=lambda _: False)

    def test_stops_search_at_max_depth(self):
        """Test that the search stops at the maximum depth."""
        # Add a couple of subdirectories to start searching from.
        # We don't actually have to create the directories, just the paths.
        start_path = os.path.join(self.root_dir, "subdir1/subdir2")

        is_root_counter = mock.Mock()
        is_root_counter.side_effect = lambda _: False

        result = find_project_root(start_path,
                                   max_depth=1,
                                   is_root_heuristic=is_root_counter)

        self.assertIsNone(result)
        # 2 calls because we do the current path + the parent.
        self.assertEqual(2, is_root_counter.call_count)

    def test_finds_at_first_level(self):
        """Test that the search stops at the maximum depth."""
        # Add a couple of subdirectories to start searching from.
        start_path = os.path.join(self.root_dir, "subdir1/subdir2")

        is_root_counter = mock.Mock()
        is_root_counter.side_effect = lambda _: True

        result = find_project_root(start_path,
                                   max_depth=3,
                                   is_root_heuristic=is_root_counter)

        self.assertEqual(start_path, result)
        is_root_counter.assert_called_once_with(start_path)

    def test_finds_root(self):
        """Test that the search finds the root based of the heuristic."""

        def is_root(path: str) -> bool:
            return os.path.exists(os.path.join(path, self.test_file_name))

        start_path = os.path.join(self.root_dir, "subdir1/subdir2")

        result = find_project_root(start_path,
                                   max_depth=5,
                                   is_root_heuristic=is_root)

        self.assertEqual(self.root_dir, result)
