# biblioteka-vsp templates

Canonical process and entrypoint templates.

## Current user entrypoints

| Use case | Template | Version |
|---|---|---:|
| Start a new book branch for RAG + chapter cheatsheets | [book-branch-bootstrap-v1.4.yaml](book-branch-bootstrap-v1.4.yaml) | 1.4 |
| Start analysis of one chapter | [chapter-analysis-request-v1.4.yaml](chapter-analysis-request-v1.4.yaml) | 1.4 |

## Current process contracts

| Responsibility | Template | Version |
|---|---|---:|
| Branch/process compliance router | [process-compliance-router-v1.2.yaml](process-compliance-router-v1.2.yaml) | 1.2 |
| Interrupted-chat recovery / durable Git checkpoint | [session-recovery-v1.0.yaml](session-recovery-v1.0.yaml) | 1.0 |
| Git execution / local-exception policy | [git-execution-policy-v1.0.yaml](git-execution-policy-v1.0.yaml) | 1.0 |
| Optional one-shot preload of many future PDF/EPUB LFS objects | [source-vault-batch-stage-v1.0.yaml](source-vault-batch-stage-v1.0.yaml) | 1.0 |
| One-time book source/RAG preparation | [book-onboarding-v1.3.yaml](book-onboarding-v1.3.yaml) | 1.3 |
| Strict acceptance of new/rebuilt RAG generations | [rag-ingestion-acceptance-v1.0.yaml](rag-ingestion-acceptance-v1.0.yaml) | 1.0 |
| Read-only chapter-analysis readiness gate | [book-readiness-v1.3.yaml](book-readiness-v1.3.yaml) | 1.3 |
| Chapter direct Git publication and progress | [chapter-publication-v1.0.yaml](chapter-publication-v1.0.yaml) | 1.0 |
| Chapter artifact production | [chapter-artifact-collection-v1.8.yaml](chapter-artifact-collection-v1.8.yaml) | 1.8 |

## Git execution rule

Routine repository work is agent-owned and remote-first:

```text
GitHub connector/API
  ↓
repository-native GitHub Actions
  ↓
other safe remote executor when available
  ↓
user-local Git only as an evidence-backed exception
```

Local Git is not a convenience path. A local request must include a valid
reason code, verified remote limitation, minimal scope, verification, rollback
and an explicit resume point back to remote execution.

The expected common exception for book ingest is
`GIT_LFS_BINARY_UPLOAD_REQUIRED`: the exact canonical PDF or EPUB source must become a real Git LFS
object but the available connector cannot upload the binary LFS object. After
that one source upload is verified on GitHub, RAG/PR/CI/readiness work returns
to GitHub tools.

## Normal flow

```text
PROCESS-COMPLIANCE-ROUTER v1.2
  ↓
New book branch
  ↓
BOOK-BRANCH-BOOTSTRAP v1.4
  ↓
BOOK-READINESS v1.3
  ├─ READY ──────────────────────────────┐
  └─ BLOCKED → BOOK-ONBOARDING v1.3
                 ↓
          RAG-INGESTION-ACCEPTANCE v1.0
                 ↓
              readiness
                                        ↓
                              READY_FOR_CHAPTER_ANALYSIS
                                        ↓
                                  "Анализ главы N"
                                        ↓
                          CHAPTER-ANALYSIS-REQUEST v1.4
                                        ↓
                     CHAPTER-ARTIFACT-COLLECTION v1.8
```

## Compatibility

Older accepted versions remain in the repository for reproducibility. New book
and chapter work uses the versions listed above or a later explicitly ACCEPTED
successor.

## Optional source-vault preload

If many future books are already available locally, use the source-vault batch stage once instead of repeating one local Git/LFS upload per book.

```text
local PDF/EPUB batch
  ↓ one justified local LFS upload
source-vault/<batch>
  ↓ later, remotely
promote existing LFS pointer into books/<book_id>/source/book.<ext>
  ↓
BOOK-ONBOARDING / RAG / readiness
```

The vault does not register books and does not trigger RAG. It only preloads immutable source candidates so subsequent book onboarding can stay remote-first.


## RAG generation acceptance

Current builds/rebuilds use deterministic generation identity and are not
published merely because chunks/index were created.

```text
canonical source + SHA
  ↓
build derived RAG
  ↓
RAG-INGESTION-ACCEPTANCE v1.0
  ├─ REJECTED/ERROR → do not commit generated generation
  └─ ACCEPTED → commit/push → BOOK-READINESS v1.3
```

Existing legacy RAG remains valid under the compatibility path until its next
controlled rebuild. Rebuild by the current pipeline makes strict acceptance
mandatory.

## Chapter publication is Git-first (no ZIP fallback)

From every book-chat startup and before each chapter analysis, show the total
number of numbered chapters **grounded in the book's canonical RAG TOC** (or
`[Needs confirmation]` with the reason), the chapter numbers published in Git,
and the completed/remaining progression. Prefer a verified,
source-SHA-bound `books/<book_id>/notes/chapters/plan.yaml`.

The reference report is
`python scripts/chapter_publication_status.py --book-id <book_id>`;
it counts only chapter directories whose six required files are in Git HEAD,
not drafts or ZIP archives. Do not infer the book total from note directories.
Keep `notes/chapters/README.md` links/progress in sync after each commit.

Chapter output must be individual files in a book branch, with GitHub read-back,
commit/PR links and CI. ZIP/RAR/7z/tar or sandbox/download-only handoffs do
**not** satisfy a chapter request. If files cannot all be published now, report
the completed Git paths, missing paths and explicit blocker as PARTIAL/BLOCKED;
never claim the chapter was fully delivered.

## Resuming after a chat disconnect (Git checkpoint, not model memory)

The canonical [session recovery contract](session-recovery-v1.0.yaml) applies
to multi-step book/RAG/chapter/registry/PR/process work. Record a brief,
technical checkpoint at `.workflow/checkpoints/<task-key>.yaml` in a
**non-main** branch and commit it before/after verified milestones. Store task
identity, confirmed branch/HEAD, completed work with GitHub evidence,
pending work and the first safe read-only action. Never store chat transcripts,
secrets or hidden model reasoning.

On **«Ковальски, проверка после обрыва связи»** re-fetch GitHub branch
state, files, PR and CI before retrying anything. A tool timeout is an
**unknown** remote outcome, not evidence that the write failed. Avoid
duplicate files/PRs, force pushes and blind retries. If continuation cannot
be grounded in GitHub, explicitly return `RECOVERY_BLOCKED` and the smallest
missing piece of evidence.

The protocol cannot prevent ChatGPT message/thread limits. It instead
preserves recoverable repository state between chats. Finish each bounded
work unit with commit/read-back and an honest progress report; never claim
background execution will continue after the chat ends.
