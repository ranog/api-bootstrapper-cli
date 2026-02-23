from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.files import read_text, write_text
from api_bootstrapper_cli.core.logger import logger
from api_bootstrapper_cli.core.shell import exec_cmd


@dataclass(frozen=True)
class PreCommitManager:
    def create_config(self, project_root: Path) -> tuple[Path, dict[str, str]]:
        if not project_root.exists():
            raise ValueError(f"Project root does not exist: {project_root}")

        config_path = project_root / ".pre-commit-config.yaml"
        content = self._generate_config_content()
        write_text(config_path, content, overwrite=True)

        self._add_dependencies(project_root)
        versions = self._extract_versions_from_pyproject(project_root)
        self._update_config_versions(config_path, versions)
        self._install_hooks(project_root)

        return config_path, versions

    def _generate_config_content(self) -> str:
        return """\
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: ""
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/commitizen-tools/commitizen
    rev: ""
    hooks:
      - id: commitizen
        stages: [commit-msg]
"""

    def _add_dependencies(self, project_root: Path) -> None:
        logger.info("Adding pre-commit, ruff, and commitizen to dev dependencies...")
        pyproject_path = project_root / "pyproject.toml"

        if not pyproject_path.exists():
            logger.error("pyproject.toml not found")
            raise FileNotFoundError(f"pyproject.toml not found in {project_root}")

        content = read_text(pyproject_path)

        dev_section = "[tool.poetry.group.dev.dependencies]"
        if dev_section not in content:
            if "[build-system]" in content:
                content = content.replace(
                    "[build-system]", f"{dev_section}\n\n[build-system]"
                )
            else:
                content += f"\n{dev_section}\n"

        dependencies = {
            "pre-commit": "^4.5.1",
            "ruff": "^0.15.2",
            "commitizen": "^4.13.8",
        }

        for dep, version in dependencies.items():
            if f"{dep} =" not in content:
                content = re.sub(
                    r"(\[tool\.poetry\.group\.dev\.dependencies\]\n)",
                    rf'\1{dep} = "{version}"\n',
                    content,
                )

        write_text(pyproject_path, content, overwrite=True)
        logger.success("Dependencies added to pyproject.toml")

        logger.info("Updating poetry.lock...")
        try:
            exec_cmd(
                ["poetry", "lock"],
                cwd=str(project_root),
                check=True,
            )
            logger.success("poetry.lock updated")
        except Exception as e:
            logger.error(f"Failed to update lock file: {e}")
            raise

        logger.info("Installing dependencies...")
        try:
            exec_cmd(
                ["poetry", "install", "--no-root"],
                cwd=str(project_root),
                check=True,
            )
            logger.success("Dependencies installed")
        except Exception as e:
            logger.error(f"Failed to install dependencies: {e}")
            raise

    def _extract_versions_from_pyproject(self, project_root: Path) -> dict[str, str]:
        pyproject_path = project_root / "pyproject.toml"
        if not pyproject_path.exists():
            logger.warning("pyproject.toml not found, cannot extract versions")
            return {}

        content = read_text(pyproject_path)

        if "[tool.poetry.group.dev.dependencies]" not in content:
            logger.warning("[tool.poetry.group.dev.dependencies] section not found")

        versions = {}

        if match := re.search(r'pre-commit\s*=\s*"[^"]*?([0-9.]+)"', content):
            versions["pre-commit"] = match.group(1)

        if match := re.search(r'ruff\s*=\s*"[^"]*?([0-9.]+)"', content):
            versions["ruff"] = match.group(1)

        if match := re.search(r'commitizen\s*=\s*"[^"]*?([0-9.]+)"', content):
            versions["commitizen"] = match.group(1)

        if not versions:
            logger.warning("No versions found in pyproject.toml")

        return versions

    def _update_config_versions(
        self, config_path: Path, versions: dict[str, str]
    ) -> None:
        if not config_path.exists():
            logger.warning("Config file not found, cannot update versions")
            return

        if not versions:
            logger.warning("No versions to update in config file")
            return

        content = read_text(config_path)
        original_content = content

        if "ruff" in versions:
            content = re.sub(
                r'(astral-sh/ruff-pre-commit\s+rev:\s+)"[^"]*"',
                rf'\1"v{versions["ruff"]}"',
                content,
            )

        if "commitizen" in versions:
            content = re.sub(
                r'(commitizen-tools/commitizen\s+rev:\s+)"[^"]*"',
                rf'\1"v{versions["commitizen"]}"',
                content,
            )

        if content == original_content:
            logger.warning("No version replacements were made in config file")

        write_text(config_path, content, overwrite=True)

    def _install_hooks(self, project_root: Path) -> None:
        logger.info("Installing pre-commit hooks...")
        try:
            exec_cmd(
                [
                    "poetry",
                    "run",
                    "pre-commit",
                    "install",
                    "--hook-type",
                    "pre-commit",
                    "--hook-type",
                    "commit-msg",
                ],
                cwd=str(project_root),
                check=True,
            )
            logger.success("Pre-commit hooks installed successfully")
        except Exception as e:
            logger.warning(f"Failed to install hooks: {e}")
            # Don't raise - hooks can be installed manually later
