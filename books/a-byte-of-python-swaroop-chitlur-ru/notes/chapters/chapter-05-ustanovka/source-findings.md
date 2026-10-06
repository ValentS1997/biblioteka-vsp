# Source findings — глава 5 «Установка»

Mode: `rag_only`

## Finding 1 — damaged Python download URL

Classification: **[Source extraction issue]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0032:c01`, PDF page 32,
section 5.2.

RAG variant:

`hp://www.python.org/download/`

Issue: URL scheme contains an anomalous extracted glyph.

Action: do not silently normalize or present it as a verified current URL.

## Finding 2 — command/error casing mismatch

Classification: **[Source wording/code mismatch]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0031:c01`, PDF page 31,
section 5.1.

Command shown:

```text
python -V
```

Example failure output shown:

```text
bash: Python: command not found
```

Issue: command token is lowercase `python`, while the displayed error names
uppercase `Python`.

Action: preserve both source variants. Do not silently rewrite the output.

## Finding 3 — historical paths/commands require current applicability check

Classification: **[Needs confirmation]**

Provenance: `p0032:c01` and `p0033:c01`.

Examples:

- `C:\Python33`
- `C:\AUTOEXEC.BAT`
- `AUTOEXEC.NT`
- `ruby -e "$(curl -fsSkL raw.github.com/mxcl/homebrew/go)"`

Issue: these are explicitly source-grounded historical installation instructions, but
the chapter itself does not establish their applicability to a current system.

Action: retain as book content; do not promote to current operational recommendation
without separate verification outside `rag_only`.
