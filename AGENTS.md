# AGENTS.md

## Project

Public collection of reusable Codex skills and slash-command workflows.
Each top-level skill is an independently installable folder, not application source.

## Commands

- No repository-wide build or test command exists.
- Validate changed helper scripts directly; `github/scripts/` contains the current Python helpers.

## Structure

- `<skill>/SKILL.md` — required skill instructions and frontmatter.
- `<skill>/agents/openai.yaml` — OpenAI-facing metadata when supplied.
- `github/references/` — detailed GitHub workflow, safety, research, and template guidance.
- `github/scripts/` — repository audit and remote-guard helpers.
- `README.md` — public inventory; keep it synchronized with top-level skill folders.

## Rules

- Keep each skill narrowly scoped with accurate `name` and `description` frontmatter.
- Read a changed skill completely before editing its supporting references or scripts.
- Keep `SKILL.md` concise; move optional depth into `references/` and route to it explicitly.
- Use relative links within a skill package so installed copies remain portable.
- Keep destructive/external actions explicit and guarded.
- Update matching `agents/openai.yaml` metadata when skill identity or invocation changes.
- Do not add generated caches, local credentials, or machine-specific paths.

## Before finishing

- Re-read the changed skill as an agent would, following every referenced relative path.
- Confirm frontmatter parses and all referenced files exist.
- Update `README.md` when adding, removing, or renaming a public skill.
