#!/usr/bin/env python3
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

import fitz

REPO = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


builder = load_module("build_book_rag_for_acceptance", REPO / "scripts" / "build_book_rag.py")
validator = load_module("validate_rag_ingestion", REPO / "scripts" / "validate_rag_ingestion.py")


class RagIngestionAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.book = self.root / "acceptance-book"
        source_dir = self.book / "source"
        source_dir.mkdir(parents=True)

        pdf_path = source_dir / "book.pdf"
        doc = fitz.open()
        for page_text in (
            "alpha deterministic provenance first sample",
            "middle deterministic provenance second sample",
            "omega deterministic provenance final sample",
        ):
            page = doc.new_page()
            page.insert_text((72, 72), page_text)
        doc.save(pdf_path)
        doc.close()

        digest = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
        (source_dir / "SHA256").write_text(f"{digest}  book.pdf\n", encoding="utf-8")
        builder.build(self.book)

    def test_generated_book_is_accepted(self):
        result = validator.validate_book(self.book)
        self.assertEqual("ACCEPTED", result["status"])
        self.assertEqual([], result["failed_checks"])

    def test_tampered_chunk_is_rejected(self):
        first = (self.book / "rag" / "chunk-index.jsonl").read_text(encoding="utf-8").splitlines()[0]
        import json
        record = json.loads(first)
        chunk_path = self.book / record["path"]
        chunk_path.write_text(chunk_path.read_text(encoding="utf-8") + "tamper\n", encoding="utf-8")

        result = validator.validate_book(self.book)
        self.assertEqual("REJECTED", result["status"])
        self.assertIn("all_chunk_provenance_and_hashes_resolve", result["failed_checks"])


if __name__ == "__main__":
    unittest.main()
