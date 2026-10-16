#!/usr/bin/env python3
"""Compute capability-specific readiness for biblioteka-vsp books."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "books" / "index.yaml"
CHAPTER_TEMPLATE = ROOT / "templates" / "chapter-artifact-collection-v1.8.yaml"

READY_RE = re.compile(r"^READY")
TOKEN_RE = re.compile(r"[0-9a-zа-я]+", flags=re.IGNORECASE)
SUPPORTED_SOURCE_NAMES = {"book.pdf", "book.epub"}

NEXT_ACTIONS = {
    "BOOK_NOT_REGISTERED": "register the book in books/index.yaml",
    "METADATA_MISSING": "create and declare books/<book_id>/metadata.yaml",
    "METADATA_ID_MISMATCH": "make metadata.yaml id match book_id",
    "CANONICAL_SOURCE_MISSING": "ingest and declare books/<book_id>/source/book.pdf or books/<book_id>/source/book.epub",
    "SOURCE_CHECKSUM_RECORD_MISSING": "create source/SHA256 for the canonical source",
    "SOURCE_PROVENANCE_INCOMPLETE": "make metadata expected_sha256, source/SHA256 and RAG source.sha256 consistent",
    "RAG_MANIFEST_MISSING": "build full-book RAG on an ingest branch",
    "RAG_ID_MISMATCH": "rebuild/fix RAG so manifest book_id matches the book",
    "RAG_SOURCE_MISMATCH": "rebuild/fix RAG so manifest source path and checksum match the canonical source",
    "RAG_VALIDATION_NOT_READY": "resolve RAG validation failures and rebuild if required",
    "RAG_INGESTION_ACCEPTANCE_FAILED": "run/fix strict RAG ingestion acceptance for the current generation",
    "CHUNK_INDEX_MISSING": "generate rag/chunk-index.jsonl",
    "ADDRESSABLE_CHUNKS_MISSING": "generate addressable rag/chunks files",
    "RETRIEVAL_INDEX_MISSING": "generate rag/search-index including manifest.json",
    "RETRIEVAL_INTEGRITY_FAILED": "repair/rebuild deterministic retrieval artifacts and rerun the smoke test",
    "CHAPTER_TEMPLATE_MISSING": "install an ACCEPTED BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.8 template",
}


class RepositoryError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RepositoryError(f"cannot parse YAML {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise RepositoryError(f"YAML root is not a mapping: {path.relative_to(ROOT)}")
    return data


def result_check(
    check_id: str,
    ok: bool,
    expected: Any,
    actual: Any,
    evidence: str,
    reason_code: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "id": check_id,
        "status": "PASS" if ok else "FAIL",
        "expected": expected,
        "actual": actual,
        "evidence": evidence,
    }
    if not ok and reason_code:
        item["reason_code"] = reason_code
        item["next_action"] = NEXT_ACTIONS[reason_code]
    return item


def read_sha_record(path: Path) -> str | None:
    if not path.is_file():
        return None
    parts = path.read_text(encoding="utf-8").strip().split()
    if not parts or not re.fullmatch(r"[0-9a-fA-F]{64}", parts[0]):
        raise RepositoryError(f"invalid SHA256 record: {path.relative_to(ROOT)}")
    return parts[0].lower()


def normalize_token(token: str) -> str:
    return token.lower().replace("ё", "е")


def lexical_tokens(text: str) -> list[str]:
    return [
        normalize_token(token)
        for token in TOKEN_RE.findall(text.lower().replace("ё", "е"))
        if 4 <= len(token) <= 64
    ]


def retrieval_key(token: str) -> str:
    token = normalize_token(token)
    return token if len(token) <= 4 else token[:4]


def search_shard_for_key(key: str, prefix_chars: int) -> str:
    return f"_short/{key}" if len(key) < prefix_chars else key[:prefix_chars]


def read_chunk(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise RepositoryError(f"chunk front matter missing: {path.relative_to(ROOT)}")
    try:
        _, front, body = text.split("---\n", 2)
    except ValueError as exc:
        raise RepositoryError(f"chunk front matter malformed: {path.relative_to(ROOT)}") from exc
    meta = yaml.safe_load(front)
    if not isinstance(meta, dict):
        raise RepositoryError(f"chunk metadata malformed: {path.relative_to(ROOT)}")
    return meta, body


def load_chunk_index(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    line_number = 0
    try:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError("record is not an object")
            records.append(record)
    except Exception as exc:
        raise RepositoryError(
            f"invalid chunk index {path.relative_to(ROOT)}: line {line_number}: {exc}"
        ) from exc
    if not records:
        raise RepositoryError(f"empty chunk index: {path.relative_to(ROOT)}")
    return records


def source_locator(record: dict[str, Any]) -> tuple[str, Any, str] | None:
    unit_type = record.get("source_unit_type")
    unit = record.get("source_unit")
    locator = record.get("source_locator")
    if unit_type is not None and unit is not None and locator is not None:
        return str(unit_type), unit, str(locator)
    pdf_page = record.get("pdf_page")
    if pdf_page is not None:
        return "pdf_page", pdf_page, str(pdf_page)
    return None


def retrieval_integrity_smoke_test(
    *,
    book_dir: Path,
    book_id: str,
    chunk_index_path: Path,
    search_index_dir: Path,
    expected_source_path: str,
    expected_source_sha: str,
    search_prefix_chars: int,
) -> tuple[bool, str]:
    records = load_chunk_index(chunk_index_path)
    by_id = {str(record.get("chunk_id")): record for record in records}

    seed = records[0]
    seed_path_value = seed.get("path")
    if not isinstance(seed_path_value, str):
        return False, "first chunk-index record has no path"
    seed_path = book_dir / seed_path_value
    if not seed_path.is_file():
        return False, f"seed chunk missing: {seed_path_value}"

    _, seed_body = read_chunk(seed_path)
    tokens = list(dict.fromkeys(lexical_tokens(seed_body)))
    if not tokens:
        return False, "seed chunk has no deterministic informative token"

    for token in tokens:
        key = retrieval_key(token)
        shard_rel = f"{search_shard_for_key(key, search_prefix_chars)}.json"
        shard_path = search_index_dir / shard_rel
        if not shard_path.is_file():
            continue
        try:
            shard = json.loads(shard_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise RepositoryError(
                f"invalid search shard {shard_path.relative_to(ROOT)}: {exc}"
            ) from exc

        posting = (shard.get("exact_terms") or {}).get(token)
        if not isinstance(posting, dict):
            continue
        chunk_id = str(posting.get("chunk_id"))
        indexed = by_id.get(chunk_id)
        if not indexed:
            return False, f"search posting references unknown chunk_id {chunk_id}"
        rel_path = posting.get("path")
        if not isinstance(rel_path, str) or rel_path != indexed.get("path"):
            return False, f"path mismatch for {chunk_id}"
        chunk_path = book_dir / rel_path
        if not chunk_path.is_file():
            return False, f"retrieved chunk missing: {rel_path}"

        meta, body = read_chunk(chunk_path)
        locators = [source_locator(meta), source_locator(posting), source_locator(indexed)]
        locator_ok = all(locator is not None for locator in locators) and len(set(locators)) == 1
        checks = {
            "book_id": meta.get("book_id") == book_id,
            "chunk_id": meta.get("chunk_id") == chunk_id,
            "source_locator": locator_ok,
            "source_path": meta.get("source_path") == indexed.get("source_path") == expected_source_path,
            "source_sha256": (
                str(meta.get("source_sha256", "")).lower()
                == str(indexed.get("source_sha256", "")).lower()
                == expected_source_sha
            ),
            "token": token in lexical_tokens(body),
        }
        if not all(checks.values()):
            failed = ",".join(name for name, ok in checks.items() if not ok)
            return False, f"retrieved chunk provenance mismatch: {failed}"
        return True, f"token={token} shard={shard_rel} chunk={chunk_id} locator={locators[0]}"

    return False, "no seed token resolved through exact_terms in deterministic search index"


def build_output(book_id: str, checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema": "biblioteka-vsp/readiness-result/v1",
        "book_id": book_id,
        "capability": "chapter-analysis",
        "status": "READY" if not failed else "BLOCKED",
        "checks": checks,
        "failed_checks": [
            {
                key: item[key]
                for key in ("id", "reason_code", "expected", "actual", "evidence", "next_action")
                if key in item
            }
            for item in failed
        ],
    }


def compute_readiness(book_id: str) -> dict[str, Any]:
    if not INDEX.is_file():
        raise RepositoryError("books/index.yaml is missing")
    index = load_yaml(INDEX)
    books = index.get("books") or []
    matches = [book for book in books if isinstance(book, dict) and book.get("id") == book_id]
    if len(matches) > 1:
        raise RepositoryError(f"duplicate book id in books/index.yaml: {book_id}")

    checks: list[dict[str, Any]] = [
        result_check("book_id_resolved", bool(book_id), True, bool(book_id), "CLI --book-id"),
    ]
    if not matches:
        checks.append(result_check("knowledge_registered", False, True, False, "books/index.yaml", "BOOK_NOT_REGISTERED"))
        return build_output(book_id, checks)

    book = matches[0]
    paths = book.get("paths") or {}
    if not isinstance(paths, dict):
        raise RepositoryError(f"paths is not a mapping for {book_id}")
    checks.append(result_check("knowledge_registered", True, True, True, "books/index.yaml"))
    book_dir = ROOT / "books" / book_id

    metadata_rel = paths.get("metadata")
    metadata_path = ROOT / metadata_rel if isinstance(metadata_rel, str) else None
    metadata_exists = bool(metadata_path and metadata_path.is_file())
    checks.append(result_check(
        "metadata_exists", metadata_exists, True, metadata_exists,
        str(metadata_rel or "[undeclared]"), None if metadata_exists else "METADATA_MISSING",
    ))
    metadata: dict[str, Any] = load_yaml(metadata_path) if metadata_exists and metadata_path else {}
    metadata_id_ok = metadata_exists and metadata.get("id") == book_id
    checks.append(result_check(
        "metadata_id_matches", metadata_id_ok, book_id, metadata.get("id"),
        str(metadata_rel or "[undeclared]"), None if metadata_id_ok else "METADATA_ID_MISMATCH",
    ))

    source_rel = paths.get("source")
    source_path = ROOT / source_rel if isinstance(source_rel, str) else None
    canonical_name_ok = bool(
        source_path
        and source_path.parent == book_dir / "source"
        and source_path.name in SUPPORTED_SOURCE_NAMES
    )
    canonical_source_exists = bool(canonical_name_ok and source_path and source_path.is_file())
    checks.append(result_check(
        "canonical_source_exists", canonical_source_exists,
        "declared source/book.pdf or source/book.epub exists",
        {"declared": source_rel, "exists": bool(source_path and source_path.is_file()), "supported_name": canonical_name_ok},
        str(source_rel or "[undeclared]"), None if canonical_source_exists else "CANONICAL_SOURCE_MISSING",
    ))

    sha_path = source_path.parent / "SHA256" if source_path else book_dir / "source" / "SHA256"
    source_sha = read_sha_record(sha_path) if sha_path.is_file() else None
    checks.append(result_check(
        "source_checksum_record_exists", source_sha is not None, True, source_sha is not None,
        str(sha_path.relative_to(ROOT)), None if source_sha is not None else "SOURCE_CHECKSUM_RECORD_MISSING",
    ))

    metadata_source = metadata.get("source") or {}
    metadata_sha = metadata_source.get("expected_sha256") if isinstance(metadata_source, dict) else None
    metadata_sha = str(metadata_sha).lower() if metadata_sha else None
    metadata_sha_ok = bool(metadata_sha and re.fullmatch(r"[0-9a-f]{64}", metadata_sha))
    checks.append(result_check(
        "metadata_expected_sha256_exists", metadata_sha_ok, "64-char lowercase SHA-256",
        metadata_sha or "[missing]", str(metadata_rel or "[undeclared]"),
        None if metadata_sha_ok else "SOURCE_PROVENANCE_INCOMPLETE",
    ))

    manifest_rel = paths.get("rag_manifest")
    manifest_path = ROOT / manifest_rel if isinstance(manifest_rel, str) else None
    manifest_exists = bool(manifest_path and manifest_path.is_file())
    checks.append(result_check(
        "rag_manifest_exists", manifest_exists, True, manifest_exists,
        str(manifest_rel or "[undeclared]"), None if manifest_exists else "RAG_MANIFEST_MISSING",
    ))
    manifest: dict[str, Any] = load_yaml(manifest_path) if manifest_exists and manifest_path else {}
    manifest_id_ok = manifest_exists and manifest.get("book_id") == book_id
    checks.append(result_check(
        "rag_manifest_book_id_matches", manifest_id_ok, book_id, manifest.get("book_id"),
        str(manifest_rel or "[undeclared]"), None if manifest_id_ok else "RAG_ID_MISMATCH",
    ))

    manifest_source = manifest.get("source") or {}
    if not isinstance(manifest_source, dict):
        manifest_source = {}
    manifest_sha = str(manifest_source.get("sha256", "")).lower() or None
    expected_manifest_source_path = (
        source_path.relative_to(book_dir).as_posix()
        if source_path and source_path.is_relative_to(book_dir)
        else str(Path("source") / (source_path.name if source_path else "book.[pdf|epub]"))
    )
    manifest_source_ok = bool(
        manifest_exists
        and manifest_source.get("path") == expected_manifest_source_path
        and source_sha
        and manifest_sha == source_sha
    )
    checks.append(result_check(
        "rag_manifest_source_matches", manifest_source_ok,
        {"path": expected_manifest_source_path, "sha256": source_sha},
        {"path": manifest_source.get("path"), "sha256": manifest_sha},
        str(manifest_rel or "[undeclared]"), None if manifest_source_ok else "RAG_SOURCE_MISMATCH",
    ))

    provenance_ok = bool(source_sha and metadata_sha_ok and manifest_sha and source_sha == metadata_sha == manifest_sha)
    checks.append(result_check(
        "source_provenance_consistent", provenance_ok,
        "source/SHA256 == metadata expected_sha256 == RAG source.sha256",
        provenance_ok, "source/SHA256 + metadata.yaml + rag/manifest.yaml",
        None if provenance_ok else "SOURCE_PROVENANCE_INCOMPLETE",
    ))

    validation = manifest.get("validation") or {}
    validation_status = validation.get("status") if isinstance(validation, dict) else None
    rag_ready = bool(isinstance(validation_status, str) and READY_RE.match(validation_status))
    checks.append(result_check(
        "rag_validation_ready", rag_ready, "^READY", validation_status,
        str(manifest_rel or "[undeclared]"), None if rag_ready else "RAG_VALIDATION_NOT_READY",
    ))

    generation = manifest.get("generation") or {}
    if not isinstance(generation, dict):
        generation = {}
    corpus_generation_id = generation.get("corpus_generation_id")
    index_generation_id = generation.get("index_generation_id")
    generation_aware = bool(corpus_generation_id or index_generation_id)
    acceptance_path = book_dir / "rag" / "acceptance.yaml"
    acceptance_ok = True
    acceptance_evidence: Any = "legacy RAG compatibility path; strict acceptance applies on next rebuild"
    if generation_aware:
        acceptance_ok = False
        acceptance_evidence = str(acceptance_path.relative_to(ROOT))
        if acceptance_path.is_file() and corpus_generation_id and index_generation_id and source_sha:
            acceptance = load_yaml(acceptance_path)
            acceptance_ok = bool(
                acceptance.get("status") == "ACCEPTED"
                and acceptance.get("book_id") == book_id
                and str(acceptance.get("source_sha256", "")).lower() == source_sha
                and acceptance.get("corpus_generation_id") == corpus_generation_id
                and acceptance.get("index_generation_id") == index_generation_id
            )
            acceptance_evidence = {
                "path": str(acceptance_path.relative_to(ROOT)),
                "status": acceptance.get("status"),
                "source_sha256": acceptance.get("source_sha256"),
                "corpus_generation_id": acceptance.get("corpus_generation_id"),
                "index_generation_id": acceptance.get("index_generation_id"),
            }
    checks.append(result_check(
        "rag_ingestion_acceptance_passed", acceptance_ok,
        "ACCEPTED for current source/corpus/index generation, or legacy compatibility",
        acceptance_evidence,
        str(acceptance_path.relative_to(ROOT)),
        None if acceptance_ok else "RAG_INGESTION_ACCEPTANCE_FAILED",
    ))

    chunk_index_rel = paths.get("rag_chunk_index")
    chunk_index_path = ROOT / chunk_index_rel if isinstance(chunk_index_rel, str) else None
    chunk_index_exists = bool(chunk_index_path and chunk_index_path.is_file())
    checks.append(result_check(
        "chunk_index_exists", chunk_index_exists, True, chunk_index_exists,
        str(chunk_index_rel or "[undeclared]"), None if chunk_index_exists else "CHUNK_INDEX_MISSING",
    ))

    chunks_rel = paths.get("rag_chunks")
    chunks_path = ROOT / chunks_rel if isinstance(chunks_rel, str) else None
    chunks_exist = bool(chunks_path and chunks_path.is_dir() and any(chunks_path.rglob("*.md")))
    checks.append(result_check(
        "addressable_chunks_exist", chunks_exist, True, chunks_exist,
        str(chunks_rel or "[undeclared]"), None if chunks_exist else "ADDRESSABLE_CHUNKS_MISSING",
    ))

    search_rel = paths.get("rag_search_index")
    search_dir = ROOT / search_rel if isinstance(search_rel, str) else None
    search_manifest = search_dir / "manifest.json" if search_dir else None
    search_exists = bool(search_manifest and search_manifest.is_file())
    checks.append(result_check(
        "retrieval_index_manifest_exists", search_exists, True, search_exists,
        str((Path(search_rel) / "manifest.json") if isinstance(search_rel, str) else "[undeclared]"),
        None if search_exists else "RETRIEVAL_INDEX_MISSING",
    ))

    search_prefix_chars: int | None = None
    if search_exists and search_manifest:
        try:
            search_manifest_data = json.loads(search_manifest.read_text(encoding="utf-8"))
        except Exception as exc:
            raise RepositoryError(
                f"invalid search index manifest {search_manifest.relative_to(ROOT)}: {exc}"
            ) from exc
        normalization = search_manifest_data.get("normalization") or {}
        prefix_value = normalization.get("shard_prefix_chars") if isinstance(normalization, dict) else None
        if prefix_value is None:
            # Backward compatibility: v1 and early synthetic/test manifests predate
            # explicit shard_prefix_chars and used the repository-wide 3-char routing rule.
            search_prefix_chars = 3
        elif isinstance(prefix_value, int) and 1 <= prefix_value <= 4:
            search_prefix_chars = prefix_value
        else:
            raise RepositoryError(
                f"invalid shard_prefix_chars in {search_manifest.relative_to(ROOT)}: {prefix_value!r}"
            )

    smoke_ok = False
    smoke_evidence = "prerequisites missing"
    if (
        chunk_index_exists and chunks_exist and search_exists and source_sha
        and search_dir and chunk_index_path and canonical_source_exists
        and search_prefix_chars is not None
    ):
        smoke_ok, smoke_evidence = retrieval_integrity_smoke_test(
            book_dir=book_dir,
            book_id=book_id,
            chunk_index_path=chunk_index_path,
            search_index_dir=search_dir,
            expected_source_path=expected_manifest_source_path,
            expected_source_sha=source_sha,
            search_prefix_chars=search_prefix_chars,
        )
    checks.append(result_check(
        "retrieval_integrity_smoke_test_passed", smoke_ok, True, smoke_ok,
        smoke_evidence, None if smoke_ok else "RETRIEVAL_INTEGRITY_FAILED",
    ))

    chapter_template_ok = False
    template_evidence = str(CHAPTER_TEMPLATE.relative_to(ROOT))
    if CHAPTER_TEMPLATE.is_file():
        template_doc = load_yaml(CHAPTER_TEMPLATE)
        template = template_doc.get("template") or {}
        chapter_template_ok = bool(
            isinstance(template, dict)
            and template.get("id") == "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION"
            and str(template.get("version")) == "1.8"
            and template.get("status") == "ACCEPTED"
        )
    checks.append(result_check(
        "chapter_template_available", chapter_template_ok, "ACCEPTED v1.8",
        chapter_template_ok, template_evidence,
        None if chapter_template_ok else "CHAPTER_TEMPLATE_MISSING",
    ))

    return build_output(book_id, checks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", required=True)
    parser.add_argument("--capability", default="chapter-analysis")
    args = parser.parse_args()
    if args.capability != "chapter-analysis":
        print(yaml.safe_dump({
            "schema": "biblioteka-vsp/readiness-result/v1",
            "book_id": args.book_id,
            "capability": args.capability,
            "status": "ERROR",
            "error": "unsupported capability",
        }, allow_unicode=True, sort_keys=False), end="")
        return 2
    try:
        output = compute_readiness(args.book_id)
    except RepositoryError as exc:
        print(yaml.safe_dump({
            "schema": "biblioteka-vsp/readiness-result/v1",
            "book_id": args.book_id,
            "capability": args.capability,
            "status": "ERROR",
            "error": str(exc),
        }, allow_unicode=True, sort_keys=False), end="")
        return 2
    print(yaml.safe_dump(output, allow_unicode=True, sort_keys=False), end="")
    return 0 if output["status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
