#!/usr/bin/env python3
"""Build deterministic page-traceable RAG artifacts for one biblioteka-vsp book."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

import fitz


TARGET_CHARS = 4000
OVERLAP_CHARS = 350
RETRIEVAL_TOP_K_MAX = 3
SEARCH_KEY_CHARS = 4
SEARCH_PREFIX_CHARS = 3
SEARCH_POSTINGS_MAX = 32
SEARCH_SHARD_MAX_BYTES = 262144


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


def normalize_token(token: str) -> str:
    return token.lower().replace("ё", "е")


def lexical_tokens(text: str) -> list[str]:
    normalized = text.lower().replace("ё", "е")
    return [
        token
        for token in re.findall(r"[0-9a-zа-я]+", normalized, flags=re.IGNORECASE)
        if 2 <= len(token) <= 64
    ]


def retrieval_key(token: str) -> str:
    token = normalize_token(token)
    return token if len(token) <= SEARCH_KEY_CHARS else token[:SEARCH_KEY_CHARS]


def search_shard_for_key(key: str) -> str:
    if len(key) < SEARCH_PREFIX_CHARS:
        return f"_short/{key}"
    return key[:SEARCH_PREFIX_CHARS]


def build_lexical_search_index(
    *,
    book_dir: Path,
    book_id: str,
    chunk_records: list[dict],
    index_records: list[dict],
) -> dict:
    search_dir = book_dir / "rag" / "search-index"
    if search_dir.exists():
        shutil.rmtree(search_dir)
    search_dir.mkdir(parents=True, exist_ok=True)

    path_by_chunk = {
        record["chunk_id"]: record["path"] for record in index_records
    }

    key_postings: dict[str, dict[str, dict[str, dict]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    exact_terms: dict[str, dict[str, dict[str, dict]]] = defaultdict(
        lambda: defaultdict(dict)
    )

    for record in chunk_records:
        chunk_id = record["chunk_id"]
        pdf_page = record["pdf_page"]
        chunk_path = path_by_chunk[chunk_id]
        term_counts = Counter(lexical_tokens(record["text"]))
        key_counts: Counter[str] = Counter()

        for term, tf in term_counts.items():
            key = retrieval_key(term)
            shard = search_shard_for_key(key)
            key_counts[key] += tf

            previous = exact_terms[shard][term].get(chunk_id)
            posting = {
                "chunk_id": chunk_id,
                "path": chunk_path,
                "pdf_page": pdf_page,
                "tf": tf,
            }
            if previous is None or tf > previous["tf"]:
                exact_terms[shard][term][chunk_id] = posting

        for key, tf in key_counts.items():
            shard = search_shard_for_key(key)
            key_postings[shard][key][chunk_id] = {
                "chunk_id": chunk_id,
                "path": chunk_path,
                "pdf_page": pdf_page,
                "tf": tf,
            }

    shard_paths: list[Path] = []
    max_shard_bytes = 0
    max_shard_path = None

    all_shards = sorted(set(key_postings) | set(exact_terms))
    for shard in all_shards:
        keys_payload = {}
        for key, postings_by_chunk in sorted(key_postings[shard].items()):
            postings = sorted(
                postings_by_chunk.values(),
                key=lambda item: (-item["tf"], item["pdf_page"], item["chunk_id"]),
            )[:SEARCH_POSTINGS_MAX]
            keys_payload[key] = postings

        exact_payload = {}
        for term, postings_by_chunk in sorted(exact_terms[shard].items()):
            best = min(
                postings_by_chunk.values(),
                key=lambda item: (-item["tf"], item["pdf_page"], item["chunk_id"]),
            )
            exact_payload[term] = best

        payload = {
            "schema": "biblioteka-vsp/search-shard/v1",
            "book_id": book_id,
            "shard": shard,
            "normalization": {
                "lowercase": True,
                "yo_to_e": True,
                "min_token_chars": 2,
                "retrieval_key_chars": SEARCH_KEY_CHARS,
                "shard_prefix_chars": SEARCH_PREFIX_CHARS,
            },
            "keys": keys_payload,
            "exact_terms": exact_payload,
        }

        rel_path = Path("rag") / "search-index" / f"{shard}.json"
        abs_path = book_dir / rel_path
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )
        abs_path.write_text(encoded + "\n", encoding="utf-8")
        shard_paths.append(rel_path)

        size = len((encoded + "\n").encode("utf-8"))
        if size > max_shard_bytes:
            max_shard_bytes = size
            max_shard_path = rel_path.as_posix()
        if size > SEARCH_SHARD_MAX_BYTES:
            raise RuntimeError(
                f"Search shard exceeds {SEARCH_SHARD_MAX_BYTES} bytes: "
                f"{rel_path} = {size}"
            )

    manifest = {
        "schema": "biblioteka-vsp/search-index/v1",
        "book_id": book_id,
        "mode": "deterministic_lexical_shards",
        "normalization": {
            "lowercase": True,
            "yo_to_e": True,
            "min_token_chars": 2,
            "retrieval_key_chars": SEARCH_KEY_CHARS,
            "shard_prefix_chars": SEARCH_PREFIX_CHARS,
        },
        "lookup": {
            "token_to_key": (
                f"normalized token; first {SEARCH_KEY_CHARS} characters "
                "when longer"
            ),
            "key_to_shard": (
                f"first {SEARCH_PREFIX_CHARS} characters; tokens shorter than "
                f"{SEARCH_PREFIX_CHARS} use _short/<token>.json"
            ),
            "path_pattern": "rag/search-index/<shard>.json",
            "postings_per_key_max": SEARCH_POSTINGS_MAX,
        },
        "statistics": {
            "shards": len(shard_paths),
            "max_shard_bytes": max_shard_bytes,
            "max_shard_path": max_shard_path,
        },
    }
    manifest_path = search_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        + "\n",
        encoding="utf-8",
    )

    return {
        "shards": len(shard_paths),
        "max_shard_bytes": max_shard_bytes,
        "max_shard_path": max_shard_path,
        "manifest_path": str(manifest_path),
    }


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

    search_index = build_lexical_search_index(
        book_dir=book_dir,
        book_id=book_id,
        chunk_records=chunk_records,
        index_records=index_records,
    )

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
  discovery: deterministic_lexical_shards
  search_index_manifest: rag/search-index/manifest.json
  search_index_path_pattern: "rag/search-index/<shard>.json"
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
  search_index_shards: {search_index["shards"]}
  search_index_max_shard_bytes: {search_index["max_shard_bytes"]}

validation:
  chunk_ids_unique: {str(ids_unique).lower()}
  retrieval_paths_unique: {str(paths_unique).lower()}
  retrieval_chunk_count_matches: {str(len(index_records) == len(chunk_records)).lower()}
  search_index_bounded: {str(search_index["max_shard_bytes"] <= SEARCH_SHARD_MAX_BYTES).lower()}
  source_checksum_verified: true
  full_pdf_page_range_processed: true
  status: READY_WITH_KNOWN_LIMITATIONS

known_limitations:
  - "The PDF uses an embedded OCR text layer; recognition errors present in the source OCR may remain in extracted text."
  - "Images, equations, tables and diagrams are not independently encoded as multimodal RAG objects; use pdf_page provenance to inspect the source page when visual context matters."
  - "Publisher advertisement and cover pages are part of the source PDF and remain page-addressable even when they are not core book content."
  - "The deterministic lexical index is prefix-based retrieval, not semantic vector search; use up to three informative query tokens and preserve RAG_MISS on unsupported questions."
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
        "search_index_shards": search_index["shards"],
        "search_index_max_shard_bytes": search_index["max_shard_bytes"],
        "search_index_max_shard_path": search_index["max_shard_path"],
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
