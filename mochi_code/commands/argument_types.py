"""Helper functions for argparse argument types."""

import argparse
from typing import Optional


def valid_prompt(user_prompt: Optional[str]) -> str:
    """Validate the user prompt."""
    prompt = (user_prompt or "").strip()
    if not prompt:
        raise argparse.ArgumentTypeError("Prompt cannot be empty.")
    return prompt
