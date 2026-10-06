# Cheatsheet — глава 13 «Многопроцессорные параллельные вычисления»

## Goal

Определить, когда параллельная реализация:

- корректна;
- масштабируется;
- не теряет время на coordination больше, чем выполняет useful work.

## 1. Activation cost

Source compares:

```bash
./gotim1
./gotim2
./forktim
./thretim
```

and repeats at several N values.

Interpretation rule:

```text
activation benchmark
≠
application throughput benchmark
```

Large `fork`/`pthread` counts also interact with OS resource limits and memory.

## 2. Resource limits

Read-only:

```bash
ulimit -u
ulimit -i
ulimit -s
cat /proc/sys/kernel/threads-max
```

Source also shows modifying these limits as root.

Do not treat such changes as benchmark boilerplate. Save original values and understand scope/rollback first.

## 3. Data race

Unsynchronized source pattern:

```go
counter++
```

Multiple goroutines update the same variable.

Observed properties:

- result is below expected `N * 1,000,000`;
- repeated runs differ;
- larger concurrency amplifies the error in the shown experiment.

## 4. Race detector

Build:

```bash
go build -race race.go
```

Source output reports:

```text
WARNING: DATA RACE
Read ...
Previous write ...
Found 1 data race(s)
```

Important: instrumentation changes performance significantly, so race-detector timings are diagnostic timings, not production-performance timings.

## 5. Shared-state protection

### Atomic

Use specialized atomic operation for one scalar shared value.

Source result: correct count, substantial overhead versus unsafe increment.

### Mutex

Pattern:

```go
mu.Lock()
// critical section
mu.Unlock()
```

Correctness is restored, but contention increases with more competing goroutines.

### Channel-based coordination

Source uses channels as synchronization primitives and analogizes buffered channels to semaphores.

Exact equivalence is source-scoped; one shown `races.go` listing is inconsistent with its claimed results. See `source-findings.md`.

## 6. Scaling workload

The chapter's local MD5 toy example demonstrates:

```text
1 worker
→ more workers
→ reduced elapsed time
→ diminishing/no benefit beyond available CPU
```

Treat this only as a controlled local CPU-scaling example.

Do not infer current password-security guarantees from its timings.

## 7. Channel pipeline

`multy.go` chains goroutines through channels:

```text
input
→ child 0
→ child 1
→ child 2
→ child 3
```

This demonstrates directional channels and relay-style message flow.

## 8. Timers / tickers

Examples cover:

- timer channel;
- `time.AfterFunc`;
- periodic `time.NewTicker`;
- stopping a ticker.

Operational lesson: asynchronous time events are another source of concurrency and require lifecycle control.

## 9. When parallelism loses

Sequential Basel series:

```bash
./bazel0 1e-13
```

Parallel attempt:

```bash
./bazel 1 1e-13
./bazel 2 1e-13
./bazel 10 1e-13
./bazel 20 1e-13
./bazel 40 1e-13
```

Shown data makes the parallel implementation much slower.

Reason visible in code:

- one tiny operation per goroutine;
- goroutine creation at very fine granularity;
- shared accumulator;
- mutex on every term.

## Acceptance criteria

Parallelization is useful only if:

1. result is deterministic/correct;
2. race detector and logic checks pass;
3. synchronization scope is known;
4. task granularity is large enough;
5. elapsed time beats a sequential baseline;
6. performance improves over a meaningful range of worker counts;
7. resource-limit changes are not required merely to make the design survive.

## Next action

Page 280 starts the book conclusion.
