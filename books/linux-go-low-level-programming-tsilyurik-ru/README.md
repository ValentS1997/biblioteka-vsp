# Linux и Go. Эффективное низкоуровневое программирование

Book ID: `linux-go-low-level-programming-tsilyurik-ru`

Author: Олег Иванович Цилюрик.

## Reading state

Reading state is not activated by the current request. Current state: `planned`.

Canonical reading state: [reading/progress.yaml](reading/progress.yaml).

## Source

Canonical destination: `source/book.pdf` (Git LFS).

Verified source-vault object:

- SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- size: `2092569` bytes
- source-vault branch: `source-vault/2026-09-30-rag-books`
- source-vault path: `source-vault/objects/df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2.pdf`

The canonical PDF path in this branch reuses the already uploaded Git LFS object.

## RAG

RAG scope: full book.

Current state: onboarding in progress. Generated RAG artifacts must be produced by `.github/workflows/build-book-rag.yml` and then pass the canonical readiness check.

Canonical readiness command:

`python scripts/check_book_readiness.py --book-id linux-go-low-level-programming-tsilyurik-ru --capability chapter-analysis`
