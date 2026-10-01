# Registry architecture v2

Status: accepted. This is the canonical registry architecture for `main` as of 2026-09-24.

## Canonical sources

| State | Canonical source |
|---|---|
| Inventory, holdings, bibliographic registry data, electronic-copy mapping | `registry/books.yaml` |
| Knowledge lifecycle membership | `books/index.yaml` |
| Reading state | `books/<knowledge-id>/reading/progress.yaml` |
| RAG state | `books/<knowledge-id>/rag/manifest.yaml` |
| Human-readable registry view | `registry/README.md` (generated, non-canonical) |

`registry/reestr_knig_0046.xlsx` remains the source snapshot. It is not rewritten by schema v2 tooling.

## Registry -> knowledge foreign keys

Inventory records in `registry/books.yaml` may contain optional `knowledge_id`.

Rules:
1. Inventory `knowledge_id` MUST reference an `id` in `books/index.yaml`.
2. One inventory `knowledge_id` MUST NOT map to multiple inventory records.
3. Missing inventory `knowledge_id` means that inventory record is not in the knowledge lifecycle.
4. Filesystem paths are owned by `books/index.yaml`, not stored as registry foreign keys.

Electronic holdings may also contain optional `knowledge_id`. This is primarily
used when a verified electronic book is in the knowledge lifecycle but has no
physical/private inventory number. `match_status: unregistered` therefore means
"outside inventory", not "absent from books/index.yaml".

A holding-level `knowledge_id` MUST reference `books/index.yaml`. If both an
inventory reference and a holding-level `knowledge_id` exist, they must not
contradict the inventory→knowledge mapping.

## Reading and RAG state

Schema v2 stores no reading/RAG status in `registry/books.yaml`.

The generated README derives reading from `reading_progress` and RAG from `rag_manifest` in the linked `books/index.yaml` entry. A knowledge entry may exist without RAG.

Chapter-analysis readiness is a separate computed capability. A reading-only knowledge entry is valid but is not eligible for RAG-dependent chapter analysis until the book-level onboarding/readiness contract passes. Readiness is not persisted in `registry/books.yaml`; see `docs/BOOK-LIFECYCLE.md`, `templates/book-readiness-v1.2.yaml`, and `templates/chapter-artifact-collection-v1.6.yaml`.

## Taxonomy

`direction` remains display-only. Schema v2 permits optional normalized `domains`, `topics`, and `level`. Migration is incremental.

## Generated README

```bash
python scripts/generate_registry_readme.py
python scripts/generate_registry_readme.py --check
```

`registry/README.md` is generated and non-canonical. Manual status edits are overwritten/detected as stale.

## Validation

```bash
python -m pip install PyYAML jsonschema
python scripts/validate_registry.py
```

The validator checks schema conformance, inventory uniqueness/count, source snapshot SHA-256/size, electronic-holdings summary counters/references, inventory/holding knowledge mappings, per-book reading/RAG references, and forbids the legacy duplicated `reading_rag_status` block.

## Rollback

Promotion rollback point: `098d02443d022c078b8ba78bd646fb4979b5b688` (pre-v2 `main`). Optional `knowledge_id` fields can be removed without changing inventory numbers. CI/generator tooling can be disabled independently without mutating inventory numbers.
