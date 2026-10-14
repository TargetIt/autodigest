#!/usr/bin/env python3
"""Verify research submodule locations and cited files without running upstream code."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "Research" / "evidence"


def git(path, *args):
    return subprocess.check_output(
        ["git", "-C", str(path), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def main():
    checkouts = json.loads((EVIDENCE / "source-checkouts.json").read_text())["repositories"]
    source_index = json.loads((EVIDENCE / "source-index.json").read_text())
    sources = source_index["sources"]
    failures = []
    repositories = [row["repository"] for row in checkouts]
    expected_paths = {"Research/repos/" + repo for repo in repositories}
    if len(repositories) != 40 or len(set(repositories)) != 40:
        failures.append("checkout manifest must contain 40 distinct repositories")
    if set(repositories) != {source["repository"] for source in sources}:
        failures.append("checkout manifest and source index repository sets differ")
    if len(sources) != source_index["source_link_count"]:
        failures.append("source reference count differs from source index metadata")
    if {row["path"] for row in checkouts} != expected_paths:
        failures.append("checkout paths do not match repository names")
    gitlinks = {
        line.split("\t", 1)[1]
        for line in git(ROOT, "ls-files", "--stage", "--", "Research/repos").splitlines()
        if line.startswith("160000 ")
    }
    configured_paths = [
        line.split(" ", 1)[1]
        for line in git(ROOT, "config", "--file", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$").splitlines()
    ]
    if gitlinks != expected_paths:
        failures.append("parent gitlink paths differ from checkout manifest")
    if len(configured_paths) != 40 or set(configured_paths) != expected_paths:
        failures.append(".gitmodules paths differ from checkout manifest")
    locations = {}
    for row in checkouts:
        repo = row["repository"]
        relative = row["path"]
        location = ROOT / relative
        locations[repo] = (location, row["commit_sha"])
        try:
            if not (location / ".git").exists():
                raise ValueError("submodule is not initialized")
            if git(location, "rev-parse", "--show-toplevel") != str(location):
                raise ValueError("path is not the submodule worktree root")
            if git(location, "rev-parse", "HEAD") != row["commit_sha"]:
                raise ValueError("HEAD differs from research version")
            entry = git(ROOT, "ls-files", "--stage", "--", relative)
            if entry != "160000 {} 0\t{}".format(row["commit_sha"], relative):
                raise ValueError("parent index gitlink differs from research version")
            for key, expected in (("path", relative), ("url", row["url"])):
                actual = git(ROOT, "config", "--file", ".gitmodules", "submodule.{}.{}".format(repo, key))
                if actual != expected:
                    raise ValueError(".gitmodules {} differs".format(key))
            if git(location, "status", "--porcelain", "--untracked-files=all"):
                raise ValueError("submodule contains local changes")
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            failures.append("{}: {}".format(repo, exc))

    for source in sources:
        label = "{}:{}".format(source["repository"], source["path"])
        try:
            location, commit = locations[source["repository"]]
            if commit != source["commit_sha"]:
                raise ValueError("cited commit differs from checkout manifest")
            content = (location / source["path"]).read_bytes()
            if hashlib.sha256(content).hexdigest() != source["file_sha256"]:
                raise ValueError("cited file SHA-256 differs")
            line_count = len(content.decode("utf-8").splitlines())
            start, end = source["line_start"], source["line_end"]
            if line_count != source["file_lines"]:
                raise ValueError("cited file line count differs")
            if (start is not None or end is not None) and not (
                isinstance(start, int) and isinstance(end, int) and 1 <= start <= end <= line_count
            ):
                raise ValueError("cited line range is outside file")
        except (KeyError, OSError, ValueError) as exc:
            failures.append("{}: {}".format(label, exc))

    if failures:
        print("Source checkout verification failed:", file=sys.stderr)
        for failure in failures:
            print("- " + failure, file=sys.stderr)
        return 1
    print("Verified {} fixed-version submodules and {} source references.".format(len(checkouts), len(sources)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
