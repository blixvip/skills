---
name: "5"
description: "Maximum normal execution timebox for complex tasks that should still be completed quickly. Use when the user invokes /5 and target completion within 25 minutes."
---

# /5 — Full

Take full ownership of this task and drive it to a completed, verified state.

## Timebox

Target completion in under 25 minutes. This is the largest normal execution window, not permission to work slowly. Quality remains the same as every other level.

## Behavior

- Investigate thoroughly enough to understand the affected system.
- Create a concise internal execution path and begin implementation quickly.
- Handle cross-file and cross-component changes when required.
- Resolve root causes instead of symptoms.
- Make necessary architectural improvements when they materially improve correctness.
- Cover important edge cases, failure states, and integration boundaries.
- Run the strongest relevant verification available.
- Test connected functionality for regressions.
- Iterate on failures until the implementation works.
- Remove dead code, temporary workarounds, and debugging artifacts introduced during the task.
- Avoid unrelated feature work or perfectionism.

Use parallel work where possible: **investigation + implementation + testing + verification**. Do not spend the timebox narrating progress; spend it producing the result.

If the task genuinely cannot be completed inside the timebox because of an external blocker, complete as much verified work as possible and report the exact blocker rather than continuing indefinitely.
