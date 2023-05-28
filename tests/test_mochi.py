from unittest import TestCase
from unittest.mock import patch
from mochi_code.ask import cli, EmptyPromptError
from pytest import raises, MonkeyPatch


class TestAskCli(TestCase):
    """Test the cli function in ask.py"""

    @patch("mochi_code.ask.ask")
    def test_empty_prompt_fails(self, mock_ask):
        """Test that an empty prompt fails."""
        mock_ask.return_value = None

        MonkeyPatch().setattr("sys.argv", ["mochi"])
        with raises(EmptyPromptError):
            cli()

        MonkeyPatch().setattr("sys.argv", ["mochi", "--ask", ""])
        with raises(EmptyPromptError):
            cli()

        MonkeyPatch().setattr("sys.argv", ["mochi", "--ask", "         "])
        with raises(EmptyPromptError):
            cli()

    @patch("mochi_code.ask.ask")
    def test_non_empty_prompt_succeeds(self, mock_ask):
        """Test that a non-empty prompt succeeds."""
        mock_ask.return_value = None

        prompt = "test"
        MonkeyPatch().setattr("sys.argv", ["mochi", "--ask", prompt])
        cli()

        mock_ask.assert_called_once_with(prompt)
