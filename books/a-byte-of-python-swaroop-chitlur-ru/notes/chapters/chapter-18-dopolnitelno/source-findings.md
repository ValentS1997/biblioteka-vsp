# Source findings — глава 18 «Дополнительно»

Mode: `rag_only`

## Finding 1 — special-method table extraction corruption

Classification: **[Source extraction issue]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0138:c01`, PDF page 138,
section 18.2.

RAG table contains corrupted forms such as:

- `__del__(sel)`
- `__str__(sel)`
- `__len__(sel)`

Issue: the `self` token is corrupted by an extraction/font ligature artifact.

Action: canonical concept uses the method names and intended `self` parameter, while
the extraction anomaly is preserved here.

## Finding 2 — exec input wording

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0140:c01`, section 18.7.

Source says `exec` executes Python commands contained in a string or file.

Issue: this is a broad API/input-form statement whose exact current calling semantics
are not established in this `rag_only` workflow.

Action: canonical example remains limited to the shown string form:

`exec('print("Здравствуй, Мир!")')`.

## Finding 3 — exec/eval execution boundary

Classification: **[Source operational risk]**

Provenance: `p0140:c01`–`p0141:c01`.

Source explicitly describes:

- `exec` as executing Python program text;
- `eval` as evaluating Python expressions stored in strings.

Impact: runtime effect depends on the supplied code/expression.

Action: only fixed source-known strings are used in canonical examples; unverified
runtime strings are outside the safe chapter workflow.

## Finding 4 — repr round-trip generalization

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0141:c01`, section 18.9.

Source states:

`в большинстве случаев eval(repr(object)) == object`

The demonstrated object is a list containing `'item'`.

Issue: the prose generalizes beyond the shown example.

Action: canonical acceptance is limited to the demonstrated list round-trip.

## Finding 5 — raw-string “no special processing” wording

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0142:c01`, section 18.11.

Source describes prefix `r` / `R` as producing a string in which no special
processing such as escape-sequence handling occurs.

Issue: this is a broad language-semantics formulation not further qualified in the
chapter.

Action: preserve as source framing; canonical example remains
`r"Перевод строки обозначается \n"`.

## Finding 6 — assert recommendation is source guidance

Classification: **[Source guidance]**

Provenance: `p0141:c01`, section 18.8.

Source recommends using `assert` prudently and says that in many cases exception
handling plus user-facing error handling is preferable.

Action: preserve as author guidance; no external policy or current best-practice claim
is added.

## Finding 7 — blank final chapter page

Classification: **[Source layout note]**

Provenance: `p0144:c01`, PDF page 144.

The chunk contains only the running footer:

`136 Глава 18. Дополнительно`

Action: keep it inside the verified chapter boundary because chapter 19 begins at
PDF page 145, while recording that substantive content ends at PDF page 143.
