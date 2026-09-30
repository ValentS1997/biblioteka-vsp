#!/usr/bin/env python3
import hashlib
import importlib.util
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
        book = root / "test-epub"
        source_dir = book / "source"
        source_dir.mkdir(parents=True)
        epub_path = source_dir / "book.epub"

        container_xml = """<?xml version="1.0"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>"""
        opf = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
  <manifest>
    <item id="c1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    <item id="c2" href="chapter2.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine><itemref idref="c1"/><itemref idref="c2"/></spine>
</package>"""
        ch1 = """<html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Chapter one</h1><p>Deterministic EPUB retrieval text.</p></body></html>"""
        ch2 = """<html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Chapter two</h1><p>Second spine item text.</p></body></html>"""

        with zipfile.ZipFile(epub_path, "w") as zf:
            zf.writestr("mimetype", "application/epub+zip")
            zf.writestr("META-INF/container.xml", container_xml)
            zf.writestr("OEBPS/content.opf", opf)
            zf.writestr("OEBPS/chapter1.xhtml", ch1)
            zf.writestr("OEBPS/chapter2.xhtml", ch2)

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
        self.assertEqual("source/book.pdf", manifest["source"]["path"])
        self.assertEqual("unclassified_extractable_pdf_text", manifest["extraction"]["text_layer"])

    def test_pdf_missing_expected_checksum_is_not_reported_verified(self):
        book = self.make_pdf_book(with_expected_sha=False)
        result = module.build(book)
        manifest = yaml.safe_load((book / "rag" / "manifest.yaml").read_text(encoding="utf-8"))

        self.assertFalse(result["source_checksum_expected_present"])
        self.assertFalse(result["source_checksum_matched_expected"])
        self.assertFalse(manifest["validation"]["source_checksum_verified"])

    def test_epub_spine_is_extracted_with_source_provenance(self):
        book = self.make_epub_book()
        result = module.build(book)
        manifest = yaml.safe_load((book / "rag" / "manifest.yaml").read_text(encoding="utf-8"))
        index_lines = (book / "rag" / "chunk-index.jsonl").read_text(encoding="utf-8").splitlines()

        self.assertEqual("epub", result["source_format"])
        self.assertEqual(2, result["source_units"])
        self.assertEqual("source/book.epub", manifest["source"]["path"])
        self.assertEqual("epub", manifest["source"]["format"])
        self.assertEqual("per_epub_spine_item", manifest["chunking"]["scope"])
        self.assertTrue(any('"kind":"epub_spine_item"' in line for line in index_lines))
        self.assertTrue(any(":s0001:c01" in line for line in index_lines))
        self.assertIn("Deterministic EPUB retrieval text", (book / "rag" / "text.md").read_text(encoding="utf-8"))

    def test_ambiguous_dual_source_is_rejected(self):
        book = self.make_epub_book()
        (book / "source" / "book.pdf").write_bytes(b"%PDF-1.4\n")
        with self.assertRaisesRegex(RuntimeError, "ambiguous"):
            module.build(book)


if __name__ == "__main__":
    unittest.main()
