# Source findings — Chapter 13

## [Source structure] No conventional summary or review section

Chapter 13 is bibliographic. It contains:
- section 13.1 with topic-organized recommendations;
- section 13.2 referring to a detailed alphabetical bibliography.

It does not contain a conventional chapter-end summary or review questions.

Handling: `summary.md` is explicitly marked as a synthesis from the chapter body; review artifacts record `0/0` rather than inventing content.

## [Source completeness limitation] Section 13.2 is not present as a full bibliography

PDF page 1119 states that the detailed alphabetical bibliography can be downloaded from the publisher website. The local canonical PDF does not include that full list.

Handling: the external bibliography is not imported under `rag_only`.

## [Text-layer/list numbering anomaly] Recommendation numbering is noisy in places

In the extracted text layer, some recommendation descriptions appear with list numbers of their own, especially in sections such as 13.1.2 and 13.1.7. This can make the ordinal sequence look doubled or discontinuous.

Handling: artifacts identify recommendations by author/title rather than relying on unstable extracted ordinals.

## [Historical freshness boundary] Editions, URLs and venue cadence are source-era

The chapter names specific editions and describes conference cadence/current relevance from the book's publication context.

Handling: these are preserved as source claims. Current editions, schedules, URLs and availability remain `[Needs confirmation]` unless external research is explicitly enabled.

## [End-of-book boundary]

PDF page 1120 is publisher/printing colophon material and not Chapter 14.

Handling: Chapter 13 is treated as the final numbered chapter, ending at PDF 1119.
