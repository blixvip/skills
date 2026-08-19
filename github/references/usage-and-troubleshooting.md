# Failures

Use this reference when a targeted command fails.

- Re-run only the affected command after fixing its direct cause.
- Do not suppress failing tests, change lockfiles opportunistically, or reinstall dependencies unless the project requires it.
- For authentication failures, inspect `gh auth status`; do not reveal tokens or ask users to paste them.
- For remote rejection, fetch and inspect the target branch before integrating; never force-push.
- For missing tooling, report the exact command and dependency needed instead of substituting unrelated checks.
