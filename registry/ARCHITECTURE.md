# Registry architecture v2

Status: accepted. This is the canonical registry architecture for `main` as of 2026-10-08.

## Canonical sources

| State | Canonical source |
|---|---|
| Inventory, holdings, bibliographic registry data, electronic-copy mapping | `registry/books.yaml` |
| Knowledge lifecycle membership | `books/index.yaml` |
| Knowledge-project completion | `books/index.yaml: project_status` |
| Reading state | `books/<knowledge-id>/reading/progress.yaml` |
| RAG state | `books/<knowledge-id>/rag/manifest.yaml` |
| Study/extract coverage | Derived from substantive artifacts under `books/<knowledge-id>/notes/` |
| Human-readable registry view | `registry/README.md` (generated, non-canonical) |

`registry/reestr_knig_0046.xlsx` remains the historical source snapshot. It is not rewritten by schema v2 tooling and may contain items later excluded from the canonical technical/professional inventory (for example, hobby acquisitions). `registry/books.yaml` is authoritative for current registry membership.

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

## Project, reading, RAG and study-artifact state

Schema v2 stores no duplicated reading/RAG/study-artifact status in
`registry/books.yaml`.

The generated README derives:

- reading from `reading_progress`;
- RAG from `rag_manifest`;
- study/extract coverage from substantive files under the linked `notes/` path;
- the `Выжимки` link from an existing chapter index (or chapter directory if its index is missing), book synthesis index, or substantive extract file; no link is shown when no extract exists;
- project completion from `books/index.yaml: project_status`.

`project_status: completed` is a user-confirmed workflow fact and is separate
from reading completion. For the 2026-10-08 migration audit, completion is
grounded in the user's explicit rule that book-chat titles marked with `+`
are completed at the current processing stage. These entries retain
`project_status_evidence: user_chat_plus` and a confirmation date.

A knowledge entry may legitimately exist without RAG or study artifacts.
However, a project marked completed while its expected artifacts are absent
from `main` is surfaced in the generated `Migration gaps` view. The gap is
not silently repaired or treated as proof that historical chat work never
existed.

Chapter-analysis readiness is a separate computed capability. A reading-only
knowledge entry is valid but is not eligible for RAG-dependent chapter analysis
until the book-level onboarding/readiness contract passes. Readiness is not
persisted in `registry/books.yaml`; see `docs/BOOK-LIFECYCLE.md`,
`templates/book-readiness-v1.3.yaml`, and
`templates/chapter-artifact-collection-v1.7.yaml`.

## Taxonomy

`direction` remains display-only. Schema v2 permits optional normalized `domains`, `topics`, and `level`. Migration is incremental.

## Generated README

```bash
python scripts/generate_registry_readme.py
python scripts/generate_registry_readme.py --check
```

`registry/README.md` is generated and non-canonical. Manual status or link edits are overwritten/detected as stale. When book notes are published, regenerate and commit the registry in the same branch; the registry validation workflow checks this for changes under `books/**/notes/**`.

### Full registry table invariant

The `## Реестр книг` table MUST always contain every inventory record from
`registry/books.yaml` exactly as represented by the canonical inventory set.
Derived views such as `Сейчас читаю`, `Прочитано`, `Нужен PDF`, RAG-related
views, or any future filtered section MAY duplicate inventory entries, but MUST
NOT remove or relocate them out of the full registry table.

Generation MUST fail if `len(registry.books) != registry.scope.book_count`.

## Validation

```bash
python -m pip install PyYAML jsonschema
python scripts/validate_registry.py
```

The validator checks schema conformance, inventory uniqueness/count, source snapshot SHA-256/size, electronic-holdings summary counters/references, inventory/holding knowledge mappings, per-book reading/RAG references, project-completion provenance, and forbids the legacy duplicated `reading_rag_status` block.

## Rollback

Promotion rollback point: `098d02443d022c078b8ba78bd646fb4979b5b688` (pre-v2 `main`). Optional `knowledge_id` fields can be removed without changing inventory numbers. CI/generator tooling can be disabled independently without mutating inventory numbers.
