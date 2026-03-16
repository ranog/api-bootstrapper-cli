from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from api_bootstrapper_cli.core.files import read_text, write_text
from api_bootstrapper_cli.core.protocols import ManagerChoice
from api_bootstrapper_cli.core.shell import ShellError, exec_cmd


POETRY_MYPY_VERSION = "^1.19.1"
UV_MYPY_SPEC = "mypy>=1.19.1,<2"

MYPY_CONFIG_TEMPLATE = """[tool.mypy]
python_version = "3.12"
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
no_implicit_optional = true

[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false
check_untyped_defs = false
"""


@dataclass(frozen=True)
class MypySetupResult:
    manager: ManagerChoice
    pyproject_path: Path
    config_already_existed: bool
    version: str | None


@dataclass(frozen=True)
class MypyManager:
    def _detect_manager(self, project_root: Path) -> ManagerChoice:
        pyproject_path = project_root / "pyproject.toml"
        if not pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found in {project_root}")

        content = read_text(pyproject_path)

        if "[tool.poetry]" in content:
            return ManagerChoice.pyenv

        if "[project]" in content:
            return ManagerChoice.uv

        return ManagerChoice.pyenv

    def setup(
        self,
        project_root: Path,
        manager: ManagerChoice | None = None,
    ) -> MypySetupResult:
        if not project_root.exists():
            raise ValueError(f"Project root does not exist: {project_root}")

        pyproject_path = project_root / "pyproject.toml"
        if not pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found in {project_root}")

        selected_manager = manager or self._detect_manager(project_root)
        content = read_text(pyproject_path)
        config_already_existed = "[tool.mypy]" in content

        if selected_manager == ManagerChoice.pyenv:
            content = self._ensure_poetry_dev_section(content)
            content = self._ensure_poetry_dependency(content)
        else:
            content = self._ensure_uv_dev_section(content)
            content = self._ensure_uv_dependency(content)

        if not config_already_existed:
            content = self._append_mypy_config(content)

        write_text(pyproject_path, content, overwrite=True)
        self._sync_dependencies(project_root, selected_manager)
        version = self._extract_version(content, selected_manager)

        return MypySetupResult(
            manager=selected_manager,
            pyproject_path=pyproject_path,
            config_already_existed=config_already_existed,
            version=version,
        )

    def _ensure_poetry_dev_section(self, content: str) -> str:
        dev_section = "[tool.poetry.group.dev.dependencies]"
        if dev_section in content:
            return content

        if "[build-system]" in content:
            return content.replace(
                "[build-system]", f"{dev_section}\n\n[build-system]", 1
            )

        return f"{content}\n{dev_section}\n"

    def _ensure_poetry_dependency(self, content: str) -> str:
        if re.search(r"(?m)^mypy\s*=", content):
            return content

        return re.sub(
            r"(\[tool\.poetry\.group\.dev\.dependencies\]\n)",
            rf'\1mypy = "{POETRY_MYPY_VERSION}"\n',
            content,
            count=1,
        )

    def _ensure_uv_dev_section(self, content: str) -> str:
        dev_section = "[project.optional-dependencies]"
        if dev_section in content and re.search(r"(?m)^dev\s*=", content):
            return content
        if dev_section in content:
            return content.replace(dev_section, f"{dev_section}\ndev = []", 1)

        if "[build-system]" in content:
            return content.replace(
                "[build-system]",
                f"{dev_section}\ndev = []\n\n[build-system]",
                1,
            )

        if "[project]" in content:
            match = re.search(r"(\[project\].*?)(\n\[|\Z)", content, re.DOTALL)
            if match:
                project_section = match.group(1)
                rest = match.group(2)
                return content.replace(
                    match.group(0),
                    f"{project_section}\n\n{dev_section}\ndev = []\n{rest}",
                    1,
                )

        return f"{content}\n{dev_section}\ndev = []\n"

    def _ensure_uv_dependency(self, content: str) -> str:
        if re.search(r'["\']mypy(?:[<>=]|$)', content):
            return content

        return re.sub(
            r"(dev\s*=\s*\[)",
            rf'\1\n    "{UV_MYPY_SPEC}",',
            content,
            count=1,
        )

    def _append_mypy_config(self, content: str) -> str:
        normalized = content if content.endswith("\n") else f"{content}\n"
        return f"{normalized}\n{MYPY_CONFIG_TEMPLATE}"

    def _extract_version(
        self,
        content: str,
        manager: ManagerChoice,
    ) -> str | None:
        if manager == ManagerChoice.pyenv:
            match = re.search(r'(?m)^mypy\s*=\s*"[^"]*?([0-9.]+)"', content)
            return match.group(1) if match else None

        match = re.search(r'"mypy>=([0-9.]+)', content)
        return match.group(1) if match else None

    def _sync_dependencies(
        self,
        project_root: Path,
        manager: ManagerChoice,
    ) -> None:
        try:
            if manager == ManagerChoice.pyenv:
                exec_cmd(["poetry", "lock"], cwd=str(project_root), check=True)
                exec_cmd(
                    ["poetry", "install", "--no-root"],
                    cwd=str(project_root),
                    check=True,
                )
            else:
                exec_cmd(
                    ["uv", "sync", "--all-groups"], cwd=str(project_root), check=True
                )
        except (ShellError, FileNotFoundError) as error:
            raise RuntimeError(
                f"Failed to sync dependencies using {manager.value}: {error}"
            ) from error
