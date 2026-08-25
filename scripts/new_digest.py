#!/usr/bin/env python3
"""创建一组关联的 Auto Digest 中文消化文件。"""

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
    content = content.replace("添加日期：", f"添加日期：{date.today().isoformat()}")
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("用法：python3 scripts/new_digest.py \"主题名称\"")
        return 2

    title = " ".join(sys.argv[1:]).strip()
    slug = slugify(title)
    digest_dir = ROOT / "digests" / slug

    files = [
        (ROOT / "sources" / f"{slug}.md", "source.md"),
        (ROOT / "concepts" / f"{slug}.md", "concept.md"),
        (digest_dir / "00-源信息账本.md", "source-ledger.md"),
        (digest_dir / "01-核心解释.md", "digest.md"),
        (digest_dir / "02-最小例子.md", "minimal-example.md"),
        (digest_dir / "03-误解与反例.md", "misconceptions.md"),
        (digest_dir / "04-追问修复.md", "questions.md"),
        (digest_dir / "05-可选视角扩展.md", "view-selection.md"),
        (digest_dir / "06-检视记录.md", "review.md"),
        (digest_dir / "07-最终输出草稿.md", "output.md"),
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
        print("已创建：")
        for path in created:
            print(f"  {path}")
    if skipped:
        print("已跳过已存在文件：")
        for path in skipped:
            print(f"  {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
