"""Utilities to extract project information."""
import os
from typing import Callable, Optional

RootHeuristicType = Callable[[str], bool]


def is_project_root(path: str) -> bool:
    """Check if the path is a project root."""
    # We implement this by looking for files that would usually only be at the
    # root of a project.
    # There are cases when it's ambiguous, for example, if a project contains
    # both a frontend and backend where the frontend might define package.json
    # and the backend might define pyproject.toml.
    # In these cases we're conservative and return True (project root) as for
    # now that means, at worst, Mochi will see the different areas of the
    # project as separate projects. This should be ok as they have different
    # tech stacks, but might miss on the overall project structure.
    # In the future this is a good candidate for improvement!
    return os.path.exists(os.path.join(path, "pyproject.toml"))


def find_project_root(
        start_path: str,
        max_depth: int = 3,
        is_root_heuristic: RootHeuristicType = is_project_root
) -> Optional[str]:
    """Find the project root directory, navigating up the directory tree to the
    maximum depth, and using the heuristic function to check if the directory is
    a project root.
    
    Remarks:
        If you're trying to find if the current directory is a project root,
        please use `is_project_root` instead.
    
    Args:
        start_path: The path to start searching from.
        max_depth: The maximum depth to search for the project root (> 0).
            max_depth = 1 means the function will check the current directory
            and its parent.
        
    Returns:
        The path to the project root, or None if it could not be found.
    """
    assert max_depth > 0

    current_path = os.path.abspath(start_path)
    while max_depth >= 0:
        max_depth -= 1
        if is_root_heuristic(current_path):
            return current_path
        current_path = os.path.dirname(current_path)
    return None
