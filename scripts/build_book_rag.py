#!/usr/bin/env python3
"""Build deterministic source-traceable RAG artifacts for one biblioteka-vsp book."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
from zipfile import ZipFile

import fitz


TARGET_CHARS = 4000
OVERLAP_CHARS = 350
RETRIEVAL_TOP_K_MAX = 3
SEARCH_KEY_CHARS = 4
SEARCH_PREFIX_CHARS = 3
SEARCH_POSTINGS_MAX = 32
SEARCH_SHARD_MAX_BYTES = 262144
SUPPORTED_SOURCES = {"book.pdf": "pdf", "book.epub": "epub"}


class EpubTextExtractor(HTMLParser):
    """Small deterministic XHTML-to-text extractor for EPUB spine documents."""

    BLOCK_TAGS = {
        "address", "article", "aside", "blockquote", "br", "dd", "div", "dl",
        "dt", "figcaption", "figure", "footer", "h1", "h2", "h3", "h4", "h5",
        "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre", "section",
        "table", "tbody", "td", "tfoot", "th", "thead", "tr", "ul",
    }
    SKIP_TAGS = {"head", "script", "style"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def _newline(self) -> None:
        if self.skip_depth == 0:
            self.parts.append("\n")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in self.BLOCK_TAGS:
            self._newline()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag in self.BLOCK_TAGS:
            self._newline()

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


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
    text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)
    return text.strip()


def split_unit(text: str) -> list[str]:
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


def resolve_source(book_dir: Path) -> tuple[Path, str]:
    source_dir = book_dir / "source"
    candidates = [source_dir / name for name in SUPPORTED_SOURCES if (source_dir / name).is_file()]
    if not candidates:
        supported = ", ".join(sorted(SUPPORTED_SOURCES))
        raise FileNotFoundError(f"Canonical source missing in {source_dir}; expected one of: {supported}")
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        raise RuntimeError(f"Ambiguous canonical source: multiple supported files exist: {names}")
    source = candidates[0]
    return source, SUPPORTED_SOURCES[source.name]


def unit_prefix(source_format: str) -> str:
    return "p" if source_format == "pdf" else "e"


def chunk_shard(source_format: str, source_unit: int) -> str:
    prefix = unit_prefix(source_format)
    start = ((source_unit - 1) // 100) * 100 + 1
    end = start + 99
    return f"{prefix}{start:04d}-{prefix}{end:04d}"


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


def pdf_units(source: Path) -> tuple[list[dict], dict]:
    document = fitz.open(source)
    units: list[dict] = []
    for pdf_page, page in enumerate(document, start=1):
        units.append(
            {
                "source_unit": pdf_page,
                "source_unit_type": "pdf_page",
                "source_locator": str(pdf_page),
                "text": normalize_text(page.get_text("text", sort=True)),
            }
        )
    page_count = len(document)
    document.close()
    if page_count == 0:
        raise RuntimeError("PDF contains no pages")
    return units, {
        "engine": "PyMuPDF",
        "engine_version": getattr(fitz, "VersionBind", "[Needs confirmation]"),
        "unit_coordinate_system": "source_pdf_1_indexed",
        "content_model": "unclassified_extractable_pdf_text",
    }


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def epub_units(source: Path) -> tuple[list[dict], dict]:
    with ZipFile(source) as archive:
        try:
            container_root = ET.fromstring(archive.read("META-INF/container.xml"))
        except Exception as exc:
            raise RuntimeError(f"Invalid EPUB container.xml: {exc}") from exc

        rootfile = next(
            (node for node in container_root.iter() if _local_name(node.tag) == "rootfile"),
            None,
        )
        opf_path = rootfile.attrib.get("full-path") if rootfile is not None else None
        if not opf_path:
            raise RuntimeError("EPUB container does not declare an OPF rootfile")

        try:
            opf_root = ET.fromstring(archive.read(opf_path))
        except Exception as exc:
            raise RuntimeError(f"Cannot parse EPUB OPF {opf_path}: {exc}") from exc

        manifest: dict[str, dict[str, str]] = {}
        spine_ids: list[str] = []
        for node in opf_root.iter():
            name = _local_name(node.tag)
            if name == "item" and node.attrib.get("id"):
                manifest[node.attrib["id"]] = dict(node.attrib)
            elif name == "itemref" and node.attrib.get("idref"):
                spine_ids.append(node.attrib["idref"])

        if not spine_ids:
            raise RuntimeError("EPUB OPF spine is empty")

        opf_dir = posixpath.dirname(opf_path)
        units: list[dict] = []
        unsupported_media_types: set[str] = set()
        for ordinal, idref in enumerate(spine_ids, start=1):
            item = manifest.get(idref)
            if not item or not item.get("href"):
                raise RuntimeError(f"EPUB spine idref has no manifest item: {idref}")
            href = unquote(item["href"].split("#", 1)[0])
            member = posixpath.normpath(posixpath.join(opf_dir, href))
            media_type = item.get("media-type", "")
            text = ""
            if media_type in {"application/xhtml+xml", "text/html"}:
                try:
                    raw = archive.read(member)
                except KeyError as exc:
                    raise RuntimeError(f"EPUB spine resource missing: {member}") from exc
                parser = EpubTextExtractor()
                parser.feed(raw.decode("utf-8-sig", errors="replace"))
                parser.close()
                text = normalize_text(parser.text())
            else:
                unsupported_media_types.add(media_type or "[missing]")

            units.append(
                {
                    "source_unit": ordinal,
                    "source_unit_type": "epub_spine_item",
                    "source_locator": member,
                    "source_item_id": idref,
                    "text": text,
                }
            )

    return units, {
        "engine": "python-zipfile-htmlparser",
        "engine_version": f"python-{sys.version_info.major}.{sys.version_info.minor}",
        "unit_coordinate_system": "epub_spine_1_indexed",
        "content_model": "xhtml_text",
        "unsupported_spine_media_types": sorted(unsupported_media_types),
    }


def extract_units(source: Path, source_format: str) -> tuple[list[dict], dict]:
    if source_format == "pdf":
        return pdf_units(source)
    if source_format == "epub":
        return epub_units(source)
    raise RuntimeError(f"Unsupported source format: {source_format}")


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

    path_by_chunk = {record["chunk_id"]: record["path"] for record in index_records}
    key_postings: dict[str, dict[str, dict[str, dict]]] = defaultdict(lambda: defaultdict(dict))
    exact_terms: dict[str, dict[str, dict[str, dict]]] = defaultdict(lambda: defaultdict(dict))

    for record in chunk_records:
        chunk_id = record["chunk_id"]
        chunk_path = path_by_chunk[chunk_id]
        term_counts = Counter(lexical_tokens(record["text"]))
        key_counts: Counter[str] = Counter()

        for term, tf in term_counts.items():
            key = retrieval_key(term)
            shard = search_shard_for_key(key)
            key_counts[key] += tf
            base = {
                "chunk_id": chunk_id,
                "path": chunk_path,
                "source_unit": record["source_unit"],
                "source_unit_type": record["source_unit_type"],
                "source_locator": record["source_locator"],
                "tf": tf,
            }
            if record.get("pdf_page") is not None:
                base["pdf_page"] = record["pdf_page"]
            previous = exact_terms[shard][term].get(chunk_id)
            if previous is None or tf > previous["tf"]:
                exact_terms[shard][term][chunk_id] = base

        for key, tf in key_counts.items():
            shard = search_shard_for_key(key)
            base = {
                "chunk_id": chunk_id,
                "path": chunk_path,
                "source_unit": record["source_unit"],
                "source_unit_type": record["source_unit_type"],
                "source_locator": record["source_locator"],
                "tf": tf,
            }
            if record.get("pdf_page") is not None:
                base["pdf_page"] = record["pdf_page"]
            key_postings[shard][key][chunk_id] = base

    shard_paths: list[Path] = []
    max_shard_bytes = 0
    max_shard_path = None
    all_shards = sorted(set(key_postings) | set(exact_terms))
    for shard in all_shards:
        keys_payload = {}
        for key, postings_by_chunk in sorted(key_postings[shard].items()):
            postings = sorted(
                postings_by_chunk.values(),
                key=lambda item: (-item["tf"], item["source_unit"], item["chunk_id"]),
            )[:SEARCH_POSTINGS_MAX]
            keys_payload[key] = postings

        exact_payload = {}
        for term, postings_by_chunk in sorted(exact_terms[shard].items()):
            best = min(
                postings_by_chunk.values(),
                key=lambda item: (-item["tf"], item["source_unit"], item["chunk_id"]),
            )
            exact_payload[term] = best

        payload = {
            "schema": "biblioteka-vsp/search-shard/v2",
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
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        abs_path.write_text(encoded + "\n", encoding="utf-8")
        shard_paths.append(rel_path)
        size = len((encoded + "\n").encode("utf-8"))
        if size > max_shard_bytes:
            max_shard_bytes = size
            max_shard_path = rel_path.as_posix()
        if size > SEARCH_SHARD_MAX_BYTES:
            raise RuntimeError(f"Search shard exceeds {SEARCH_SHARD_MAX_BYTES} bytes: {rel_path} = {size}")

    manifest = {
        "schema": "biblioteka-vsp/search-index/v2",
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
            "token_to_key": f"normalized token; first {SEARCH_KEY_CHARS} characters when longer",
            "key_to_shard": f"first {SEARCH_PREFIX_CHARS} characters; tokens shorter than {SEARCH_PREFIX_CHARS} use _short/<token>.json",
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
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n",
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
    source_format: str,
    source_path: str,
    source_sha: str,
    source_unit: int,
    source_unit_type: str,
    source_locator: str,
    chunk_in_unit: int,
    chunk_text: str,
) -> dict:
    prefix = unit_prefix(source_format)
    chunk_id = f"{book_id}:{prefix}{source_unit:04d}:c{chunk_in_unit:02d}"
    rel_path = Path("rag") / "chunks" / chunk_shard(source_format, source_unit) / f"{prefix}{source_unit:04d}-c{chunk_in_unit:02d}.md"
    abs_path = book_dir / rel_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)

    front = [
        "---",
        "schema: biblioteka-vsp/chunk/v2",
        f"chunk_id: {chunk_id}",
        f"book_id: {book_id}",
        f"source_format: {source_format}",
        f"source_unit_type: {source_unit_type}",
        f"source_unit: {source_unit}",
        f"source_locator: {json.dumps(source_locator, ensure_ascii=False)}",
    ]
    if source_format == "pdf":
        front.append(f"pdf_page: {source_unit}")
        front.append(f"chunk_in_page: {chunk_in_unit}")
    front.extend(
        [
            f"chunk_in_unit: {chunk_in_unit}",
            f"source_path: {source_path}",
            f"source_sha256: {source_sha}",
            "---",
            "",
            chunk_text,
            "",
        ]
    )
    abs_path.write_text("\n".join(front), encoding="utf-8")

    record = {
        "chunk_id": chunk_id,
        "book_id": book_id,
        "source_format": source_format,
        "source_unit_type": source_unit_type,
        "source_unit": source_unit,
        "source_locator": source_locator,
        "chunk_in_unit": chunk_in_unit,
        "path": rel_path.as_posix(),
        "source_path": source_path,
        "source_sha256": source_sha,
        "chars": len(chunk_text),
        "text_sha256": sha256_text(chunk_text),
    }
    if source_format == "pdf":
        record["pdf_page"] = source_unit
        record["chunk_in_page"] = chunk_in_unit
    return record


def build(book_dir: Path) -> dict:
    source, source_format = resolve_source(book_dir)
    source_rel = f"source/{source.name}"
    book_id = book_dir.name
    source_sha = sha256_file(source)
    expected = expected_sha(book_dir)
    checksum_expected_present = expected is not None
    checksum_matched_expected = bool(expected and source_sha == expected)
    if expected and source_sha != expected:
        raise RuntimeError(f"Source checksum mismatch: expected {expected}, got {source_sha}")

    rag_dir = book_dir / "rag"
    rag_dir.mkdir(parents=True, exist_ok=True)
    retrieval_dir = rag_dir / "chunks"
    if retrieval_dir.exists():
        shutil.rmtree(retrieval_dir)
    retrieval_dir.mkdir(parents=True, exist_ok=True)

    units, extraction = extract_units(source, source_format)
    text_parts: list[str] = ["# Extracted text\n"]
    chunk_records: list[dict] = []
    index_records: list[dict] = []
    blank_units: list[int] = []
    extracted_characters = 0
    prefix = unit_prefix(source_format)

    for unit in units:
        source_unit = int(unit["source_unit"])
        source_unit_type = str(unit["source_unit_type"])
        source_locator = str(unit["source_locator"])
        text = str(unit["text"])
        extracted_characters += len(text)
        if not text:
            blank_units.append(source_unit)

        if source_format == "pdf":
            heading = f"PDF page {source_unit:04d}"
            missing = "[No extractable text on this PDF page]"
        else:
            heading = f"EPUB spine item {source_unit:04d} — {source_locator}"
            missing = "[No extractable text in this EPUB spine item]"
        text_parts.append(
            f"<!-- source_unit: {source_unit_type}:{source_unit:04d}; locator: {source_locator} -->\n"
            f"## {heading}\n\n{text if text else missing}\n"
        )

        for chunk_in_unit, chunk_text in enumerate(split_unit(text), start=1):
            chunk_id = f"{book_id}:{prefix}{source_unit:04d}:c{chunk_in_unit:02d}"
            record = {
                "chunk_id": chunk_id,
                "book_id": book_id,
                "source_format": source_format,
                "source_unit_type": source_unit_type,
                "source_unit": source_unit,
                "source_locator": source_locator,
                "chunk_in_unit": chunk_in_unit,
                "source_path": source_rel,
                "source_sha256": source_sha,
                "text": chunk_text,
            }
            if source_format == "pdf":
                record["pdf_page"] = source_unit
                record["chunk_in_page"] = chunk_in_unit
            chunk_records.append(record)
            index_records.append(
                write_retrieval_chunk(
                    book_dir=book_dir,
                    book_id=book_id,
                    source_format=source_format,
                    source_path=source_rel,
                    source_sha=source_sha,
                    source_unit=source_unit,
                    source_unit_type=source_unit_type,
                    source_locator=source_locator,
                    chunk_in_unit=chunk_in_unit,
                    chunk_text=chunk_text,
                )
            )

    if not units:
        raise RuntimeError(f"{source_format.upper()} contains no source units")

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
            stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    with index_path.open("w", encoding="utf-8", newline="\n") as stream:
        for record in index_records:
            stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")

    chunk_ids = [record["chunk_id"] for record in chunk_records]
    ids_unique = len(chunk_ids) == len(set(chunk_ids))
    paths_unique = len(index_records) == len({record["path"] for record in index_records})
    source_count_key = "pdf_pages" if source_format == "pdf" else "epub_spine_items"
    source_unit_name = "pdf_page" if source_format == "pdf" else "epub_spine_item"
    chunk_pattern = (
        "rag/chunks/p####-p####/p####-c##.md"
        if source_format == "pdf"
        else "rag/chunks/e####-e####/e####-c##.md"
    )
    source_specific = f"  {source_count_key}: {len(units)}\n"
    unsupported = extraction.get("unsupported_spine_media_types") or []
    unsupported_line = ""
    if source_format == "epub":
        unsupported_line = f"  unsupported_spine_media_types: {json.dumps(unsupported, ensure_ascii=False)}\n"

    known_limitations = [
        "Images, equations, tables and diagrams are not independently encoded as multimodal RAG objects.",
        "The deterministic lexical index is prefix-based retrieval, not semantic vector search; use up to three informative query tokens and preserve RAG_MISS on unsupported questions.",
    ]
    if source_format == "pdf":
        known_limitations[:0] = [
            "The extractor reads the PDF text layer but does not classify native text versus OCR; content_model therefore does not assert OCR origin.",
            "Recognition/extraction errors already present in the PDF text layer may remain in extracted text.",
            "PDF page provenance is available for source inspection when visual context matters.",
        ]
    else:
        known_limitations[:0] = [
            "EPUB is reflowable; spine/XHTML locators are canonical provenance and are not equivalent to printed or PDF page numbers.",
            "CSS layout, embedded fonts, interactive content and non-text rendering are not reproduced in the text RAG.",
        ]

    manifest = f"""schema: biblioteka-vsp/rag/v2
