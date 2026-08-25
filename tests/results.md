# AutoDigest Test Results

Date: 2026-08-25

## Scope

Three regression test groups were added for `scripts/new_digest.py`.

1. English title generation: verifies the new core workflow files are generated and the old default ten-article files are not generated.
2. Chinese title generation: verifies Chinese slugs, title substitution, and date substitution in generated templates.
3. Duplicate run behavior: verifies existing files are skipped and not overwritten.

## Command

```bash
python3 tests/test_new_digest.py
```

## Result

Passed.

```text
test_chinese_title_preserves_chinese_slug_and_template_content (__main__.NewDigestTests) ... ok
test_duplicate_run_skips_existing_files_without_overwriting (__main__.NewDigestTests) ... ok
test_english_title_generates_core_workflow_files (__main__.NewDigestTests) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.022s

OK
```

## Notes

- Tests run in a temporary project root and copy only `templates/`, so they do not modify real digest content.
- The English-title test verifies the new default workflow files and confirms the old default ten-article file `01-第一性原理.md` is not generated.
- The Chinese-title test verifies Chinese slug preservation and `添加日期：YYYY-MM-DD` substitution.
- The duplicate-run test verifies existing files are skipped without overwriting local edits.
