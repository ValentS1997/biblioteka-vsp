# Source findings — приложение Д

## Finding 1 — sample project ID mismatch

Classification: **[Source wording/code mismatch]**

Provenance:
- chunk: `e0036:c02`
- EPUB spine item: `36`
- locator: `OEBPS/Text/978544614112-33.xhtml`

CLI output and shown command use a sample project identifier rendered as:

```text
votohz445ljyg
```

The following prose refers to a visually different identifier:

```text
votohz4451jyg
```

The difference is the `l`/digit-`1` position.

Adjudication: actual intended sample ID `[Needs confirmation]`.

Canonical operational guidance therefore uses `<project-id>`, discovered from the real environment, rather than either sample value.

## Finding 2 — chunk overlap

Classification: **[Source extraction issue]**

Provenance:
- chunk starts: `e0036:c02–c06`

Later chunks contain continuation/repeated fragments from preceding chunks. Adjacent chunks preserve the full diagnostic sequence and no appendix-level semantic loss was detected.
