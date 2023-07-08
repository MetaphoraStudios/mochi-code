"""The init command. This command is used to initialize Mochi for a new 
project."""

import argparse
import pathlib

from dotenv import dotenv_values
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from retry import retry

from mochi_code.code.mochi_config import create_config, search_mochi_config
from mochi_code.commands.exceptions import MochiCannotContinue

# Load keys for the different model backends. This needs to be setup separately.
keys = dotenv_values(".keys")


class ProjectDetails(BaseModel):
    """The details of a project."""
    language: str = Field(
        description=
        "name of the programming language of a project with these files")
    dependencies: str = Field(
        description=
        "single config file defining the list of dependencies of the " +
        "project, excluding lock file!")
    package_manager: str = Field(
        description="package manager name or 'unknown'")


def setup_init_arguments(parser: argparse.ArgumentParser) -> None:
    """Setup the arguments for the init command.

    Args:
        parser (argparse.ArgumentParser): The parser to add the arguments to.
    """
    parser.add_argument("-f",
                        "--force",
                        action="store_true",
                        help="Force creating the config, without overriding.")


def run_init_command(args: argparse.Namespace) -> None:
    """Run the init command with the provided arguments."""
    # Arguments should be validated by the parser.
    project_path = pathlib.Path.cwd()
    existing_root = search_mochi_config(project_path)

    if not args.force and existing_root is not None:
        raise MochiCannotContinue(
            f"🚫 Mochi is already initialized at '{existing_root.parent}'.")

    if existing_root is not None and existing_root.parent == project_path:
        print("😎 Mochi already exists in this folder, left intact.")
        return

    init(project_path)


def init(project_path: pathlib.Path) -> None:
    """Run the init command.
    
    Args:
        project_path (pathlib.Path): The path to the project to initialize (the
        config folder will be created here).
    """
    print(f"⚙️ Initializing mochi for project '{project_path}'.")
    config_path = create_config(project_path)

    print("🤖 Gathering information about your project...")

    project_files = [p.name for p in project_path.glob("*")]
    project_details = _get_project_details(project_files)

    # write a json file named 'project_details.json' in the config folder with
    # the project_details.json() content
    project_details_path = config_path / "project_details.json"
    with open(project_details_path, "w",
              encoding="utf-8") as project_details_file:
        project_details_file.write(project_details.json())


@retry(tries=3)
def _get_project_details(project_files: list[str]) -> ProjectDetails:
    """Get the details of a project from the user.

    Returns:
        ProjectDetails: The details of the project.
    """
    llm = OpenAI(temperature=0.9,
                 openai_api_key=keys["OPENAI_API_KEY"])  # type: ignore

    parser = PydanticOutputParser(pydantic_object=ProjectDetails,)
    template = PromptTemplate(
        input_variables=["files"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
        template="You are a professional software engineer helping other " +
        "engineers. I'm going to provide a comma separated list of " +
        "files from a project and you need to reply with some " +
        "information about the project in a valid single line JSON " +
        "format with lower case values.\n{format_instructions}\nOutput must " +
        "be a valid json!\nHere's the list of files:\n{files}",
    )
    chain = LLMChain(llm=llm, prompt=template)

    response = chain.run(files=",".join(project_files), verbose=True)

    return parser.parse(response)
