# Source findings — глава 6 «Первые шаги»

Mode: `rag_only`

## Finding 1 — Hello World casing variants

Classification: **[Source wording/code mismatch]**

Provenance:
- `a-byte-of-python-swaroop-chitlur-ru:p0035:c01`, PDF page 35;
- `a-byte-of-python-swaroop-chitlur-ru:p0036:c01`, PDF page 36.

Variant A in explanatory text:

```python
print('Hello World')
```

Variant B in the captured interpreter session:

```python
print('hello world')
```

Corresponding output is also lowercase in the session example.

Issue: casing differs between the prose instruction and the displayed interpreter session.

Action: preserve both variants; do not silently normalize them into one canonical example.

## Finding 2 — extraction glyph in chmod footnote

Classification: **[Source extraction issue]**

Provenance: `p0039:c01`, PDF page 39.

RAG variant:

`ange mode`

Issue: first character of the English phrase in the translator footnote is damaged.

Impact: does not change the source explanation that `chmod` changes file mode.

## Finding 3 — historical/editor references

Classification: **[Needs confirmation]**

Provenance: `p0035:c01`–`p0037:c01`.

Source references include:

- `Python 3.0` Start-menu path for IDLE;
- Komodo Edit as the beginner recommendation;
- external Vim/Emacs introductions/plugins/configuration.

Issue: the chapter establishes these as historical source recommendations, not their
current availability or applicability.

Action: retain as book content; current applicability is outside `rag_only`.

## Finding 4 — source-specific PATH/user directories

Classification: **[Needs confirmation]**

Provenance: `p0040:c01`, PDF page 40.

Examples:

- `/home/swaroop/bin`
- `/home/swaroop/mydir`

Issue: these paths are explicitly tied to the author's source environment.

Action: do not treat them as valid paths for another system without confirmation.
