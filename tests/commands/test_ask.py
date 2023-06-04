"""Test the command function in ask.py"""

import argparse
from unittest import TestCase
from unittest.mock import patch

from pytest import raises

from mochi_code.commands.ask import run_ask_command


class TestRunAskCommand(TestCase):
    """Test the command function in ask.py"""

    @patch("mochi_code.commands.ask.ask")
    def test_empty_prompt_fails(self, mock_ask):
        """Test that an empty prompt fails."""
        mock_ask.return_value = None

        with raises(ValueError):
            args = argparse.Namespace(prompt=None)
            run_ask_command(args)

        with raises(ValueError):
            args = argparse.Namespace(prompt="")
            run_ask_command(args)

        with raises(ValueError):
            args = argparse.Namespace(prompt="         ")
            run_ask_command(args)

    @patch("mochi_code.commands.ask.ask")
    def test_non_empty_prompt_succeeds(self, mock_ask):
        """Test that a non-empty prompt succeeds."""
        mock_ask.return_value = None

        prompt = "test"
        args = argparse.Namespace(prompt=prompt)
        run_ask_command(args)

        mock_ask.assert_called_once_with(prompt)
