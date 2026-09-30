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
| Canonical source ready | declared `source/book.pdf` or `source/book.epub` exists | No |
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

A supplied PDF or EPUB is not by itself equal to canonical repository ingest.

## Canonical entrypoints

New RAG/chapter book branch:

```text
BIBLIOTEKA-VSP-BOOK-BRANCH-BOOTSTRAP v1.2
```

Normal chapter command:

```text
"Анализ главы N"
  ↓
BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.1
```

The entrypoint templates orchestrate the contracts below; they do not duplicate
book/RAG/chapter implementation logic.

## Contracts

One-time book preparation:

```text
BIBLIOTEKA-VSP-BOOK-ONBOARDING v1.2
    ↓
canonical source + provenance
    ↓
full-book RAG
    ↓
retrieval integrity
```

Read-only gate:

```text
BIBLIOTEKA-VSP-BOOK-READINESS v1.2
    ↓ READY
BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.6
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
BOOK-BRANCH-BOOTSTRAP v1.0
        ↓
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
"Анализ главы N"
        ↓
CHAPTER-ANALYSIS-REQUEST v1.0
        ↓
CHAPTER-ARTIFACT-COLLECTION v1.4
```

## Git execution discipline

The default execution path is remote and agent-owned:

1. GitHub connector/API for branch/ref/file/PR/merge/read-back operations.
2. Repository-native GitHub Actions for build/test/validation work.
3. Other safe remote execution when available.
4. User-local Git only as a justified exception.

Local Git is never requested because it is faster, familiar or convenient. A
local exception must follow `BIBLIOTEKA-VSP-GIT-EXECUTION-POLICY v1.0` and
must record the reason code, blocked remote operation, evidence, minimal local
scope, verification, rollback and remote resume point.

The expected book-ingest exception is `GIT_LFS_BINARY_UPLOAD_REQUIRED`: the
exact canonical PDF or EPUB must be stored as a real Git LFS object while the available connector
cannot upload the binary LFS object. In that case only the minimal source upload
is local; after GitHub confirms it, RAG/PR/CI/readiness return to remote tools.

Book source ingest and generated RAG use a non-main ingest branch. The RAG
workflow writes generated artifacts back to that branch. Merge only after
readiness succeeds. Never force-push or silently replace the declared canonical source.


## Canonical source formats

Current RAG onboarding accepts exactly one declared canonical source per book:

- `source/book.pdf` — source units are 1-indexed PDF pages;
- `source/book.epub` — source units are 1-indexed EPUB spine items with XHTML ZIP-member locators.

The source format is preserved. A reflowable EPUB locator is provenance, not a
printed/PDF page number. Existing PDF RAG artifacts using legacy `pdf_page`
provenance remain valid and do not require rebuild solely because EPUB support
was added.
