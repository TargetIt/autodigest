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

    files = [
        (ROOT / "sources" / f"{slug}.md", "source.md"),
        (ROOT / "digests" / f"{slug}.md", "digest.md"),
        (ROOT / "concepts" / f"{slug}.md", "concept.md"),
        (ROOT / "outputs" / slug / "00-输出计划.md", "output.md"),
        (ROOT / "outputs" / slug / "01-第一性原理.md", "articles/01-first-principles.md"),
        (ROOT / "outputs" / slug / "02-客户需求.md", "articles/02-customer-demand.md"),
        (ROOT / "outputs" / slug / "03-生活化类比.md", "articles/03-everyday-analogy.md"),
        (ROOT / "outputs" / slug / "04-历史发展.md", "articles/04-history.md"),
        (ROOT / "outputs" / slug / "05-层次化系统.md", "articles/05-layered-system.md"),
        (ROOT / "outputs" / slug / "06-控制论与反馈.md", "articles/06-cybernetics-feedback.md"),
        (ROOT / "outputs" / slug / "07-信息论.md", "articles/07-information-theory.md"),
        (ROOT / "outputs" / slug / "08-最小Demo.md", "articles/08-demo.md"),
        (ROOT / "outputs" / slug / "09-数据结构.md", "articles/09-data-structures.md"),
        (ROOT / "outputs" / slug / "10-费曼式消化.md", "articles/10-feynman.md"),
        (ROOT / "outputs" / slug / "11-检视记录.md", "review.md"),
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
