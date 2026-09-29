# Book lifecycle and chapter readiness

Status: accepted for biblioteka-vsp.

This document separates inventory, reading, source ingest, RAG, retrieval and
chapter-analysis capabilities. These states are intentionally independent.

## Capability matrix

| Capability | Canonical evidence | Implies chapter analysis? |
|---|---|---|
| Inventory registered | `registry/books.yaml` | No |
| Electronic holding known | `registry/books.yaml` holding mapping | No |
| Knowledge registered | `books/index.yaml` | No |
| Reading active | `books/<id>/reading/progress.yaml` | No |
| Metadata ready | declared `metadata.yaml` exists and matches book_id | No |
| Canonical source ready | declared `source/book.pdf` exists | No |
| Source provenance verified | `source/SHA256`, metadata expected SHA and RAG source SHA agree | No |
| RAG ready | manifest exists and `validation.status` starts with `READY` | No |
| Retrieval ready | addressable chunks + deterministic search index + integrity smoke test | No |
| Chapter analysis ready | all book-level RAG prerequisites + accepted chapter template | Yes |

There is no single persisted global READY flag. Chapter readiness is computed.

## User-intent matrix

| User intent | Inventory | Reading | Full RAG onboarding |
|---|:---:|:---:|:---:|
| "Добавь книгу в реестр" | Yes | No | No |
| "Начинаю читать" | as applicable | Yes | No |
| "Ветка новой книги для RAG и шпор" | as applicable | as applicable | Yes |
| "Будем разбирать главы как Немет" | as applicable | as applicable | Yes |
| "Анализ главы N" | unchanged | unchanged | Must already be READY; otherwise onboarding/blocker first |

A supplied PDF is not by itself equal to canonical repository ingest.

## Contracts

One-time book preparation:

```text
BIBLIOTEKA-VSP-BOOK-ONBOARDING v1.0
    ↓
canonical source + provenance
    ↓
full-book RAG
    ↓
retrieval integrity
```

Read-only gate:

```text
BIBLIOTEKA-VSP-BOOK-READINESS v1.0
    ↓ READY
BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.4
```

The accepted v1.3 chapter template remains immutable for reproducibility.
v1.4 adds only the mandatory book-readiness precondition.

## Reading-only books

Reading-only knowledge entries remain valid. They may have:

```text
knowledge_registered = true
reading_active = true
rag_ready = false
chapter_analysis_ready = false
```

This is a valid lifecycle state, not an error.

## Failure model

Readiness uses only:

- `READY`
- `BLOCKED`
- `ERROR` for malformed repository/configuration or unsupported invocation.

Specific blockers are reason codes rather than additional top-level states, for
example:

- `CANONICAL_SOURCE_MISSING`
- `RAG_MANIFEST_MISSING`
- `RAG_VALIDATION_NOT_READY`
- `RETRIEVAL_INTEGRITY_FAILED`

## Readiness check

```bash
python scripts/check_book_readiness.py \
  --book-id <book_id> \
  --capability chapter-analysis
```

Exit codes:

- `0` — READY
- `1` — BLOCKED
- `2` — malformed repository/configuration or unsupported invocation

The retrieval smoke test validates deterministic retrieval plumbing and
provenance consistency. It is not a semantic-quality benchmark.

## New-book flow

```text
Inventory / reading
        ↓
capability preflight
        ↓
BOOK-ONBOARDING v1.0 when RAG-dependent work is requested
        ↓
canonical source + SHA provenance
        ↓
full-book RAG
        ↓
retrieval integrity test
        ↓
BOOK-READINESS v1.0
        ↓
READY
        ↓
Chapter loop v1.4
        ↓
"Анализ главы N"
```

## Git discipline

Book source ingest and generated RAG use a non-main ingest branch.
The RAG workflow writes generated artifacts back to that branch.
Merge only after readiness succeeds. Never force-push or silently replace
`source/book.pdf`.
