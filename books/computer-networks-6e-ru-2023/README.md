# Компьютерные сети — 6-е издание

Book ID: `computer-networks-6e-ru-2023`

Authors:

- Эндрю Таненбаум
- Ник Фимстер
- Дэвид Уэзеролл

Russian edition: Питер, 2023. ISBN `978-5-4461-1766-6`.

## Reading state

The user confirmed that the complete book was read from June 2025 through April 2026.

Canonical reading state: [reading/progress.yaml](reading/progress.yaml).

## Source

Canonical path: `source/book.pdf`.

Expected source:

- SHA-256: `67dc11d4bdadd4e02d012545f3bafaed63bbab89cd47626dcac28528ddd6bf3d`
- size: `132007784` bytes
- PDF pages: `994`

The source PDF exceeds normal GitHub Git-object limits and is therefore tracked through Git LFS. The source is not considered present until the LFS object is successfully uploaded and the checksum matches `source/SHA256`.

## RAG

RAG scope: full book.

When `source/book.pdf` is pushed to an ingest branch through Git LFS, the repository workflow runs `scripts/build_book_rag.py` and generates:

- `rag/manifest.yaml`
- `rag/text.md`
- `rag/chunks.jsonl`

Chunk IDs use source-PDF page coordinates:

```text
computer-networks-6e-ru-2023:p0120:c01
```

The embedded OCR text layer is used as the extraction source. Visual material remains available through the source PDF and page provenance; diagrams/images are not separately encoded as multimodal RAG objects by the v1 pipeline.

## Cross-model reference

- [OSI ↔ TCP/IP ↔ Таненбаум](notes/network-models-reference.md) — сводная таблица уровней, протоколов, команд и примеров + визуальная шпаргалка.

## Print edition

- [tanenbaum-computer-networks-notes-a4.pdf](exports/tanenbaum-computer-networks-notes-a4.pdf) — единый печатный A4-конспект по материалам `notes/`: главы 1–9, compact/detailed visual cheat sheets, команды, cheatsheets, схемы, резюме, контрольные вопросы и RAG-grounded ответы.
- PDF pages: `205`
- size: `1203615` bytes
- SHA-256: `8ceb1ebac584fe8a71a7fef0b6372786af82491685f11ba8ed84a26605c45361`
- source snapshot used for the build: `35b4e5e9f4dfa5ce2437bb4e549c2939f27aa22e`

The print PDF is built from the repository's reviewed `notes/` artifacts, not from `source/book.pdf`. Files derived from `review-answers.md` are RAG-grounded study answers, not an official publisher solution manual.
