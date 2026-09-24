# Skills

Agent skills by [@blixvip](https://github.com/blixvip) for Codex and Claude Code. Each top-level folder is one self-contained skill: a `SKILL.md`, plus optional `agents/openai.yaml` metadata and `references/`.

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
- [`ui-intergrity`](ui-intergrity/): prevent and fix overlap, stacking, clipping, and layout-shift bugs, especially in extensions and injected UI.

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

For the full motion-graphics system, copy all six motion skills: `motion-pipeline`, `motion-plan`, `motion-assets`, `motion-design`, `motion-animate`, and `ae-extendscript`. Restart Codex or Claude Code after installing.
