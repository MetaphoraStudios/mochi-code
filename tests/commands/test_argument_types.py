"""Tests for the argument type validators used in the commands."""

import argparse
from unittest import TestCase

from mochi_code.commands.argument_types import valid_prompt


class TestValidPrompt(TestCase):
    """Test the valid_prompt function."""

    def test_none_prompt_fails(self):
        """Test that None prompt fails."""
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_prompt(None)

    def test_empty_prompt_fails(self):
        """Test that an empty prompt fails."""
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_prompt("")

    def test_whitespace_prompt_fails(self):
        """Test that a whitespace prompt fails."""
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_prompt("         ")

    def test_non_empty_prompt_succeeds(self):
        """Test that a non-empty prompt succeeds."""
        prompt = "test"
        self.assertEqual(valid_prompt(prompt), prompt)

    def test_prompt_is_stripped(self):
        """Test that a prompt with leading and trailing whitespace is stripped."""
        prompt = "    test    "
        self.assertEqual(valid_prompt(prompt), prompt.strip())