book_id: {book_id}

source:
  path: {source_rel}
  format: {source_format}
  sha256: {source_sha}
{source_specific}
extraction:
  engine: {extraction['engine']}
  engine_version: "{extraction['engine_version']}"
  unit_coordinate_system: {extraction['unit_coordinate_system']}
  content_model: {extraction['content_model']}
{unsupported_line}  normalization:
    - remove_NUL
    - remove_soft_hyphen_marker
    - normalize_line_endings
    - trim_trailing_horizontal_whitespace

chunking:
  scope: per_source_unit
  source_unit_type: {source_unit_name}
  target_chars: {TARGET_CHARS}
  overlap_chars: {OVERLAP_CHARS}
  id_pattern: "<book-slug>:{prefix}<source-unit-4d>:c<chunk-2d>"

retrieval:
  mode: addressable_small_chunks
  discovery: deterministic_lexical_shards
  search_index_manifest: rag/search-index/manifest.json
  search_index_path_pattern: "rag/search-index/<shard>.json"
  search_scope: rag/chunks/
  chunk_index: rag/chunk-index.jsonl
  top_k_max: {RETRIEVAL_TOP_K_MAX}
  chunk_file_pattern: "{chunk_pattern}"
  bulk_files:
    - rag/text.md
    - rag/chunks.jsonl
  bulk_files_for_query_retrieval: false

