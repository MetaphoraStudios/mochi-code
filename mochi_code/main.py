from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import dotenv_values
import argparse


# Load keys for the different model backends. This needs to be setup separately.
keys = dotenv_values(".keys")


def main(user_query: str):
    chain = create_chain()
    print(chain.run(user_query))


def create_chain() -> LLMChain:
    llm = OpenAI(temperature=0.9, openai_api_key=keys["OPENAI_API_KEY"])  # type: ignore
    prompt = PromptTemplate(
        input_variables=["query"],
        template="""You are an great software engineer helping other engineers.
        Whenever possible provide code examples, prioritise copying code from 
        the following prompt (if available). If you're creating a function or 
        command, please show how to call it.
        Keep answers related to code, if you think the query is not related to 
        code, please ask to clarify, provide more context or rephrase the query,
        but keep it very polite and friendly, or create a pun with it.
        Please answer this query: '{query}'""",
    )
    return LLMChain(llm=llm, prompt=prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="Your non-empty prompt to run.")
    args = parser.parse_args()

    prompt = args.prompt
    if not prompt.strip():
        print("Prompt cannot be empty.")
        parser.print_help()
        exit(1)

    main(prompt)
