"""The init command. This command is used to initialize Mochi for a new 
project."""

import argparse
import pathlib

from dotenv import dotenv_values
from langchain import LLMChain, OpenAI, PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from retry import retry

from mochi_code.code import ProjectDetails, ProjectDetailsWithDependencies
from mochi_code.code.mochi_config import create_config, search_mochi_config
from mochi_code.commands.exceptions import MochiCannotContinue

# Load keys for the different model backends. This needs to be setup separately.
keys = dotenv_values(".keys")


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
    print("🤖 Gathering information about your project...")

    project_files = [p.name for p in project_path.glob("*")]
    project_details = _get_project_details(project_files)

    print("🤖 Gathering list of dependencies...")
    dependencies = _get_dependencies_list(project_path)
    complete_project_details = ProjectDetailsWithDependencies(
        **project_details.dict(), dependencies=dependencies)

    config_path = create_config(project_path, complete_project_details)

    config_display_uri = config_path.relative_to(project_path).as_posix()
    print(f"🤖 Created the config at {config_display_uri}")


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


def _get_dependencies_list(dependencies_config_path: pathlib.Path) -> list[str]:
    """Get the list of dependencies from the dependencies file.

    Args:
        dependencies_config_path (pathlib.Path): The path to the config file
        defining the dependencies. This may not actually exist, the code will
        validate first.
    
    Returns:
        list[str]: The list of dependencies or empty if none could be found.
    """
    if not dependencies_config_path.exists():
        return []

    return []
