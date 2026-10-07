# Современные операционные системы. 4-е изд.

Book ID: `modern-operating-systems-tanenbaum-bos-4e-ru`

Inventory: `0005`.

Authors:

- Эндрю С. Таненбаум
- Херберт Бос

Edition: 4.

Translators/editors from the canonical registry:

- А. Леонтьева
- М. Малышева
- Н. Вильчинский

Russian edition: ООО Издательство «Питер», 2015. ISBN `978-5-496-01395-6`. Publication extent: `1120` pages. Original-edition ISBN: `978-0133591620`.

## Reading state

The user explicitly declared the complete book finished on `2026-10-08`.

Canonical reading state: [reading/progress.yaml](reading/progress.yaml).

The exact reading start date was not previously recorded and remains `[Needs confirmation]`.

## Source

Canonical source: `source/book.pdf` (Git LFS).

Verified source-vault provenance:

- original name: `Современные операционные системы. Таненбаун,Бос.pdf`
- SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- size: `14229645` bytes
- source-vault branch: `source-vault/2026-09-30-rag-books`
- source-vault path: `source-vault/objects/57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd.pdf`
- PDF pages: `1120`
- text layer: `unclassified_extractable_pdf_text`

The source-vault manifest and LFS pointer OID/size agree. GitHub Actions successfully materialized
the real LFS object during the RAG build, and the build recomputed the same SHA-256.

## RAG

RAG scope: full book.

Validation status: `READY_WITH_KNOWN_LIMITATIONS`.

- source units with text: `1119`
- blank source units: `1`
- addressable chunks: `1130`
- deterministic search-index shards: `9576`
- generated commit: `be63c2baf2f979f14171ddb3a5338af8497b9fc3`

Canonical readiness command:

`python scripts/check_book_readiness.py --book-id modern-operating-systems-tanenbaum-bos-4e-ru --capability chapter-analysis`

## Chapter artifacts

- [Глава 1 — Введение](notes/chapters/chapter-01-introduction/README.md) — RAG-grounded, PDF source locators 22–110.
- [Глава 2 — Процессы и потоки](notes/chapters/chapter-02-processes-and-threads/README.md) — RAG-grounded, PDF source locators 111–213.
- [Глава 3 — Управление памятью](notes/chapters/chapter-03-memory-management/README.md) — RAG-grounded, PDF source locators 214–300.
- [Глава 4 — Файловые системы](notes/chapters/chapter-04-file-systems/README.md) — RAG-grounded, PDF source locators 301–379.
- [Глава 5 — Ввод и вывод информации](notes/chapters/chapter-05-input-output/README.md) — RAG-grounded, PDF source locators 380–487.
- [Глава 6 — Взаимоблокировка](notes/chapters/chapter-06-deadlock/README.md) — RAG-grounded, PDF source locators 488–526.
- [Глава 7 — Виртуализация и облако](notes/chapters/chapter-07-virtualization-cloud/README.md) — RAG-grounded, PDF source locators 527–575.
- [Глава 8 — Многопроцессорные системы](notes/chapters/chapter-08-multiprocessor-systems/README.md) — RAG-grounded, PDF source locators 576–658.
- [Глава 9 — Безопасность](notes/chapters/chapter-09-security/README.md) — RAG-grounded, PDF source locators 659–783.
- [Глава 10 — Изучение конкретных примеров: Unix, Linux и Android](notes/chapters/chapter-10-unix-linux-android/README.md) — RAG-grounded, PDF source locators 784–930.
- [Глава 11 — Изучение конкретных примеров: Windows 8](notes/chapters/chapter-11-windows-8/README.md) — RAG-grounded, PDF source locators 931–1057.
- [Глава 12 — Разработка операционных систем](notes/chapters/chapter-12-operating-system-design/README.md) — RAG-grounded, PDF source locators 1058–1109.
- [Глава 13 — Библиография](notes/chapters/chapter-13-bibliography/README.md) — RAG-grounded, PDF source locators 1110–1119.

## Completion audit

Completion declared: `2026-10-08`.

Repository-wide verification at closure:

- numbered chapters present: `13/13`;
- chapter-analysis coverage: PDF pages `22–1119`, contiguous with no gaps between numbered chapters;
- front matter before Chapter 1 remains outside chapter artifacts by design;
- PDF page `1120` is publisher colophon/end matter, not another numbered chapter;
- chapter directories: `13`;
- chapter artifact files: `129` total;
- Chapter 7 correctly has no `summary.md` because the source contains no separate chapter-end summary;
- all chapter READMEs report `RAG_GROUNDED`;
- review questions: `580/580` across Chapters 1–12;
- RAG-grounded review answers: `580/580`;
- Chapter 13 contains no source review questions and is recorded as `0/0`;
- canonical full-book RAG remains `READY_WITH_KNOWN_LIMITATIONS`;
- full-book RAG: `1119` source units with text, `1` blank source unit, `1130` addressable chunks;
- canonical source SHA-256 remains `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`;
- source/RAG derived state was not rebuilt or rewritten during completion.

Book status: **COMPLETED**.