statistics:
  source_units_with_text: {len(units) - len(blank_units)}
  blank_source_units: {len(blank_units)}
  blank_source_unit_numbers: {json.dumps(blank_units)}
  extracted_characters: {extracted_characters}
  chunks: {len(chunk_records)}
  retrieval_chunk_files: {len(index_records)}
  search_index_shards: {search_index['shards']}
  search_index_max_shard_bytes: {search_index['max_shard_bytes']}

validation:
  chunk_ids_unique: {str(ids_unique).lower()}
  retrieval_paths_unique: {str(paths_unique).lower()}
  retrieval_chunk_count_matches: {str(len(index_records) == len(chunk_records)).lower()}
  search_index_bounded: {str(search_index['max_shard_bytes'] <= SEARCH_SHARD_MAX_BYTES).lower()}
  source_checksum_computed: true
  source_checksum_expected_present: {str(checksum_expected_present).lower()}
  source_checksum_matched_expected: {str(checksum_matched_expected).lower()}
  source_checksum_verified: {str(checksum_matched_expected).lower()}
  full_source_unit_range_processed: true
  status: READY_WITH_KNOWN_LIMITATIONS

known_limitations:
""" + "\n".join(f"  - {json.dumps(item, ensure_ascii=False)}" for item in known_limitations) + "\n"
    manifest_path.write_text(manifest, encoding="utf-8")

    if not ids_unique:
        raise RuntimeError("Generated chunk IDs are not unique")
    if not paths_unique:
        raise RuntimeError("Generated retrieval chunk paths are not unique")
    if len(index_records) != len(chunk_records):
        raise RuntimeError("Retrieval chunk count does not match chunk count")

    return {
        "book_id": book_id,
        "source_format": source_format,
        "source_path": source_rel,
        "source_sha256": source_sha,
        "source_checksum_expected_present": checksum_expected_present,
        "source_checksum_matched_expected": checksum_matched_expected,
        "source_units": len(units),
        "source_units_with_text": len(units) - len(blank_units),
        "blank_source_units": blank_units,
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
