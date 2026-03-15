from __future__ import annotations

import enum
import os
import shutil
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from api_bootstrapper_cli.skills_validation import SKILL_NAMES


class SkillsDistribution(str, enum.Enum):
    codex = "codex"
    agentskills = "agentskills"


@dataclass(frozen=True)
class SkillsInstallResult:
    distribution: SkillsDistribution
    source_root: Path
    target_root: Path
    installed_skills: tuple[str, ...]
    overwritten_skills: tuple[str, ...]
    skipped_skills: tuple[str, ...]


def get_default_codex_target() -> Path:
    codex_home = os.getenv("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"

    return Path.home() / ".codex" / "skills"


def get_default_agentskills_target() -> Path:
    agentskills_home = os.getenv("AGENT_SKILLS_HOME")
    if agentskills_home:
        return Path(agentskills_home).expanduser()

    return Path.home() / ".agent-skills"


def get_default_skills_target(distribution: SkillsDistribution) -> Path:
    if distribution == SkillsDistribution.agentskills:
        return get_default_agentskills_target()

    return get_default_codex_target()


def _remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def _copy_skills(
    distribution: SkillsDistribution,
    source_root: Path,
    target_root: Path,
    overwrite: bool,
) -> SkillsInstallResult:
    if not source_root.exists() or not source_root.is_dir():
        raise RuntimeError(f"Embedded skills source not found: {source_root}")

    target_root.mkdir(parents=True, exist_ok=True)

    installed_skills: list[str] = []
    overwritten_skills: list[str] = []
    skipped_skills: list[str] = []

    for skill_name in SKILL_NAMES:
        source_skill = source_root / skill_name
        target_skill = target_root / skill_name

        if not source_skill.exists() or not source_skill.is_dir():
            raise RuntimeError(f"Embedded skill not found: {source_skill}")

        if target_skill.exists():
            if overwrite:
                _remove_path(target_skill)
                overwritten_skills.append(skill_name)
            else:
                skipped_skills.append(skill_name)
                continue

        shutil.copytree(source_skill, target_skill)
        installed_skills.append(skill_name)

    return SkillsInstallResult(
        distribution=distribution,
        source_root=source_root,
        target_root=target_root,
        installed_skills=tuple(installed_skills),
        overwritten_skills=tuple(overwritten_skills),
        skipped_skills=tuple(skipped_skills),
    )


def install_skills_distribution(
    distribution: SkillsDistribution,
    target_root: Path | None = None,
    overwrite: bool = True,
    source_root: Path | None = None,
) -> SkillsInstallResult:
    effective_target = target_root or get_default_skills_target(distribution)

    if source_root is not None:
        return _copy_skills(distribution, source_root, effective_target, overwrite)

    traversable = resources.files("api_bootstrapper_cli").joinpath(
        "embedded_skills",
        distribution.value,
    )

    if not traversable.is_dir():
        raise RuntimeError(
            f"Embedded {distribution.value} skills are not available in this installation."
        )

    with resources.as_file(traversable) as source_path:
        return _copy_skills(distribution, source_path, effective_target, overwrite)


def install_codex_skills(
    target_root: Path | None = None,
    overwrite: bool = True,
    source_root: Path | None = None,
) -> SkillsInstallResult:
    return install_skills_distribution(
        distribution=SkillsDistribution.codex,
        target_root=target_root,
        overwrite=overwrite,
        source_root=source_root,
    )


def install_agentskills(
    target_root: Path | None = None,
    overwrite: bool = True,
    source_root: Path | None = None,
) -> SkillsInstallResult:
    return install_skills_distribution(
        distribution=SkillsDistribution.agentskills,
        target_root=target_root,
        overwrite=overwrite,
        source_root=source_root,
    )
