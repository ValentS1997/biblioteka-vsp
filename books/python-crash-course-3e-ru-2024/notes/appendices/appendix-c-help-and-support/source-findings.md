# Source findings — приложение В

## Finding 1 — Stack Overflow spelling/domain typo

Classification: **[Source wording/code mismatch]**

Provenance:
- chunk: `e0034:c02`
- EPUB spine item: `34`
- locator: `OEBPS/Text/978544614112-31.xhtml`

Source text names:

```text
Stack Overlow
http://stackoverlow.com/
```

The surrounding prose clearly discusses the well-known programming Q&A resource under that spelling, but canonical artifacts do not silently rewrite source text in RAG-only mode.

Adjudication/correct current spelling or URL: `[Needs confirmation]`.

## Finding 2 — chunk overlap

Classification: **[Source extraction issue]**

Provenance:
- chunk starts: `e0034:c02–c03`

Both later chunks begin with continuation/repeated text from the preceding chunk. Adjacent chunks preserve continuity and no appendix-level semantic loss was detected.
