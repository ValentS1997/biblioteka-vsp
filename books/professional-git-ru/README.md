# Профессиональная работа с Git

Book ID: `professional-git-ru`. Inventory number: `0019`.

## Verified edition identity

- Registered and PDF title: «Профессиональная работа с Git».
- Original source collection: *Git Notes for Professionals* (Stack Overflow / Goalkicker contributors).
- Publisher: Издательство АСТ, Moscow; publication year: 2024.
- Russian translation: ООО «Интеджер».
- ISBN: `978-5-17-160274-1`.
- Print extent: 160 pages; PDF extent: 162 pages.
- Edition number: **[Needs confirmation]**; no edition number is inferred.
- Bibliographic evidence: canonical PDF page 3, extracted RAG chunk at `rag/chunks/p0001-p0100/p0003-c01.md`.
- Registry contributor attribution: Aaron Critchley, Aaron Skomra, aavrug and other Goalkicker contributors. This is a contributor list, not evidence of exclusive single-author authorship.
- The original filename contains `edited`. The checksum identifies the exact source, but edits relative to another PDF copy are not established.

## Canonical source and LFS provenance

- Source path: `source/book.pdf`, Git LFS.
- SHA-256: `5eb8376c990ff58103fb110ae36467bb407f015bedf45aa2db6dae5678f8b5fb`.
- Size: 5,209,527 bytes.
- Reused Git LFS pointer blob from vault branch `source-vault/2026-10-13-found-books-14`, SHA `ba777e1900e886c685be453afc36c3fa20626bcc`.
- Source commit: `95e8d0a449d85479aadb98f66f599a2d590df8f6`.
- Real LFS binary retrieved and source checksum independently computed and matched in successful [RAG workflow run 38373665574](https://github.com/vsp-corp/biblioteka-vsp/actions/runs/38373665574).

## Full-book RAG

- Generated commit: `f7f806120ebae9e366b54119943e6d6a2d2c0749`.
- Source units: 162 PDF pages; 161 with extracted text, 1 blank page (PDF page 1).
- Extracted characters: 477,296.
- Addressable chunks: 180; deterministic lexical search shards: 3,208.
- Parser: PyMuPDF 1.28.2.
- Manifest validation: `READY_WITH_KNOWN_LIMITATIONS`.
- Strict ingestion acceptance: **ACCEPTED**. Source SHA, generation identities, source-unit coverage, chunk integrity, sampled retrieval and negative exact-term behavior all passed.
- Limitations: PDF text-layer extraction is not a visual page audit; images, equations, tables and diagrams are not separately encoded as multimodal RAG objects.

## Reading state

No `reading/progress.yaml` was created or modified. Reading status remains **[Needs confirmation]**.

## Chapter work

Compute chapter-analysis readiness with `python scripts/check_book_readiness.py --book-id professional-git-ru --capability chapter-analysis`. Do not claim READY until that gate and branch CI pass.
