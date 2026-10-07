# Source findings — Chapter 12

## [Source/TOC numbering issue] Final section numbers differ from the table of contents

The extracted table of contents on PDF page 16 labels:
- embedded systems as `12.6.8`;
- the summary as `12.8`.

The chapter body itself labels:
- PDF page 1105: `12.6.6. Встроенные системы`;
- PDF page 1106: `12.7. Краткие выводы`.

Handling: chapter-body numbering is used in canonical artifacts; the TOC inconsistency is preserved here rather than silently ignored.

## [Source framing] Chapter is intentionally opinionated/speculative

PDF page 1058 explicitly says this chapter is more personal, speculative and controversial than the preceding chapters.

Handling: design preferences are reported as the source's engineering guidance, not converted into timeless universal laws.

## [Needs confirmation] Review question 15 requires benchmarking

The parity macro can be designed from chapter techniques, but the requested speed ratio relative to a loop depends on compiler, CPU, optimization flags and memory hierarchy.

Handling: algorithm/design is answered; measured speedup remains `[Needs confirmation]`.

## [Needs confirmation] Review question 23 asks whether a cost estimate is realistic

The chapter supplies an approximate Windows line-count range and Brooks' productivity heuristic, so a naive numerical estimate can be calculated. Actual Windows 8 development cost is not supplied.

Handling: distinguish the arithmetic estimate from any claim about real Microsoft expenditure.

## [Needs confirmation] Review question 24 depends on current market prices

The chapter asks for a calculation using current RAM prices, but chapter RAG contains no current price dataset.

Handling: provide the formula only; numerical current-market result remains `[Needs confirmation]`.

## [Needs confirmation] Review questions 27–28 require implementation/runtime evidence

- Q27 requires programs plus performance measurements and a crossover point.
- Q28 requires an implemented in-memory filesystem simulator.

Handling: provide source-grounded design/acceptance criteria, but do not fabricate code execution or benchmark results.

## Historical trend boundary

Predictions about cloud systems, many-core processors, large address spaces, mobile/battery systems and embedded systems are preserved in the edition's timeframe. No external modernization is applied under `rag_only`.
