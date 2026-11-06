#!/usr/bin/env python3
"""Check that every top-level skill folder has a SKILL.md with valid YAML frontmatter.

Rules (from CONTRIBUTING.md): frontmatter parses, `name` equals the folder name,
`description` is a non-empty string under 1024 characters.
Run from the repo root: python3 .github/scripts/check_skills.py
"""
import sys
from pathlib import Path

import yaml

MAX_DESCRIPTION = 1024


def check(path: Path, skill_md: Path) -> list[str]:
    folder = path.parent.name
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [f"{skill_md}: must start with a '---' frontmatter line"]
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return [f"{skill_md}: frontmatter has no closing '---'"]
    try:
        meta = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as error:
        return [f"{skill_md}: frontmatter is not valid YAML: {error}"]
    if not isinstance(meta, dict):
        return [f"{skill_md}: frontmatter must be a YAML mapping"]
    errors = []
    name, description = meta.get("name"), meta.get("description")
    if not isinstance(name, str) or not name:
        errors.append(f"{skill_md}: 'name' is missing or not a string (quote it if it starts with a digit)")
    elif name != folder:
        errors.append(f"{skill_md}: 'name' is {name!r} but the folder is {folder!r}")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{skill_md}: 'description' is missing or empty")
    elif len(description) >= MAX_DESCRIPTION:
        errors.append(f"{skill_md}: 'description' is {len(description)} characters (keep it under {MAX_DESCRIPTION})")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    folders = sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
    errors = []
    checked = 0
    for folder in folders:
        skill_md = folder / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{folder.name}/: top-level folder has no SKILL.md")
            continue
        errors += check(skill_md, skill_md.relative_to(root))
        checked += 1
    for error in errors:
        print(f"error: {error}")
    print(f"Checked {checked} skills, {len(errors)} problem(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
