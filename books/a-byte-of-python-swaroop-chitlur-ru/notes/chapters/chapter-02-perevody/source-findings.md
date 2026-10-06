# Source findings — глава 2 «Переводы»

Mode: `rag_only`

## Finding 1 — damaged URL glyphs

Classification: **[Source extraction issue]**

Provenance: multiple chunks, including `p0016:c01`, `p0017:c01`,
`p0019:c01`, `p0020:c01`, `p0021:c01`.

Examples preserved in RAG:

- `hp://code.google.com/p/zhpy/wiki/ByteOfZhpy`
- `hp://abop-german.berlios.de`
- `hp://python.or.id/moin.cgi/ByteofPython`
- `hp://www.swaroopch.org/notes/Python_ro`
- `hp://wombat.org.ua/AByteOfPython`

Issue: URL scheme contains an anomalous extracted glyph.

Action: do not silently normalize or present these as verified current URLs.

## Finding 2 — damaged names/words

Classification: **[Source extraction issue]**

Examples:

- `Christoph Zwerske` — `p0017:c01`
- `How to ink Like a Computer Scientist` — `p0018:c01`
- `Daar_Isi` — `p0019:c01`
- `luballons2010` — `p0019:c01`
- `ﬁdel`, `uniﬁ` — `p0019:c01`
- `Gustavo Eeverria` — `p0021:c01`
- `burk` — `p0022:c01`

Issue: ligatures/private-use glyphs or extraction substitutions are present.

Action: preserve the source-derived variants; exact normalization requires separate
source verification outside this RAG-only workflow.

## Finding 3 — Slovak/Bulgarian mismatch

Classification: **[Source contradiction]**

Provenance: `p0021:c01`, subsection 2.1.19.

Variant A:
- heading: `2.1.19 Словацкий`
- text: Albertio Ward is stated to have translated the book into Slovak.

Variant B:
- quoted motivation says the translation was made to help `болгарам` understand
  the book and refers to the population of the translator's country.

Issue: language identity inside the same subsection is inconsistent.

Action: preserve both variants. Do not choose Slovak or Bulgarian as the corrected
interpretation from model memory or external sources.

## Finding 4 — Greek line punctuation

Classification: **[Source extraction issue]**

Provenance: `p0018:c01`, subsection 2.1.8.

RAG variant:

`Греческое сообщество Ubuntu перевело книгу на греческий язык), ...`

Issue: unmatched closing parenthesis after `язык`.

Impact: minor; does not change the core statement.
