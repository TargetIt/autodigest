#!/usr/bin/env python3
"""Regression tests for scripts/new_digest.py.

The tests run the generator against a temporary project root so fixtures do not
modify the real digest, source, or concept directories.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "new_digest.py"


def load_new_digest_module():
    spec = importlib.util.spec_from_file_location("new_digest", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NewDigestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(REPO_ROOT / "templates", self.root / "templates")
        self.module = load_new_digest_module()
        self.module.ROOT = self.root

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_generator(self, *args: str) -> tuple[int, str]:
        old_argv = sys.argv[:]
        stdout = io.StringIO()
        try:
            sys.argv = ["new_digest.py", *args]
            with contextlib.redirect_stdout(stdout):
                code = self.module.main()
        finally:
            sys.argv = old_argv
        return code, stdout.getvalue()

    def assert_file_contains(self, path: Path, text: str) -> None:
        self.assertTrue(path.exists(), f"Missing file: {path}")
        self.assertIn(text, path.read_text(encoding="utf-8"))

    def test_english_title_generates_core_workflow_files(self) -> None:
        code, output = self.run_generator("Transformer Attention")

        self.assertEqual(code, 0)
        self.assertIn("已创建：", output)
        digest_dir = self.root / "digests" / "transformer-attention"
        expected_files = [
            self.root / "sources" / "transformer-attention.md",
            self.root / "concepts" / "transformer-attention.md",
            digest_dir / "00-源信息账本.md",
            digest_dir / "01-核心解释.md",
            digest_dir / "02-最小例子.md",
            digest_dir / "03-误解与反例.md",
            digest_dir / "04-追问修复.md",
            digest_dir / "05-可选视角扩展.md",
            digest_dir / "06-检视记录.md",
            digest_dir / "07-最终输出草稿.md",
        ]

        for path in expected_files:
            self.assertTrue(path.exists(), f"Expected generated file: {path}")

        self.assertFalse((digest_dir / "01-第一性原理.md").exists())
        self.assert_file_contains(digest_dir / "01-核心解释.md", "# 核心解释：Transformer Attention")
        self.assert_file_contains(digest_dir / "05-可选视角扩展.md", "十个视角是工具箱，不是必填项")

    def test_chinese_title_preserves_chinese_slug_and_template_content(self) -> None:
        code, output = self.run_generator("复杂系统 学习方法")

        self.assertEqual(code, 0)
        self.assertIn("digests/复杂系统-学习方法/00-源信息账本.md", output)
        source_file = self.root / "sources" / "复杂系统-学习方法.md"
        digest_dir = self.root / "digests" / "复杂系统-学习方法"

        self.assert_file_contains(source_file, "# 源材料：复杂系统 学习方法")
        self.assert_file_contains(source_file, f"添加日期：{date.today().isoformat()}")
        self.assert_file_contains(digest_dir / "00-源信息账本.md", "# 源信息账本：复杂系统 学习方法")
        self.assert_file_contains(digest_dir / "03-误解与反例.md", "## 最容易出现的误解")

    def test_duplicate_run_skips_existing_files_without_overwriting(self) -> None:
        first_code, _ = self.run_generator("Duplicate Guard")
        target = self.root / "digests" / "duplicate-guard" / "01-核心解释.md"
        target.write_text("sentinel content\n", encoding="utf-8")

        second_code, second_output = self.run_generator("Duplicate Guard")

        self.assertEqual(first_code, 0)
        self.assertEqual(second_code, 0)
        self.assertIn("已跳过已存在文件：", second_output)
        self.assertEqual(target.read_text(encoding="utf-8"), "sentinel content\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
