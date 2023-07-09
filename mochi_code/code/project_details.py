"""The class used to define the project details. This is used to generate the
mochi config."""

from pydantic import BaseModel, Field


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
