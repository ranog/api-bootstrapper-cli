from __future__ import annotations

import re
from pathlib import Path


SKILL_NAMES: tuple[str, ...] = (
    "api-bootstrapper-init",
    "api-bootstrapper-bootstrap-env",
    "api-bootstrapper-add-pre-commit",
    "api-bootstrapper-add-docker",
    "api-bootstrapper-add-alembic",
    "api-bootstrapper-bootstrap-flow",
    "api-bootstrapper-sync-branch",
    "api-bootstrapper-generate-commit-message",
    "api-bootstrapper-prepare-task",
    "api-bootstrapper-staff-review",
    "api-bootstrapper-understand-system",
    "api-bootstrapper-implement-feature-tdd",
    "api-bootstrapper-refactor-safely",
    "api-bootstrapper-create-tests",
    "api-bootstrapper-debug-issue",
    "api-bootstrapper-add-tool-support",
    "api-bootstrapper-review-code",
    "api-bootstrapper-prepare-pr",
    "api-bootstrapper-execute-task-universal",
)

SKILL_DIR_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

CODEX_INTERFACE: dict[str, dict[str, str]] = {
    "api-bootstrapper-init": {
        "display_name": "API Bootstrapper Init",
        "short_description": "Initialize a Python API project in one command.",
        "default_prompt": "Use $api-bootstrapper-init to initialize ./my-api with Python 3.12.12 and manager pyenv.",
    },
    "api-bootstrapper-bootstrap-env": {
        "display_name": "API Bootstrapper Bootstrap Env",
        "short_description": "Configure Python env and VSCode settings safely.",
        "default_prompt": "Use $api-bootstrapper-bootstrap-env to configure ./my-api with Python 3.12.12 and manager uv.",
    },
    "api-bootstrapper-add-pre-commit": {
        "display_name": "API Bootstrapper Add Pre Commit",
        "short_description": "Configure Ruff and Commitizen pre-commit hooks.",
        "default_prompt": "Use $api-bootstrapper-add-pre-commit to configure hooks in ./my-api.",
    },
    "api-bootstrapper-add-docker": {
        "display_name": "API Bootstrapper Add Docker",
        "short_description": "Create a Dockerfile for an existing Python API.",
        "default_prompt": "Use $api-bootstrapper-add-docker to add Docker support to ./my-api with Python 3.13.",
    },
    "api-bootstrapper-add-alembic": {
        "display_name": "API Bootstrapper Add Alembic",
        "short_description": "Configure Alembic migrations for a Python API project.",
        "default_prompt": "Use $api-bootstrapper-add-alembic to configure Alembic in ./my-api.",
    },
    "api-bootstrapper-bootstrap-flow": {
        "display_name": "API Bootstrapper Bootstrap Flow",
        "short_description": "Orchestrate full project bootstrap command sequences.",
        "default_prompt": "Use $api-bootstrapper-bootstrap-flow to propose and execute the full bootstrap flow for ./my-api.",
    },
    "api-bootstrapper-sync-branch": {
        "display_name": "API Bootstrapper Sync Branch",
        "short_description": "Safely sync the current branch with the remote default branch.",
        "default_prompt": "Use $api-bootstrapper-sync-branch to sync my current branch with origin/main before I commit.",
    },
    "api-bootstrapper-generate-commit-message": {
        "display_name": "API Bootstrapper Generate Commit Message",
        "short_description": "Generate a Conventional Commit message from staged changes.",
        "default_prompt": "Use $api-bootstrapper-generate-commit-message to propose a commit message from my current git diff.",
    },
    "api-bootstrapper-prepare-task": {
        "display_name": "API Bootstrapper Prepare Task",
        "short_description": "Structure complex tasks with context, requirements, tests, and validation.",
        "default_prompt": "Use $api-bootstrapper-prepare-task to structure this implementation request before coding.",
    },
    "api-bootstrapper-staff-review": {
        "display_name": "API Bootstrapper Staff Review",
        "short_description": "Run a staff-level review focused on architecture, risks, and test quality.",
        "default_prompt": "Use $api-bootstrapper-staff-review to review this change with staff engineer rigor.",
    },
    "api-bootstrapper-understand-system": {
        "display_name": "API Bootstrapper Understand System",
        "short_description": "Explain architecture and execution flow before making changes.",
        "default_prompt": "Use $api-bootstrapper-understand-system to explain this module flow before we modify it.",
    },
    "api-bootstrapper-implement-feature-tdd": {
        "display_name": "API Bootstrapper Implement Feature TDD",
        "short_description": "Implement features following TDD with small, safe changes.",
        "default_prompt": "Use $api-bootstrapper-implement-feature-tdd to implement this feature using tests first.",
    },
    "api-bootstrapper-refactor-safely": {
        "display_name": "API Bootstrapper Refactor Safely",
        "short_description": "Refactor code while preserving behavior and architectural boundaries.",
        "default_prompt": "Use $api-bootstrapper-refactor-safely to refactor this module without behavior changes.",
    },
    "api-bootstrapper-create-tests": {
        "display_name": "API Bootstrapper Create Tests",
        "short_description": "Create behavior-focused pytest coverage for existing modules.",
        "default_prompt": "Use $api-bootstrapper-create-tests to add missing tests for this module.",
    },
    "api-bootstrapper-debug-issue": {
        "display_name": "API Bootstrapper Debug Issue",
        "short_description": "Debug issues with reproduce-first, test-first correction workflow.",
        "default_prompt": "Use $api-bootstrapper-debug-issue to investigate and fix this bug with a failing test first.",
    },
    "api-bootstrapper-add-tool-support": {
        "display_name": "API Bootstrapper Add Tool Support",
        "short_description": "Add support for new external tools with managers and services.",
        "default_prompt": "Use $api-bootstrapper-add-tool-support to add support for this external tool in the CLI architecture.",
    },
    "api-bootstrapper-review-code": {
        "display_name": "API Bootstrapper Review Code",
        "short_description": "Perform technical code review focused on risks and regressions.",
        "default_prompt": "Use $api-bootstrapper-review-code to review this implementation before merge.",
    },
    "api-bootstrapper-prepare-pr": {
        "display_name": "API Bootstrapper Prepare PR",
        "short_description": "Prepare pull request summary with impact, tests, and validation commands.",
        "default_prompt": "Use $api-bootstrapper-prepare-pr to generate a PR summary from this branch changes.",
    },
    "api-bootstrapper-execute-task-universal": {
        "display_name": "API Bootstrapper Execute Task Universal",
        "short_description": "Apply a universal workflow for planning, tests, implementation, and validation.",
        "default_prompt": "Use $api-bootstrapper-execute-task-universal to execute this task end-to-end with the project workflow.",
    },
}


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_agentskills_root(repo_root: Path | None = None) -> Path:
    root = repo_root or get_repo_root()
    return root / "skills" / "agentskills"


