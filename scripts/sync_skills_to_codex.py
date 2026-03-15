from __future__ import annotations

import shutil
from pathlib import Path

from api_bootstrapper_cli.skills_validation import (
    CODEX_INTERFACE,
    SKILL_NAMES,
    get_agentskills_root,
    get_codex_root,
    get_embedded_agentskills_root,
    get_embedded_codex_root,
    render_openai_yaml,
)


def _sync_to_target(
    agents_root: Path,
    target_root: Path,
    *,
    with_openai_yaml: bool,
) -> int:
    target_root.mkdir(parents=True, exist_ok=True)
    for skill_name in SKILL_NAMES:
        source_dir = agents_root / skill_name
        target_dir = target_root / skill_name

        if with_openai_yaml and skill_name not in CODEX_INTERFACE:
            print(f"Missing CODEX_INTERFACE metadata for skill: {skill_name}")
            return 1

        if not source_dir.exists():
            print(f"Missing canonical skill source: {source_dir}")
            return 1

        if target_dir.exists():
            shutil.rmtree(target_dir)

        shutil.copytree(source_dir, target_dir)

        if with_openai_yaml:
            agents_dir = target_dir / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)

            openai_file = agents_dir / "openai.yaml"
            openai_file.write_text(render_openai_yaml(skill_name), encoding="utf-8")

    print(f"Synced {len(SKILL_NAMES)} skills to {target_root}")
    return 0


def sync_skills() -> int:
    agents_root = get_agentskills_root()
    codex_root = get_codex_root()
    embedded_root = get_embedded_codex_root()
    embedded_agentskills_root = get_embedded_agentskills_root()

    if not agents_root.exists():
        print(f"Missing canonical skills directory: {agents_root}")
        return 1

    status = _sync_to_target(agents_root, codex_root, with_openai_yaml=True)
    if status != 0:
        return status

    status = _sync_to_target(agents_root, embedded_root, with_openai_yaml=True)
    if status != 0:
        return status

    status = _sync_to_target(
        agents_root,
        embedded_agentskills_root,
        with_openai_yaml=False,
    )
    if status != 0:
        return status

    return 0


def main() -> int:
    return sync_skills()


if __name__ == "__main__":
    raise SystemExit(main())
