# Commands and tasks — глава 19 «Что дальше»

## Source command status

Chapter 19 does **not** provide a canonical executable implementation or concrete shell
command for its two main exercises.

Do not synthesize a `replace` CLI, `pip install ...` command, address-book script or
filesystem mutation command into the canonical chapter artifacts.

## Task 1 — address book

Source requirements:

```text
command-line address book
- view
- add
- modify
- delete
- search
- persist data on disk
```

Source hint maps the design to:

```text
class → contact object
dict → contacts keyed by name
pickle → persistent storage
dict methods → add/change/delete
```

Classification: future implementation would be **state-changing / persistent**.

Unknowns:

- file path: [Needs confirmation]
- serialization format details beyond source `pickle` hint: [Needs confirmation]
- conflict/update policy: [Needs confirmation]
- rollback/recovery: [Needs confirmation]

## Task 2 — replace

Source requirement:

```text
replace one string with another in a list of supplied files
```

Optional complexity mentioned by source:

- literal string replacement;
- pattern/regular-expression search.

Classification: future implementation would be **state-changing filesystem operation**.

Unknowns:

- CLI syntax: [Needs confirmation]
- target files: [Needs confirmation]
- encoding: [Needs confirmation]
- backup strategy: [Needs confirmation]
- atomic-write behavior: [Needs confirmation]
- regex/literal semantics: [Needs confirmation]

## Package installation

Section 19.9 says libraries from the Python package catalog can be installed with
`pip`.

No concrete package name or complete `pip` command is provided.

Do not synthesize one.

## GUI tools named by source

- Kivy
- PyGTK
- PyQt
- wxPython

These are references, not commands.

## Python implementations named by source

- CPython
- Jython
- IronPython
- PyPy
- Stackless Python
- CLPython
- IronMonkey

These are source-described implementations; chapter provides no installation/run
commands.

## Rollback

No canonical state-changing command is present in chapter 19 itself.

Rollback for any later implementation remains **[Needs confirmation]** until its design
is explicit.
