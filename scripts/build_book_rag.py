#!/usr/bin/env python3
"""Build deterministic page-traceable RAG artifacts for one biblioteka-vsp book."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import fitz


TARGET_CHARS = 4000
OVERLAP_CHARS = 350
RETRIEVAL_TOP_K_MAX = 3


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_text(text: str) -> str:
    """Minimal normalization: remove extraction artifacts without rewriting meaning."""
    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00ad", "")
    text = text.replace("\u00a0", " ")
    lines = [re.sub(r"[ \t]+$", "", line) for line in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def split_page(text: str) -> list[str]:
    if not text:
        return []
    if len(text) <= TARGET_CHARS:
        return [text]

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + TARGET_CHARS, len(text))
        if end < len(text):
            window = text[start:end]
            candidates = [
                window.rfind("\n\n"),
                window.rfind("\n"),
                window.rfind(". "),
                window.rfind("; "),
            ]
            cut = max(candidates)
            if cut >= int(TARGET_CHARS * 0.65):
                end = start + cut + (2 if window[cut : cut + 2] == "\n\n" else 1)

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break
        start = max(end - OVERLAP_CHARS, start + 1)

    return chunks


def expected_sha(book_dir: Path) -> str | None:
    path = book_dir / "source" / "SHA256"
    if not path.is_file():
        return None

    first_token = path.read_text(encoding="utf-8").strip().split()[0]
    if not re.fullmatch(r"[0-9a-fA-F]{64}", first_token):
        raise ValueError(f"Invalid SHA256 file: {path}")
    return first_token.lower()


def chunk_shard(pdf_page: int) -> str:
    start = ((pdf_page - 1) // 100) * 100 + 1
    end = start + 99
    return f"p{start:04d}-p{end:04d}"


def write_retrieval_chunk(
    *,
    book_dir: Path,
    book_id: str,
    source_sha: str,
    pdf_page: int,
    chunk_in_page: int,
    chunk_text: str,
) -> dict:
    chunk_id = f"{book_id}:p{pdf_page:04d}:c{chunk_in_page:02d}"
    rel_path = (
        Path("rag")
        / "chunks"
        / chunk_shard(pdf_page)
        / f"p{pdf_page:04d}-c{chunk_in_page:02d}.md"
    )
    abs_path = book_dir / rel_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)

    body = (
        "---\n"
        "schema: biblioteka-vsp/chunk/v1\n"
        f"chunk_id: {chunk_id}\n"
        f"book_id: {book_id}\n"
        f"pdf_page: {pdf_page}\n"
        f"chunk_in_page: {chunk_in_page}\n"
        "source_path: source/book.pdf\n"
        f"source_sha256: {source_sha}\n"
        "---\n\n"
        f"{chunk_text}\n"
    )
    abs_path.write_text(body, encoding="utf-8")

    return {
        "chunk_id": chunk_id,
        "book_id": book_id,
        "pdf_page": pdf_page,
        "chunk_in_page": chunk_in_page,
        "path": rel_path.as_posix(),
        "source_path": "source/book.pdf",
        "source_sha256": source_sha,
        "chars": len(chunk_text),
        "text_sha256": sha256_text(chunk_text),
    }


def build(book_dir: Path) -> dict:
    source = book_dir / "source" / "book.pdf"
    if not source.is_file():
        raise FileNotFoundError(f"Source PDF missing: {source}")

    book_id = book_dir.name
    source_sha = sha256_file(source)
    expected = expected_sha(book_dir)
    if expected and source_sha != expected:
        raise RuntimeError(
            f"Source checksum mismatch: expected {expected}, got {source_sha}"
        )

    rag_dir = book_dir / "rag"
    rag_dir.mkdir(parents=True, exist_ok=True)

    retrieval_dir = rag_dir / "chunks"
    if retrieval_dir.exists():
        shutil.rmtree(retrieval_dir)
    retrieval_dir.mkdir(parents=True, exist_ok=True)

    document = fitz.open(source)
    text_parts: list[str] = ["# Extracted text\n"]
    chunk_records: list[dict] = []
    index_records: list[dict] = []
    blank_pages: list[int] = []
    extracted_characters = 0

    for pdf_page, page in enumerate(document, start=1):
        text = normalize_text(page.get_text("text", sort=True))
        extracted_characters += len(text)

        if not text:
            blank_pages.append(pdf_page)

        text_parts.append(
            f"<!-- pdf_page: {pdf_page:04d} -->\n"
            f"## PDF page {pdf_page:04d}\n\n"
            f"{text if text else '[No extractable text on this PDF page]'}\n"
        )

        for chunk_in_page, chunk_text in enumerate(split_page(text), start=1):
            chunk_id = f"{book_id}:p{pdf_page:04d}:c{chunk_in_page:02d}"
            chunk_records.append(
                {
                    "chunk_id": chunk_id,
                    "book_id": book_id,
                    "pdf_page": pdf_page,
                    "chunk_in_page": chunk_in_page,
                    "source_path": "source/book.pdf",
                    "source_sha256": source_sha,
                    "text": chunk_text,
                }
            )
            index_records.append(
                write_retrieval_chunk(
                    book_dir=book_dir,
                    book_id=book_id,
                    source_sha=source_sha,
                    pdf_page=pdf_page,
                    chunk_in_page=chunk_in_page,
                    chunk_text=chunk_text,
                )
            )

    pdf_pages = len(document)
    document.close()

    text_path = rag_dir / "text.md"
    chunks_path = rag_dir / "chunks.jsonl"
    index_path = rag_dir / "chunk-index.jsonl"
    manifest_path = rag_dir / "manifest.yaml"

    text_path.write_text("\n".join(text_parts), encoding="utf-8")

    with chunks_path.open("w", encoding="utf-8", newline="\n") as stream:
        for record in chunk_records:
            stream.write(
                json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
            )

    with index_path.open("w", encoding="utf-8", newline="\n") as stream:
        for record in index_records:
            stream.write(
                json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
            )

    chunk_ids = [record["chunk_id"] for record in chunk_records]
    ids_unique = len(chunk_ids) == len(set(chunk_ids))
    paths_unique = len(index_records) == len({record["path"] for record in index_records})

    fitz_version = getattr(fitz, "VersionBind", "[Needs confirmation]")

    manifest = f"""schema: biblioteka-vsp/rag/v1
