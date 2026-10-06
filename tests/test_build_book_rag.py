#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
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
    def make_pdf_book(self, with_expected_sha: bool) -> Path:
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
            (source_dir / "SHA256").write_text(f"{sha}  book.pdf\n", encoding="utf-8")
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        return book

    def make_epub_book(self) -> Path:
        root = Path(tempfile.mkdtemp())
        book = root / "epub-book"
        source_dir = book / "source"
        source_dir.mkdir(parents=True)
        epub_path = source_dir / "book.epub"
        with zipfile.ZipFile(epub_path, "w") as zf:
            zf.writestr("mimetype", "application/epub+zip")
            zf.writestr(
                "META-INF/container.xml",
                '<?xml version="1.0"?>'
                '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                '<rootfiles><rootfile full-path="OEBPS/content.opf" '
                'media-type="application/oebps-package+xml"/></rootfiles></container>',
            )
            zf.writestr(
                "OEBPS/content.opf",
                '<?xml version="1.0" encoding="utf-8"?>'
                '<package xmlns="http://www.idpf.org/2007/opf">'
                '<manifest><item id="ch1" href="Text/ch1.xhtml" '
                'media-type="application/xhtml+xml"/></manifest>'
                '<spine><itemref idref="ch1"/></spine></package>',
            )
            zf.writestr(
                "OEBPS/Text/ch1.xhtml",
                '<?xml version="1.0" encoding="utf-8"?>'
                '<html xmlns="http://www.w3.org/1999/xhtml"><body>'
                '<h1>Глава 1</h1><p>Проверка EPUB retrieval и provenance.</p>'
                '</body></html>',
            )
        sha = sha256_file(epub_path)
        (source_dir / "SHA256").write_text(f"{sha}  book.epub\n", encoding="utf-8")
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        return book

    def test_pdf_expected_checksum_is_verified(self):
        book = self.make_pdf_book(with_expected_sha=True)
        result = module.build(book)
        manifest = yaml.safe_load((book / "rag" / "manifest.yaml").read_text(encoding="utf-8"))

        self.assertEqual("pdf", result["source_format"])
        self.assertTrue(result["source_checksum_expected_present"])
        self.assertTrue(result["source_checksum_matched_expected"])
        self.assertTrue(manifest["validation"]["source_checksum_verified"])
        self.assertEqual("pdf", manifest["source"]["format"])
        self.assertEqual("pdf_page", manifest["chunking"]["source_unit_type"])
        self.assertEqual("1.0", manifest["ingestion"]["pipeline_version"])
        self.assertEqual(
            module.CHUNKING_POLICY_ID,
            manifest["ingestion"]["chunking_policy_id"],
        )
        self.assertRegex(manifest["generation"]["corpus_generation_id"], r"^[0-9a-f]{64}$")
        self.assertRegex(manifest["generation"]["index_generation_id"], r"^[0-9a-f]{64}$")

        index_record = json.loads(
            (book / "rag" / "chunk-index.jsonl").read_text(encoding="utf-8").splitlines()[0]
        )
        self.assertRegex(index_record["chunk_uid"], r"^[0-9a-f]{64}$")
        self.assertRegex(index_record["text_sha256"], r"^[0-9a-f]{64}$")
        chunk_text = (book / index_record["path"]).read_text(encoding="utf-8")
        self.assertIn(f"chunk_uid: {index_record['chunk_uid']}", chunk_text)
        self.assertIn(f"text_sha256: {index_record['text_sha256']}", chunk_text)

    def test_missing_expected_checksum_is_not_reported_verified(self):
        book = self.make_pdf_book(with_expected_sha=False)
        result = module.build(book)
        manifest = yaml.safe_load((book / "rag" / "manifest.yaml").read_text(encoding="utf-8"))

        self.assertFalse(result["source_checksum_expected_present"])
        self.assertFalse(result["source_checksum_matched_expected"])
        self.assertFalse(manifest["validation"]["source_checksum_verified"])

    def test_epub_build_uses_spine_provenance(self):
        book = self.make_epub_book()
        result = module.build(book)
        manifest = yaml.safe_load((book / "rag" / "manifest.yaml").read_text(encoding="utf-8"))
        index_line = (book / "rag" / "chunk-index.jsonl").read_text(encoding="utf-8").splitlines()[0]
        index_record = __import__("json").loads(index_line)
        chunk_path = book / index_record["path"]
        chunk_text = chunk_path.read_text(encoding="utf-8")

        self.assertEqual("epub", result["source_format"])
        self.assertEqual(1, result["source_units"])
        self.assertEqual("source/book.epub", manifest["source"]["path"])
        self.assertEqual("epub", manifest["source"]["format"])
        self.assertEqual("epub_spine_item", manifest["chunking"]["source_unit_type"])
        self.assertEqual("epub_spine_item", index_record["source_unit_type"])
        self.assertEqual("OEBPS/Text/ch1.xhtml", index_record["source_locator"])
        self.assertIn("Проверка EPUB retrieval", chunk_text)

    def test_ambiguous_supported_sources_fail(self):
        book = self.make_pdf_book(with_expected_sha=True)
        (book / "source" / "book.epub").write_bytes(b"placeholder")
        with self.assertRaisesRegex(RuntimeError, "Ambiguous canonical source"):
            module.build(book)


    def test_rebuild_preserves_generation_and_chunk_uid(self):
        book = self.make_pdf_book(with_expected_sha=True)
        first = module.build(book)
        first_records = [
            json.loads(line)
            for line in (book / "rag" / "chunk-index.jsonl").read_text(encoding="utf-8").splitlines()
        ]

        second = module.build(book)
        second_records = [
            json.loads(line)
            for line in (book / "rag" / "chunk-index.jsonl").read_text(encoding="utf-8").splitlines()
        ]

        self.assertEqual(first["corpus_generation_id"], second["corpus_generation_id"])
        self.assertEqual(first["index_generation_id"], second["index_generation_id"])
        self.assertEqual(
            [record["chunk_uid"] for record in first_records],
            [record["chunk_uid"] for record in second_records],
        )


if __name__ == "__main__":
    unittest.main()
