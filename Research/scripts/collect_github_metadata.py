#!/usr/bin/env python3
"""Snapshot public GitHub repository metrics; requires an authenticated gh CLI.

Run from any directory. This only reads GitHub and writes the named local output.
It does not install repositories or refresh the prose report automatically.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
from urllib.parse import quote


RESEARCH = Path(__file__).resolve().parents[1]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def api(endpoint: str, optional: bool = False):
    result = subprocess.run(
        ["gh", "api", endpoint, "-H", "Accept: application/vnd.github+json"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        if optional and "HTTP 404" in result.stderr:
            return None
        raise RuntimeError(f"{endpoint}: {result.stderr.strip()}")
    return json.loads(result.stdout)


def collect(slug: str) -> dict:
    repo_endpoint = f"repos/{slug}"
    repo = api(repo_endpoint)
    canonical = repo["full_name"]
    commit_endpoint = f"repos/{canonical}/commits/{quote(repo['default_branch'], safe='')}"
    release_endpoint = f"repos/{canonical}/releases/latest"
    commit = api(commit_endpoint)
    release = api(release_endpoint, optional=True)
    fields = (
        "id", "full_name", "html_url", "description", "homepage", "stargazers_count",
        "forks_count", "subscribers_count", "open_issues_count", "language", "license",
        "created_at", "updated_at", "pushed_at", "archived", "disabled", "fork",
        "default_branch", "topics", "size", "visibility",
    )
    return {
        "requested_slug": slug,
        "retrieved_at_utc": now(),
        "api_endpoints": {
            "repository": f"https://api.github.com/{repo_endpoint}",
            "head_commit": f"https://api.github.com/{commit_endpoint}",
            "latest_release": f"https://api.github.com/{release_endpoint}",
        },
        "repository": {key: repo.get(key) for key in fields},
        "default_branch_head": {
            "sha": commit["sha"],
            "html_url": commit["html_url"],
            "committed_at": commit["commit"]["committer"]["date"],
            "subject": commit["commit"]["message"].splitlines()[0],
        },
        "latest_release": None if release is None else {
            key: release.get(key)
            for key in ("tag_name", "name", "html_url", "published_at", "prerelease", "draft")
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repos", type=Path, default=RESEARCH / "evidence" / "repositories.json")
    parser.add_argument("--output", type=Path, default=RESEARCH / "evidence" / "github-metadata.json")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    slugs = json.loads(args.repos.read_text(encoding="utf-8"))
    if not isinstance(slugs, list) or not all(isinstance(s, str) and s.count('/') == 1 for s in slugs):
        raise SystemExit("--repos must contain a JSON array of owner/repository strings")
    started = now()
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        records = list(executor.map(collect, slugs))
    snapshot = {
        "schema_version": 1,
        "collection_started_at_utc": started,
        "collection_finished_at_utc": now(),
        "method": "GitHub REST API through gh api; metrics are repository-level, not skill-level",
        "notes": [
            "open_issues_count includes open pull requests; it is not a defect count",
            "updated_at can change without code changes; default_branch_head.committed_at is supplied separately",
            "latest_release null means the endpoint returned 404, not that the project is inactive",
            "latest_release can describe a monorepo subpackage rather than the entire project",
            "repository.license is GitHub detection; the source license must be reviewed separately",
        ],
        "repositories": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    for record in records:
        r = record["repository"]
        print(f"{r['full_name']}: {r['stargazers_count']:,} stars; {r['forks_count']:,} forks")
    print(f"Saved {len(records)} repositories to {args.output}")


if __name__ == "__main__":
    main()
