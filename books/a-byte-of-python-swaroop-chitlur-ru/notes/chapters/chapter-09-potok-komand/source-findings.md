# Source findings — глава 9 «Поток команд»

Mode: `rag_only`

## Finding 1 — while.py code/output wording mismatch

Classification: **[Source wording/code mismatch]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0062:c01`, PDF page 62.

Code messages:

- `Нет, загаданное число немного больше этого`
- `Нет, загаданное число немного меньше этого.`

Displayed output:

- `Нет, число несколько больше.`
- `Нет, число несколько меньше.`

Issue: source code strings and shown output are not textually identical.

Action: preserve both variants; do not silently rewrite code or output.

## Finding 2 — if.py success punctuation mismatch

Classification: **[Source wording/code mismatch]**

Provenance:
- `p0059:c01` code;
- `p0060:c01` output.

Code variant:

`(хотя и не выиграли никакого приза!)`

Displayed output variant:

`(хотя и не выиграли никакого приза.)`

Issue: ending punctuation differs.

Action: preserve both source variants.

## Finding 3 — range wording

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0063:c01`, section 9.3.

Source says both that:

- `range(1,5) даёт последовательность [1, 2, 3, 4]`;
- `range() генерирует ... только по одному числу за раз`;
- `list(range())` can be used to see the full sequence.

Issue: these descriptions mix a conceptual sequence representation with execution/runtime
wording.

Action: preserve source framing; do not restate it as a current verified implementation
model outside the RAG-only workflow.

## Finding 4 — Boolean equivalence statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0063:c01`.

RAG/source statement:

`True и False ... вы можете считать их эквивалентными значениям 1 и 0 соответственно.`

Action: retain as source teaching statement. Current semantic nuance is not externally
verified in this chapter workflow.
