#!/usr/bin/env python3
"""Strict acceptance validation for newly built biblioteka-vsp RAG generations."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_book_rag as builder


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML root is not a mapping: {path}")
    return data


def read_sha_record(path: Path) -> str:
    parts = path.read_text(encoding="utf-8").strip().split()
    if not parts or not re.fullmatch(r"[0-9a-fA-F]{64}", parts[0]):
        raise ValueError(f"invalid SHA256 record: {path}")
    return parts[0].lower()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ValueError(f"{path}: line {line_number} is not an object")
        records.append(item)
    if not records:
        raise ValueError(f"empty JSONL: {path}")
    return records


def read_chunk(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ValueError(f"chunk front matter missing: {path}")
    try:
        _, front, body = raw.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"chunk front matter malformed: {path}") from exc
    meta = yaml.safe_load(front)
    if not isinstance(meta, dict):
        raise ValueError(f"chunk metadata malformed: {path}")
    return meta, body.strip("\n")


def check(checks: list[dict[str, Any]], check_id: str, ok: bool, evidence: Any) -> None:
    checks.append(
        {
            "id": check_id,
            "status": "PASS" if ok else "FAIL",
            "evidence": evidence,
        }
    )


def lexical_tokens(text: str) -> list[str]:
    return [
        token.lower().replace("ё", "е")
        for token in re.findall(r"[0-9a-zа-я]+", text.lower().replace("ё", "е"), flags=re.IGNORECASE)
        if 4 <= len(token) <= 64
    ]


def sample_retrieval_resolves(
    *,
    book_dir: Path,
    record: dict[str, Any],
    search_manifest: dict[str, Any],
) -> tuple[bool, str]:
    rel = record.get("path")
    if not isinstance(rel, str):
        return False, "chunk-index record has no path"
    chunk_path = book_dir / rel
    if not chunk_path.is_file():
        return False, f"chunk missing: {rel}"
    _, body = read_chunk(chunk_path)

    normalization = search_manifest.get("normalization") or {}
    prefix_chars = normalization.get("shard_prefix_chars")
    if not isinstance(prefix_chars, int) or prefix_chars not in {3, 4}:
        return False, f"invalid shard_prefix_chars={prefix_chars!r}"

    tokens = sorted(set(lexical_tokens(body)), key=lambda item: (-len(item), item))
    for token in tokens[:64]:
        key = builder.retrieval_key(token)
        shard_rel = f"{builder.search_shard_for_key(key, prefix_chars)}.json"
        shard_path = book_dir / "rag" / "search-index" / shard_rel
        if not shard_path.is_file():
            continue
        shard = json.loads(shard_path.read_text(encoding="utf-8"))

        exact = (shard.get("exact_terms") or {}).get(token)
        if isinstance(exact, dict) and exact.get("chunk_id") == record.get("chunk_id"):
            return True, f"exact term {token!r} -> {record.get('chunk_id')} via {shard_rel}"

        postings = (shard.get("keys") or {}).get(key) or []
        if any(
            isinstance(item, dict) and item.get("chunk_id") == record.get("chunk_id")
            for item in postings
        ):
            return True, f"key {key!r} contains {record.get('chunk_id')} via {shard_rel}"

    return False, f"sample chunk not resolvable through bounded lexical index: {record.get('chunk_id')}"


def validate_book(book_dir: Path) -> dict[str, Any]:
    book_dir = book_dir.resolve()
    book_id = book_dir.name
    checks: list[dict[str, Any]] = []

    source, source_format = builder.resolve_source(book_dir)
    source_rel = f"source/{source.name}"
    sha_record_path = book_dir / "source" / "SHA256"
    if not sha_record_path.is_file():
        raise ValueError(f"source checksum record missing: {sha_record_path}")
    recorded_sha = read_sha_record(sha_record_path)
    actual_sha = sha256_file(source)
    check(checks, "source_hash_matches", actual_sha == recorded_sha, {
        "recorded": recorded_sha,
        "actual": actual_sha,
    })

    manifest_path = book_dir / "rag" / "manifest.yaml"
    manifest = read_yaml(manifest_path)
    manifest_source = manifest.get("source") or {}
    check(checks, "manifest_book_id_matches", manifest.get("book_id") == book_id, manifest.get("book_id"))
    check(
        checks,
        "manifest_source_matches",
        manifest_source.get("path") == source_rel
        and manifest_source.get("format") == source_format
        and str(manifest_source.get("sha256", "")).lower() == actual_sha,
        manifest_source,
    )

    ingestion = manifest.get("ingestion") or {}
    generation = manifest.get("generation") or {}
    extraction = manifest.get("extraction") or {}
    chunking = manifest.get("chunking") or {}
    retrieval = manifest.get("retrieval") or {}

    required_ingestion = {
        "pipeline_version": builder.PIPELINE_VERSION,
        "normalization_policy_id": builder.NORMALIZATION_POLICY_ID,
        "chunking_policy_id": builder.CHUNKING_POLICY_ID,
        "retrieval_policy_id": builder.RETRIEVAL_POLICY_ID,
    }
    check(
        checks,
        "generation_metadata_present",
        all(ingestion.get(k) == v for k, v in required_ingestion.items())
        and bool(generation.get("corpus_generation_id"))
        and bool(generation.get("index_generation_id")),
        {"ingestion": ingestion, "generation": generation},
    )

    corpus_payload = {
        "pipeline_version": builder.PIPELINE_VERSION,
        "source_sha256": actual_sha,
        "source_format": source_format,
        "extractor_engine": extraction.get("engine"),
        "extractor_version": extraction.get("engine_version"),
        "unit_coordinate_system": extraction.get("unit_coordinate_system"),
        "content_model": extraction.get("content_model"),
        "normalization_policy_id": builder.NORMALIZATION_POLICY_ID,
        "chunking_policy_id": builder.CHUNKING_POLICY_ID,
        "target_chars": chunking.get("target_chars"),
        "overlap_chars": chunking.get("overlap_chars"),
        "repeated_pdf_boilerplate": {
            "min_units": builder.REPEATED_PDF_BOILERPLATE_MIN_UNITS,
            "min_fraction": builder.REPEATED_PDF_BOILERPLATE_MIN_FRACTION,
            "max_line_chars": builder.REPEATED_PDF_BOILERPLATE_MAX_LINE_CHARS,
        },
    }
    expected_corpus_generation = builder.sha256_json(corpus_payload)
    expected_index_generation = builder.sha256_json(
        {
            "corpus_generation_id": expected_corpus_generation,
            "retrieval_policy_id": builder.RETRIEVAL_POLICY_ID,
            "retrieval_key_chars": builder.SEARCH_KEY_CHARS,
            "search_prefix_chars_min": builder.SEARCH_PREFIX_CHARS,
            "postings_per_key_max": builder.SEARCH_POSTINGS_MAX,
            "max_shard_bytes": builder.SEARCH_SHARD_MAX_BYTES,
            "top_k_max": builder.RETRIEVAL_TOP_K_MAX,
        }
    )
    check(
        checks,
        "generation_ids_recompute",
        generation.get("corpus_generation_id") == expected_corpus_generation
        and generation.get("index_generation_id") == expected_index_generation,
        {
            "corpus_expected": expected_corpus_generation,
            "corpus_actual": generation.get("corpus_generation_id"),
            "index_expected": expected_index_generation,
            "index_actual": generation.get("index_generation_id"),
        },
    )

    chunk_index_path = book_dir / "rag" / "chunk-index.jsonl"
    records = read_jsonl(chunk_index_path)
    ids = [str(item.get("chunk_id")) for item in records]
    uids = [str(item.get("chunk_uid")) for item in records]
    paths = [str(item.get("path")) for item in records]
    check(checks, "chunks_addressable_unique", len(ids) == len(set(ids)) and len(paths) == len(set(paths)), len(records))
    check(
        checks,
        "chunk_uids_unique",
        all(re.fullmatch(r"[0-9a-f]{64}", uid or "") for uid in uids)
        and len(uids) == len(set(uids)),
        len(uids),
    )

    all_chunks_ok = True
    failure: str | None = None
    units_with_chunks: set[int] = set()
    for record in records:
        try:
            if record.get("book_id") != book_id:
                raise ValueError(f"book_id mismatch for {record.get('chunk_id')}")
            if record.get("source_path") != source_rel or str(record.get("source_sha256", "")).lower() != actual_sha:
                raise ValueError(f"source provenance mismatch for {record.get('chunk_id')}")
            if record.get("chunking_policy_id") != builder.CHUNKING_POLICY_ID:
                raise ValueError(f"chunking policy mismatch for {record.get('chunk_id')}")

            rel_path = record.get("path")
            if not isinstance(rel_path, str):
                raise ValueError(f"path missing for {record.get('chunk_id')}")
            chunk_path = book_dir / rel_path
            meta, body = read_chunk(chunk_path)
            text_hash = sha256_text(body)
            expected_uid = builder.chunk_uid(
                source_sha=actual_sha,
                source_unit_type=str(record.get("source_unit_type")),
                source_locator=str(record.get("source_locator")),
                chunk_in_unit=int(record.get("chunk_in_unit")),
                chunk_text_sha256=text_hash,
            )
            required_equal = {
                "chunk_id": record.get("chunk_id"),
                "chunk_uid": expected_uid,
                "book_id": book_id,
                "source_format": source_format,
                "source_unit_type": record.get("source_unit_type"),
                "source_unit": record.get("source_unit"),
                "source_locator": str(record.get("source_locator")),
                "chunk_in_unit": record.get("chunk_in_unit"),
                "source_path": source_rel,
                "source_sha256": actual_sha,
                "chunk_path": rel_path,
                "chunking_policy_id": builder.CHUNKING_POLICY_ID,
                "text_sha256": text_hash,
            }
            for key, expected_value in required_equal.items():
                actual_value = meta.get(key)
                if key == "source_locator":
                    actual_value = str(actual_value)
                if actual_value != expected_value:
                    raise ValueError(
                        f"{record.get('chunk_id')} metadata mismatch {key}: "
                        f"{actual_value!r} != {expected_value!r}"
                    )
            if record.get("text_sha256") != text_hash:
                raise ValueError(f"text hash mismatch in chunk-index for {record.get('chunk_id')}")
            if record.get("chunk_uid") != expected_uid:
                raise ValueError(f"chunk_uid mismatch in chunk-index for {record.get('chunk_id')}")
            units_with_chunks.add(int(record.get("source_unit")))
        except Exception as exc:
            all_chunks_ok = False
            failure = str(exc)
            break
    check(checks, "all_chunk_provenance_and_hashes_resolve", all_chunks_ok, failure or f"{len(records)} chunks")

    source_count_key = "pdf_pages" if source_format == "pdf" else "epub_spine_items"
    source_unit_count = manifest_source.get(source_count_key)
    blank_units = set((manifest.get("statistics") or {}).get("blank_source_unit_numbers") or [])
    coverage_ok = isinstance(source_unit_count, int) and (
        units_with_chunks | {int(x) for x in blank_units}
    ) == set(range(1, source_unit_count + 1))
    check(
        checks,
        "source_unit_coverage_complete",
        coverage_ok,
        {
            "source_units": source_unit_count,
            "units_with_chunks": len(units_with_chunks),
            "blank_units": sorted(blank_units),
        },
    )

    stats = manifest.get("statistics") or {}
    check(
        checks,
        "manifest_chunk_counts_match",
        stats.get("chunks") == len(records)
        and stats.get("retrieval_chunk_files") == len(records),
        {"manifest": stats.get("chunks"), "actual": len(records)},
    )

    search_manifest_path = book_dir / "rag" / "search-index" / "manifest.json"
    search_manifest = json.loads(search_manifest_path.read_text(encoding="utf-8"))
    check(
        checks,
        "search_index_generation_matches",
        search_manifest.get("book_id") == book_id
        and search_manifest.get("retrieval_policy_id") == builder.RETRIEVAL_POLICY_ID
        and search_manifest.get("corpus_generation_id") == expected_corpus_generation
        and search_manifest.get("index_generation_id") == expected_index_generation,
        {
            "corpus_generation_id": search_manifest.get("corpus_generation_id"),
            "index_generation_id": search_manifest.get("index_generation_id"),
        },
    )

    sample_indices = sorted({0, len(records) // 2, len(records) - 1})
    sample_results = []
    samples_ok = True
    for index in sample_indices:
        ok, evidence = sample_retrieval_resolves(
            book_dir=book_dir,
            record=records[index],
            search_manifest=search_manifest,
        )
        sample_results.append({"chunk_id": records[index].get("chunk_id"), "ok": ok, "evidence": evidence})
        samples_ok = samples_ok and ok
    check(checks, "deterministic_retrieval_samples_pass", samples_ok, sample_results)

    synthetic = f"zzzzbibliotekavspunsupported{actual_sha[:8]}"
    prefix_chars = int((search_manifest.get("normalization") or {}).get("shard_prefix_chars", 3))
    synthetic_key = builder.retrieval_key(synthetic)
    synthetic_shard = book_dir / "rag" / "search-index" / f"{builder.search_shard_for_key(synthetic_key, prefix_chars)}.json"
    negative_ok = True
    negative_evidence = "synthetic shard absent"
    if synthetic_shard.is_file():
        shard = json.loads(synthetic_shard.read_text(encoding="utf-8"))
        negative_ok = synthetic not in (shard.get("exact_terms") or {})
        negative_evidence = f"exact_terms contains synthetic={not negative_ok}"
    check(checks, "negative_exact_term_behavior_pass", negative_ok, negative_evidence)

    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema": "biblioteka-vsp/rag-ingestion-acceptance/v1",
        "book_id": book_id,
        "status": "ACCEPTED" if not failed else "REJECTED",
        "source_sha256": actual_sha,
        "corpus_generation_id": generation.get("corpus_generation_id"),
        "index_generation_id": generation.get("index_generation_id"),
        "checks": checks,
        "failed_checks": [item["id"] for item in failed],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-dir", required=True)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    book_dir = Path(args.book_dir)
    try:
        result = validate_book(book_dir)
    except Exception as exc:
        result = {
            "schema": "biblioteka-vsp/rag-ingestion-acceptance/v1",
            "book_id": book_dir.name,
            "status": "ERROR",
            "error": str(exc),
        }

    output = yaml.safe_dump(result, allow_unicode=True, sort_keys=False)
    print(output, end="")

    if args.write_result:
        rag_dir = book_dir / "rag"
        rag_dir.mkdir(parents=True, exist_ok=True)
        (rag_dir / "acceptance.yaml").write_text(output, encoding="utf-8")

    return 0 if result.get("status") == "ACCEPTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
