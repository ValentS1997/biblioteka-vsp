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

## Inventory -> knowledge foreign key

`registry/books.yaml` may contain optional `knowledge_id`.

Rules:
1. `knowledge_id` MUST reference an `id` in `books/index.yaml`.
2. One `knowledge_id` MUST NOT map to multiple inventory records.
3. Missing `knowledge_id` means the inventory record is not in the knowledge lifecycle.
4. Filesystem paths are owned by `books/index.yaml`, not stored as registry foreign keys.

## Reading and RAG state

Schema v2 stores no reading/RAG status in `registry/books.yaml`.

The generated README derives reading from `reading_progress` and RAG from `rag_manifest` in the linked `books/index.yaml` entry. A knowledge entry may exist without RAG.

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

The validator checks schema conformance, inventory uniqueness/count, holding references, knowledge mappings, per-book reading/RAG references, and forbids the legacy duplicated `reading_rag_status` block.

## Rollback

Promotion rollback point: `098d02443d022c078b8ba78bd646fb4979b5b688` (pre-v2 `main`). Optional `knowledge_id` fields can be removed without changing inventory numbers. CI/generator tooling can be disabled independently without mutating inventory numbers.
