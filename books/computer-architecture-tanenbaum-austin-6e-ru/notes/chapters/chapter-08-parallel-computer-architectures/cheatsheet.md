# Cheatsheet — глава 8 «Параллельные компьютерные архитектуры»

**Provenance:** RAG `p0590:c01`–`p0698:c01`. Policy: **rag_only**.

## Parallelism ladder

```text
ILP
→ hardware multithreading
→ multicore
→ coprocessor
→ shared-memory multiprocessor
→ multicomputer / cluster
→ distributed/grid system
```

## ILP

### Superscalar
Hardware issues several ready instructions per cycle.

Limits: dependencies, unavailable functional units, branches and memory stalls.

### VLIW
Compiler packages compatible operations into one instruction/bundle.

Trade-off: simpler runtime hardware, more compiler responsibility.

## TriMedia

- up to 5 operations per command;
- 128 general 32-bit registers;
- load/store use dedicated functional blocks;
- slot/function compatibility matters;
- unsupported combinations are not repaired dynamically.

Saturating example from source:

```text
8-bit unsigned 130 + 130 → 255
```

## Multithreading

| Model | Scheduling |
|---|---|
| fine-grained | rotate threads frequently |
| coarse-grained | switch on long/potential stalls |
| SMT | issue operations from multiple threads in same cycle |

Goal: fill pipeline/function-unit slots that would otherwise idle.

## Fermi / GPU

```text
16 SM × 32 CUDA cores = 512 CUDA cores
```

Within an SM the source describes SIMD-style execution. Divergent control paths serialize work and reduce utilization.

## Flynn / memory model

```text
SISD
SIMD
MIMD
  ├─ multiprocessor: shared memory
  └─ multicomputer: message passing
```

## Memory consistency

- strict → latest real-time write;
- sequential → one global order visible to all;
- processor → preserve each writer's order and per-location order;
- weak → order is forced at synchronization;
- release-style → `acquire` / `release` delimit shared-data regions.

## Coherence vs consistency

**Coherence:** do cached copies of one location agree?

**Consistency:** which global ordering of memory operations may software observe?

### MESI

| State | Meaning |
|---|---|
| M | only valid cache copy; memory stale |
| E | only cache copy; memory current |
| S | one or more cache copies; memory current |
| I | invalid |

## UMA / NUMA / COMA

| Architecture | Address space | Access |
|---|---|---|
| UMA | shared | uniform latency |
| NUMA | shared | local faster than remote |
| COMA | shared | data migrates; no fixed home |
| multicomputer | separate hardware memories | message passing |

## Interconnects

Shared bus: cheap/simple, poor scaling.

Crossbar: nonblocking, expensive.

Omega:

```text
stages = log2(n)
switches = (n/2) log2(n)
```

Cheaper, but blocking.

## Directory coherence

Directory tracks where cache-line copies are and their state.

More nodes require more metadata unless sparse/list encodings are used.

## Message passing / MPI

Source send semantics:

- synchronous;
- buffered;
- nonblocking.

MPI core concepts:

- communicators;
- datatypes;
- communication operations;
- virtual topologies.

## Network metrics

- degree;
- diameter;
- bisection bandwidth;
- aggregate bandwidth;
- latency;
- fault tolerance.

Useful formulas:

- ring: `diameter=floor(N/2)`;
- `m×n` mesh: `(m-1)+(n-1)`;
- `m×n` torus: `floor(m/2)+floor(n/2)`;
- d-dimensional hypercube: `N=2^d`, diameter `d`.

## Amdahl

```text
S(n) = n / (1 + (n-1)f)
S(∞) = 1/f
```

where `f` is sequential fraction.

## Scalability

Shared bus:

```text
per-processor bandwidth ≈ b/N → 0
```

2D mesh has growing link count, so aggregate bandwidth per processor can remain finite, though diameter and latency increase.
