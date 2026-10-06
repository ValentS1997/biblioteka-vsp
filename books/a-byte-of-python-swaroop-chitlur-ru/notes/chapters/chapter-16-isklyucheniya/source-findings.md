# Source findings — глава 16 «Исключения»

Mode: `rag_only`

## Finding 1 — “syntax error” wording vs NameError output

Classification: **[Source wording/code mismatch]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0127:c01`, PDF page 127,
section 16.1.

Source prose calls the mistyped call:

`Print('Привет, Мир!')`

a syntax error.

Displayed traceback ends with:

`NameError: name 'Print' is not defined`

Issue: prose classification and shown exception type differ.

Action: preserve both; do not silently correct the source narrative.

## Finding 2 — try requires except statement conflicts with later try/finally

Classification: **[Source internal contradiction]**

Provenance:
- `p0129:c01`, section 16.3;
- `p0130:c01`, section 16.5.

Section 16.3 says every `try` must have at least one corresponding `except`.
Section 16.5 then demonstrates a `try ... except ... finally` example and frames
`finally` as the cleanup mechanism; the wording in 16.3 is broader than the later
chapter structure supports.

Action: record the contradiction without replacing either source statement with external
language rules.

## Finding 3 — finally.py depends on prior poem.txt

Classification: **[Source dependency gap]**

Provenance: `p0130:c01`, section 16.5.

The example opens:

`open('poem.txt')`

but chapter 16 does not create that file. The file was created by an earlier chapter
example, but standalone chapter execution does not establish its presence.

Action: mark `poem.txt` existence **[Needs confirmation]** before standalone execution.

## Finding 4 — finally cleanup assumption if open fails

Classification: **[Source technical caveat / Needs confirmation]**

Provenance: `p0130:c01`.

Source places `f = open('poem.txt')` inside `try` and calls `f.close()` in
`finally`.

Issue: the chapter does not discuss the path where resource acquisition itself fails
before the variable is assigned.

Action: preserve source code as written; do not silently restructure it.

## Finding 5 — context-manager protocol wording / ligature

Classification: **[Source extraction/wording issue]**

Provenance: `p0131:c01`, section 16.6.

RAG/source introduces a hypothetical object name as:

`theﬁle`

while the following method names use `thefile.__enter__` and
`thefile.__exit__`.

Issue: ligature `ﬁ` and inconsistent rendering of the same illustrative name.

Action: preserve the source anomaly in findings; canonical concept remains the
`__enter__` / `__exit__` protocol described by the source.

## Finding 6 — broad bare-except statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0128:c01`, section 16.3.

Source says that when no error/exception name is specified in an `except` expression,
all errors and exceptions will be handled.

Action: retain as source teaching statement only; exact modern semantics are outside the
RAG-only workflow.