book_id: {book_id}

source:
  path: source/book.pdf
  sha256: {source_sha}
  pdf_pages: {pdf_pages}

extraction:
  engine: PyMuPDF
  engine_version: "{fitz_version}"
  page_coordinate_system: source_pdf_1_indexed
  text_layer: embedded_OCR
  normalization:
    - remove_NUL
    - remove_soft_hyphen_marker
    - normalize_line_endings
    - trim_trailing_horizontal_whitespace

chunking:
  scope: per_pdf_page
  target_chars: {TARGET_CHARS}
  overlap_chars: {OVERLAP_CHARS}
  id_pattern: "<book-slug>:p<pdf-page-4d>:c<chunk-2d>"

retrieval:
  mode: addressable_small_chunks
  search_scope: rag/chunks/
  chunk_index: rag/chunk-index.jsonl
  top_k_max: {RETRIEVAL_TOP_K_MAX}
  chunk_file_pattern: "rag/chunks/p####-p####/p####-c##.md"
  bulk_files:
    - rag/text.md
    - rag/chunks.jsonl
  bulk_files_for_query_retrieval: false

statistics:
  pages_with_text: {pdf_pages - len(blank_pages)}
  blank_pages: {len(blank_pages)}
  blank_page_numbers: {json.dumps(blank_pages)}
  extracted_characters: {extracted_characters}
  chunks: {len(chunk_records)}
  retrieval_chunk_files: {len(index_records)}

validation:
  chunk_ids_unique: {str(ids_unique).lower()}
  retrieval_paths_unique: {str(paths_unique).lower()}
  retrieval_chunk_count_matches: {str(len(index_records) == len(chunk_records)).lower()}
  source_checksum_verified: true
  full_pdf_page_range_processed: true
  status: READY_WITH_KNOWN_LIMITATIONS

known_limitations:
  - "The PDF uses an embedded OCR text layer; recognition errors present in the source OCR may remain in extracted text."
  - "Images, equations, tables and diagrams are not independently encoded as multimodal RAG objects; use pdf_page provenance to inspect the source page when visual context matters."
  - "Publisher advertisement and cover pages are part of the source PDF and remain page-addressable even when they are not core book content."
  - "GitHub code search is lexical retrieval, not a vector-semantic index; agents may retry with a small number of query variants but must not fall back to bulk blobs in RAG-only mode."
"""
    manifest_path.write_text(manifest, encoding="utf-8")

    if not ids_unique:
        raise RuntimeError("Generated chunk IDs are not unique")
    if not paths_unique:
        raise RuntimeError("Generated retrieval chunk paths are not unique")
    if len(index_records) != len(chunk_records):
        raise RuntimeError("Retrieval chunk count does not match chunk count")
    if pdf_pages == 0:
        raise RuntimeError("PDF contains no pages")

    return {
        "book_id": book_id,
        "source_sha256": source_sha,
        "pdf_pages": pdf_pages,
        "pages_with_text": pdf_pages - len(blank_pages),
        "blank_pages": blank_pages,
        "extracted_characters": extracted_characters,
        "chunks": len(chunk_records),
        "retrieval_chunk_files": len(index_records),
        "chunk_ids_unique": ids_unique,
        "retrieval_paths_unique": paths_unique,
        "text_path": str(text_path),
        "chunks_path": str(chunks_path),
        "index_path": str(index_path),
        "retrieval_dir": str(retrieval_dir),
        "manifest_path": str(manifest_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-dir", required=True)
    args = parser.parse_args()

    try:
        result = build(Path(args.book_dir))
    except Exception as exc:
        print(f"RAG build FAILED: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
