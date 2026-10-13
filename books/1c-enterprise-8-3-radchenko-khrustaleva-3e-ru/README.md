# 1С:Предприятие 8.3. Практическое пособие разработчика. Издание 3

Book ID: `1c-enterprise-8-3-radchenko-khrustaleva-3e-ru`; inventory: `0030`.

Authors according to `registry/books.yaml`: М. Г. Радченко, Е. Ю. Хрусталева.

## Edition verification

Registry, staged filename and **PDF page 2 text** identify the third edition. The imprint explicitly refers to the printed 3rd edition. Extracted glyphs on this page are partly corrupted (e.g., `8.P`, `P-е`); do not silently fix extracted book text. Publication year, publisher and ISBN: [Needs confirmation].

## Source

Canonical path: `source/book.pdf` (Git LFS).
Staged in `source-vault/2026-10-13-found-books-14` as `source-vault/objects/ce8fa0fbf0d8bb38f724ed04f130c2443c1e181eb51edafac692c4786874c923.pdf`.
The **same Git LFS pointer blob** was reused; no synthetic PDF or duplicate binary was created.

- Expected SHA-256: `ce8fa0fbf0d8bb38f724ed04f130c2443c1e181eb51edafac692c4786874c923`
- Expected size: `24311627` bytes
- GitHub Actions LFS checkout and real PDF SHA-256 verification: **PASS** (run `38392309161`). PDF parsed successfully; 983 pages.

## RAG

Full-book RAG was built and accepted by `templates/rag-ingestion-acceptance-v1.0.yaml` before commit. Acceptance: `ACCEPTED`; generated commit: `e090af298d6c7d1fbe42444655d98221c607aa4e`. 995 addressable chunks, 2,145 search shards. RAG status: `READY_WITH_KNOWN_LIMITATIONS`; text-layer extraction and non-text PDF content may have limitations. Run `python scripts/check_book_readiness.py --book-id 1c-enterprise-8-3-radchenko-khrustaleva-3e-ru --capability chapter-analysis` after generation.

## Reading state

Reading status is **not modified by this onboarding**. Existing registry reading fields are unchanged. See `reading/progress.yaml` for an explicitly unknown state rather than an invented reading transition.
