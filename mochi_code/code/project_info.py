"""Utilities to extract project information."""
import os
from typing import Callable, Optional

RootHeuristicType = Callable[[str], bool]


def is_project_root(path: str) -> bool:
    """Check if the path is a project root."""
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
        
    Returns:
        The path to the project root, or None if it could not be found.
    """
    assert max_depth > 0

    current_path = start_path
    while max_depth > 0:
        max_depth -= 1
        if is_root_heuristic(current_path):
            return current_path
        current_path = os.path.join(current_path, "..")
    return None
