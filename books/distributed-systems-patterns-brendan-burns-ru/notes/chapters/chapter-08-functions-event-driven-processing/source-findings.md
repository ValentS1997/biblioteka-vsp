# Source findings — глава 8

Этот файл фиксирует source/RAG code defects и security-sensitive example data без silent correction.

## Finding 1 — credential-like example values

Classification: `[Needs confirmation]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0146:c01`

2FA example contains illustrative account/token/contact literals.

Action:
- reusable artifacts do not treat them as real credentials;
- production secret handling is outside chapter scope.

## Finding 2 — library naming mismatch

Classification: `[Source wording/code mismatch]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0146:c01`

Prose spelling of the messaging library differs from the module name used in code.

Action:
- discrepancy preserved;
- exact intended spelling: `[Needs confirmation]`.

## Finding 3 — 2FA Python formatting

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0146:c01`

PDF text extraction affects numeric/string/phone-like formatting and line wrapping.

Action:
- analyze semantic flow only;
- do not present the block as verified copy/paste-safe Python.

## Finding 4 — user-registration code defects

Classification: `[Source code mismatch]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0149:c01`

Extracted code shows:
- inconsistent indentation in optional-handler block;
- inconsistent message quoting;
- a context-variable spelling inconsistency.

Action:
- artifacts preserve intended control flow;
- corrected compile-ready code: `[Needs confirmation]`.

## Finding 5 — current platform compatibility

Classification: `[Needs confirmation]`

Source commands use Kubeless and the printed Python runtime identifier.

Under `rag_only`, no current platform verification or modernization is performed.
