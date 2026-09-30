# Внутреннее устройство Linux — 3-е издание

Book ID: `how-linux-works-3e-ru-2022`

Author:

- Брайан Уорд

Russian edition: Питер, 2022. ISBN `978-5-4461-3946-0`.

## Reading state

Reading started on 2026-09-30.

Canonical reading state: [reading/progress.yaml](reading/progress.yaml).

## Source

Canonical destination: `source/book.pdf`.

Verified source candidate supplied for onboarding:

- SHA-256: `60bb698fc2ff849a9814f099c12ca56e8f40c11b0518436f3ce3c44e96152df9`
- size: `8120657` bytes
- PDF pages: `480`
- storage requirement: Git LFS

The exact binary PDF is not considered canonically ingested until the real Git LFS
object is uploaded to `source/book.pdf` and the repository checksum matches
[source/SHA256](source/SHA256).

## RAG

RAG scope: full book.

Current state on this ingest scaffold: source binary upload is pending. No RAG
artifacts are considered ready yet.

After the canonical Git LFS source is pushed to this non-`main` ingest branch,
the **Build book RAG** workflow must generate and validate:

- `rag/manifest.yaml`
- `rag/text.md`
- `rag/chunks.jsonl`
- `rag/chunk-index.jsonl`
- `rag/chunks/**/*.md`
- `rag/search-index/manifest.json`
- `rag/search-index/**/*.json`

The branch must not be merged to `main` until
`scripts/check_book_readiness.py --book-id how-linux-works-3e-ru-2022 --capability chapter-analysis`
returns `READY`.
