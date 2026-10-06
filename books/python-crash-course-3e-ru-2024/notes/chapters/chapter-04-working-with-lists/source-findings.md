# Source findings — глава 4

## Finding 1 — chunk-boundary clipping

Classification: **[Source extraction issue]**

Provenance:

- EPUB spine item: `13`
- locator: `OEBPS/Text/978544614112-10.xhtml`
- affected chunks observed: `e0013:c02`, `c03`, `c08`, `c10`, `c11`, `c12`, `c13`

Observed starts include incomplete fragments such as `енной переменной...`, `yone. That was...`, `з начинается...`, `nd_pizzas...`, `dimensions:"...`, `, чтобы редактор...` and `ой главе...`.

Cross-check:

- adjacent preceding chunks preserve the missing transition context;
- exercises 4.1–4.15 remain available;
- chapter-end summary remains available across `c12–c13`;
- chapter boundary to `e0014:c01` is intact;
- no semantic loss was found when reading the complete ordered range `e0013:c01–c13`.

Adjudication: the exact extractor/chunker cause is `[Needs confirmation]`.

Policy action:

- keep the legacy RAG unchanged during chapter work;
- do not silently rewrite chunk text;
- verify chunk starts/ends during a future controlled RAG rebuild.
