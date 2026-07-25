---
name: affine-native
description: Automate the native AFFiNE desktop app through local Electron CDP with compact deterministic commands for connection, page creation, titles, Edgeless canvas construction, inspection, and screenshots. Use when an agent must connect to AFFiNE, edit AFFiNE notes, create or modify an Edgeless board, convert structured content into an AFFiNE canvas, or recover an AFFiNE automation session while minimizing tokens and avoiding repeated DOM/API discovery.
---

# AFFiNE Native

Use the bundled helper. Do not rediscover AFFiNE internals during normal work.

## Fast path

Set the helper path once:

```powershell
$affineTool = "$env:USERPROFILE\.codex\skills\affine-native\scripts\affine.py"
```

Then run only the required commands:

```powershell
python $affineTool ensure
python $affineTool new --title "Page title"
python $affineTool board --spec C:\path\board.json
python $affineTool info
python $affineTool screenshot --path C:\path\check.png --y 650
```

If `ensure` reports AFFiNE already running without CDP, give one short update, then use `ensure --relaunch` for an authorized write task. It closes AFFiNE gracefully and relaunches it with debugging bound to `127.0.0.1:9222`. Never expose the port externally.

## Board spec

Describe rows, not individual coordinates. The helper calculates placement and card heights.

```json
{
  "title": "Page title",
  "newPage": false,
  "width": 2360,
  "rows": [
    {"kind": "title", "text": "MAIN TITLE"},
    {"kind": "section", "text": "01 / FIRST PHASE"},
    {"items": [
      {"kind": "card", "text": "A\n- Point\n- Point"},
      {"kind": "card", "text": "B\n- Point\n- Point"}
    ]},
    {"kind": "warning", "text": "COMMON FAILURE\nHow to avoid it"}
  ]
}
```

Supported kinds: `title`, `section`, `card`, `note`, `warning`, `quote`, `flow`. Use row `height` only when deterministic auto-height is unsuitable. Use `clearExisting: true` only when the user explicitly authorized replacement.

## Execution order

1. Convert source material into a hierarchy privately.
2. Decide new page versus existing page from the request; never assume replacement.
3. Run `ensure`; do not browse the web or open AFFiNE's website.
4. Run `new` only when a new document is required.
5. Write one compact row spec.
6. Run one `board` command. Keep batches under 80 nodes.
7. Run `info`. Screenshot only regions needing visual judgment.
8. Patch the spec or use one compact `eval` call; do not rebuild unaffected content.
9. Leave the viewport on the overview and return a terse result.

## Token rules

- Never dump `document.body.innerText`, full DOM, `outerHTML`, all buttons, or Base64 screenshots.
- Never search installed bundles for selectors unless the helper and recovery reference both fail.
- Never create one tool call per canvas node. Batch nodes in one spec.
- Return counts, document ID, title, bounds, and errors only.
- Use short ASCII text in automation payloads; avoid shell-encoding surprises.
- Reuse the current page and target. Let the helper rediscover a target only after navigation or reload.
- Prefer auto-height and equal-width rows over coordinate-by-coordinate design.
- Verify structurally first. Use at most one screenshot per uncertain region.
- Keep progress updates to one short sentence. Keep the final response to outcome plus essential location/status.
- Do not narrate analysis, connection mechanics, styling choices, or intermediate retries.

## Failure budget

Apply a known recovery once. If it fails again, read [references/protocol.md](references/protocol.md). Do not load that file during successful normal runs. After three repetitions of the same blocker, stop and report the exact blocker.

## Custom operations

Pipe JavaScript only when the helper lacks an operation:

```powershell
python $affineTool eval --file C:\path\operation.js
```

Keep the expression self-contained and return a small JSON object. Read [references/protocol.md](references/protocol.md) before writing custom AFFiNE operations.
