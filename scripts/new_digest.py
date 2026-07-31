#!/usr/bin/env python3
"""Create a linked Auto Digest packet."""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", title.strip().lower())
    slug = slug.strip("-")
    return slug or "untitled"


def read_template(name: str) -> str:
    return (ROOT / "templates" / name).read_text(encoding="utf-8")


def write_from_template(path: Path, template_name: str, title: str) -> bool:
    if path.exists():
        return False
    content = read_template(template_name).replace("{{title}}", title)
    content = content.replace("Date added:", f"Date added: {date.today().isoformat()}")
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/new_digest.py \"Topic Title\"")
        return 2

    title = " ".join(sys.argv[1:]).strip()
    slug = slugify(title)

    files = [
        (ROOT / "sources" / f"{slug}.md", "source.md"),
        (ROOT / "digests" / f"{slug}.md", "digest.md"),
        (ROOT / "concepts" / f"{slug}.md", "concept.md"),
        (ROOT / "outputs" / slug / "00-output-plan.md", "output.md"),
        (ROOT / "outputs" / slug / "01-first-principles.md", "articles/01-first-principles.md"),
        (ROOT / "outputs" / slug / "02-customer-demand.md", "articles/02-customer-demand.md"),
        (ROOT / "outputs" / slug / "03-everyday-analogy.md", "articles/03-everyday-analogy.md"),
        (ROOT / "outputs" / slug / "04-history.md", "articles/04-history.md"),
        (ROOT / "outputs" / slug / "05-layered-system.md", "articles/05-layered-system.md"),
        (ROOT / "outputs" / slug / "06-cybernetics-feedback.md", "articles/06-cybernetics-feedback.md"),
        (ROOT / "outputs" / slug / "07-information-theory.md", "articles/07-information-theory.md"),
        (ROOT / "outputs" / slug / "08-demo.md", "articles/08-demo.md"),
    ]

    created = []
    skipped = []
    for path, template in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        if write_from_template(path, template, title):
            created.append(path.relative_to(ROOT))
        else:
            skipped.append(path.relative_to(ROOT))

    if created:
        print("Created:")
        for path in created:
            print(f"  {path}")
    if skipped:
        print("Skipped existing:")
        for path in skipped:
            print(f"  {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