def get_codex_root(repo_root: Path | None = None) -> Path:
    root = repo_root or get_repo_root()
    return root / "skills" / "codex"


def get_embedded_codex_root(repo_root: Path | None = None) -> Path:
    root = repo_root or get_repo_root()
    return root / "src" / "api_bootstrapper_cli" / "embedded_skills" / "codex"


def get_embedded_agentskills_root(repo_root: Path | None = None) -> Path:
    root = repo_root or get_repo_root()
    return root / "src" / "api_bootstrapper_cli" / "embedded_skills" / "agentskills"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with frontmatter delimiter '---'.")

    closing_marker = text.find("\n---\n", 4)
    if closing_marker == -1:
        raise ValueError("SKILL.md frontmatter closing delimiter not found.")

    frontmatter_block = text[4:closing_marker]
    parsed: dict[str, str] = {}

    for line in frontmatter_block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        key, separator, value = stripped.partition(":")
        if not separator:
            raise ValueError(f"Invalid frontmatter line: {line!r}")

        parsed[key.strip()] = value.strip().strip('"').strip("'")

    return parsed


def render_openai_yaml(skill_name: str) -> str:
    data = CODEX_INTERFACE[skill_name]
    return (
        "interface:\n"
        f'  display_name: "{data["display_name"]}"\n'
        f'  short_description: "{data["short_description"]}"\n'
        f'  default_prompt: "{data["default_prompt"]}"\n'
    )


