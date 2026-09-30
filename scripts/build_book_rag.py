#!/usr/bin/env python3
"""Build deterministic source-traceable RAG artifacts for one biblioteka-vsp book."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import posixpath
import re
import shutil
import sys
import urllib.parse
import zipfile
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

import fitz


TARGET_CHARS = 4000
OVERLAP_CHARS = 350
RETRIEVAL_TOP_K_MAX = 3
SEARCH_KEY_CHARS = 4
SEARCH_PREFIX_CHARS = 3
SEARCH_POSTINGS_MAX = 32
SEARCH_SHARD_MAX_BYTES = 262144
SUPPORTED_SOURCE_NAMES = ("book.pdf", "book.epub")


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
    matches = [
        book_dir / "source" / name
        for name in SUPPORTED_SOURCE_NAMES
        if (book_dir / "source" / name).is_file()
    ]
    if not matches:
        raise FileNotFoundError(
            f"Canonical source missing; expected one of: {', '.join(SUPPORTED_SOURCE_NAMES)}"
        )
    if len(matches) != 1:
        raise RuntimeError(
            "Canonical source is ambiguous; exactly one of book.pdf or book.epub must exist"
        )
    source = matches[0]
    return source, source.suffix.lower().lstrip(".")


def coordinate_shard(prefix: str, source_seq: int) -> str:
    start = ((source_seq - 1) // 100) * 100 + 1
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


class _HTMLTextExtractor(HTMLParser):
    BLOCK_TAGS = {
        "address", "article", "aside", "blockquote", "br", "div", "figcaption",
        "figure", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "header",
        "hr", "li", "main", "nav", "ol", "p", "pre", "section", "table",
        "tbody", "td", "tfoot", "th", "thead", "tr", "ul",
    }
    SKIP_TAGS = {"script", "style", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        if not self.skip_depth and tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if not self.skip_depth and tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)


def html_to_text(raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    parser = _HTMLTextExtractor()
    parser.feed(text)
    parser.close()
    return normalize_text(html.unescape("".join(parser.parts)))


def _xml_local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def extract_epub_units(source: Path) -> tuple[list[dict], dict]:
    with zipfile.ZipFile(source) as archive:
        try:
            container_root = ET.fromstring(archive.read("META-INF/container.xml"))
        except Exception as exc:
            raise RuntimeError(f"EPUB container.xml unreadable: {exc}") from exc

        rootfiles = [
            elem.attrib.get("full-path")
            for elem in container_root.iter()
            if _xml_local_name(elem.tag) == "rootfile" and elem.attrib.get("full-path")
        ]
        if not rootfiles:
            raise RuntimeError("EPUB package document not declared in container.xml")

        opf_path = rootfiles[0]
        try:
            opf_root = ET.fromstring(archive.read(opf_path))
        except Exception as exc:
            raise RuntimeError(f"EPUB package document unreadable: {exc}") from exc

        manifest: dict[str, tuple[str, str]] = {}
        spine_ids: list[str] = []
        for elem in opf_root.iter():
            name = _xml_local_name(elem.tag)
            if name == "item":
                item_id = elem.attrib.get("id")
                href = elem.attrib.get("href")
                media_type = elem.attrib.get("media-type", "")
                if item_id and href:
                    manifest[item_id] = (href, media_type)
            elif name == "itemref":
                idref = elem.attrib.get("idref")
                linear = elem.attrib.get("linear", "yes").lower()
                if idref and linear != "no":
                    spine_ids.append(idref)

        if not spine_ids:
            raise RuntimeError("EPUB spine contains no readable items")

        opf_dir = posixpath.dirname(opf_path)
        units: list[dict] = []
        for spine_index, idref in enumerate(spine_ids, start=1):
            item = manifest.get(idref)
            if not item:
                raise RuntimeError(f"EPUB spine references missing manifest id: {idref}")
            href, media_type = item
            href_path = urllib.parse.unquote(urllib.parse.urlsplit(href).path)
            member = posixpath.normpath(posixpath.join(opf_dir, href_path))
            if member.startswith("../"):
                raise RuntimeError(f"EPUB manifest path escapes package root: {href}")
            try:
                raw = archive.read(member)
            except KeyError as exc:
                raise RuntimeError(f"EPUB spine member missing: {member}") from exc

            if media_type not in {"application/xhtml+xml", "text/html"}:
                text = ""
            else:
                text = html_to_text(raw)

            units.append(
                {
                    "source_seq": spine_index,
                    "source_unit": {
                        "kind": "epub_spine_item",
                        "index": spine_index,
                        "href": member,
                    },
                    "text": text,
                }
            )

        return units, {
            "engine": "python-stdlib-zipfile+xml.etree+html.parser",
            "coordinate_system": "epub_spine_1_indexed",
            "package_document": opf_path,
        }


def extract_pdf_units(source: Path) -> tuple[list[dict], dict]:
    document = fitz.open(source)
    units: list[dict] = []
    for pdf_page, page in enumerate(document, start=1):
        units.append(
            {
                "source_seq": pdf_page,
                "source_unit": {"kind": "pdf_page", "index": pdf_page},
                "text": normalize_text(page.get_text("text", sort=True)),
            }
        )
    document.close()
    return units, {
        "engine": "PyMuPDF",
        "engine_version": getattr(fitz, "VersionBind", "[Needs confirmation]"),
        "coordinate_system": "source_pdf_1_indexed",
    }


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
        source_seq = record["source_seq"]
        chunk_path = path_by_chunk[chunk_id]
        term_counts = Counter(lexical_tokens(record["text"]))
        key_counts: Counter[str] = Counter()

        for term, tf in term_counts.items():
            key = retrieval_key(term)
            shard = search_shard_for_key(key)
            key_counts[key] += tf
            posting = {
                "chunk_id": chunk_id,
                "path": chunk_path,
                "source_seq": source_seq,
                "source_unit": record["source_unit"],
                "tf": tf,
            }
            if record["source_unit"]["kind"] == "pdf_page":
                posting["pdf_page"] = source_seq
            previous = exact_terms[shard][term].get(chunk_id)
            if previous is None or tf > previous["tf"]:
                exact_terms[shard][term][chunk_id] = posting

        for key, tf in key_counts.items():
            shard = search_shard_for_key(key)
            posting = {
                "chunk_id": chunk_id,
                "path": chunk_path,
                "source_seq": source_seq,
                "source_unit": record["source_unit"],
                "tf": tf,
            }
            if record["source_unit"]["kind"] == "pdf_page":
                posting["pdf_page"] = source_seq
            key_postings[shard][key][chunk_id] = posting

    shard_paths: list[Path] = []
    max_shard_bytes = 0
    max_shard_path = None

    def order_key(item: dict) -> tuple:
        return (-item["tf"], int(item.get("source_seq", item.get("pdf_page", 0))), item["chunk_id"])

    for shard in sorted(set(key_postings) | set(exact_terms)):
        keys_payload = {}
        for key, postings_by_chunk in sorted(key_postings[shard].items()):
            keys_payload[key] = sorted(postings_by_chunk.values(), key=order_key)[:SEARCH_POSTINGS_MAX]

        exact_payload = {}
        for term, postings_by_chunk in sorted(exact_terms[shard].items()):
            exact_payload[term] = min(postings_by_chunk.values(), key=order_key)

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
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        abs_path.write_text(encoded + "\n", encoding="utf-8")
        shard_paths.append(rel_path)

        size = len((encoded + "\n").encode("utf-8"))
        if size > max_shard_bytes:
            max_shard_bytes = size
            max_shard_path = rel_path.as_posix()
        if size > SEARCH_SHARD_MAX_BYTES:
            raise RuntimeError(
                f"Search shard exceeds {SEARCH_SHARD_MAX_BYTES} bytes: {rel_path} = {size}"
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
            "token_to_key": f"normalized token; first {SEARCH_KEY_CHARS} characters when longer",
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
    (search_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "shards": len(shard_paths),
        "max_shard_bytes": max_shard_bytes,
        "max_shard_path": max_shard_path,
    }


def chunk_identity(book_id: str, source_format: str, source_seq: int, chunk_in_unit: int) -> tuple[str, str, str]:
    prefix = "p" if source_format == "pdf" else "s"
    chunk_id = f"{book_id}:{prefix}{source_seq:04d}:c{chunk_in_unit:02d}"
    shard = coordinate_shard(prefix, source_seq)
    filename = f"{prefix}{source_seq:04d}-c{chunk_in_unit:02d}.md"
    return chunk_id, shard, filename


def write_retrieval_chunk(
    *,
    book_dir: Path,
    book_id: str,
    source_format: str,
    source_path: str,
    source_sha: str,
    source_seq: int,
    source_unit: dict,
    chunk_in_unit: int,
    chunk_text: str,
) -> dict:
    chunk_id, shard, filename = chunk_identity(book_id, source_format, source_seq, chunk_in_unit)
    rel_path = Path("rag") / "chunks" / shard / filename
    abs_path = book_dir / rel_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)

    meta = {
        "schema": "biblioteka-vsp/chunk/v2" if source_format == "epub" else "biblioteka-vsp/chunk/v1",
        "chunk_id": chunk_id,
        "book_id": book_id,
        "source_format": source_format,
        "source_seq": source_seq,
        "source_unit": source_unit,
        "chunk_in_unit": chunk_in_unit,
        "source_path": source_path,
        "source_sha256": source_sha,
    }
    if source_format == "pdf":
        meta["pdf_page"] = source_seq
        meta["chunk_in_page"] = chunk_in_unit

    front = "\n".join(
        [
            "---",
            *(f"{key}: {json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value}" for key, value in meta.items()),
            "---",
            "",
        ]
    )
    abs_path.write_text(front + "\n" + chunk_text + "\n", encoding="utf-8")

    record = {
        "chunk_id": chunk_id,
        "book_id": book_id,
        "source_format": source_format,
        "source_seq": source_seq,
        "source_unit": source_unit,
        "chunk_in_unit": chunk_in_unit,
        "path": rel_path.as_posix(),
        "source_path": source_path,
        "source_sha256": source_sha,
        "chars": len(chunk_text),
        "text_sha256": sha256_text(chunk_text),
    }
    if source_format == "pdf":
        record["pdf_page"] = source_seq
        record["chunk_in_page"] = chunk_in_unit
    return record


def build(book_dir: Path) -> dict:
    source, source_format = resolve_source(book_dir)
    source_rel = source.relative_to(book_dir).as_posix()
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

    if source_format == "pdf":
        units, extraction_meta = extract_pdf_units(source)
        text_layer = "unclassified_extractable_pdf_text"
        chunk_scope = "per_pdf_page"
        id_pattern = "<book-slug>:p<pdf-page-4d>:c<chunk-2d>"
    elif source_format == "epub":
        units, extraction_meta = extract_epub_units(source)
        text_layer = "structured_epub_xhtml_text"
        chunk_scope = "per_epub_spine_item"
        id_pattern = "<book-slug>:s<spine-item-4d>:c<chunk-2d>"
    else:
        raise RuntimeError(f"Unsupported source format: {source_format}")

    text_parts: list[str] = ["# Extracted text\n"]
    chunk_records: list[dict] = []
    index_records: list[dict] = []
    blank_units: list[int] = []
    extracted_characters = 0

    for unit in units:
        source_seq = unit["source_seq"]
        source_unit = unit["source_unit"]
        text = unit["text"]
        extracted_characters += len(text)
        if not text:
            blank_units.append(source_seq)

        if source_format == "pdf":
            heading = f"PDF page {source_seq:04d}"
            marker = f"pdf_page: {source_seq:04d}"
        else:
            heading = f"EPUB spine item {source_seq:04d}"
            marker = f"epub_spine_item: {source_seq:04d} href={source_unit['href']}"

        text_parts.append(
            f"<!-- {marker} -->\n## {heading}\n\n"
            f"{text if text else '[No extractable text in this source unit]'}\n"
        )

        for chunk_in_unit, chunk_text in enumerate(split_unit(text), start=1):
            record = write_retrieval_chunk(
                book_dir=book_dir,
                book_id=book_id,
                source_format=source_format,
                source_path=source_rel,
                source_sha=source_sha,
                source_seq=source_seq,
                source_unit=source_unit,
                chunk_in_unit=chunk_in_unit,
                chunk_text=chunk_text,
            )
            chunk_records.append({**record, "text": chunk_text})
            index_records.append({key: value for key, value in record.items() if key != "text"})

    if not units:
        raise RuntimeError("Source contains no addressable units")
    if not chunk_records:
        raise RuntimeError("Source contains no extractable text chunks")

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

    extraction_lines = [
        f"  engine: {json.dumps(extraction_meta['engine'], ensure_ascii=False)}",
    ]
    if extraction_meta.get("engine_version"):
        extraction_lines.append(f"  engine_version: {json.dumps(extraction_meta['engine_version'])}")
    extraction_lines.extend(
        [
            f"  source_coordinate_system: {extraction_meta['coordinate_system']}",
            f"  text_layer: {text_layer}",
        ]
    )
    if extraction_meta.get("package_document"):
        extraction_lines.append(
            f"  package_document: {json.dumps(extraction_meta['package_document'], ensure_ascii=False)}"
        )

    manifest = f"""schema: biblioteka-vsp/rag/v1
