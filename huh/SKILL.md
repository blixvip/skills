---
name: huh
description: Instantly report what is happening right now. Use when the user invokes /huh or asks for a terse status of current or recent activity; prioritize speed and avoid deep analysis, searches, tests, builds, or expensive tool calls.
---

# /huh

Report the current activity immediately.

## Constraints

- Target a response in 15 seconds or less.
- Use the fastest available model when model switching is supported.
- Inspect only recent context/output and quick Git status when needed.
- Do not perform deep analysis, searches, tests, builds, or expensive tool calls.

## Response format

Return no more than five lines in this exact shape:

⚡ **[Active / Done / Blocked / Waiting]**

- **Doing:** State the current activity.
- **Just did:** State the last important action and result.
- **Changed:** State what actually changed.
- **Next:** State what happens next.

Put errors or blockers first. Report only current or recent activity; do not guess, recap the project, add filler, or explain.