def _validate_required_skill_dirs(root: Path) -> list[str]:
    errors: list[str] = []

    if not root.exists():
        return [f"Missing skills directory: {root}"]

    existing_dirs = {p.name for p in root.iterdir() if p.is_dir()}
    missing = sorted(set(SKILL_NAMES) - existing_dirs)
    extra = sorted(existing_dirs - set(SKILL_NAMES))

    if missing:
        errors.append(f"Missing skills in {root}: {', '.join(missing)}")

    if extra:
        errors.append(f"Unexpected skills in {root}: {', '.join(extra)}")

    return errors


def validate_structure(repo_root: Path | None = None) -> list[str]:
    root = repo_root or get_repo_root()
    agents_root = get_agentskills_root(root)

    errors = _validate_required_skill_dirs(agents_root)

    for skill_name in SKILL_NAMES:
        skill_dir = agents_root / skill_name
        if not skill_dir.exists():
            continue

        if not SKILL_DIR_PATTERN.match(skill_name):
            errors.append(f"Skill directory must be hyphen-case: {skill_name}")

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"Missing SKILL.md: {skill_md}")
            continue

        content = skill_md.read_text(encoding="utf-8")

        try:
            frontmatter = parse_frontmatter(content)
        except ValueError as exc:
            errors.append(f"Invalid frontmatter in {skill_md}: {exc}")
            continue

        keys = set(frontmatter)
        expected_keys = {"name", "description"}
        if keys != expected_keys:
            errors.append(
                f"Frontmatter keys in {skill_md} must be exactly name/description, got: {sorted(keys)}"
            )

        if frontmatter.get("name") != skill_name:
            errors.append(
                f"Frontmatter name mismatch in {skill_md}: {frontmatter.get('name')} != {skill_name}"
            )

        if not frontmatter.get("description", "").strip():
            errors.append(f"Frontmatter description cannot be empty: {skill_md}")

        reference_file = skill_dir / "references" / "parameters-and-errors.md"
        if not reference_file.exists():
            errors.append(f"Missing references file: {reference_file}")

    return errors


