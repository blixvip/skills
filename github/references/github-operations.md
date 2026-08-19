# GitHub operations

Use this reference for any remote action.

1. Run `gh auth status` and confirm the intended account.
2. Preserve the remote's existing visibility and default branch unless the user explicitly authorizes a change.
3. Before pushing, run:

   ```sh
   python <skill-dir>/scripts/remote_guard.py --path . --remote origin --dry-run
   ```

4. Push only after the dry run passes:

   ```sh
   python <skill-dir>/scripts/remote_guard.py --path . --remote origin --push
   ```

5. Verify the pushed SHA with `git ls-remote origin refs/heads/<branch>` and inspect remote metadata with `gh repo view`.

Use `--expected-owner <owner>` with `remote_guard.py` when the target GitHub owner is known. The script refuses dirty worktrees, force pushes, and implicit remote targets.
