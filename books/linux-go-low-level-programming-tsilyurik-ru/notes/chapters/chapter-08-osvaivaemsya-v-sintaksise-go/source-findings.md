# Source findings — глава 8 «Осваиваемся в синтаксисе Go»

## Finding 1 — Go statistics filename mismatch

Classification: **[Source code/build mismatch]**

Provenance:

- PDF/RAG page 204, chunk `p0204:c01`
- preceding C++ source on page 203

Observed:

Go source is introduced as:

```text
skoc.go
```

but build output shows:

```bash
go build -o sko -compiler gc sko.go
```

The C++ file is `skoc.cc` and binary is `skoc`.

Impact:

It is unclear whether the intended Go source filename is `skoc.go` or `sko.go`.

Action:

- build command is preserved exactly as shown by source;
- canonical source filename: **[Needs confirmation]**;
- no silent rename performed.

## Finding 2 — flag behavior is generalized beyond the demonstrated example

Classification: **[Source wording scope]**

Provenance:

- PDF/RAG pages 197–198

Observed:

After showing behavior of package `flag`, the source states that mandatory placement of options before positional arguments is characteristic of all Go commands.

Impact:

The RAG chapter demonstrates this only for the provided `flag`-based example; it does not establish behavior of every Go command/tool.

Action:

- artifacts attribute the behavior to the source example;
- broader universal claim remains **[Needs confirmation]**.

## Finding 3 — performance comparison is explicitly confounded

Classification: **[Source experiment limitation]**

Provenance:

- PDF/RAG page 204

Observed:

The source reports a large timing difference between Go and C++ implementations of random-sequence statistics, then explicitly notes that this may result from different random number generators rather than language/runtime performance.

Impact:

The timing cannot be used as a clean Go-vs-C++ benchmark.

Action:

- preserve timings only as source observations;
- do not derive language-level performance ranking.

## Finding 4 — network examples omit systematic error handling

Classification: **[Source example limitation]**

Provenance:

- pages 210–213

Observed:

Several examples ignore returned errors, including forms such as:

```go
ln, _ := net.Listen(...)
conn, _ := ln.Accept()
http.ListenAndServe(...)
```

Impact:

The examples demonstrate syntax/network flow but do not provide a production-grade error-handling pattern.

Action:

- artifacts treat these as teaching examples only;
- no production correction is injected under `rag_only` policy.

## Finding 5 — map iteration claim is version-scoped

Classification: **[Source version note]**

Provenance:

- pages 214–215

Observed:

The source explains map iteration using historical/version wording and itself notes behavior may change in future versions.

Impact:

Exact runtime mechanics/order should not be treated as timeless implementation detail.

Stable source-level operational takeaway retained here:

```text
Do not rely on a stable map iteration order.
```

External/current Go specification adjudication: **[Needs confirmation]**.
