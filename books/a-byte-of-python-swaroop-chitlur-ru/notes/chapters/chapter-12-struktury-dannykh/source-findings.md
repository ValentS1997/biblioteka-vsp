# Source findings — глава 12 «Структуры данных»

Mode: `rag_only`

## Finding 1 — dict.items() return-type statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0092:c01`, PDF page 92,
section 12.4.

Source wording says method `items`:

`возвращает список кортежей`

Issue: this is a concrete runtime/type claim inside a book otherwise framed around
Python 3. Current semantics are not externally verified in this workflow.

Action: retain as source teaching statement only.

## Finding 2 — dictionary ordering statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0091:c01`, section 12.4.

Source says key/value pairs are not ordered and recommends separately sorting when order
is required.

Issue: exact ordering semantics are version-dependent/current-runtime-sensitive and are
not externally verified here.

Action: preserve as historical source framing.

## Finding 3 — dictionary key rule wording

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0091:c01`.

Source first says dictionary keys may use only immutable objects, then adds:

`Точнее говоря, в качестве ключей должны использоваться только простые объекты.`

Issue: this is a strong/general rule phrased with source terminology `простые объекты`;
the chapter does not define a precise runtime criterion beyond that wording.

Action: retain without replacing it with a modern generalized rule.

## Finding 4 — set output versus unordered definition

Classification: **[Source presentation caveat]**

Provenance:
- `p0095:c01`, definition of set;
- `p0096:c01`, REPL output.

Source defines sets as `неупорядоченные наборы` and then displays one concrete set
representation after intersection.

Action: treat the displayed representation as example output only; do not infer a
guaranteed element order.

## Finding 5 — full-slice copy recommendation breadth

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0097:c01`, section 12.7.

Source says that to copy a list, similar sequence, or `другого сложного объекта`, one
should use slicing.

Issue: the example specifically demonstrates a list/full-slice copy, while the wording
is broader than the demonstrated operation.

Action: preserve the broad wording as source claim but keep canonical operational example
limited to the shown list/sequence slice.

## Finding 6 — join translator-footnote punctuation

Classification: **[Source extraction/wording issue]**

Provenance: `p0098:c01`, translator footnote 3.

RAG variant:

`join – англ. «объединять’»`

Issue: closing punctuation/quote is inconsistent.

Impact: does not affect the described `join` behavior.
