# Source findings — глава 17 «Стандартная библиотека»

Mode: `rag_only`

## Finding 1 — “только Python 3.0” wording vs major-version condition

Classification: **[Source wording/code mismatch]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0134:c01`, PDF page 134,
section 17.1.

Source prose says the example can ensure that the program will run
`только в Python 3.0`.

Code condition:

```python
if sys.version_info[0] < 3:
```

Issue: the code distinguishes major versions below 3 from major versions 3 or above,
which is broader than the exact wording “только ... 3.0”.

Action: preserve both source forms; do not silently reconcile them.

## Finding 2 — historical interpreter/output variants

Classification: **[Source historical variant]**

Provenance: `p0134:c01`.

Source explicitly runs:

```text
python2.7 versioncheck.py
python3 versioncheck.py
```

The shown warning output also contains historical formatting around `RuntimeWarning`.

Action: preserve these as source examples; do not treat Python 2.7 availability or exact
warning rendering as a current environment expectation.

## Finding 3 — environment-variable logging path dependency

Classification: **[Source dependency gap]**

Provenance: `p0134:c01`–`p0135:c01`, section 17.2.

Source constructs the log path from:

- Windows: `HOMEDRIVE` + `HOMEPATH`;
- other branch: `HOME`.

Issue: the chapter does not discuss absent/unset environment variables.

Action: resolved environment values and resulting `logging_file` are
**[Needs confirmation]** before real-system use.

## Finding 4 — logging file overwrite side effect

Classification: **[Source operational risk]**

Provenance: `p0135:c01`.

Source configuration uses:

```python
filename=logging_file,
filemode='w',
```

Issue: the example is filesystem state-changing and may overwrite an existing
`test.log` target.

Action: confirm target path and overwrite intent before execution. Source rollback is
not provided.

## Finding 5 — platform detection statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0135:c01`.

Source uses:

```python
platform.platform().startswith('Windows')
```

as the branch for Windows vs other platforms.

Action: retain as the book's implementation pattern. Current cross-platform robustness
is outside this `rag_only` workflow.

## Finding 6 — further-study references lack explicit URL in RAG

Classification: **[Source reference gap]**

Provenance: `p0136:c01`, section 17.3.

Source recommends Doug Hellmann's «Модуль недели» and official Python documentation,
but the RAG chunk does not include explicit URLs.

Action: preserve the named references; do not synthesize links in canonical artifacts.
