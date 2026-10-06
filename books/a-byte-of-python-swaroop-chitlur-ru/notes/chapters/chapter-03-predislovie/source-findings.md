# Source findings — глава 3 «Предисловие»

Mode: `rag_only`

## Finding 1 — damaged URL glyph

Classification: **[Source extraction issue]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0024:c01`, PDF page 24,
section 3.4.

RAG variant:

`hp://www.swaroopch.com/notes/Python`

Issue: URL scheme contains an anomalous extracted glyph.

Action: preserve the source-derived variant. Do not silently normalize it or present
it as a verified current URL inside the RAG-only chapter artifacts.

## Finding 2 — suspicious extracted word

Classification: **[Needs confirmation]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0024:c01`, PDF page 24,
section 3.2.

RAG variant:

`...помогли мне значительно улучить книгу.`

Issue: the word `улучить` is unusual in this context and may represent either source
wording or an extraction defect.

Action: do not silently replace it. Exact adjudication requires canonical-source
inspection outside the current `rag_only` workflow.
