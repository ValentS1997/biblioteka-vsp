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

All branch work first passes the process-compliance gate:

```text
BIBLIOTEKA-VSP-PROCESS-COMPLIANCE-ROUTER v1.0
```

The router resolves branch type, checks current canonical contract versions,
preserves explicitly compatible legacy RAG, and blocks state-changing work on
critical process drift.

New RAG/chapter book branch:

```text
BIBLIOTEKA-VSP-BOOK-BRANCH-BOOTSTRAP v1.3
```

Normal chapter command:

```text
"Анализ главы N"
  ↓
BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.3
```

The entrypoint templates orchestrate the contracts below; they do not duplicate
book/RAG/chapter implementation logic.

## Contracts

One-time book preparation:

```text
BIBLIOTEKA-VSP-BOOK-ONBOARDING v1.3
    ↓
canonical source + provenance
    ↓
full-book RAG
    ↓
RAG-INGESTION-ACCEPTANCE v1.0
    ↓
retrieval integrity
```

Read-only gate:

```text
BIBLIOTEKA-VSP-BOOK-READINESS v1.3
    ↓ READY
BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7
```

Older accepted chapter templates remain immutable for reproducibility.
Current chapter work uses CHAPTER-ARTIFACT-COLLECTION v1.7 with
BOOK-READINESS v1.3 and explicit source-findings handling.

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

For a new/rebuilt generation, readiness additionally requires
`rag/acceptance.yaml` with status `ACCEPTED`, bound to the same
`source_sha256`, `corpus_generation_id` and `index_generation_id`.
Legacy RAG without generation metadata remains valid until its next controlled
rebuild.

## New-book flow

```text
BOOK-BRANCH-BOOTSTRAP v1.3
        ↓
Inventory / reading
        ↓
capability preflight
        ↓
BOOK-ONBOARDING v1.3 when RAG-dependent work is requested
        ↓
canonical source + SHA provenance
        ↓
full-book RAG
        ↓
RAG-INGESTION-ACCEPTANCE v1.0
        ↓
retrieval integrity test
        ↓
BOOK-READINESS v1.3
        ↓
READY
        ↓
"Анализ главы N"
        ↓
CHAPTER-ANALYSIS-REQUEST v1.3
        ↓
CHAPTER-ARTIFACT-COLLECTION v1.7
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


## RAG generation identity and rebuilds

The canonical source remains `books/<book_id>/source/book.pdf|book.epub`
plus `source/SHA256`. Source-vault objects are staging candidates only.

Current/new RAG generations are deterministic derived state:

- `corpus_generation_id` binds source SHA + parser/version + normalization +
  chunking policy/config;
- `index_generation_id` binds the corpus generation + retrieval/index policy;
- compatibility `chunk_id` remains the addressable path identity;
- `chunk_uid` + `text_sha256` detect silent content/chunking drift.

A rebuild is a state-changing derived-layer operation:

```text
confirm canonical source SHA
  ↓
build derived generation on non-main branch/runner
  ↓
validate all chunk provenance + content hashes + coverage
  ↓
bounded first/middle/last retrieval + negative exact-term behavior
  ↓
ACCEPTED
  ↓
commit/push generated generation
```

A rejected generation is not published by the normal build workflow. Git
branch/commit history is the rollback boundary; the canonical source is never
silently replaced by a rebuild.

## Source contradiction policy

Semantic contradictions belong to the chapter-analysis layer, not the
ingestion parser. Chapter artifacts may classify findings as:

- `[Source contradiction]`
- `[Source code mismatch]`
- `[Source wording/code mismatch]`
- `[Source extraction issue]`
- `[Needs confirmation]`

The source is not silently corrected. Relevant conflicting variants and their
provenance are preserved in conditional `source-findings.md`.
