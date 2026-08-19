#!/usr/bin/env python3
"""Report a compact, non-destructive repository audit without exposing secrets."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


MAX_GITHUB_FILE_BYTES = 100 * 1024 * 1024
SECRET_FILENAMES = {".env", ".env.local", ".env.production", "id_rsa", "id_ed25519"}
SECRET_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
DEPENDENCY_PREFIXES = ("node_modules/", ".venv/", "venv/", "__pycache__/")
MANIFESTS = (
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Pipfile",
    "Cargo.toml",
    "go.mod",
    "Gemfile",
    "pom.xml",
    "build.gradle",
)
DOCS = ("README.md", "README", "LICENSE", "LICENSE.md", "SECURITY.md", "CONTRIBUTING.md")
ENTRY_POINTS = ("src", "app", "apps", "server", "main.py", "manage.py", "index.html")


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def git(command: list[str], cwd: Path) -> tuple[bool, str]:
    result = run(["git", *command], cwd)
    return result.returncode == 0, result.stdout.strip()


def git_root(path: Path) -> Path | None:
    ok, output = git(["rev-parse", "--show-toplevel"], path)
    return Path(output) if ok and output else None


def tracked_files(root: Path) -> list[str]:
    ok, output = git(["ls-files"], root)
    return output.splitlines() if ok and output else []


def read_private_key_header(path: Path) -> bool:
    try:
        private_key_marker = b"-----" + b"BEGIN "
        return private_key_marker in path.read_bytes()[:4096]
    except OSError:
        return False


def audit(path: Path) -> dict[str, Any]:
    root = git_root(path)
    report: dict[str, Any] = {
        "path": str(path),
        "repository": str(root) if root else None,
        "git": {},
        "manifests": [],
        "docs": [],
        "entry_points": [],
        "warnings": [],
        "errors": [],
    }
    if root is None:
        report["errors"].append("Path is not inside a Git repository.")
        return report

    report["path"] = str(root)
    branch_ok, branch = git(["branch", "--show-current"], root)
    status_ok, status = git(["status", "--short"], root)
    remotes_ok, remotes = git(["remote", "-v"], root)
    log_ok, recent = git(["log", "--oneline", "-5"], root)
    report["git"] = {
        "branch": branch if branch_ok and branch else "detached-or-unknown",
        "dirty": bool(status) if status_ok else None,
        "remotes": remotes.splitlines() if remotes_ok else [],
        "recent_commits": recent.splitlines() if log_ok else [],
    }

    for name in MANIFESTS:
        if (root / name).is_file():
            report["manifests"].append(name)
    for name in DOCS:
        if (root / name).is_file():
            report["docs"].append(name)
    for name in ENTRY_POINTS:
        if (root / name).exists():
            report["entry_points"].append(name)

    if not any(name.lower().startswith("readme") for name in report["docs"]):
        report["warnings"].append("No README found at the repository root.")
    if status_ok and status:
        report["warnings"].append("Worktree has uncommitted changes; stage only intended paths.")
    if not report["git"]["remotes"]:
        report["warnings"].append("No Git remote is configured.")

    for relative_name in tracked_files(root):
        relative = relative_name.replace("\\", "/")
        candidate = root / relative_name
        lower_name = Path(relative).name.lower()
        suffix = Path(relative).suffix.lower()
        if lower_name in SECRET_FILENAMES or suffix in SECRET_SUFFIXES:
            report["errors"].append(f"Potential credential file is tracked: {relative}")
        if relative.startswith(DEPENDENCY_PREFIXES):
            report["errors"].append(f"Dependency or cache directory is tracked: {relative}")
        try:
            if candidate.is_file() and candidate.stat().st_size > MAX_GITHUB_FILE_BYTES:
                report["errors"].append(f"Tracked file exceeds GitHub's 100 MB limit: {relative}")
            if candidate.is_file() and read_private_key_header(candidate):
                report["errors"].append(f"Potential private-key content is tracked: {relative}")
        except OSError:
            report["warnings"].append(f"Could not inspect tracked file: {relative}")

    report["errors"] = sorted(set(report["errors"]))
    report["warnings"] = sorted(set(report["warnings"]))
    return report


def emit_text(report: dict[str, Any]) -> None:
    print(f"Repository: {report['repository'] or report['path']}")
    git_info = report.get("git", {})
    if git_info:
        print(f"Branch: {git_info.get('branch', 'unknown')}")
        print(f"Worktree: {'dirty' if git_info.get('dirty') else 'clean'}")
        print("Remotes: " + (", ".join(git_info.get("remotes", [])) or "none"))
        print("Recent commits:")
        for commit in git_info.get("recent_commits", []):
            print(f"  {commit}")
    for label in ("manifests", "docs", "entry_points", "warnings", "errors"):
        values = report.get(label, [])
        print(f"{label.replace('_', ' ').title()}: " + (", ".join(values) if values else "none"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=".", help="Repository path to inspect.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when a safety error is found.")
    args = parser.parse_args()

    path = Path(args.path).expanduser().resolve()
    if not path.exists():
        print(f"error: path does not exist: {path}", file=sys.stderr)
        return 2
    report = audit(path)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        emit_text(report)
    return 1 if args.strict and report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
