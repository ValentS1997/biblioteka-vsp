# Source findings — глава 1 «Обложка»

Mode: `rag_only`

Ниже фиксируются дефекты извлечённого текстового слоя. Они не исправляются молча и
не разрешаются по внешним источникам.

## Finding 1

Classification: **[Source extraction issue]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0013:c01`, PDF page 13.

RAG variant:

`Creative Commons Aribution-Share Alike 3.0 Unported`

Issue: в слове названия лицензии присутствует аномальный извлечённый символ ``.

Action: сохранять как source-derived variant; точное написание требует визуальной
проверки canonical source, которая запрещена текущим `rag_only` chapter workflow.

## Finding 2

Classification: **[Source extraction issue]**

Provenance: `p0013:c01`, PDF page 13.

RAG variant:

`hp://www.swaroopch.com/notes/Python`

Issue: схема URL содержит тот же аномальный извлечённый символ.

Action: не нормализовать URL молча и не использовать его как проверенную ссылку.

## Finding 3

Classification: **[Source extraction issue]**

Provenance: `p0011:c01` and `p0012:c01`.

Examples preserved in RAG:

- `MaGallivan`
- `StackOverﬂow`
- `cﬂ` inside an obfuscated e-mail fragment

Issue: текстовый слой содержит повреждения/лигатуры в отдельных именах и строках.

Impact: не влияет на главную логику главы, но точные имена/адреса нельзя считать
нормализованными без отдельной source verification.
