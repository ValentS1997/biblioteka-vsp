# Source-confirmed instructions, calls and primitives

Scope: chapter 8 RAG only, PDF pages 576–658.

| Item | Class | Source-grounded role | Risk / verification |
|---|---|---|---|
| `TSL` | state-changing | Atomic test-and-set used to acquire a multiprocessor lock | Repeated writes can bounce the cache line and waste bus bandwidth. |
| ordinary read of lock word | read-only | Poll lock without forcing exclusive cache ownership | A FREE read is only a hint; TSL must still arbitrate. |
| `SWP` | state-changing | Atomic swap proposed in review Q12 as alternative lock primitive | Must remain atomic with respect to all CPUs. |
| `MONITOR` | state-changing | Defines an address range to watch for writes | Used with MWAIT; exact CPU semantics are implementation-specific. |
| `MWAIT` | state-changing | Blocks/waits until monitored memory is modified | Verify wake condition and lock state after wake. |
| `send(dest, &mptr)` | state-changing | Send a message to a destination process | Source form blocks until the message is sent. |
| `receive(addr, &mptr)` | state-changing | Wait for and receive a message | Source form blocks until a matching message arrives. |
| `LOAD` | read-only | DSM access may fault if referenced page is nonlocal | Page must be fetched/mapped before restart. |
| `STORE` | state-changing | DSM write may require ownership/invalidation | Verify no conflicting writable replica remains. |
| `out(...)` | state-changing | Linda: insert tuple into tuple space | Can wake a blocked matching `in`. |
| `in(...)` | state-changing | Linda: atomically match and remove tuple; blocks if absent | Matching and removal must be atomic. |
| `read(...)` | read-only | Linda: match tuple without removing it | Blocks if no matching tuple exists. |
| `eval(...)` | workload-generating | Linda: evaluate parameters in parallel and insert resulting tuple | Creates parallel computation. |
| `clock` / `times` | read-only | Review Q34 timing functions for measuring buffer-copy cost | Actual measurements are environment-specific. |

## Source lock pattern

```text
repeat:
    while lock != FREE:
        ordinary read / backoff
    old = atomic TSL(lock)
until old == FREE
```

## Source message-passing interface

```c
send(dest, &mptr);
receive(addr, &mptr);
```

## Source Linda examples

```c
out("abc", 2, 5);
in("abc", 2, ?i);
out("semaphore S");
in("semaphore S");
```

## Safety boundary

The chapter provides architecture-level primitives and APIs, not current Linux commands for NUMA, CPU affinity, RDMA, RPC tracing or process migration. Production commands are not invented in this RAG-only artifact.
