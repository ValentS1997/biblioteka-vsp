# biblioteka-vsp templates

Canonical process and entrypoint templates.

## User entrypoints

| Use case | Template | Version |
|---|---|---|
| Start a new book branch for RAG + chapter cheatsheets | [book-branch-bootstrap-v1.0.yaml](book-branch-bootstrap-v1.0.yaml) | 1.0 |
| Start analysis of one chapter | [chapter-analysis-request-v1.0.yaml](chapter-analysis-request-v1.0.yaml) | 1.0 |

## Process contracts

| Responsibility | Template | Version |
|---|---|---|
| One-time book source/RAG preparation | [book-onboarding-v1.0.yaml](book-onboarding-v1.0.yaml) | 1.0 |
| Read-only chapter-analysis readiness gate | [book-readiness-v1.0.yaml](book-readiness-v1.0.yaml) | 1.0 |
| Chapter artifact production | [chapter-artifact-collection-v1.4.yaml](chapter-artifact-collection-v1.4.yaml) | 1.4 |

## Normal flow

```text
New book branch
  ↓
BOOK-BRANCH-BOOTSTRAP v1.0
  ↓
BOOK-READINESS v1.0
  ├─ READY ──────────────────────────────┐
  └─ BLOCKED → BOOK-ONBOARDING v1.0 → readiness
                                        ↓
                              READY_FOR_CHAPTER_ANALYSIS
                                        ↓
                                  "Анализ главы N"
                                        ↓
                          CHAPTER-ANALYSIS-REQUEST v1.0
                                        ↓
                     CHAPTER-ARTIFACT-COLLECTION v1.4
```

## Compatibility

`chapter-artifact-collection-v1.3.yaml` remains retained for reproducibility of
older accepted work. New chapter work uses v1.4 or a later explicitly ACCEPTED
successor.
