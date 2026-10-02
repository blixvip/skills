<h1 align="center">Skills</h1>

<p align="center">
  <b>Drop-in agent skills that make Codex and Claude Code better at motion graphics, thumbnails, UI polish, and shipping fast.</b>
</p>

<p align="center">
  <a href="https://github.com/blixvip/skills/stargazers"><img src="https://img.shields.io/github/stars/blixvip/skills?style=flat-square&color=a371f7" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-111?style=flat-square" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/skills-21-111?style=flat-square" alt="21 skills">
  <img src="https://img.shields.io/badge/works%20with-Codex%20%C2%B7%20Claude%20Code-111?style=flat-square" alt="Codex and Claude Code">
  <a href="https://discord.gg/zEB4VjmfSb"><img src="https://img.shields.io/badge/Discord-Join%20the%20community-5865F2?style=flat-square&logo=discord&logoColor=white" alt="Discord"></a>
</p>

<p align="center">
  <a href="#motion-graphics">Motion graphics</a> ·
  <a href="#thumbnails">Thumbnails</a> ·
  <a href="#ui-and-frontend">UI and frontend</a> ·
  <a href="#working-speed">Working speed</a> ·
  <a href="#project-workflow">Project workflow</a> ·
  <a href="#install">Install</a>
</p>

---

Agent skills by [@blixvip](https://github.com/blixvip) for Codex and Claude Code. Each top-level folder is one self-contained skill: a `SKILL.md`, plus optional `agents/openai.yaml` metadata and `references/`. No build step, no dependencies: copy a folder and the agent picks it up.

## Motion graphics

A complete system for turning footage and a script into edits that don't look AI-generated. Start with `motion-pipeline`; it runs the other four in order.

| Skill | What it does |
| --- | --- |
| [`motion-pipeline`](motion-pipeline/) | The end-to-end runbook: stage order, quality gates, on-disk layout, engine choice, parallel shot builds, and the ship checklist. Use it first for any whole edit. |
| [`motion-plan`](motion-plan/) | Turns a script or transcript into a shot-by-shot plan: which lines earn a visual, which stay bare A-roll, what each shows, and how long it holds. |
| [`motion-assets`](motion-assets/) | Sources, generates, and conforms real assets (palette from the footage, references, 3D/Lottie/SVG/textures/SFX, AI stills) into one look. |
| [`motion-design`](motion-design/) | Designs the frames: footage-derived palette, type pairing, five scene archetypes, layering for depth, and an anti-slop checklist. |
| [`motion-animate`](motion-animate/) | The motion vocabulary: pop-blur-fade text, staggers, eased cameras, entrances, and timing/easing tables, with Remotion and HyperFrames (GSAP) code. |
| [`ae-extendscript`](ae-extendscript/) | Drives After Effects with ExtendScript: a result-file bridge for real errors, a PNG render loop to see the result, and the ES3 traps that break scripts. |

## Thumbnails

- [`thumbnail`](thumbnail/): finished YouTube thumbnails from a topic, title, script, or reference photo, with strong hooks, readable composition, and controlled A/B variants.

## UI and frontend

- [`components`](components/): improve an existing site or app with components from a curated list of high-quality UI libraries.
- [`shader-ui`](shader-ui/): tasteful, localized shaders for accents, animated fills, edge lighting, liquid glass, and WebGL backgrounds.
- [`ui-intergrity`](ui-intergrity/) (folder name kept as-is so existing installs keep working): prevent and fix overlap, stacking, clipping, and layout-shift bugs, especially in extensions and injected UI.

## Working speed

- [`1`](1/) · [`2`](2/) · [`3`](3/) · [`4`](4/) · [`5`](5/): execution timeboxes from 3 to 25 minutes, scaled to how involved the task is.
- [`asap`](asap/): the shortest reliable path to a working result.
- [`instant`](instant/): the fastest useful answer, with no unnecessary tool calls.
- [`huh`](huh/): a terse status of what's happening right now.

## Project workflow

- [`github`](github/): audit, document, validate, commit, and safely publish a project to GitHub.
- [`backbefore`](backbefore/): restore the version before a rejected change, then reapply the latest request minimally.
- [`quick-context`](quick-context/): load a project's `CLAUDE.md` when a session starts outside it.

## Install

Clone once, then copy the skills you want:

```powershell
git clone https://github.com/blixvip/skills.git

# Codex
Copy-Item -Recurse .\skills\motion-pipeline "$env:USERPROFILE\.codex\skills\motion-pipeline"

# Claude Code
Copy-Item -Recurse .\skills\motion-pipeline "$env:USERPROFILE\.claude\skills\motion-pipeline"
```

On macOS or Linux:

```bash
git clone https://github.com/blixvip/skills.git

# Codex
mkdir -p ~/.codex/skills && cp -R skills/motion-pipeline ~/.codex/skills/

# Claude Code
mkdir -p ~/.claude/skills && cp -R skills/motion-pipeline ~/.claude/skills/
```

For the full motion-graphics system, copy all six motion skills: `motion-pipeline`, `motion-plan`, `motion-assets`, `motion-design`, `motion-animate`, and `ae-extendscript`. Restart Codex or Claude Code after installing.

## Anatomy of a skill

```
<skill>/
  SKILL.md             name + description frontmatter, then the instructions
  agents/openai.yaml   optional display metadata for Codex
  references/          optional deeper docs the skill links to
  scripts/             optional helpers (e.g. github/scripts/*.py)
```

## Community

💬 [Join the Discord](https://discord.gg/zEB4VjmfSb) for questions, help, feedback, and updates.

## License

[MIT](LICENSE).
