# Unix и Linux: руководство системного администратора — 5-е издание

Book ID: `unix-linux-system-administration-handbook-5e-ru-2020`

Authors:

- Эви Немет
- Гарт Снайдер
- Трент Хейн
- Бен Уэйли
- Дэн Макин

Russian edition: ООО "Диалектика", 2020. ISBN `978-5-907144-10-1`.

## Reading state

The user confirmed that reading started in May 2026 and the complete book was finished on 2026-09-21.

Canonical reading state: [reading/progress.yaml](reading/progress.yaml).

## Source

Canonical path: `source/book.pdf`.

Expected source:

- SHA-256: `4c1872cfa8d8d28b91b7c72db1eea7a1e1f50e6c045b7e7e4cd2089127da51ff`
- size: `35463093` bytes
- PDF pages: `1168`
- text layer: embedded OCR

The source PDF must be stored through Git LFS. The uploaded chat artifact was inspected and checksummed, but the canonical Git LFS object is not yet present on this ingest branch because the available Git connector does not provide Git LFS object upload.

Do not merge this branch until `source/book.pdf` is uploaded through Git LFS and its checksum matches `source/SHA256`.

## RAG

RAG scope: full book.

When `source/book.pdf` is pushed to this ingest branch through Git LFS, the repository workflow runs `scripts/build_book_rag.py` and generates:

- `rag/manifest.yaml`
- `rag/text.md`
- `rag/chunks.jsonl`

Chunk IDs use source-PDF page coordinates:

```text
unix-linux-system-administration-handbook-5e-ru-2020:p0120:c01
```

RAG status remains blocked until the canonical source is present and the workflow completes.
