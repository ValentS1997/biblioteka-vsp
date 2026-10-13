# Основы администрирования информационных систем: учебное пособие

Book ID: `information-systems-administration-bobyntsev-ru`. Inventory: `0024`.

Source identity: `registry/books.yaml` inventory `0024` and source-vault manifest record with original filename `Основы_администрирования_информационных_систем_2021_Бобынцев_.pdf`.

Authors (inventory): Д. О. Бобынцев; А. Л. Марухленко; Л. О. Марухленко; С. А. Кужелева; Л. А. Лисицын.

Publication year `2021` appears in the source filename only; bibliographic year, publisher, edition number and ISBN remain `[Needs confirmation]` pending inspection of the actual PDF.

## Canonical source

- PDF: `source/book.pdf` (Git LFS pointer reused from source-vault, not a new binary upload).
- SHA-256 / Git LFS OID: `a5d6a2677d4b0e33a34dec3b7aae8b77f711bb748046d25766becb479f66663f`.
- LFS reported size: `12547520` bytes.
- Vault ref: `source-vault/2026-10-13-found-books-14` at commit `1ee2c759ba976c0cba0a18f6207915d76b3e3860`.
- Vault object: `source-vault/objects/a5d6a2677d4b0e33a34dec3b7aae8b77f711bb748046d25766becb479f66663f.pdf`.
- Real PDF binary, pagination, title page, edition and checksum must be confirmed by GitHub Actions LFS checkout and RAG build.

## Reading

Reading status is not modified by this ingest. No `reading/progress.yaml` is created or updated.

## RAG

Full-book source-derived RAG is generated only by `.github/workflows/build-book-rag.yml`, followed by `scripts/validate_rag_ingestion.py --write-result` and `scripts/check_book_readiness.py --book-id information-systems-administration-bobyntsev-ru --capability chapter-analysis`.

Do not declare READY or open a PR before verified acceptance and required CI PASS.
