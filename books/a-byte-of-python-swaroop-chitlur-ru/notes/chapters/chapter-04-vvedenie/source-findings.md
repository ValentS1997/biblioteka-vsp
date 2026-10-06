# Source findings — глава 4 «Введение»

Mode: `rag_only`

## Finding 1 — FLOSS extraction glyph

Classification: **[Source extraction issue]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0028:c01`, PDF page 28,
section 4.1.3.

RAG variant:

`Free/Libré and Open Source Soware`

Issue: в слове `Software` присутствует аномальный извлечённый glyph ``.

Action: сохранить source-derived вариант и не нормализовать молча.

## Finding 2 — suspicious word in section 4.2

Classification: **[Needs confirmation]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0030:c01`, PDF page 30,
section 4.2.

RAG variant:

`Если вас не интересует разница между Python 2 и Python 3, вы можете пропустить этот радел.`

Issue: слово `радел` выглядит аномально в контексте; по RAG нельзя надёжно определить,
является ли это ошибкой исходного текста или extraction defect.

Action: не заменять автоматически.

## Finding 3 — compacted platform list

Classification: **[Source extraction issue]**

Provenance: `p0028:c01`, section 4.1.5.

RAG variant:

`Amiga,AROS`

Issue: отсутствует пробел после запятой в перечне платформ.

Impact: не влияет на концептуальную мысль о портируемости.
