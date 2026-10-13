# Проектирование систем машинного обучения

Book ID: `designing-machine-learning-systems-chip-huyen-ru`. Inventory number: `0031`.

## Verified Russian publication

- Author: Чип Хьюен.
- Publisher: ТОО «Издательство «Фолиант», Астана.
- Publication year: **2023**.
- ISBN (Russian): `978-601-271-727-3`; ISBN (original): `978-1-098-10796-3`.
- Print publication: **368 pages**; source PDF: **370 PDF pages**.
- Edition number: **[Needs confirmation]**; never infer a first edition.
- Evidence: `rag/chunks/p0001-p0100/p0004-c01.md` (Russian title page) and `rag/chunks/p0001-p0100/p0005-c01.md` (bibliographic/copyright page); both are derived from the verified canonical PDF.

## Canonical PDF and Git LFS

- Canonical source: `source/book.pdf`.
- Original filename: `Khyuen_Ch_Proektirovanie_sistem_mashinnogo_obuchenia_2023.pdf`.
- SHA-256: `0bcacadb4e1dc2235cb58f975111e1633527217127c5871edb894fe2b8f4c80c`.
- Size: `33138426` bytes.
- Git LFS pointer reused unchanged from `source-vault/2026-10-13-found-books-14`, Git blob SHA `310ffe2a9c24a9801d1d6fc71e56aa64ac2eeb69`.
- Source-ingest commit: `5125c2269139ba38602c594f65a583fc5e9bbd4c`.
- Actual Git LFS checkout and checksum verified by GitHub Actions build run `38392253220`.

## Full-book RAG

- Generation commit: `59fca8531d0771279bb5c0ce4fee0a42914549e1`.
- Extractor: PyMuPDF 1.28.2; text-layer origin unclassified.
- Source units processed: **370** PDF pages; **366** with extractable text, blank pages **1, 3, 13, 370**.
- **376** uniquely addressable chunks; **4212** deterministic lexical search-index shards.
- `rag/manifest.yaml`: `READY_WITH_KNOWN_LIMITATIONS`.
- `rag/acceptance.yaml`: `ACCEPTED`; all required integrity, provenance, coverage, generation identity and bounded retrieval checks PASS.
- Known limitation: figures, equations, tables and diagrams are not indexed as independent multimodal objects.

## Reading and chapter work

- Existing `reading/progress.yaml` is preserved verbatim: `planned`; its pairing with `ai-engineering-chip-huyen-ru` remains unchanged.
- Chapter-analysis readiness must be computed using `python scripts/check_book_readiness.py --book-id designing-machine-learning-systems-chip-huyen-ru --capability chapter-analysis` and confirmed by CI before any PR.
- For future chapter analysis use canonical RAG only; preserve `RAG_MISS` rather than substituting external material.
