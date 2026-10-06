# Source findings — глава 6 «Параллелизм и многопроцессорность»

## Finding 1 — sync API capitalization/name inconsistencies

Classification: **[Source code mismatch]**

Provenance:

- PDF/RAG pages 164–166
- chunks `p0164:c01` … `p0166:c01`

Observed variants:

For Mutex source lists:

```text
func (m *Mutex) UnLock()
```

but surrounding prose uses:

```text
Unlock()
```

For RWMutex source lists names including:

```text
Rlocker()
Runlock()
```

while surrounding prose later uses `RUnlock()`.

Impact:

Method spellings/capitalization are internally inconsistent.

Action:

- chapter artifacts use the names consistently used in explanatory prose (`Unlock`, `RLock`, `RUnlock`) only as a normalized descriptive shorthand;
- original mismatch remains recorded here;
- external API adjudication: **[Needs confirmation]** under rag-only policy.

## Finding 2 — unbuffered-channel capacity wording

Classification: **[Source wording mismatch]**

Provenance:

- PDF/RAG pages 158–159
- chunks `p0158:c01`, `p0159:c01`

Observed:

The chapter first distinguishes:

```go
make(chan string)
make(chan string, 100)
```

as unbuffered vs buffered channels, but later explains immediate blocking of an unbuffered sender with wording:

```text
N ведь равно 1
```

Impact:

The prose mixes the synchronization event count with buffer-capacity terminology in a way that is not internally clean.

Action:

- artifact states only the observable blocking rule described by source;
- numeric capacity interpretation is left **[Needs confirmation]**.

## Finding 3 — closure loop-variable behavior is version-scoped

Classification: **[Needs confirmation]**

Provenance:

- PDF/RAG pages 162–164
- `closure1.go`, `closure2.go`, `closure3.go`

Observed:

The source states that direct closure capture of loop variable `v` produces repeated final value (`c c c`) and shows two binding workarounds.

Impact:

The book itself spans many Go releases; this behavior is therefore retained only as behavior of the source example/environment, not asserted as current universal Go behavior.

Action:

- no external modernization performed;
- example output retained as source evidence only.

## Finding 4 — GOMAXPROCS historical behavior explicitly changes by Go version

Classification: **[Source version note]**

Provenance:

- PDF/RAG page 169, chunk `p0169:c01`

Observed:

The main prose recalls an early default of one processor, while footnote 25 says that this applied only to early Go versions and later defaults changed to the system CPU count.

Impact:

Statements about default `GOMAXPROCS` require version context.

Action:

- artifacts describe `runtime.GOMAXPROCS` as source mechanism;
- no single historical default is promoted as timeless behavior.

## Finding 5 — benchmark remainder visible in source output

Classification: **[Source experiment behavior]**

Provenance:

- pages 170–171
- `smp2.go`

Observed:

The code performs integer division:

```go
повторы = повторы / потоки
```

For `10000000 / 3`, the source output reports:

```text
9999999
```

completed cycles.

Impact:

The requested total work is not preserved when the repetition count is not divisible by the number of workers.

Action:

- benchmark results must be interpreted using the actual reported work count;
- no correction injected into source code.