book_id: {book_id}

source:
  path: {source_rel}
  format: {source_format}
  sha256: {source_sha}
  units: {len(units)}

extraction:
{chr(10).join(extraction_lines)}
  normalization:
    - remove_NUL
    - remove_soft_hyphen_marker
    - normalize_line_endings
    - trim_trailing_horizontal_whitespace

chunking:
  scope: {chunk_scope}
  target_chars: {TARGET_CHARS}
  overlap_chars: {OVERLAP_CHARS}
  id_pattern: "{id_pattern}"

retrieval:
  mode: addressable_small_chunks
  discovery: deterministic_lexical_shards
  search_index_manifest: rag/search-index/manifest.json
  search_index_path_pattern: "rag/search-index/<shard>.json"
  search_scope: rag/chunks/
  chunk_index: rag/chunk-index.jsonl
  top_k_max: {RETRIEVAL_TOP_K_MAX}
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
  search_index_shards: {search_index["shards"]}
  search_index_max_shard_bytes: {search_index["max_shard_bytes"]}

validation:
  chunk_ids_unique: {str(ids_unique).lower()}
  retrieval_paths_unique: {str(paths_unique).lower()}
  retrieval_chunk_count_matches: {str(len(index_records) == len(chunk_records)).lower()}
  search_index_bounded: {str(search_index["max_shard_bytes"] <= SEARCH_SHARD_MAX_BYTES).lower()}
  source_checksum_computed: true
  source_checksum_expected_present: {str(checksum_expected_present).lower()}
  source_checksum_matched_expected: {str(checksum_matched_expected).lower()}
  source_checksum_verified: {str(checksum_matched_expected).lower()}
  full_source_range_processed: true
  status: READY_WITH_KNOWN_LIMITATIONS

known_limitations:
  - "The extractor preserves source-unit provenance but does not independently encode images, equations, tables or diagrams as multimodal RAG objects."
  - "The deterministic lexical index is prefix-based retrieval, not semantic vector search; use up to three informative query tokens and preserve RAG_MISS on unsupported questions."
"""
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
