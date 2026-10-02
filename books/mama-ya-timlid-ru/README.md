# Мама, я тимлид! Практические советы по руководству IT-командой

Book ID: `mama-ya-timlid-ru`

Inventory: `0022`.

Author:

- Марина Перескокова

Edition number, publisher, publication year, publication page count and ISBN: [Needs confirmation].

## Reading state

Canonical reading state already exists and is `completed`. This bootstrap does not activate, reset or otherwise modify reading state.

Canonical reading state: [reading/progress.yaml](reading/progress.yaml).

## Source

Canonical destination: `source/book.epub` (Git LFS).

Verified source-vault candidate:

- original name: `Мама, я тимлид! Практические советы по руководству IT-командой. Перескокова.epub`
- SHA-256: `f02343c1718bae4029e820efbd2420904f599712eb64ba9db1ce47f43381792f`
- size: `1976472` bytes
- source-vault branch: `source-vault/2026-09-30-rag-books`
- source-vault path: `source-vault/objects/f02343c1718bae4029e820efbd2420904f599712eb64ba9db1ce47f43381792f.epub`

The source-vault manifest and Git LFS pointer OID/size match.

## RAG

RAG scope: full book.

Validation status: `READY_WITH_KNOWN_LIMITATIONS`.

Verified by RAG build:

- EPUB spine items: `16`
- spine items with text: `16`
- blank spine items: `0`
- extracted text model: `xhtml_text`
- addressable chunks: `81`
- deterministic search-index shards: `1302`
- source promotion commit: `d031e3c931c4af59f88501130d78394eb2553c19`
- generated RAG commit: `c9a11ee08f11481f087b4958e4b8db3083c32ca6`
- workflow run: `36871287917`

GitHub Actions materialized the real LFS object and recomputed the expected SHA-256 successfully.

Canonical readiness command:

`python scripts/check_book_readiness.py --book-id mama-ya-timlid-ru --capability chapter-analysis`


## Chapter artifacts

- [Глава 1. Вы стали руководителем](notes/chapters/chapter-01-vy-stali-rukovoditelem/) — `RAG_GROUNDED`; EPUB spine 3, `OPS/ch1-2.xhtml`, chunks `e0003:c01–c08`.
- [Глава 2. Вы и начальство](notes/chapters/chapter-02-vy-i-nachalstvo/) — `RAG_GROUNDED`; EPUB spine 4, `OPS/ch1-3.xhtml`, chunks `e0004:c01–c04`.
- [Глава 3. Вы и команда](notes/chapters/chapter-03-vy-i-komanda/) — `RAG_GROUNDED`; EPUB spine 5, `OPS/ch1-4.xhtml`, chunks `e0005:c01–c11`.
- [Глава 4. Работа с индивидуальностью](notes/chapters/chapter-04-rabota-s-individualnostyu/) — `RAG_GROUNDED`; EPUB spine 6–7, `OPS/ch1-5.xhtml` + `OPS/ch1-6.xhtml`, chunks `e0006:c01–c12` + `e0007:c01–c13`.
- [Глава 5. Создаем слаженную команду](notes/chapters/chapter-05-sozdaem-slazhennuyu-komandu/) — `RAG_GROUNDED`; EPUB spine 8, `OPS/ch1-7.xhtml`, chunks `e0008:c01–c08`.
- [Глава 6. Забота как часть работы](notes/chapters/chapter-06-zabota-kak-chast-raboty/) — `RAG_GROUNDED`; EPUB spine 9, `OPS/ch1-8.xhtml`, chunks `e0009:c01–c04`.
- [Глава 7. Целеполагание](notes/chapters/chapter-07-celepolaganie/) — `RAG_GROUNDED`; EPUB spine 10, `OPS/ch1-9.xhtml`, chunks `e0010:c01–c04`.
- [Глава 8. Секреты творческой атмосферы](notes/chapters/chapter-08-sekrety-tvorcheskoy-atmosfery/) — `RAG_GROUNDED`; EPUB spine 11, `OPS/ch1-10.xhtml`, chunks `e0011:c01–c05`.
- [Глава 9. Работа с распределенной командой](notes/chapters/chapter-09-rabota-s-raspredelennoy-komandoy/) — `RAG_GROUNDED`; EPUB spine 12, `OPS/ch1-11.xhtml`, chunks `e0012:c01–c04`.

## Supplemental materials

The numbered chapter sequence ends at chapter 9. Post-chapter source material is indexed separately:

- [Supplemental materials](notes/supplements/) — beginner-manager checklist, author's reading list, bibliography/provenance.
