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
) -> Path:
    if project_name is None:
        project_name = project_root.name

    pyproject_path = project_root / "pyproject.toml"

    if pyproject_path.exists():
        return pyproject_path

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


def update_python_constraint(pyproject_path: Path, python_version: str) -> bool:
    if not pyproject_path.exists():
        return False

    version_parts = python_version.split(".")
    major_minor = f"{version_parts[0]}.{version_parts[1]}"
    target_constraint = f"^{major_minor}"

    content = read_text(pyproject_path)

    python_constraint_pattern = r'(python\s*=\s*)["\']([^"\'\n]+)["\']'

    if not (match := re.search(python_constraint_pattern, content)):
        return False

    current_constraint = match.group(2)
    if current_constraint == target_constraint:
        return False

    new_content = re.sub(
        python_constraint_pattern,
        f'\\1"{target_constraint}"',
        content,
        count=1,
    )

    write_text(pyproject_path, new_content, overwrite=True)
    return True
