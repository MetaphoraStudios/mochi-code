from typing import Optional, Sequence
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import dotenv_values
import argparse


# Load keys for the different model backends. This needs to be setup separately.
keys = dotenv_values(".keys")


class EmptyPromptError(Exception):
    pass


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ask", type=str, help="Your non-empty prompt to run.")
    args = parser.parse_args()

    prompt = args.ask
    if prompt is None or not prompt.strip():
        parser.print_help()
        raise EmptyPromptError("Prompt cannot be empty.")

    ask(prompt)


def ask(prompt: str):
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
