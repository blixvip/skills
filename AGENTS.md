# AGENTS.md

## Project

Public repository of two reusable agent skills: native AFFiNE automation and production UI work.
Each skill folder is copied directly into a Codex skills directory.

## Commands

- No repository-wide build or test command exists.
- Exercise `affine-native/scripts/affine.py` only through the workflow documented by that skill.

## Structure

- `affine-native/SKILL.md` — native AFFiNE automation instructions.
- `affine-native/scripts/affine.py` — desktop automation helper.
- `affine-native/references/protocol.md` — automation protocol details.
- `ui-max/SKILL.md` — UI design/implementation workflow.
- `ui-max/references/` — component selection and design standards.
- `*/agents/openai.yaml` — skill metadata.
- `README.md` — public inventory and installation instructions.

## Rules

- Keep skill frontmatter names/descriptions accurate and scoped.
- Read the entire changed `SKILL.md` and every routed reference before editing.
- Prefer concise core instructions with explicit links to optional references.
- Keep relative paths portable after copying a skill to another machine.
- Update `agents/openai.yaml` when a skill name, description, or invocation changes.
- Never embed credentials, machine state, or private project data.
- Keep README inventory/install paths synchronized with actual folders.

## Before finishing

- Follow the changed skill from entrypoint through each required reference/script.
- Confirm all links and paths resolve after standalone installation.
- Validate Python syntax when `affine-native/scripts/affine.py` changes.
