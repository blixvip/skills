---
name: "2"
description: "Short execution timebox for straightforward tasks requiring a little investigation and verification. Use when the user invokes /2 and target completion within 8 minutes."
---

# /2 — Short

Complete the task efficiently while maintaining full implementation quality.

## Timebox

Target completion in under 8 minutes. Quality stays constant; spend the additional time on necessary understanding and verification rather than unnecessary explanation.

## Behavior

- Quickly inspect the relevant code before changing it.
- Form a lightweight implementation approach internally.
- Make the smallest complete change.
- Follow existing architecture and conventions.
- Investigate dependencies only when necessary.
- Test the primary behavior and obvious nearby edge cases.
- Fix regressions introduced by the change.
- Avoid unrelated cleanup and speculative improvements.
- Do not narrate routine work.

Prioritize: **understand → implement → verify → finish**. Return a concise completion summary.
