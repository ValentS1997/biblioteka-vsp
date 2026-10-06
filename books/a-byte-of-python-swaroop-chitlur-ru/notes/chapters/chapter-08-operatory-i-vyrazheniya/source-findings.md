# Source findings — глава 8 «Операторы и выражения»

Mode: `rag_only`

## Finding 1 — damaged translator footnote

Classification: **[Source extraction issue]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0055:c01`, PDF page 55.

RAG variant:

`“False” - англ. “«ибочно (Ложь)».`

Issue: beginning of the translated word is damaged/missing in extraction/source variant.

Action: preserve the variant; do not silently normalize the exact wording.

## Finding 2 — comparison-table claim

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0055:c01`, operator `>` row.

RAG/source statement says that when both operands are numbers they are converted to the
same type before comparison; otherwise it `всегда возвращается False`.

Issue: this is a strong behavioral claim. Current correctness is not established inside
the chapter workflow.

Action: retain as source content only. Do not upgrade it to a current verified Python rule
without external verification.

## Finding 3 — associativity notation

Classification: **[Source wording/code mismatch]**

Provenance: `p0058:c01`, section 8.4.

RAG variant:

`a = b = c рассматривается как a = (b = c)`

Issue: the parenthesized form is presented as an explanatory representation of
right-to-left associativity. The chapter does not separately establish it as executable
Python syntax.

Action: preserve the wording as conceptual source notation; do not present
`a = (b = c)` as a verified executable example.

## Finding 4 — precedence table extraction layout

Classification: **[Source extraction issue]**

Provenance: `p0057:c01`, section 8.2.

Issue: the precedence table is flattened into text and one row begins with a visually
misaligned footnote marker before `(выражения, ...)`.

Impact: operator names remain mostly recoverable, but exact table layout should not be
reconstructed beyond what RAG supports.
