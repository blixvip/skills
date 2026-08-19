# Safety response

Use this reference when the audit finds a risk.

- Never print a suspected secret value. Identify only the file and risk type.
- Stop before staging or pushing a tracked credential, private key, environment file, or oversized file.
- If a secret is already committed, recommend rotation and history remediation before publishing; removing it from the working tree alone is insufficient.
- Preserve unrelated user work. Do not reset, clean, force-push, or rewrite history to resolve a risk.
- Treat unclear ownership, target repository, or existing-visibility changes as blockers that require explicit direction.