def validate_sync(repo_root: Path | None = None) -> list[str]:
    root = repo_root or get_repo_root()
    agents_root = get_agentskills_root(root)
    codex_root = get_codex_root(root)
    embedded_root = get_embedded_codex_root(root)
    embedded_agentskills_root = get_embedded_agentskills_root(root)

    errors = _validate_required_skill_dirs(codex_root)
    errors.extend(_validate_required_skill_dirs(embedded_root))
    errors.extend(_validate_required_skill_dirs(embedded_agentskills_root))

    for skill_name in SKILL_NAMES:
        agent_skill_dir = agents_root / skill_name
        codex_skill_dir = codex_root / skill_name
        embedded_skill_dir = embedded_root / skill_name

        if not agent_skill_dir.exists() or not codex_skill_dir.exists():
            continue

        agent_skill_md = agent_skill_dir / "SKILL.md"
        codex_skill_md = codex_skill_dir / "SKILL.md"

        if not codex_skill_md.exists():
            errors.append(f"Missing codex SKILL.md: {codex_skill_md}")
        elif agent_skill_md.read_text(encoding="utf-8") != codex_skill_md.read_text(
            encoding="utf-8"
        ):
            errors.append(f"SKILL.md divergence: {agent_skill_md} != {codex_skill_md}")

        agent_ref = agent_skill_dir / "references" / "parameters-and-errors.md"
        codex_ref = codex_skill_dir / "references" / "parameters-and-errors.md"

        if not codex_ref.exists():
            errors.append(f"Missing codex references file: {codex_ref}")
        elif agent_ref.read_text(encoding="utf-8") != codex_ref.read_text(
            encoding="utf-8"
        ):
            errors.append(f"References divergence: {agent_ref} != {codex_ref}")

        openai_yaml = codex_skill_dir / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            errors.append(f"Missing codex metadata file: {openai_yaml}")
        else:
            yaml_content = openai_yaml.read_text(encoding="utf-8")
            if f"${skill_name}" not in yaml_content:
                errors.append(
                    f"default_prompt in {openai_yaml} must mention ${skill_name}"
                )

        if not embedded_skill_dir.exists():
            continue

        embedded_skill_md = embedded_skill_dir / "SKILL.md"
        if not embedded_skill_md.exists():
            errors.append(f"Missing embedded SKILL.md: {embedded_skill_md}")
        elif agent_skill_md.read_text(encoding="utf-8") != embedded_skill_md.read_text(
            encoding="utf-8"
        ):
            errors.append(
                f"Embedded SKILL.md divergence: {agent_skill_md} != {embedded_skill_md}"
            )

        embedded_ref = embedded_skill_dir / "references" / "parameters-and-errors.md"
        if not embedded_ref.exists():
            errors.append(f"Missing embedded references file: {embedded_ref}")
        elif agent_ref.read_text(encoding="utf-8") != embedded_ref.read_text(
            encoding="utf-8"
        ):
            errors.append(
                f"Embedded references divergence: {agent_ref} != {embedded_ref}"
            )

        embedded_openai = embedded_skill_dir / "agents" / "openai.yaml"
        if not embedded_openai.exists():
            errors.append(f"Missing embedded metadata file: {embedded_openai}")
        else:
            embedded_yaml = embedded_openai.read_text(encoding="utf-8")
            if f"${skill_name}" not in embedded_yaml:
                errors.append(
                    f"default_prompt in {embedded_openai} must mention ${skill_name}"
                )

        embedded_agentskills_dir = embedded_agentskills_root / skill_name
        if not embedded_agentskills_dir.exists():
            continue

        embedded_agentskill_md = embedded_agentskills_dir / "SKILL.md"
        if not embedded_agentskill_md.exists():
            errors.append(
                f"Missing embedded Agent Skill SKILL.md: {embedded_agentskill_md}"
            )
        elif agent_skill_md.read_text(
            encoding="utf-8"
        ) != embedded_agentskill_md.read_text(encoding="utf-8"):
            errors.append(
                f"Embedded Agent Skill SKILL.md divergence: {agent_skill_md} != {embedded_agentskill_md}"
            )

        embedded_agentskill_ref = (
            embedded_agentskills_dir / "references" / "parameters-and-errors.md"
        )
        if not embedded_agentskill_ref.exists():
            errors.append(
                f"Missing embedded Agent Skill references file: {embedded_agentskill_ref}"
            )
        elif agent_ref.read_text(encoding="utf-8") != embedded_agentskill_ref.read_text(
            encoding="utf-8"
        ):
            errors.append(
                f"Embedded Agent Skill references divergence: {agent_ref} != {embedded_agentskill_ref}"
            )

    return errors


def validate_smoke(repo_root: Path | None = None) -> list[str]:
    root = repo_root or get_repo_root()
    agents_root = get_agentskills_root(root)

    errors: list[str] = []

    for skill_name in SKILL_NAMES:
        skill_md = agents_root / skill_name / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        if "Proceed? (yes/no)" not in content:
            errors.append(
                f"Skill must require explicit confirmation prompt: {skill_md}"
            )

    bootstrap_skill = (
        agents_root / "api-bootstrapper-bootstrap-env" / "SKILL.md"
    ).read_text(encoding="utf-8")

    if "--manager pyenv" not in bootstrap_skill:
        errors.append("Bootstrap-env skill must include a pyenv command example.")

    if "--manager uv" not in bootstrap_skill:
        errors.append("Bootstrap-env skill must include a uv command example.")

    flow_skill = (
        agents_root / "api-bootstrapper-bootstrap-flow" / "SKILL.md"
    ).read_text(encoding="utf-8")

    if "api-bootstrapper init --python" not in flow_skill:
        errors.append("Bootstrap-flow skill must include init command path.")

    alembic_skill = (
        agents_root / "api-bootstrapper-add-alembic" / "SKILL.md"
    ).read_text(encoding="utf-8")

    if "api-bootstrapper add-alembic --path" not in alembic_skill:
        errors.append("Add-alembic skill must include command usage with --path.")

    return errors


def validate_all(repo_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_structure(repo_root))
    errors.extend(validate_sync(repo_root))
    errors.extend(validate_smoke(repo_root))
    return errors


def main() -> int:
    errors = validate_all()

    if not errors:
        print("Skills validation succeeded.")
        return 0

    print("Skills validation failed:")
    for error in errors:
        print(f"- {error}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
