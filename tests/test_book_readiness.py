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
        module.CHAPTER_TEMPLATE = self.root / "templates" / "chapter-artifact-collection-v1.8.yaml"
        module.CHAPTER_TEMPLATE.write_text(
            yaml.safe_dump(
                {
                    "template": {
                        "id": "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION",
                        "version": "1.8",
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
            yaml.safe_dump({"books": [{"id": "test-book", "paths": paths}]}, sort_keys=False),
            encoding="utf-8",
        )

    def write_ready_book(self, source_format="pdf", metadata_sha=None, legacy_pdf=False):
        sha = "a" * 64
        metadata_sha = metadata_sha or sha
        extension = "pdf" if source_format == "pdf" else "epub"
        source_name = f"book.{extension}"
        source_rel = f"source/{source_name}"
        book = self.root / "books" / "test-book"
        (book / "source").mkdir(parents=True)
        shard_dir = "p0001-p0100" if source_format == "pdf" else "e0001-e0100"
        (book / "rag" / "chunks" / shard_dir).mkdir(parents=True)
        (book / "rag" / "search-index").mkdir(parents=True)

        paths = {
            "metadata": "books/test-book/metadata.yaml",
            "source": f"books/test-book/{source_rel}",
            "rag_manifest": "books/test-book/rag/manifest.yaml",
            "rag_chunks": "books/test-book/rag/chunks/",
            "rag_chunk_index": "books/test-book/rag/chunk-index.jsonl",
            "rag_search_index": "books/test-book/rag/search-index/",
        }
        self.write_index(paths)
        (book / "metadata.yaml").write_text(
            yaml.safe_dump({"id": "test-book", "title": "Test Book", "source": {"expected_sha256": metadata_sha}}, sort_keys=False),
            encoding="utf-8",
        )
        (book / "source" / source_name).write_text("git-lfs-pointer", encoding="utf-8")
        (book / "source" / "SHA256").write_text(f"{sha}  {source_name}\n", encoding="utf-8")
        source_manifest = {"path": source_rel, "sha256": sha}
        if not legacy_pdf:
            source_manifest["format"] = source_format
        (book / "rag" / "manifest.yaml").write_text(
            yaml.safe_dump({"book_id": "test-book", "source": source_manifest, "validation": {"status": "READY_WITH_KNOWN_LIMITATIONS"}}, sort_keys=False),
            encoding="utf-8",
        )

        if source_format == "pdf":
            chunk_id = "test-book:p0001:c01"
            rel = "rag/chunks/p0001-p0100/p0001-c01.md"
            if legacy_pdf:
                front = (
                    "---\n"
                    "schema: biblioteka-vsp/chunk/v1\n"
                    f"chunk_id: {chunk_id}\n"
                    "book_id: test-book\n"
                    "pdf_page: 1\n"
                    "chunk_in_page: 1\n"
                    f"source_path: {source_rel}\n"
                    f"source_sha256: {sha}\n"
                    "---\n\n"
                )
                record = {"chunk_id": chunk_id, "book_id": "test-book", "pdf_page": 1, "chunk_in_page": 1, "path": rel, "source_path": source_rel, "source_sha256": sha}
                posting = {"chunk_id": chunk_id, "path": rel, "pdf_page": 1, "tf": 1}
            else:
                front = (
                    "---\n"
                    "schema: biblioteka-vsp/chunk/v2\n"
                    f"chunk_id: {chunk_id}\n"
                    "book_id: test-book\n"
                    "source_format: pdf\n"
                    "source_unit_type: pdf_page\n"
                    "source_unit: 1\n"
                    'source_locator: "1"\n'
                    "pdf_page: 1\n"
                    "chunk_in_page: 1\n"
                    "chunk_in_unit: 1\n"
                    f"source_path: {source_rel}\n"
                    f"source_sha256: {sha}\n"
                    "---\n\n"
                )
                record = {"chunk_id": chunk_id, "book_id": "test-book", "source_unit_type": "pdf_page", "source_unit": 1, "source_locator": "1", "pdf_page": 1, "path": rel, "source_path": source_rel, "source_sha256": sha}
                posting = {"chunk_id": chunk_id, "path": rel, "source_unit_type": "pdf_page", "source_unit": 1, "source_locator": "1", "pdf_page": 1, "tf": 1}
        else:
            chunk_id = "test-book:e0001:c01"
            rel = "rag/chunks/e0001-e0100/e0001-c01.md"
            front = (
                "---\n"
                "schema: biblioteka-vsp/chunk/v2\n"
                f"chunk_id: {chunk_id}\n"
                "book_id: test-book\n"
                "source_format: epub\n"
                "source_unit_type: epub_spine_item\n"
                "source_unit: 1\n"
                'source_locator: "OEBPS/Text/ch1.xhtml"\n'
                "chunk_in_unit: 1\n"
                f"source_path: {source_rel}\n"
                f"source_sha256: {sha}\n"
                "---\n\n"
            )
            record = {"chunk_id": chunk_id, "book_id": "test-book", "source_unit_type": "epub_spine_item", "source_unit": 1, "source_locator": "OEBPS/Text/ch1.xhtml", "path": rel, "source_path": source_rel, "source_sha256": sha}
            posting = {"chunk_id": chunk_id, "path": rel, "source_unit_type": "epub_spine_item", "source_unit": 1, "source_locator": "OEBPS/Text/ch1.xhtml", "tf": 1}

        (book / rel).write_text(front + "пример проверочного содержимого retrieval\n", encoding="utf-8")
        (book / "rag" / "chunk-index.jsonl").write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
        shard = {"exact_terms": {"пример": posting}, "keys": {}}
        (book / "rag" / "search-index" / "при.json").write_text(json.dumps(shard, ensure_ascii=False), encoding="utf-8")
        (book / "rag" / "search-index" / "manifest.json").write_text("{}\n", encoding="utf-8")

    def test_full_ready_pdf_book(self):
        self.write_ready_book("pdf")
        result = module.compute_readiness("test-book")
        self.assertEqual("READY", result["status"])
        self.assertEqual([], result["failed_checks"])

    def test_legacy_pdf_artifacts_remain_ready(self):
        self.write_ready_book("pdf", legacy_pdf=True)
        result = module.compute_readiness("test-book")
        self.assertEqual("READY", result["status"])

    def test_manifest_declared_four_char_shards_are_ready(self):
        self.write_ready_book("pdf")
        search_dir = self.root / "books" / "test-book" / "rag" / "search-index"
        legacy_shard = search_dir / "при.json"
        adaptive_shard = search_dir / "прим.json"
        adaptive_shard.write_text(legacy_shard.read_text(encoding="utf-8"), encoding="utf-8")
        legacy_shard.unlink()
        (search_dir / "manifest.json").write_text(
            json.dumps({"normalization": {"shard_prefix_chars": 4}}, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        result = module.compute_readiness("test-book")
        self.assertEqual("READY", result["status"])
        self.assertEqual([], result["failed_checks"])

    def test_full_ready_epub_book(self):
        self.write_ready_book("epub")
        result = module.compute_readiness("test-book")
        self.assertEqual("READY", result["status"])
        self.assertEqual([], result["failed_checks"])

    def test_reading_only_entry_is_blocked_not_error(self):
        book = self.root / "books" / "test-book" / "reading"
        book.mkdir(parents=True)
        (book / "progress.yaml").write_text("book_id: test-book\nstatus: in_progress\n", encoding="utf-8")
        self.write_index({"reading_progress": "books/test-book/reading/progress.yaml"})
        result = module.compute_readiness("test-book")
        self.assertEqual("BLOCKED", result["status"])
        reasons = {item.get("reason_code") for item in result["failed_checks"]}
        self.assertIn("CANONICAL_SOURCE_MISSING", reasons)
        self.assertIn("RAG_MANIFEST_MISSING", reasons)

    def test_provenance_mismatch_blocks(self):
        self.write_ready_book("epub", metadata_sha="b" * 64)
        result = module.compute_readiness("test-book")
        self.assertEqual("BLOCKED", result["status"])
        failed_ids = {item["id"] for item in result["failed_checks"]}
        self.assertIn("source_provenance_consistent", failed_ids)


    def test_new_generation_requires_bound_acceptance(self):
        self.write_ready_book("pdf")
        book = self.root / "books" / "test-book"
        manifest_path = book / "rag" / "manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["generation"] = {
            "corpus_generation_id": "c" * 64,
            "index_generation_id": "d" * 64,
        }
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

        blocked = module.compute_readiness("test-book")
        self.assertEqual("BLOCKED", blocked["status"])
        self.assertIn(
            "rag_ingestion_acceptance_passed",
            {item["id"] for item in blocked["failed_checks"]},
        )

        (book / "rag" / "acceptance.yaml").write_text(
            yaml.safe_dump(
                {
                    "schema": "biblioteka-vsp/rag-ingestion-acceptance/v1",
                    "book_id": "test-book",
                    "status": "ACCEPTED",
                    "source_sha256": "a" * 64,
                    "corpus_generation_id": "c" * 64,
                    "index_generation_id": "d" * 64,
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        ready = module.compute_readiness("test-book")
        self.assertEqual("READY", ready["status"])


if __name__ == "__main__":
    unittest.main()
