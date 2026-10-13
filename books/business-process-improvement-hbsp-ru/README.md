# Руководство по улучшению бизнес-процессов

Book ID: `business-process-improvement-hbsp-ru`; inventory: `0036`.

## PDF / edition verification

Verified from canonical source PDF pages 1–4 (RAG extraction): Russian translation of
*Improving Business Processes: Expert Solutions to Everyday Challenges*.
Harvard Business School Press / Harvard Business Review Press.
Russian publisher: **Альпина Паблишер**, **2015**, **132 printed pages**.
Russian ISBN: `978-5-9614-4923-5`; original ISBN: `978-1-4221-2973-9`.
Translator: Е. Милицкая; editor: М. Оверченко.
The source does not explicitly state a numbered edition: **[Needs confirmation]**.
PDF physical page count: **136**.

## Verified canonical source

Path: `source/book.pdf` (Git LFS), promoted by reusing the exact pointer/blob from
`source-vault/2026-10-13-found-books-14` rather than uploading a duplicate.
SHA-256: `4c75aaaa000434b6fd7aeac337e163327060dcbe084e30a1c9793b923b855172`.
LFS size: **16715531 bytes**.

GitHub Actions checked out the real LFS object and the full-book RAG build verified
the binary SHA-256 against `source/SHA256`.

## RAG

Full-book RAG: `rag/manifest.yaml`, `rag/text.md`, `rag/chunks.jsonl`,
`rag/chunk-index.jsonl`, `rag/chunks/`, `rag/search-index/`.
Coverage: 136 PDF pages (117 pages with extracted text, 19 blank pages),
117 addressable chunks, 1363 lexical shards.
Strict RAG acceptance: `rag/acceptance.yaml` — **ACCEPTED**.
Extractor classification remains `unclassified_extractable_pdf_text`; diagram/table
content is not represented as separate multimodal retrieval objects.

## Reading status

Reading status remains **[Needs confirmation]**; this source/RAG ingest does not
mark the book as started, finished, or change existing reading state.

## Readiness

The canonical chapter-analysis readiness gate is
`python scripts/check_book_readiness.py --book-id business-process-improvement-hbsp-ru --capability chapter-analysis`.
