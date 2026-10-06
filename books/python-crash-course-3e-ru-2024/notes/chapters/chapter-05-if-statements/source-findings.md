# Source findings — глава 5

## Finding 1 — chunk-boundary clipping

Classification: **[Source extraction issue]**

Provenance:

- EPUB spine item: `14`
- locator: `OEBPS/Text/978544614112-11.xhtml`
- affected starts observed: `e0014:c02`–`e0014:c11`

Observed boundaries include duplicated/partial starts such as `два значения...`, `кольких условий...`, `черный список...`, `ыполняются...`, `thon выполняет...`, `но условие...`, continuation text from exercise 5.4, `eese']...`, `g your pizza!...` and `thon; они...`.

Cross-check:

- adjacent preceding chunks preserve the transition context;
- all major sections remain readable in ordered range `c01–c11`;
- exercises 5.1–5.13 are present;
- chapter-end summary is present;
- boundary to chapter 6 is confirmed by `e0015:c01`;
- no semantic loss was detected.

Adjudication: exact extractor/chunker cause is `[Needs confirmation]`.

Policy action:

- keep legacy RAG unchanged during chapter work;
- do not silently rewrite chunk contents;
- re-check chunk boundaries during a future controlled RAG rebuild.
