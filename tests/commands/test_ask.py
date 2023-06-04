"""Test the command function in ask.py"""

import argparse
from unittest import TestCase
from unittest.mock import patch

from pytest import raises

from mochi_code.commands.ask import run_ask_command, setup_ask_arguments


class TestSetupAskCommand(TestCase):
    """Test the command setup function in ask.py"""

    def test_empty_prompt_fails(self):
        """Test that an empty prompt fails."""
        parser = argparse.ArgumentParser()
        setup_ask_arguments(parser)

        with raises(SystemExit):
            parser.parse_args([])

        with raises(SystemExit):
            parser.parse_args([""])

        with raises(SystemExit):
            parser.parse_args(["         "])


class TestRunAskCommand(TestCase):
    """Test the command function in ask.py"""

    @patch("mochi_code.commands.ask.ask")
    def test_prompt_is_called(self, mock_ask):
        """Test that a non-empty prompt succeeds."""
        mock_ask.return_value = None

        prompt = "test"
        args = argparse.Namespace(prompt=prompt)
        run_ask_command(args)

        mock_ask.assert_called_once_with(prompt)
