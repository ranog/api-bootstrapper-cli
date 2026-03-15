from __future__ import annotations

from pathlib import Path

import pytest

from api_bootstrapper_cli.core.skills_installer import (
    SkillsDistribution,
    get_default_agentskills_target,
    get_default_codex_target,
    get_default_skills_target,
    install_agentskills,
    install_codex_skills,
)
from api_bootstrapper_cli.skills_validation import SKILL_NAMES


def _create_source_skill_tree(
    source_root: Path,
    *,
    with_openai_yaml: bool,
) -> None:
    for skill_name in SKILL_NAMES:
        skill_root = source_root / skill_name
        skill_root.mkdir(parents=True)

        (skill_root / "SKILL.md").write_text(
            f"---\nname: {skill_name}\ndescription: skill\n---\nProceed? (yes/no)\n",
            encoding="utf-8",
        )
        (skill_root / "references").mkdir()
        (skill_root / "references" / "parameters-and-errors.md").write_text(
            "# ref\n", encoding="utf-8"
        )

        if with_openai_yaml:
            (skill_root / "agents").mkdir()
            (skill_root / "agents" / "openai.yaml").write_text(
                f'interface:\n  default_prompt: "Use ${skill_name}"\n',
                encoding="utf-8",
            )


def test_should_install_all_codex_skills_to_target_directory(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    target_root = tmp_path / "target"
    _create_source_skill_tree(source_root, with_openai_yaml=True)

    result = install_codex_skills(
        target_root=target_root,
        overwrite=True,
        source_root=source_root,
    )

    assert result.distribution == SkillsDistribution.codex
    assert result.target_root == target_root
    assert result.source_root == source_root
    assert set(result.installed_skills) == set(SKILL_NAMES)
    assert result.overwritten_skills == ()
    assert result.skipped_skills == ()

    for skill_name in SKILL_NAMES:
        assert (target_root / skill_name / "SKILL.md").exists()
        assert (
            target_root / skill_name / "references" / "parameters-and-errors.md"
        ).exists()
        assert (target_root / skill_name / "agents" / "openai.yaml").exists()


def test_should_install_all_agentskills_to_target_directory(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    target_root = tmp_path / "target"
    _create_source_skill_tree(source_root, with_openai_yaml=False)

    result = install_agentskills(
        target_root=target_root,
        overwrite=True,
        source_root=source_root,
    )

    assert result.distribution == SkillsDistribution.agentskills
    assert set(result.installed_skills) == set(SKILL_NAMES)

    for skill_name in SKILL_NAMES:
        assert (target_root / skill_name / "SKILL.md").exists()
        assert (
            target_root / skill_name / "references" / "parameters-and-errors.md"
        ).exists()
        assert not (target_root / skill_name / "agents" / "openai.yaml").exists()


def test_should_overwrite_existing_skill_when_overwrite_enabled(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    target_root = tmp_path / "target"
    _create_source_skill_tree(source_root, with_openai_yaml=True)

    stale_skill_file = target_root / SKILL_NAMES[0] / "SKILL.md"
    stale_skill_file.parent.mkdir(parents=True, exist_ok=True)
    stale_skill_file.write_text("stale", encoding="utf-8")

    result = install_codex_skills(
        target_root=target_root,
        overwrite=True,
        source_root=source_root,
    )

    assert SKILL_NAMES[0] in result.overwritten_skills
    assert "stale" not in stale_skill_file.read_text(encoding="utf-8")


def test_should_skip_existing_skill_when_overwrite_disabled(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    target_root = tmp_path / "target"
    _create_source_skill_tree(source_root, with_openai_yaml=True)

    existing_skill = target_root / SKILL_NAMES[0]
    existing_skill.mkdir(parents=True, exist_ok=True)
    existing_file = existing_skill / "SKILL.md"
    existing_file.write_text("keep-this", encoding="utf-8")

    result = install_codex_skills(
        target_root=target_root,
        overwrite=False,
        source_root=source_root,
    )

    assert SKILL_NAMES[0] in result.skipped_skills
    assert existing_file.read_text(encoding="utf-8") == "keep-this"


def test_should_use_codex_home_env_as_default_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_root = tmp_path / "source"
    _create_source_skill_tree(source_root, with_openai_yaml=True)
    codex_home = tmp_path / "codex-home"
    monkeypatch.setenv("CODEX_HOME", str(codex_home))

    result = install_codex_skills(source_root=source_root)

    assert result.target_root == codex_home / "skills"


def test_should_use_agentskills_home_env_as_default_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_root = tmp_path / "source"
    _create_source_skill_tree(source_root, with_openai_yaml=False)
    agentskills_home = tmp_path / "agentskills-home"
    monkeypatch.setenv("AGENT_SKILLS_HOME", str(agentskills_home))

    result = install_agentskills(source_root=source_root)

    assert result.target_root == agentskills_home


def test_should_fallback_to_home_dot_codex_when_codex_home_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CODEX_HOME", raising=False)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    target = get_default_codex_target()

    assert target == tmp_path / ".codex" / "skills"


def test_should_fallback_to_home_dot_agent_skills_when_env_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AGENT_SKILLS_HOME", raising=False)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    target = get_default_agentskills_target()

    assert target == tmp_path / ".agent-skills"


def test_should_return_distribution_specific_default_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))
    monkeypatch.setenv("AGENT_SKILLS_HOME", str(tmp_path / "agentskills-home"))

    codex_target = get_default_skills_target(SkillsDistribution.codex)
    agentskills_target = get_default_skills_target(SkillsDistribution.agentskills)

    assert codex_target == tmp_path / "codex-home" / "skills"
    assert agentskills_target == tmp_path / "agentskills-home"


def test_should_raise_when_source_root_is_missing(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="Embedded skills source not found"):
        install_codex_skills(
            target_root=tmp_path / "target",
            source_root=tmp_path / "missing-source",
        )


def test_should_raise_when_a_required_skill_is_missing_in_source(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "source"
    source_root.mkdir(parents=True)

    with pytest.raises(RuntimeError, match="Embedded skill not found"):
        install_codex_skills(
            target_root=tmp_path / "target",
            source_root=source_root,
        )
