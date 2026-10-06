# Source findings — глава 3 «Неформально о синтаксисе Go»

## Finding 1 — inconsistent delimiters in grouped const/iota example

Classification: **[Source code mismatch]**

Provenance:

- PDF page 75
- RAG chunk `p0075:c01`

Observed source variants in the same subsection:

Earlier example:

```go
const (
   red = iota
   blue
   green
)
```

Later example:

```go
const {
   a, b = iota, iota;
}
```

The source therefore presents two different delimiter forms for what it describes as grouped `const` declarations.

Impact:

- The canonical syntax for the second example cannot be adjudicated under `rag_only` policy from this chapter artifact alone.
- The second variant must not be silently normalized.

Action:

- preserve both variants as source evidence;
- mark the second form as a source code mismatch;
- external/specification adjudication: **[Needs confirmation]**.

## Finding 2 — wording/typo noise in type discussion

Classification: **[Source wording/code mismatch]**

Provenance:

- PDF page 70
- RAG chunk `p0070:c01`

Observed:

The paragraph contains both `float64` and the token `floaf64` later in the same discussion.

Impact:

This is treated as source wording/code noise. No technical correction is injected into canonical chapter artifacts.

Action:

- use the clearly repeated `float64` spelling when referring to the source example elsewhere;
- retain this finding instead of silently treating every source token as intentional.
