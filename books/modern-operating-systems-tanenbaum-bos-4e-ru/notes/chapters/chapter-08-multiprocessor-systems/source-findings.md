# Source findings — Chapter 8

## [Source contradiction] Section numbering in body differs from the table of contents

The TOC on PDF pages 11–12 gives:

- `8.2.1` Hardware of multicomputers;
- `8.4.1 … 8.4.6` subsections of distributed systems;
- `8.5` research;
- `8.6` summary.

The chapter body contains conflicting headings:

- PDF 608: `8.3.1. Аппаратное обеспечение мультикомпьютеров` while the enclosing section is `8.2. Мультикомпьютеры`;
- PDF 633: `8.3.1. Сетевое оборудование`;
- PDF 636: `8.3.2. Сетевые службы и протоколы`;
- PDF 640: `8.3.3...`;
- PDF 641: body page header says `8.4. Распределенные системы`, but subsection says `8.3.4`;
- PDF 646: `8.3.5...`;
- PDF 648: `8.3.6...`;
- PDF 651: research heading appears as `8.4`, while the TOC labels research `8.5`;
- PDF 652 returns to `8.6. Краткие выводы`.

Handling: README navigation follows the TOC because it provides the coherent hierarchy, but the conflicting body numbering is not silently rewritten or treated as authoritative numbering.

## [Needs confirmation] Figure-dependent review questions

Several review questions depend on graphical topology/state that is not independently encoded in the text RAG, notably Q4, Q5, Q15, Q23 and Q26–27.

Handling: answers use prose-derived facts and general formulas where the source supplies sufficient structure. Exact figure-specific values remain `[Needs confirmation]` when the needed topology/state cannot be reconstructed.

## [Needs confirmation] Programming and benchmark exercises require execution

Review questions 34–37 require writing/running programs or producing environment-dependent measurements.

Handling: provide source-grounded implementation designs where possible, but compilation, runtime output and benchmark values remain `[Needs confirmation]`.
