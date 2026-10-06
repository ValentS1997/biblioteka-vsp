# biblioteka-vsp templates

Canonical process and entrypoint templates.

## Current user entrypoints

| Use case | Template | Version |
|---|---|---:|
| Start a new book branch for RAG + chapter cheatsheets | [book-branch-bootstrap-v1.3.yaml](book-branch-bootstrap-v1.3.yaml) | 1.3 |
| Start analysis of one chapter | [chapter-analysis-request-v1.3.yaml](chapter-analysis-request-v1.3.yaml) | 1.3 |

## Current process contracts

| Responsibility | Template | Version |
|---|---|---:|
| Git execution / local-exception policy | [git-execution-policy-v1.0.yaml](git-execution-policy-v1.0.yaml) | 1.0 |
| Optional one-shot preload of many future PDF/EPUB LFS objects | [source-vault-batch-stage-v1.0.yaml](source-vault-batch-stage-v1.0.yaml) | 1.0 |
| One-time book source/RAG preparation | [book-onboarding-v1.3.yaml](book-onboarding-v1.3.yaml) | 1.3 |
| Strict acceptance of new/rebuilt RAG generations | [rag-ingestion-acceptance-v1.0.yaml](rag-ingestion-acceptance-v1.0.yaml) | 1.0 |
| Read-only chapter-analysis readiness gate | [book-readiness-v1.3.yaml](book-readiness-v1.3.yaml) | 1.3 |
| Chapter artifact production | [chapter-artifact-collection-v1.7.yaml](chapter-artifact-collection-v1.7.yaml) | 1.7 |

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
New book branch
  ↓
BOOK-BRANCH-BOOTSTRAP v1.3
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
                          CHAPTER-ANALYSIS-REQUEST v1.3
                                        ↓
                     CHAPTER-ARTIFACT-COLLECTION v1.7
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
