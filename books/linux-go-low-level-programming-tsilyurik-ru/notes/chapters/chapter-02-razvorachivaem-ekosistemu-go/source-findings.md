# Source findings — глава 2 «Разворачиваем экосистему Go»

## Finding 1 — example filename mismatch around Cgo build

Classification: **[Source wording/code mismatch]**

Provenance:

- PDF/RAG page 59, chunk `p0059:c01`

Observed variants in the same source passage:

- code block is introduced as `hello.go`;
- the build command shown is `go build tiny.c.go`;
- the subsequent artifact check is `ls -l tiny.c`.

Impact:

The reader cannot infer from this passage alone whether the intended example filename is `hello.go`, `tiny.c.go`, or another archive filename.

Action:

- no silent correction was made;
- `commands.md` preserves the command exactly as shown: `go build tiny.c.go`;
- canonical filename mapping remains **[Needs confirmation]**.

## Finding 2 — version/environment drift is intentional source context

Classification: **[Needs confirmation]**

Provenance:

- chapter pages 26–34 and multiple later listings;
- book preface RAG explicitly states versions changed during the long writing period.

Observed:

The chapter mixes examples from different Go/Linux versions and machines.

Impact:

Concrete version numbers, package names, filesystem paths and command output are examples, not current-state guarantees.

Action:

Artifacts preserve the source commands but do not claim current applicability outside the described environment.
