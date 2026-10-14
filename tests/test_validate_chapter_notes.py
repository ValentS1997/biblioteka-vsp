#!/usr/bin/env python3
"""Discovery and aggregation regressions for chapter-note CI."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "chapter_notes_validator", REPO / "scripts" / "validate_chapter_notes.py"
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class ChapterNotesDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "books").mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def add_chapter(self, book, name="chapter-01-test"):
        chapter = self.root / "books" / book / "notes" / "chapters" / name
        chapter.mkdir(parents=True)
        return chapter

    def test_discovers_only_books_with_chapter_directories(self):
        self.add_chapter("zeta")
        self.add_chapter("alpha")
        (self.root / "books" / "empty" / "notes" / "chapters").mkdir(parents=True)
        (self.root / "books" / "unrelated").mkdir()
        self.assertEqual(
            ["alpha", "zeta"],
            [p.name for p in validator.discover_books_with_chapters(self.root)],
        )

    def test_discovery_excludes_matching_regular_files(self):
        d = self.root / "books" / "fake" / "notes" / "chapters"
        d.mkdir(parents=True)
        (d / "chapter-not-a-directory").write_text("x", encoding="utf-8")
        self.assertEqual([], validator.discover_books_with_chapters(self.root))


    def test_selects_only_touched_chapter_books(self):
        self.add_chapter("alpha")
        zeta = self.add_chapter("zeta").parents[2]
        selected = validator.select_changed_books(
            self.root,
            [
                "books/zeta/notes/chapters/chapter-01-test/README.md",
                "books/zeta/notes/README.md",
                "books/alpha/reading/progress.yaml",
                "docs/BOOK-LIFECYCLE.md",
            ],
            Path("books/alpha"),
        )
        self.assertEqual([zeta], selected)

    def test_selects_all_touched_books_deterministically(self):
        alpha = self.add_chapter("alpha").parents[2]
        zeta = self.add_chapter("zeta").parents[2]
        paths = ["books/zeta/notes/README.md", "books/alpha/notes/chapters/README.md"]
        self.assertEqual(
            [alpha, zeta],
            validator.select_changed_books(self.root, paths, Path("books/unused")),
        )

    def test_keeps_single_book_fallback_when_no_chapters_touched(self):
        self.add_chapter("zeta")
        fallback = self.root / "books" / "zeta"
        self.assertEqual(
            [fallback],
            validator.select_changed_books(
                self.root, ["scripts/validate_chapter_notes.py"], Path("books/zeta")
            ),
        )

    def test_all_books_fails_without_chapters(self):
        self.assertEqual(1, validator.validate_all_books(self.root))

    def test_all_books_aggregates_failures_without_short_circuiting(self):
        a = self.add_chapter("alpha").parents[2]
        z = self.add_chapter("zeta").parents[2]
        with patch.object(validator, "validate", side_effect=[1, 0]) as check:
            self.assertEqual(1, validator.validate_all_books(self.root))
            self.assertEqual([call(a), call(z)], check.call_args_list)

    def test_all_books_passes_when_every_book_passes(self):
        self.add_chapter("alpha")
        self.add_chapter("beta")
        with patch.object(validator, "validate", return_value=0) as check:
            self.assertEqual(0, validator.validate_all_books(self.root))
            self.assertEqual(2, check.call_count)



class Prometheus0040IndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.book = Path(self.tmp.name) / "prometheus-up-and-running-pivotto-brazil-ru-2023"
        self.chapters = self.book / "notes" / "chapters"
        self.chapters.mkdir(parents=True)
        self.chapter = self.chapters / "chapter-01-test"
        self.chapter.mkdir()
        (self.chapter / "source-findings.md").write_text("findings", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def write_index(self, content):
        (self.chapters / "README.md").write_text(content, encoding="utf-8")

    def check(self):
        issues = []
        validator.check_prometheus_chapter_index(self.book, [self.chapter], issues)
        return issues

    def test_valid_index_and_findings(self):
        self.write_index("[01](chapter-01-test/README.md)")
        self.assertEqual([], self.check())

    def test_missing_index_entry_fails(self):
        self.write_index("# No links")
        self.assertTrue(any("chapter index mismatch" in issue for issue in self.check()))

    def test_duplicate_index_entry_fails(self):
        self.write_index("[01](chapter-01-test/README.md) [01](chapter-01-test/README.md)")
        self.assertTrue(any("duplicate chapter index entry" in issue for issue in self.check()))

    def test_missing_findings_fails(self):
        self.write_index("[01](chapter-01-test/README.md)")
        (self.chapter / "source-findings.md").unlink()
        self.assertTrue(any("source-findings.md" in issue for issue in self.check()))

    def test_no_index_fails(self):
        self.assertTrue(any("index missing" in issue for issue in self.check()))



if __name__ == "__main__":
    unittest.main()
