#!/usr/bin/env python3
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

import fitz
import yaml

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "build_book_rag", REPO / "scripts" / "build_book_rag.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


class BuildBookRagTests(unittest.TestCase):
    def make_book(self, with_expected_sha: bool) -> Path:
        root = Path(tempfile.mkdtemp())
        book = root / "test-book"
        source_dir = book / "source"
        source_dir.mkdir(parents=True)

        pdf_path = source_dir / "book.pdf"
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Deterministic retrieval test page")
        doc.save(pdf_path)
        doc.close()

        if with_expected_sha:
            sha = sha256_file(pdf_path)
            (source_dir / "SHA256").write_text(
                f"{sha}  book.pdf\n", encoding="utf-8"
            )
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        return book

    def test_expected_checksum_is_verified(self):
        book = self.make_book(with_expected_sha=True)
        result = module.build(book)
        manifest = yaml.safe_load((book / "rag" / "manifest.yaml").read_text(encoding="utf-8"))

        self.assertTrue(result["source_checksum_expected_present"])
        self.assertTrue(result["source_checksum_matched_expected"])
        self.assertTrue(manifest["validation"]["source_checksum_expected_present"])
        self.assertTrue(manifest["validation"]["source_checksum_matched_expected"])
        self.assertTrue(manifest["validation"]["source_checksum_verified"])
        self.assertEqual(
            "unclassified_extractable_pdf_text",
            manifest["extraction"]["text_layer"],
        )

    def test_missing_expected_checksum_is_not_reported_verified(self):
        book = self.make_book(with_expected_sha=False)
        result = module.build(book)
        manifest = yaml.safe_load((book / "rag" / "manifest.yaml").read_text(encoding="utf-8"))

        self.assertFalse(result["source_checksum_expected_present"])
        self.assertFalse(result["source_checksum_matched_expected"])
        self.assertFalse(manifest["validation"]["source_checksum_expected_present"])
        self.assertFalse(manifest["validation"]["source_checksum_matched_expected"])
        self.assertFalse(manifest["validation"]["source_checksum_verified"])


if __name__ == "__main__":
    unittest.main()
