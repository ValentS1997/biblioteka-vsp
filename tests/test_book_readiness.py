#!/usr/bin/env python3
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_book_readiness", REPO / "scripts" / "check_book_readiness.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "books").mkdir()
        (self.root / "templates").mkdir()
        module.ROOT = self.root
        module.INDEX = self.root / "books" / "index.yaml"
        module.CHAPTER_TEMPLATE = (
            self.root / "templates" / "chapter-artifact-collection-v1.4.yaml"
        )
        module.CHAPTER_TEMPLATE.write_text(
            yaml.safe_dump(
                {
                    "template": {
                        "id": "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION",
                        "version": "1.4",
                        "status": "ACCEPTED",
                    }
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def write_index(self, paths):
        module.INDEX.write_text(
            yaml.safe_dump(
                {"books": [{"id": "test-book", "paths": paths}]},
                sort_keys=False,
            ),
            encoding="utf-8",
        )

    def write_ready_book(self, metadata_sha=None):
        sha = "a" * 64
        metadata_sha = metadata_sha or sha
        book = self.root / "books" / "test-book"
        (book / "source").mkdir(parents=True)
        (book / "rag" / "chunks" / "p0001-p0100").mkdir(parents=True)
        (book / "rag" / "search-index").mkdir(parents=True)

        paths = {
            "metadata": "books/test-book/metadata.yaml",
            "source": "books/test-book/source/book.pdf",
            "rag_manifest": "books/test-book/rag/manifest.yaml",
            "rag_chunks": "books/test-book/rag/chunks/",
            "rag_chunk_index": "books/test-book/rag/chunk-index.jsonl",
            "rag_search_index": "books/test-book/rag/search-index/",
        }
        self.write_index(paths)

        (book / "metadata.yaml").write_text(
            yaml.safe_dump(
                {
                    "id": "test-book",
                    "title": "Test Book",
                    "source": {"expected_sha256": metadata_sha},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        (book / "source" / "book.pdf").write_text("git-lfs-pointer", encoding="utf-8")
        (book / "source" / "SHA256").write_text(f"{sha}  book.pdf\n", encoding="utf-8")
        (book / "rag" / "manifest.yaml").write_text(
            yaml.safe_dump(
                {
                    "book_id": "test-book",
                    "source": {"path": "source/book.pdf", "sha256": sha},
                    "validation": {"status": "READY_WITH_KNOWN_LIMITATIONS"},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )

        chunk_id = "test-book:p0001:c01"
        rel = "rag/chunks/p0001-p0100/p0001-c01.md"
        (book / rel).write_text(
            "---\n"
            "schema: biblioteka-vsp/chunk/v1\n"
            f"chunk_id: {chunk_id}\n"
            "book_id: test-book\n"
            "pdf_page: 1\n"
            "chunk_in_page: 1\n"
            "source_path: source/book.pdf\n"
            f"source_sha256: {sha}\n"
            "---\n\n"
            "пример проверочного содержимого retrieval\n",
            encoding="utf-8",
        )
        record = {
            "chunk_id": chunk_id,
            "book_id": "test-book",
            "pdf_page": 1,
            "chunk_in_page": 1,
            "path": rel,
            "source_path": "source/book.pdf",
            "source_sha256": sha,
        }
        (book / "rag" / "chunk-index.jsonl").write_text(
            json.dumps(record, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        shard = {
            "exact_terms": {
                "пример": {
                    "chunk_id": chunk_id,
                    "path": rel,
                    "pdf_page": 1,
                    "tf": 1,
                }
            },
            "keys": {},
        }
        (book / "rag" / "search-index" / "при.json").write_text(
            json.dumps(shard, ensure_ascii=False),
            encoding="utf-8",
        )
        (book / "rag" / "search-index" / "manifest.json").write_text(
            "{}\n", encoding="utf-8"
        )

    def test_full_ready_book(self):
        self.write_ready_book()
        result = module.compute_readiness("test-book")
        self.assertEqual("READY", result["status"])
        self.assertEqual([], result["failed_checks"])

    def test_reading_only_entry_is_blocked_not_error(self):
        book = self.root / "books" / "test-book" / "reading"
        book.mkdir(parents=True)
        (book / "progress.yaml").write_text(
            "book_id: test-book\nstatus: in_progress\n", encoding="utf-8"
        )
        self.write_index(
            {"reading_progress": "books/test-book/reading/progress.yaml"}
        )
        result = module.compute_readiness("test-book")
        self.assertEqual("BLOCKED", result["status"])
        reasons = {item.get("reason_code") for item in result["failed_checks"]}
        self.assertIn("CANONICAL_SOURCE_MISSING", reasons)
        self.assertIn("RAG_MANIFEST_MISSING", reasons)

    def test_provenance_mismatch_blocks(self):
        self.write_ready_book(metadata_sha="b" * 64)
        result = module.compute_readiness("test-book")
        self.assertEqual("BLOCKED", result["status"])
        failed_ids = {item["id"] for item in result["failed_checks"]}
        self.assertIn("source_provenance_consistent", failed_ids)


if __name__ == "__main__":
    unittest.main()
