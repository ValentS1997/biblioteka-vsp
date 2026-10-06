# Source findings — глава 19 «Что дальше»

Mode: `rag_only`

## Finding 1 — external-resource references are mostly names without URLs

Classification: **[Source reference gap]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0146:c01`–`p0150:c01`.

The chapter names many external resources, including Stack Overflow, PLEAC, Rosetta Code,
java2s, Python Cookbook, Module of the Week, PyVideo, python-tutor, Planet Python,
GUI resources and functional-programming materials.

Most references appear in RAG as names/titles without explicit target URLs.

Action: preserve names only; do not synthesize links in canonical artifacts.

## Finding 2 — Kivy URL extraction corruption

Classification: **[Source extraction issue]**

Provenance: `p0147:c01`, section 19.10.

RAG variant:

`hp://kivy.org`

Issue: the URL scheme is corrupted by font/extraction glyph substitution.

Action: retain the anomaly here; canonical artifacts identify Kivy by name only.

## Finding 3 — GUI toolkit descriptions are historical source claims

Classification: **[Source technical/historical claim / Needs confirmation]**

Provenance: `p0147:c01`–`p0148:c01`, sections 19.10–19.11.

The source makes concrete claims about:

- PyGTK Windows port status;
- PyQt licensing/cost and Qt 4.5 licensing;
- wxPython portability and tooling;
- choosing toolkit by KDE/GNOME/platform context.

Issue: these ecosystem/licensing/platform statements are time-sensitive.

Action: preserve as historical source framing; do not treat them as current recommendations.

## Finding 4 — pip/package-catalog statement is source-historical

Classification: **[Source technical/historical claim / Needs confirmation]**

Provenance: `p0147:c01`, section 19.9.

Source says the Python package catalog contains many open libraries and that they can be
installed using `pip`.

Action: preserve the named mechanism; no current package-management behavior, command,
index URL or environment assumptions are added.

## Finding 5 — alternative implementation descriptions are historical

Classification: **[Source technical/historical claim / Needs confirmation]**

Provenance: `p0149:c01`, section 19.12.

Source describes CPython, Jython, IronPython, PyPy, Stackless Python, CLPython and
IronMonkey, including platform/runtime relationships and project purposes.

Issue: project status and exact capabilities are time-sensitive and not verified in this
`rag_only` workflow.

Action: preserve the source taxonomy only.

## Finding 6 — address-book task omits persistence safety details

Classification: **[Source design gap]**

Provenance: `p0145:c01`.

Source recommends `pickle` for persistent address-book storage but does not specify:

- file path;
- overwrite/update semantics;
- corruption recovery;
- backup/rollback behavior.

Action: all operational persistence details remain **[Needs confirmation]**.

## Finding 7 — replace task omits file-safety contract

Classification: **[Source design gap]**

Provenance: `p0145:c01`–`p0146:c01`.

Source asks for a command that replaces strings in a list of files and optionally supports
regular expressions, but provides no CLI syntax or write-safety design.

Action: do not synthesize an executable implementation. Target paths, encoding,
backup/atomic-write behavior and rollback remain **[Needs confirmation]**.

## Finding 8 — chapter has no separate post-summary blank page

Classification: **[Source layout note]**

Provenance:
- chapter summary ends at `p0150:c01`, PDF page 150;
- `p0151:c01` immediately begins «Приложение: FLOSS».

Action: chapter boundary ends at PDF page 150 with no extra footer-only page included.
