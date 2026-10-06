# Linux и Go. Эффективное низкоуровневое программирование

Book ID: `linux-go-low-level-programming-tsilyurik-ru`

Author: Олег Иванович Цилюрик.

## Reading state

Reading has not been activated. Current state: `planned`.

Canonical reading state: [reading/progress.yaml](reading/progress.yaml).

## Source

Canonical source: `source/book.pdf` (Git LFS).

Verified provenance:

- SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- size: `2092569` bytes
- PDF pages processed by RAG: `281`
- source-vault staging branch: `source-vault/2026-09-30-rag-books`

The canonical source is the book-local `source/book.pdf`; source-vault is staging provenance only.

## RAG

Existing RAG generation is legacy-compatible and is intentionally preserved without rebuild.

- validation: `READY_WITH_KNOWN_LIMITATIONS`
- addressable chunks: `289`
- source SHA binding: verified
- strict `rag/acceptance.yaml`: not required until the next controlled rebuild because this generation predates generation metadata

Current readiness contract:

`BIBLIOTEKA-VSP-BOOK-READINESS v1.3`

Current chapter artifact contract:

`BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`

Canonical readiness command:

`python scripts/check_book_readiness.py --book-id linux-go-low-level-programming-tsilyurik-ru --capability chapter-analysis`
