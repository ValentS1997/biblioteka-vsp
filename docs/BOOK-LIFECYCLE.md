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
BIBLIOTEKA-VSP-PROCESS-COMPLIANCE-ROUTER v1.2
```

The router resolves branch type, checks current canonical contract versions,
preserves explicitly compatible legacy RAG, and blocks state-changing work on
critical process drift.

New RAG/chapter book branch:

```text
BIBLIOTEKA-VSP-BOOK-BRANCH-BOOTSTRAP v1.4
```

Normal chapter command:

```text
"Анализ главы N"
  ↓
BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.4
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
BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.8
```

Older accepted chapter templates remain immutable for reproducibility.
Current chapter work uses CHAPTER-ARTIFACT-COLLECTION v1.8 with
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
BOOK-BRANCH-BOOTSTRAP v1.4
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
CHAPTER-ANALYSIS-REQUEST v1.4
        ↓
CHAPTER-ARTIFACT-COLLECTION v1.8
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


## Chapter notes validation

The chapter-note validator preserves the single-book entrypoint:

```sh
python scripts/validate_chapter_notes.py --book-dir books/<book_id>
```

Repository CI uses `--changed-paths-file` from the PR/push Git diff to
validate **every book whose notes are changed**: required artifacts, internal
Markdown links, and SVG rasterization with CairoSVG. When process code changes
but no chapter notes are touched, the established baseline
`computer-networks-olifer-7e-ru-2026` is validated. This avoids breaking
unrelated legacy book collections that predate the current v1.8 chapter
requirements. Both `--book-dir` (single book, backward compatible) and
`--all-books` (explicit full repository audit) remain available. The validator
never mutates source, RAG, notes or reading state.

## Git-first chapter publication and progress (contract v1.0)

Every book chat must report chapter publication progress **at startup** and
after each chapter. Resolve a source-grounded TOC from canonical RAG and commit
a `books/<book_id>/notes/chapters/plan.yaml` with `schema:
biblioteka-vsp/chapter-plan/v1`, `book_id`, RAG `source_sha256`,
`toc_evidence`, `total_chapters`, and a per-chapter list of `number`,
`title`, `slug`, and `source_locator`. Do not fabricate chapter counts:
where no verified TOC is available, show `[Needs confirmation]` and a reason,
never a false ratio/percentage.

Progress is about **Git chapter publication, not personal reading**. Run
`python scripts/chapter_publication_status.py --book-id <book_id>` in a checkout
of the relevant book branch/commit, or verify equivalent individual files via
GitHub API. Display verified chapter total, completed chapters, remaining
chapters, next chapter, branch/commit, and percentage only with verified total.
A complete chapter has all six required individual files in Git. Also update
the book-level `notes/chapters/README.md` with links and a current progress
summary.

Per `templates/chapter-publication-v1.0.yaml`, each artifact is published
directly to a GitHub book branch (not main) as an individual file. ZIP and other
archive bundles, downloadable sandbox attachments, and chat-only content are
not substitutes for Git writes. CI rejects newly changed archive files under
`books/*/notes/**`. When the assistant cannot write all chapter files in the
current execution, it must explicitly report `CHAPTER_PARTIALLY_PUBLISHED_GIT`
or `CHAPTER_PUBLICATION_BLOCKED` with actual Git paths/commits, what remains,
why it is blocked, and the next action. No promise of later background work.
Historical versions remain available and older chapters need not be rebuilt.

## Session interruption / repeated reset recovery

ChatGPT discussion-length failures and vanished intermediate reasoning are
not repository state. The project cannot change ChatGPT's conversation
limits. Every multi-step mutation uses
`templates/session-recovery-v1.0.yaml` and the process router v1.2.

Create an idempotent Git checkpoint in the **working branch** at
`.workflow/checkpoints/<task-key>.yaml`, with an unambiguous task ID, current
verified branch/ref, planned and completed steps, evidence commit/PR/CI links
and first read-only resume action. Keep it small and free of secrets/chat text.
Update it at confirmed milestones, not on unsupported assumptions. Before
merging a finished feature PR, retain final evidence in the PR and remove
the transient checkpoint if appropriate; after merge Git/PR remains truth.

After `Ковальски, проверка после обрыва связи` (or equivalent), resolve the
task from GitHub: read latest main and task-branch refs, inspect checkpoint,
compare **actual files** to reported work, inspect PR state and CI, and only
then resume the first uncompleted safe operation. A timed-out GitHub action
has UNKNOWN outcome until verified. Do not rerun a commit, build, PR or merge
blindly. Repeated resets repeat the read-only reconstruction rather than
replaying mutations. If unique task identity or evidence cannot be recovered,
return `RECOVERY_BLOCKED` with one precise missing item. Never promise
background work or recovery of hidden chain-of-thought.

For chapters, the `chapter-publication-v1.0` Git-only/no-ZIP rules and
source-grounded chapter totals remain mandatory. Checkpoint progress does
not imply personal reading progress or RAG correctness.
