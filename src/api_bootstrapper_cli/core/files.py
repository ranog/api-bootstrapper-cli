from __future__ import annotations

from pathlib import Path


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str, overwrite: bool = False) -> None:
    if not overwrite and path.exists():
        raise FileExistsError(f"File already exists: {path}")
    path.write_text(content, encoding="utf-8")


def create_minimal_pyproject(
    project_root: Path,
    project_name: str | None = None,
    python_version: str = "3.12",
) -> Path:
    """Create a minimal pyproject.toml in the project.

    Args:
        project_root: Project root directory
        project_name: Project name (default: directory name)
        python_version: Python version constraint (e.g., "3.12", "3.13.9")

    Returns:
        Path to the created pyproject.toml
    """
    if project_name is None:
        project_name = project_root.name

    pyproject_path = project_root / "pyproject.toml"

    # Don't overwrite if it already exists
    if pyproject_path.exists():
        return pyproject_path

    # Extract major.minor from version (e.g., "3.13.9" -> "3.13")
    version_parts = python_version.split(".")
    major_minor = f"{version_parts[0]}.{version_parts[1]}"

    content = f"""[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = ""
authors = []
readme = "README.md"

[tool.poetry.dependencies]
python = "^{major_minor}"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""

    write_text(pyproject_path, content)
    return pyproject_path
