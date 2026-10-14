#!/usr/bin/env python3
"""Tests for commit-based chapter progress, provenance and archive exclusion."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chapter_publication_status", ROOT / "scripts" / "chapter_publication_status.py")
status = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(status)

validator_spec = importlib.util.spec_from_file_location("chapter_notes_validator", ROOT / "scripts" / "validate_chapter_notes.py")
validator = importlib.util.module_from_spec(validator_spec)
assert validator_spec.loader is not None
validator_spec.loader.exec_module(validator)


class PublicationStatusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.book = self.root / "books" / "test-book"
        (self.book / "rag").mkdir(parents=True)
        (self.book / "notes" / "chapters").mkdir(parents=True)
        (self.book / "rag" / "manifest.yaml").write_text(
            yaml.safe_dump({"source": {"sha256": "a" * 64}}), encoding="utf-8"
        )
        subprocess.run(["git", "-C", str(self.root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "test@example.com"], check=True)

    def commit(self):
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "test"], check=True)

    def add_chapter(self, number, complete=True):
        folder = self.book / "notes" / "chapters" / f"chapter-{number:02d}-example"
        folder.mkdir()
        filenames = status.REQUIRED if complete else ("README.md",)
        for filename in filenames:
            (folder / filename).write_text("test", encoding="utf-8")

    def add_plan(self, expected_sha="a" * 64):
        plan = {
            "schema": "biblioteka-vsp/chapter-plan/v1",
            "book_id": "test-book",
            "source_sha256": expected_sha,
            "toc_evidence": "RAG chunk p0002:c01, table of contents",
            "total_chapters": 2,
            "chapters": [
                {"number": 1, "title": "First", "slug": "example", "source_locator": "p0003"},
                {"number": 2, "title": "Second", "slug": "example", "source_locator": "p0030"},
            ],
        }
        (self.book / "notes" / "chapters" / "plan.yaml").write_text(
            yaml.safe_dump(plan, allow_unicode=True), encoding="utf-8"
        )

    def test_verified_plan_counts_only_complete_committed_chapters(self):
        self.add_plan()
        self.add_chapter(1)
        self.add_chapter(2, complete=False)
        self.commit()
        result = status.get_progress(self.root, "test-book")
        self.assertEqual(2, result["total_chapters"])
        self.assertEqual([1], result["published_chapter_numbers"])
        self.assertEqual([2], result["partial_chapter_numbers"])
        self.assertEqual(1, result["remaining_chapters"])
        self.assertEqual(2, result["next_unpublished_chapter"])
        self.assertEqual(50.0, result["progress_percent"])

    def test_uncommitted_files_are_not_published(self):
        self.add_plan()
        self.commit()
        self.add_chapter(1)
        result = status.get_progress(self.root, "test-book")
        self.assertEqual(0, result["git_published_chapters"])
        self.assertEqual(0.0, result["progress_percent"])

    def test_no_plan_means_unknown_total_not_inferred(self):
        self.add_chapter(1)
        self.commit()
        result = status.get_progress(self.root, "test-book")
        self.assertIsNone(result["total_chapters"])
        self.assertEqual(1, result["git_published_chapters"])
        self.assertIsNone(result["progress_percent"])
        self.assertIsNotNone(result["unknown_reason"])

    def test_stale_plan_is_not_accepted(self):
        self.add_plan(expected_sha="b" * 64)
        self.add_chapter(1)
        self.commit()
        result = status.get_progress(self.root, "test-book")
        self.assertIsNone(result["total_chapters"])
        self.assertIn("invalid", result["unknown_reason"])

    def test_archive_only_not_counted_as_chapter(self):
        self.add_plan()
        folder = self.book / "notes" / "chapters" / "chapter-01-example"
        folder.mkdir()
        (folder / "bundle.zip").write_bytes(b"zip placeholder")
        self.commit()
        result = status.get_progress(self.root, "test-book")
        self.assertEqual(0, result["git_published_chapters"])

    def test_new_chapter_archive_diff_is_forbidden(self):
        changed = [
            "books/demo/notes/chapters/chapter-01-test/chapter.ZIP",
            "books/demo/notes/chapter.tar.gz",
            "books/demo/source/book.pdf",
        ]
        self.assertEqual(
            sorted(changed[:2]), validator.forbidden_chapter_archives(changed)
        )


if __name__ == "__main__":
    unittest.main()
