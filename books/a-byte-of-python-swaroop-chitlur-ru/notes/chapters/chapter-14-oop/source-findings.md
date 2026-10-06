# Source findings — глава 14 «Объектно-ориентированное программирование»

Mode: `rag_only`

## Finding 1 — abstract example filename/output command mismatch

Classification: **[Source wording/code mismatch]**

Provenance:
- `a-byte-of-python-swaroop-chitlur-ru:p0119:c01`, PDF page 119;
- `p0120:c01`, PDF page 120.

Source file header:

```text
# Filename: inherit_abc.py
```

Displayed output block:

```text
$ python3 inherit.py
```

Issue: the execution command names the earlier inheritance example rather than the
abstract-base-class filename.

Action: preserve both variants; do not silently replace either.

## Finding 2 — shebang/interpreter variant

Classification: **[Source wording/code mismatch]**

Provenance: `p0119:c01`.

Source shebang:

```text
#!/usr/bin/env python
```

while surrounding chapter execution examples use `python3`.

Action: retain source variant without normalization.

## Finding 3 — __del__ lifecycle statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0115:c01`, section 14.5.

Source says `__del__` is called when the object is no longer used and its memory is
returned to the operating system, while also noting that the exact moment is not known.

Issue: exact object-finalization/lifetime semantics are runtime-sensitive and are not
externally verified in this RAG-only workflow.

Action: preserve as source teaching statement only.

## Finding 4 — public/private/virtual statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0115:c01`.

Source note states that all class members are public and methods virtual, with names
starting in double underscore treated as private.

Issue: this is a broad language-semantics statement using C++/Java/C# terminology.

Action: preserve as historical source framing; do not upgrade to current verified rule.

## Finding 5 — base __init__ automatic-call statement

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0118:c01`, section 14.6.

Source says Python does not call the base-class constructor automatically and that it
must be called explicitly.

Issue: phrasing is broad; exact behavior depends on the class initialization pattern
being used.

Action: retain in the context of the shown explicit `SchoolMember.__init__(self, ...)`
example only.

## Finding 6 — metaclass section editorial note

Classification: **[Source editorial note]**

Provenance: translator footnote on `p0118:c01`.

The translator states that the metaclass section was invisible to readers in the
original version because it was inside a comment marked by the author as too sudden an
introduction.

Action: keep section 14.7 because it is present in this Russian source/RAG boundary,
while recording the editorial provenance.
