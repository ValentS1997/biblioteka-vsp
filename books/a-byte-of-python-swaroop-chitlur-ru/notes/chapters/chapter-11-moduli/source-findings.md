# Source findings — глава 11 «Модули»

Mode: `rag_only`

## Finding 1 — using_sys interpreter command variants

Classification: **[Source wording/code mismatch]**

Provenance:
- `a-byte-of-python-swaroop-chitlur-ru:p0079:c01`, PDF page 79;
- `p0080:c01`, PDF page 80.

Displayed execution:

`python3 using_sys.py we are arguments`

Explanatory prose variant:

`python using_sys.py we are arguments`

Issue: source alternates between `python3` and `python` for the same example.

Action: preserve both variants; do not normalize.

## Finding 2 — from math import * example style/version mismatch

Classification: **[Source wording/code mismatch]**

Provenance: `p0081:c01`–`p0082:c01`, section 11.2.

RAG/source example ends with:

```python
print p
```

while the surrounding book/chapter commonly uses function-call form `print(...)`.

Issue: style/syntax presentation differs from the surrounding Python 3 framing.

Action: retain as source variant; do not silently rewrite it.

## Finding 3 — .pyc placement claim

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0081:c01`, section 11.1.

Source statement says `.pyc` files are usually created in the same directory as their
corresponding `.py` files and are not created if Python cannot write there.

Issue: exact cache/file layout is version/runtime dependent and is not externally verified
in this workflow.

Action: preserve as historical source teaching statement.

## Finding 4 — sys.path / PYTHONPATH wording

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0080:c01`.

Source explains the first empty `sys.path` entry as current directory and then says it
`совпадает со значением переменной окружения PYTHONPATH`.

Issue: this is a strong environment/path statement whose current semantics are not
verified in the RAG-only workflow.

Action: retain only as source framing.

## Finding 5 — dir('print') wording

Classification: **[Source wording/code mismatch]**

Provenance: `p0085:c01`, section 11.5.

RAG/source says:

`dir('print')`, чтобы увидеть атрибуты функции print

Issue: argument shown is a string literal `'print'`, while the prose labels it as the
function `print`.

Action: preserve both code and wording; do not silently replace with `dir(print)`.

## Finding 6 — package definition is source-historical

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0085:c01`–`p0086:c01`, section 11.6.

Source defines packages as directories with modules and a special `__init__.py`.

Action: preserve as the book's package model. Current packaging/import nuances are
outside this `rag_only` analysis.
