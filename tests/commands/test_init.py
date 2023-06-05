"""Test the init command."""

from unittest import TestCase


class TestSetupInitArguments(TestCase):
    """Test the setup_init_arguments function."""


class TestRunInitCommand(TestCase):
    """Test the run_init_command function."""


class TestGetExistingMochiConfig(TestCase):
    """Test the _get_existing_mochi_config function."""

    # TODO: Mock the path.root value
    def test_starting_at_root_not_found(self):
        """Test that the function returns None when starting at the root and
        there isn't a mochi config."""

    def test_starting_at_root_found(self):
        """Test that the function returns root path when starting at the root
        and there is a mochi config."""

    def test_finds_in_parent(self):
        """Test that the function returns the parent path when there is a mochi
        config in the parent."""

    def test_finds_in_self(self):
        """Test that the function returns the current path when there is a mochi
        config in the current path."""

    def test_not_found_across_dir_tree(self):
        """Test that the function returns None when there is no mochi config
        across the directory tree."""
