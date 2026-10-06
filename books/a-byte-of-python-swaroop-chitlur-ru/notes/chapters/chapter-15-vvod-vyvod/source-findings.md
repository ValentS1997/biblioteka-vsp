# Source findings — глава 15 «Ввод-вывод»

Mode: `rag_only`

## Finding 1 — file-class wording in Python 3 framing

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0122:c01`, PDF page 122,
section 15.2.

Source wording:

`Открывать и использовать файлы ... можно путём создания объекта класса file`

Issue: this is a concrete terminology/runtime statement inside a chapter whose
execution commands use `python3`.

Action: preserve as source wording only; do not silently modernize the terminology.

## Finding 2 — missing homework reference target

Classification: **[Source reference gap]**

Provenance: `p0122:c01`, homework hint.

Source says a list of punctuation marks can be found `здесь`, but no URL/reference
target is present in the RAG text.

Action: do not invent or reconstruct the missing link.

## Finding 3 — pickle “any Python object” claim

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0124:c01`, section 15.3.

Source states that the standard `pickle` module can save `любой объект Python` to a
file and later restore it.

Issue: this is a broad capability claim whose limits are not established in this chapter.

Action: retain as source framing; canonical examples stay limited to the shown shopping
list.

## Finding 4 — read-handle close omission in pickling example

Classification: **[Source code omission]**

Provenance: `p0124:c01`–`p0125:c01`.

The source example explicitly closes the write handle after `pickle.dump`, but after
opening `shoplist.data` with `'rb'` and calling `pickle.load`, no corresponding
`f.close()` is shown before the example ends.

Action: preserve the source code as given; do not silently add a close statement to the
canonical example.

## Finding 5 — blank final chapter page

Classification: **[Source layout note]**

Provenance: `p0126:c01`, PDF page 126.

The chunk contains only:

`118 Глава 15. Ввод-вывод`

Action: keep it inside the verified chapter boundary because chapter 16 starts on PDF
page 127, while recording that substantive chapter content ends on PDF page 125.
