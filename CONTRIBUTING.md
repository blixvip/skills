# Contributing to Skills

> 💬 **Before you open a PR, join the [blix open source Discord](https://discord.gg/wJfHQXfEMM).** It's the home for contributors across every blixvip repo: ask questions, run ideas by us, and talk through your PR.

Thanks for helping! Questions and ideas are welcome in the **[Discord](https://discord.gg/wJfHQXfEMM)**, and bugs go in [GitHub issues](https://github.com/blixvip/skills/issues/new/choose).

## Finding something to work on

- [Good first issues](https://github.com/blixvip/skills/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are small and list the files and lines to touch.
- [Help wanted](https://github.com/blixvip/skills/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) issues are bigger, and that includes new skills.
- Comment on the issue to claim it so two people don't build the same thing. If you go quiet for a week, it opens up again.
- Want to add a skill nobody asked for? Open an issue or ask in Discord first and say what it does and which README category it belongs in. A skill that overlaps an existing one is usually better as an edit to that one.

By contributing, you agree your work is released under the project's [MIT License](LICENSE).

## Setup

There's no build step and no dependencies. A skill is a folder the agent reads.

```sh
git clone https://github.com/<you>/skills.git
cd skills
```

The only code is in `github/scripts/`: two stdlib-only Python scripts. To work on them you need **Python 3.9+**. Run them with `python3` (or `py -3` on Windows).

## Anatomy of a skill

```
<skill>/
  SKILL.md             frontmatter + the instructions (required)
  agents/openai.yaml   Codex display metadata (expected for every skill here)
  references/          optional deeper docs that SKILL.md links to
  scripts/             optional helpers the skill tells the agent to run
```

### Required frontmatter

```yaml
---
name: my-skill
description: What it does, then when to use it. "Use when the user asks to ..., says '...', or invokes /my-skill."
---
```

- `name` must equal the folder name: lowercase letters, digits and hyphens. The existing folder `ui-intergrity` is misspelled on purpose so existing installs keep working. Don't rename folders.
- `description` is what the agent uses to decide whether to load the skill, so put the trigger phrases in it. Keep it under 1024 characters. Most here are 150–550.
- Quote the value if it starts with a digit or contains `: ` (see `1/SKILL.md`).

### `agents/openai.yaml`

```yaml
interface:
  display_name: "My Skill"
  short_description: "Under ~60 characters"
  default_prompt: "Use $my-skill to ..."
```

If the skill should only run when invoked by name (like `quick-context`), add `policy: allow_implicit_invocation: false`. Update this file whenever the skill's name or invocation changes.

## Adding a skill

1. Create `<name>/SKILL.md` with the frontmatter above and `<name>/agents/openai.yaml`.
2. Keep `SKILL.md` focused on what the agent must do. Move long catalogues, recipes and examples into `references/` and link them with **relative** links (`[art direction](references/art-direction.md)`), so the folder still works after it's copied into `~/.claude/skills/`.
3. Don't reference other skills, tools or apps a user won't have. If you depend on another skill in this repo, name it; if it's external, link it.
4. Add the skill to the right section of `README.md` and bump the `skills-N` badge.

## Testing a skill locally

There's no automated test for instructions, so test by using it:

```sh
# Claude Code
mkdir -p ~/.claude/skills && cp -R my-skill ~/.claude/skills/
# Codex
mkdir -p ~/.codex/skills && cp -R my-skill ~/.codex/skills/
```

Restart the agent, then:

- **Trigger it implicitly** with a prompt that matches the description, without naming the skill, and check that it loads. Then check that an unrelated prompt does *not* load it.
- **Invoke it explicitly** (`/my-skill` in Claude Code, `$my-skill` in Codex) on a real task.
- **Follow every path** it mentions as the agent would: every relative link opens, and every script runs from an installed copy.
- Check that the frontmatter parses: `python3 -c "import sys,yaml; yaml.safe_load(open(sys.argv[1]).read().split('---')[1])" my-skill/SKILL.md`.

In the pull request, say which agent(s) you tested with, the prompt you used, and what happened. A short transcript excerpt is ideal.

## Before you open a pull request

```sh
python3 github/scripts/project_audit.py --path . --strict    # only if you touched github/scripts/
```

- Keep changes small and focused. One fix or one new skill per pull request.
- Don't add machine-specific paths (`C:/Users/...`, `/home/...`), credentials, or generated caches (`__pycache__/` is already ignored).
- Keep destructive or external actions in a skill explicit and guarded. For example, the `github` skill never force-pushes and never changes repository visibility without being asked.
- Don't make claims in a skill you haven't verified: tool flags, API parameters, library names, URLs.
- Scripts stay stdlib-only unless the pull request explains why not.

## Where things live

- `<skill>/SKILL.md`: one skill per top-level folder. `README.md` groups them into Motion graphics, Thumbnails, UI and frontend, Working speed, and Project workflow.
- `motion-pipeline/`: the orchestrator for `motion-plan`, `motion-assets`, `motion-design`, `motion-animate` and `ae-extendscript`. Changes to one of these often need a matching change in the pipeline.
- `github/scripts/project_audit.py`: the read-only pre-publish audit (secrets, dependency dirs, oversized files).
- `github/scripts/remote_guard.py`: validates the remote and branch, then does a non-forced push.
- `AGENTS.md`: the rules agents follow when editing this repo. They apply to humans too.

Made something with these skills? Show it off in the [Discord](https://discord.gg/wJfHQXfEMM).
