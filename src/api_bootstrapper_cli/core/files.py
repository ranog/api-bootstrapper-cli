from __future__ import annotations

import re
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
    python_version: str = "3.10",
    use_pep621: bool = False,
) -> Path:
    """Create a minimal pyproject.toml in *project_root*.

    Args:
        project_root: Directory where the file will be created.
        project_name: Project name (defaults to directory name).
        python_version: Python version string (e.g. ``"3.12.3"``).
        use_pep621: When ``True`` generate a PEP 621 ``[project]`` file
            (required by ``uv``). Otherwise generate a Poetry-style file.
    """
    if project_name is None:
        project_name = project_root.name

    pyproject_path = project_root / "pyproject.toml"

    if pyproject_path.exists():
        return pyproject_path

    version_parts = python_version.split(".")
    major_minor = f"{version_parts[0]}.{version_parts[1]}"

    if use_pep621:
        content = f"""[project]
name = "{project_name}"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">={major_minor}"
dependencies = []
"""
    else:
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


def update_python_constraint(pyproject_path: Path, python_version: str) -> bool:
    """Update the Python version constraint in an existing pyproject.toml.

    Handles both PEP 621 (``requires-python = ">=X.Y"``) and Poetry-style
    (``python = "^X.Y"``) formats.
    """
    if not pyproject_path.exists():
        return False

    version_parts = python_version.split(".")
    major_minor = f"{version_parts[0]}.{version_parts[1]}"

    content = read_text(pyproject_path)

    pep621_pattern = r'(requires-python\s*=\s*)["\']([^"\'\n]+)["\']'
    if pep621_match := re.search(pep621_pattern, content):
        target = f">={major_minor}"
        if pep621_match.group(2) == target:
            return False
        new_content = re.sub(
            pep621_pattern, f'requires-python = "{target}"', content, count=1
        )
        write_text(pyproject_path, new_content, overwrite=True)
        return True

    poetry_pattern = r'(python\s*=\s*)["\']([^"\'\n]+)["\']'
    if poetry_match := re.search(poetry_pattern, content):
        target = f"^{major_minor}"
        if poetry_match.group(2) == target:
            return False
        new_content = re.sub(poetry_pattern, f'\\1"{target}"', content, count=1)
        write_text(pyproject_path, new_content, overwrite=True)
        return True

    return False
