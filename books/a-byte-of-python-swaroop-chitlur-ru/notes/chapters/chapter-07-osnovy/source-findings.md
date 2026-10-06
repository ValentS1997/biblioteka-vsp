# Source findings — глава 7 «Основы»

Mode: `rag_only`

## Finding 1 — malformed quote in comment examples

Classification: **[Source wording/code mismatch]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0043:c01`, PDF page 43,
section 7.1.

RAG variants:

```python
print('Привет, Мир!) # print -- это функция
```

and:

```python
# print -- это функция
print('Привет, Мир!)
```

Issue: the displayed `print` string lacks a closing single quote before `)`.

Action: preserve the extracted/source variant and do not silently repair the code in
canonical chapter artifacts.

## Finding 2 — StackOverflow ligature

Classification: **[Source extraction issue]**

Provenance: `p0044:c01`, PDF page 44, section 7.4.

RAG variant:

`StackOverﬂow`

Issue: ligature glyph appears in the extracted word.

Action: do not silently normalize exact source wording.

## Finding 3 — interpreter command variants

Classification: **[Source wording/code mismatch]**

Provenance:
- `p0046:c01`, section 7.4.6;
- `p0048:c01`, standard execution procedure;
- `p0049:c01`, section 7.8.1 output.

Variants:

- `python str_format.py`
- `python3 program.py`
- `python var.py`

Issue: chapter alternates between `python` and `python3`.

Action: preserve each source command in its own context; do not normalize to one executable.

## Finding 4 — suspicious editor sentence

Classification: **[Needs confirmation]**

Provenance: `p0051:c01`, PDF page 51, section 7.10.

RAG variant:

`Хорошие редакторы, такие как Komodo Edit, буду делать это автоматически.`

Issue: wording `буду делать` appears grammatically anomalous in context.

Action: leave unchanged; exact adjudication requires canonical-source inspection outside
the current `rag_only` workflow.
