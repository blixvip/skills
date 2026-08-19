#!/usr/bin/env python3
"""Validate an explicit Git remote before a non-forced branch push."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def value(command: list[str], cwd: Path) -> str | None:
    result = run(command, cwd)
    return result.stdout.strip() if result.returncode == 0 else None


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 2


def redact_url(url: str) -> str:
    return re.sub(r"//[^/@]+@", "//***@", url)


def github_owner(url: str) -> str | None:
    match = re.search(r"github\.com[:/]([^/]+)/", url)
    return match.group(1) if match else None


def remote_sha(remote: str, branch: str, cwd: Path) -> str | None:
    result = run(["git", "ls-remote", remote, f"refs/heads/{branch}"], cwd)
    if result.returncode != 0:
        return None
    return result.stdout.split("\t", 1)[0].strip() if result.stdout.strip() else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Repository path.")
    parser.add_argument("--remote", default="origin", help="Explicit Git remote name.")
    parser.add_argument("--branch", help="Target branch; defaults to the current branch.")
    parser.add_argument("--expected-owner", help="Required GitHub owner, when known.")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--dry-run", action="store_true", help="Validate without pushing.")
    action.add_argument("--push", action="store_true", help="Push after validation; never force-pushes.")
    args = parser.parse_args()

    cwd = Path(args.path).expanduser().resolve()
    if not cwd.exists():
        return fail(f"path does not exist: {cwd}")
    root = value(["git", "rev-parse", "--show-toplevel"], cwd)
    if not root:
        return fail("path is not inside a Git repository")
    cwd = Path(root)
    if value(["git", "status", "--short"], cwd):
        return fail("worktree is dirty; commit or stash intended changes before remote actions")
    branch = args.branch or value(["git", "branch", "--show-current"], cwd)
    if not branch:
        return fail("cannot infer a branch from detached HEAD; pass --branch explicitly")
    if run(["git", "check-ref-format", "--branch", branch], cwd).returncode != 0:
        return fail(f"invalid target branch: {branch}")
    remote_url = value(["git", "remote", "get-url", args.remote], cwd)
    if not remote_url:
        return fail(f"remote is not configured: {args.remote}")
    owner = github_owner(remote_url)
    if args.expected_owner and owner != args.expected_owner:
        return fail(f"remote owner is {owner or 'not GitHub'}, not expected owner {args.expected_owner}")
    local_sha = value(["git", "rev-parse", "HEAD"], cwd)
    if not local_sha:
        return fail("cannot resolve local HEAD")
    remote_before = remote_sha(args.remote, branch, cwd)
    if remote_before is None:
        return fail("could not contact the configured remote")

    print(f"Remote: {redact_url(remote_url)}")
    print(f"Branch: {branch}")
    print(f"Local SHA: {local_sha}")
    print(f"Remote SHA: {remote_before or '(branch does not exist)'}")
    if args.dry_run:
        print("Dry run passed; no remote mutation performed.")
        return 0
    if not args.push:
        print("Guard passed; no push requested.")
        return 0

    pushed = run(["git", "push", args.remote, f"HEAD:refs/heads/{branch}"], cwd)
    if pushed.returncode != 0:
        return fail("push failed; inspect the remote branch without force-pushing")
    remote_after = remote_sha(args.remote, branch, cwd)
    if remote_after != local_sha:
        return fail("remote SHA does not match local HEAD after push")
    print(f"Pushed SHA: {remote_after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
