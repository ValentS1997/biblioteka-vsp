# biblioteka-vsp templates

Canonical process and entrypoint templates.

## Current user entrypoints

| Use case | Template | Version |
|---|---|---:|
| Start a new book branch for RAG + chapter cheatsheets | [book-branch-bootstrap-v1.1.yaml](book-branch-bootstrap-v1.1.yaml) | 1.1 |
| Start analysis of one chapter | [chapter-analysis-request-v1.1.yaml](chapter-analysis-request-v1.1.yaml) | 1.1 |

## Current process contracts

| Responsibility | Template | Version |
|---|---|---:|
| Git execution / local-exception policy | [git-execution-policy-v1.0.yaml](git-execution-policy-v1.0.yaml) | 1.0 |
| One-time book source/RAG preparation | [book-onboarding-v1.1.yaml](book-onboarding-v1.1.yaml) | 1.1 |
| Read-only chapter-analysis readiness gate | [book-readiness-v1.1.yaml](book-readiness-v1.1.yaml) | 1.1 |
| Chapter artifact production | [chapter-artifact-collection-v1.5.yaml](chapter-artifact-collection-v1.5.yaml) | 1.5 |

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
`GIT_LFS_BINARY_UPLOAD_REQUIRED`: the exact PDF must become a real Git LFS
object but the available connector cannot upload the binary LFS object. After
that one source upload is verified on GitHub, RAG/PR/CI/readiness work returns
to GitHub tools.

## Normal flow

```text
New book branch
  ↓
BOOK-BRANCH-BOOTSTRAP v1.1
  ↓
BOOK-READINESS v1.1
  ├─ READY ──────────────────────────────┐
  └─ BLOCKED → BOOK-ONBOARDING v1.1 → readiness
                                        ↓
                              READY_FOR_CHAPTER_ANALYSIS
                                        ↓
                                  "Анализ главы N"
                                        ↓
                          CHAPTER-ANALYSIS-REQUEST v1.1
                                        ↓
                     CHAPTER-ARTIFACT-COLLECTION v1.5
```

## Compatibility

Older accepted versions remain in the repository for reproducibility. New book
and chapter work uses the versions listed above or a later explicitly ACCEPTED
successor.
