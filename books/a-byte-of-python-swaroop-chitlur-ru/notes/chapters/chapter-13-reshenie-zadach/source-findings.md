# Source findings — глава 13 «Решение задач»

Mode: `rag_only`

## Finding 1 — backup_ver2 indentation/output mismatch

Classification: **[Source wording/code mismatch]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0103:c01`, PDF page 103.

RAG/source code shows:

```python
if not os.path.exists(today):
    os.mkdir(today)
print('Каталог успешно создан', today)
```

Displayed runs show the message `Каталог успешно создан ...` only on the first run,
not on the second.

Issue: if the displayed indentation is taken literally, the print would be outside the
conditional and would be expected on both runs.

Action: preserve code/output as extracted. Do not silently re-indent the canonical source
variant.

## Finding 2 — zip availability claim

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0099:c01`, section 13.1.

Source says standard command `zip` is available by default in any standard GNU/Linux
distribution.

Issue: availability is environment/distribution dependent and not verified in this
`rag_only` workflow.

Action: treat `zip` as an external dependency requiring confirmation.

## Finding 3 — os.sep Mac OS separator claim

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0101:c01`, section 13.2.

Source states `os.sep` is `/` on GNU/Linux/Unix, `\` on Windows and `:` on Mac OS.

Issue: exact platform statement is historical/current-runtime-sensitive.

Action: preserve as source claim only.

## Finding 4 — os.system result-code statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0102:c01`.

Source says `os.system` returns 0 for success and otherwise an error code.

Issue: exact semantics/platform interpretation are not externally verified in this
workflow.

Action: preserve the chapter's control-flow assumption without promoting it to universal
current guidance.

## Finding 5 — zipfile ligature extraction

Classification: **[Source extraction issue]**

Provenance: `p0107:c01`, section 13.6.

RAG variant:

`zipﬁle`

Issue: ligature glyph `ﬁ` appears in the module name in prose.

Action: exact source variant is preserved in findings; canonical concept may be referred
to as the source-named standard module `zipfile`.

## Finding 6 — version 3 syntax error is intentional

Classification: **[Intentional negative example]**

Provenance: `p0104:c01`–`p0105:c01`.

The source explicitly says the next program does not work and uses the failure to teach
debugging. The shown `SyntaxError: invalid syntax` is therefore not treated as an
accidental source defect.
