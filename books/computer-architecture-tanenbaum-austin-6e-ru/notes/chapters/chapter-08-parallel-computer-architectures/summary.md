# Краткое содержание главы 8

**Provenance:** `p0694:c01`–`p0696:c01`.

## Why parallelism

Frequency scaling faces heat and physical limits, so performance growth increasingly depends on parallel execution.

## Intraprocessor parallelism

The chapter presents:

- instruction-level parallelism;
- multithreading;
- multicore processors.

Superscalar processors discover some parallel issue dynamically. VLIW processors rely more heavily on compile-time grouping.

## Coprocessors

Specialized processors offload network, graphics/multimedia and cryptographic work.

NVIDIA Fermi is the chapter GPU example and uses SIMD-style execution inside streaming multiprocessors.

## Multiprocessors

Shared-memory MIMD systems present one address space.

The chapter distinguishes:

- UMA;
- NUMA / CC-NUMA;
- COMA.

Memory-consistency models define observable ordering. Cache-coherence protocols such as MESI keep replicated cache lines consistent.

## Multicomputers

Nodes have private hardware memory and communicate by messages.

Examples include MPP systems and clusters. MPI is presented as the dominant standardized message-passing model.

Application-level shared-memory systems such as DSM emulate shared memory over message-passing machines.

## Performance

Important metrics:

- latency;
- bisection/aggregate bandwidth;
- speedup;
- scalability.

Amdahl's law limits speedup when a serial fraction remains.

## Distributed computing

At the loosest coupling level, organizations share processors, storage, data and services. Resource ownership, security, discovery and interoperability become dominant concerns.

## Chapter synthesis

```text
available parallelism
- communication
- synchronization
- contention
- serial fraction
= realized speedup
```
