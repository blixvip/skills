---
name: quick-context
description: Quickly load the selected project's CLAUDE.md instructions when a session starts outside that project. Use only when explicitly invoked as /quick-context with an optional project name or path; avoid code scans, tests, and edits.
---

# /quick-context

Load the correct project's instructions into the session immediately.

## Find the project

Resolve the project in this order:

1. Use `$ARGUMENTS`: a project name, project path, repository path, or `CLAUDE.md` path.
2. Use the active project selected in Note Overlay, when available.
3. Use the current Git repository root.

For a project name, check Note Overlay's project registry or known project folders. Never scan the entire computer. If multiple projects match, ask for one short selection instead of guessing.

## Load the context

From the resolved project root:

- Read the complete `CLAUDE.md` and/or `.claude/CLAUDE.md`.
- Read `CLAUDE.local.md` when present.
- Follow and read any `@...` imports referenced by those files.
- Read independent context files in parallel when possible.
- Treat the resolved root as the active project root for future work.

Internalize the project's purpose, architecture, commands, conventions, constraints, priorities, and warnings. Do not scan the codebase, run tests, edit files, or summarize everything. Never claim that context is loaded until the files were actually read.

Return only:

```
⚡ Context loaded: [project]
Root: [absolute path]
Read: [context files]
```

If nothing is found, return only:

```
⛔ Context not found: [project/path]
```
