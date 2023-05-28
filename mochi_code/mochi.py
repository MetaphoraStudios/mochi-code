"""This file sets up the mochi subcommands, validates cli user input and calls
out to the subcommands."""

import argparse

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import dotenv_values


# Load keys for the different model backends. This needs to be setup separately.
keys = dotenv_values(".keys")


def cli():
    """Run the ask command from the cli (with --ask argument)."""
    parser = argparse.ArgumentParser(prog="mochi")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    ask_parser = subparsers.add_parser("ask", help="Ask a question to mochi.")
    ask_parser.add_argument("prompt", type=str, help="Your non-empty prompt to run.")
    args = parser.parse_args()

    if args.subcommand == "ask":
        prompt = args.prompt
        if prompt is None or not prompt.strip():
            print("issue: Prompt cannot be empty.")
            ask_parser.print_help()
            parser.exit(1)
            # raise EmptyPromptError("Prompt cannot be empty.")
        ask(prompt)
    else:
        parser.print_help()


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
