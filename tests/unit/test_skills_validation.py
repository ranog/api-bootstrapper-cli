from __future__ import annotations

from pathlib import Path

import pytest

import api_bootstrapper_cli.skills_validation as skills_validation
from api_bootstrapper_cli.skills_validation import (
    main,
    parse_frontmatter,
    render_openai_yaml,
    validate_all,
    validate_smoke,
    validate_structure,
    validate_sync,
)


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _skill_md(
    name: str,
    description: str = "Skill description",
    body: str = "Proceed? (yes/no)",
) -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n{body}\n"


def _create_agent_skill(
    repo_root: Path,
    skill_name: str,
    *,
    skill_content: str,
    include_reference: bool = True,
    reference_content: str = "# refs\n",
) -> None:
    skill_dir = repo_root / "skills" / "agentskills" / skill_name
    _write_file(skill_dir / "SKILL.md", skill_content)

    if include_reference:
        _write_file(
            skill_dir / "references" / "parameters-and-errors.md", reference_content
        )


def _create_codex_skill(
    repo_root: Path,
    skill_name: str,
    *,
    skill_content: str,
    include_reference: bool = True,
    reference_content: str = "# refs\n",
    openai_yaml_content: str | None = None,
) -> None:
    skill_dir = repo_root / "skills" / "codex" / skill_name
    _write_file(skill_dir / "SKILL.md", skill_content)

    if include_reference:
        _write_file(
            skill_dir / "references" / "parameters-and-errors.md", reference_content
        )

    if openai_yaml_content is not None:
        _write_file(skill_dir / "agents" / "openai.yaml", openai_yaml_content)


def _create_required_smoke_files(repo_root: Path) -> None:
    bootstrap_body = "\n".join(
        [
            "Proceed? (yes/no)",
            "api-bootstrapper bootstrap-env --manager pyenv",
            "api-bootstrapper bootstrap-env --manager uv",
        ]
    )
    flow_body = "\n".join(
        ["Proceed? (yes/no)", "api-bootstrapper init --python 3.12.12"]
    )
    alembic_body = "\n".join(
        [
            "Proceed? (yes/no)",
            "api-bootstrapper add-alembic --path ./my-api",
        ]
    )

    _create_agent_skill(
        repo_root,
        "api-bootstrapper-bootstrap-env",
        skill_content=_skill_md("api-bootstrapper-bootstrap-env", body=bootstrap_body),
    )
    _create_agent_skill(
        repo_root,
        "api-bootstrapper-bootstrap-flow",
        skill_content=_skill_md("api-bootstrapper-bootstrap-flow", body=flow_body),
    )
    _create_agent_skill(
        repo_root,
        "api-bootstrapper-add-alembic",
        skill_content=_skill_md("api-bootstrapper-add-alembic", body=alembic_body),
    )


def test_should_validate_skills_structure() -> None:
    errors = validate_structure()

    assert errors == []


def test_should_validate_skills_sync_between_agentskills_and_codex() -> None:
    errors = validate_sync()

    assert errors == []


def test_should_validate_skills_smoke_contracts() -> None:
    errors = validate_smoke()

    assert errors == []


def test_should_parse_frontmatter_with_valid_content() -> None:
    parsed = parse_frontmatter(
        "---\nname: my-skill\ndescription: do stuff\n---\n# body\n"
    )

    assert parsed == {"name": "my-skill", "description": "do stuff"}


@pytest.mark.parametrize(
    ("content", "expected_error"),
    [
        ("name: invalid", "must start"),
        ("---\nname: missing-end\ndescription: x\n", "closing delimiter"),
        ("---\ninvalid_line\n---\n", "Invalid frontmatter line"),
    ],
)
def test_should_raise_for_invalid_frontmatter_content(
    content: str,
    expected_error: str,
) -> None:
    with pytest.raises(ValueError, match=expected_error):
        parse_frontmatter(content)


def test_should_render_openai_yaml_with_skill_reference() -> None:
    rendered = render_openai_yaml("api-bootstrapper-init")

    assert "display_name" in rendered
    assert "default_prompt" in rendered
    assert "$api-bootstrapper-init" in rendered


def test_should_report_missing_agentskills_directory(tmp_path: Path) -> None:
    errors = validate_structure(repo_root=tmp_path)

    assert len(errors) == 1
    assert "Missing skills directory" in errors[0]


def test_should_report_missing_and_unexpected_skill_directories(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("expected-skill",))

    (tmp_path / "skills" / "agentskills" / "unexpected-skill").mkdir(parents=True)

    errors = validate_structure(repo_root=tmp_path)

    assert any("Missing skills" in error for error in errors)
    assert any("Unexpected skills" in error for error in errors)


def test_should_report_invalid_skill_directory_pattern(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("invalid_skill",))

    _create_agent_skill(
        tmp_path,
        "invalid_skill",
        skill_content=_skill_md("invalid_skill"),
    )

    errors = validate_structure(repo_root=tmp_path)

    assert any("hyphen-case" in error for error in errors)


def test_should_report_missing_skill_md_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("api-bootstrapper-init",))

    (tmp_path / "skills" / "agentskills" / "api-bootstrapper-init").mkdir(parents=True)

    errors = validate_structure(repo_root=tmp_path)

    assert any("Missing SKILL.md" in error for error in errors)


