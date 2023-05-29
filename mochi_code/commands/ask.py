"""The ask command. This command is used to ask mochi a single question."""

import argparse
from typing import Any
from dotenv import dotenv_values
from langchain import LLMChain, PromptTemplate, OpenAI

# Load keys for the different model backends. This needs to be setup separately.
keys = dotenv_values(".keys")


def setup_ask_command(
    command_name: str,
    subparsers: Any,
) -> argparse.ArgumentParser:
    """Setup the ask command."""
    ask_parser = subparsers.add_parser(command_name, help="Ask a question to mochi.")
    ask_parser.add_argument("prompt", type=str, help="Your non-empty prompt to run.")
    return ask_parser


def run_ask_command(args: argparse.Namespace):
    """Run the ask command."""
    prompt = args.prompt
    if prompt is None or not prompt.strip():
        raise ValueError("prompt cannot be empty.")
    ask(prompt)


def ask(prompt: str):
    """Run the ask command."""
    chain = _create_chain()
    print(chain.run(prompt))


def _create_chain() -> LLMChain:
    llm = OpenAI(temperature=0.9, openai_api_key=keys["OPENAI_API_KEY"])  # type: ignore
    prompt = PromptTemplate(
        input_variables=["user_prompt"],
        template="""You are an great software engineer helping other engineers.
        Whenever possible provide code examples, prioritise copying code from 
        the following prompt (if available). If you're creating a function or 
        command, please show how to call it.
        Keep answers related to code, if you think the query is not related to 
        code, please ask to clarify, provide more context or rephrase the query,
        but keep it very polite and friendly, or create a pun with it.
        Please answer this query: '{user_prompt}'""",
    )
    return LLMChain(llm=llm, prompt=prompt)
