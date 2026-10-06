# Source findings — глава 13 «Многопроцессорные параллельные вычисления»

## Finding 1 — one goroutine per processor wording is over-broad

Classification: **[Source technical claim / Needs confirmation]**

Provenance:

- page 263, chunk `p0263:c01`.

Observed:

Источник объясняет race experiment фразой, что каждая goroutine «будет выполняться на отдельном процессоре».

Impact:

Сам chapter earlier distinguishes goroutines, runtime scheduling and processors; the shown race program also accepts worker counts that can exceed hardware CPU count.

Action:

- canonical notes use only the observable statement: goroutines may execute concurrently/parallelly;
- one-goroutine-per-processor wording is not promoted as invariant.

## Finding 2 — `races.go` listing does not visibly implement the claimed semaphore protection

Classification: **[Source code/result mismatch]**

Provenance:

- page 267, chunk `p0267:c01`;
- results on page 268, chunk `p0268:c01`.

Observed listing:

```go
ch := make(chan bool)
var counter int64 = 0
...
for j := 0; j < циклы; j++ {
    counter++
}
```

The shown channel is used as a completion signal through deferred send and final receives. In the printed listing, there is no send/receive surrounding `counter++` and the channel is not created with capacity 1.

Yet the following page labels this as semaphore-style protection and reports exact correct counts.

Impact:

The printed code does not visibly contain the synchronization mechanism required to explain the shown correct results.

Action:

- no semaphore code is invented;
- output and listing are both preserved as source evidence;
- intended `races.go` source: **[Needs confirmation]**.

## Finding 3 — MD5 hexadecimal-length wording conflicts with the examples

Classification: **[Source internal inconsistency]**

Provenance:

- page 268 onward.

Observed:

The source correctly describes MD5 output as 128 bits / 16 bytes, but then says the string contains “16 hexadecimal numbers”.

Displayed source hashes, for example:

```text
95ebc3c7b3b9f1d2c40fec14415d3cb8
```

contain 32 hexadecimal characters.

Impact:

The textual representation count is internally inconsistent with the displayed examples.

Action:

- artifacts avoid repeating the “16 hexadecimal numbers” wording;
- no external cryptographic specification is needed to identify the mismatch.

## Finding 4 — password-security conclusions are extrapolated from a toy experiment

Classification: **[Source security/performance scope]**

Provenance:

- pages 269–272.

Observed:

The chapter benchmarks a restricted five-character MD5 search space, then makes broader statements about the practical impossibility of brute-force for six/eight-character Linux passwords.

Impact:

The toy workload does not model the full set of password hashing schemes, dictionaries, salts, hardware or attacker models.

Action:

- preserve the example strictly as local CPU-scaling evidence;
- do not promote its password-security timing conclusions as general guarantees.

## Finding 5 — Basel comparison sentence reverses the direction shown by its own timings

Classification: **[Source text/result contradiction]**

Provenance:

- page 278, chunk `p0278:c01`.

Observed source timings for `1e-13`:

```text
parallel-like bazel 1: 1.157085669s
sequential bazel0:    15.894647ms
```

Immediately afterward the text states:

```text
Последовательный вариант медленнее в 100 раз!
```

The displayed data show the opposite direction: the sequential version is much faster.

The subsequent paragraph itself returns to the data and says the many-processor result is even worse.

Action:

- canonical chapter conclusion follows the displayed timings and final chapter conclusions;
- contradictory sentence recorded here.

## Finding 6 — `bazel` “number of branches” description does not match the shown goroutine creation pattern

Classification: **[Source code/description mismatch]**

Provenance:

- pages 277–278.

Observed:

The first CLI argument is described as the number of parallel branches.

Shown code uses it to call:

```go
runtime.GOMAXPROCS(b + 1)
```

but the loop launches a new goroutine for each series term:

```go
for yet {
    go func(x float64) {
        ...
    }(float64(n))
    n++
}
```

Impact:

The source-reported “branch count” is not the literal number of goroutines launched by the displayed code.

Action:

- artifacts call it runtime execution-capacity/worker-count experiment rather than a fixed goroutine-count implementation;
- exact runtime interpretation remains source/version-scoped.

## Finding 7 — resource-limit commands are high-risk and scopes are mixed in prose

Classification: **[Operational risk]**

Provenance:

- pages 261–262.

Observed commands include:

```bash
ulimit -u 500000
echo 1100000 > /proc/sys/kernel/threads-max
ulimit -s 256
ulimit -i 120000
```

The prose groups these together as system limits.

Impact:

They affect different resource boundaries/scopes and can allow workloads to consume much more memory/process/thread capacity.

Action:

- commands are classified as high-risk tuning;
- original values must be recorded before any change;
- exact target-host rollback is **[Needs confirmation]**.

## Finding 8 — race-detector overhead numbers are experiment-specific

Classification: **[Source experiment limitation]**

Provenance:

- pages 264–265.

Observed:

The source reports roughly 10× overhead in one sequential run and up to about 1000× in a 40-worker example.

Impact:

These factors are measurements of one workload/environment, not stable properties of the Go race detector.

Action:

- retain qualitative conclusion only: diagnostic instrumentation can substantially alter performance;
- do not use race-detector runs as production benchmark timings.

## Finding 9 — channel/semaphore equivalence is presented as a conceptual analogy

Classification: **[Source conceptual model / Needs confirmation]**

Provenance:

- pages 267–268.

Observed:

The chapter states that a buffered channel of capacity 1 is “essentially” a binary semaphore and capacity >1 a counting semaphore.

Impact:

The chapter uses this as a synchronization analogy, not a formal equivalence proof covering API behavior, ownership, fairness or lifecycle.

Action:

- canonical artifacts call it a source analogy;
- exact semantic equivalence is not asserted.