def test_should_report_invalid_frontmatter_in_skill_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("api-bootstrapper-init",))

    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-init",
        skill_content="name: invalid\n",
    )

    errors = validate_structure(repo_root=tmp_path)

    assert any("Invalid frontmatter" in error for error in errors)


@pytest.mark.parametrize(
    ("skill_content", "expected_error"),
    [
        (
            "---\nname: api-bootstrapper-init\n---\nbody\n",
            "must be exactly name/description",
        ),
        (
            "---\nname: different-name\ndescription: desc\n---\nbody\n",
            "Frontmatter name mismatch",
        ),
        (
            "---\nname: api-bootstrapper-init\ndescription:\n---\nbody\n",
            "description cannot be empty",
        ),
    ],
)
def test_should_report_frontmatter_contract_violations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    skill_content: str,
    expected_error: str,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("api-bootstrapper-init",))

    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-init",
        skill_content=skill_content,
        include_reference=False,
    )

    errors = validate_structure(repo_root=tmp_path)

    assert any(expected_error in error for error in errors)


def test_should_report_missing_references_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("api-bootstrapper-init",))

    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-init",
        skill_content=_skill_md("api-bootstrapper-init"),
        include_reference=False,
    )

    errors = validate_structure(repo_root=tmp_path)

    assert any("Missing references file" in error for error in errors)


def test_should_report_missing_codex_directory(tmp_path: Path) -> None:
    errors = validate_sync(repo_root=tmp_path)

    assert any("Missing skills directory" in error for error in errors)


def test_should_report_sync_divergence_between_trees(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("api-bootstrapper-init",))

    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-init",
        skill_content=_skill_md("api-bootstrapper-init", body="Proceed? (yes/no)"),
        reference_content="agent-ref\n",
    )

    _create_codex_skill(
        tmp_path,
        "api-bootstrapper-init",
        skill_content=_skill_md("api-bootstrapper-init", body="different body"),
        reference_content="codex-ref\n",
        openai_yaml_content='interface:\n  default_prompt: "missing token"\n',
    )

    errors = validate_sync(repo_root=tmp_path)

    assert any("SKILL.md divergence" in error for error in errors)
    assert any("References divergence" in error for error in errors)
    assert any("must mention $api-bootstrapper-init" in error for error in errors)


def test_should_report_missing_codex_files_required_for_sync(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("api-bootstrapper-init",))

    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-init",
        skill_content=_skill_md("api-bootstrapper-init"),
    )
    (tmp_path / "skills" / "codex" / "api-bootstrapper-init").mkdir(parents=True)

    errors = validate_sync(repo_root=tmp_path)

    assert any("Missing codex SKILL.md" in error for error in errors)
    assert any("Missing codex references file" in error for error in errors)
    assert any("Missing codex metadata file" in error for error in errors)


def test_should_report_missing_confirmation_prompt_in_smoke_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        skills_validation, "SKILL_NAMES", ("api-bootstrapper-init", "missing-skill")
    )

    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-init",
        skill_content=_skill_md("api-bootstrapper-init", body="no confirmation here"),
    )
    _create_required_smoke_files(tmp_path)

    errors = validate_smoke(repo_root=tmp_path)

    assert any("explicit confirmation" in error for error in errors)


def test_should_report_command_contract_gaps_in_smoke_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(skills_validation, "SKILL_NAMES", ("api-bootstrapper-init",))

    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-init",
        skill_content=_skill_md("api-bootstrapper-init"),
    )
    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-bootstrap-env",
        skill_content=_skill_md(
            "api-bootstrapper-bootstrap-env", body="Proceed? (yes/no)"
        ),
    )
    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-bootstrap-flow",
        skill_content=_skill_md(
            "api-bootstrapper-bootstrap-flow", body="Proceed? (yes/no)"
        ),
    )
    _create_agent_skill(
        tmp_path,
        "api-bootstrapper-add-alembic",
        skill_content=_skill_md(
            "api-bootstrapper-add-alembic", body="Proceed? (yes/no)"
        ),
    )

    errors = validate_smoke(repo_root=tmp_path)

    assert any("pyenv command example" in error for error in errors)
    assert any("uv command example" in error for error in errors)
    assert any("init command path" in error for error in errors)
    assert any("command usage with --path" in error for error in errors)


def test_should_aggregate_validation_errors_from_all_steps(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        skills_validation, "validate_structure", lambda repo_root=None: ["a"]
    )
    monkeypatch.setattr(
        skills_validation, "validate_sync", lambda repo_root=None: ["b"]
    )
    monkeypatch.setattr(
        skills_validation, "validate_smoke", lambda repo_root=None: ["c"]
    )

    errors = validate_all()

    assert errors == ["a", "b", "c"]


def test_should_return_zero_and_print_success_when_main_has_no_errors(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(skills_validation, "validate_all", lambda repo_root=None: [])

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Skills validation succeeded." in captured.out


def test_should_return_one_and_print_errors_when_main_fails(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        skills_validation,
        "validate_all",
        lambda repo_root=None: ["err-1", "err-2"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Skills validation failed:" in captured.out
    assert "- err-1" in captured.out
    assert "- err-2" in captured.out
