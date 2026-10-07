# Chapter 8 cheatsheet — Многопроцессорные системы

## Symptom / problem framing

| Symptom | Likely boundary |
|---|---|
| lock works but scalability collapses | spin traffic, cache-line bouncing, coarse kernel lock |
| same thread is slower after migration | lost cache/TLB affinity; possible NUMA distance |
| related threads spend time waiting for each other | poor co-scheduling; consider gang/space scheduling model |
| multicomputer message latency is high | copying, kernel crossings, NIC handoffs |
| RPC works locally but fails remotely | pointers, unknown array sizes/types, globals, remote syscalls |
| DSM page ping-pongs between nodes | false sharing or write ownership movement |
| load-balancing probes spike at peak load | sender-initiated algorithm under heavy load |
| distributed file readers disagree | caching + consistency/session semantics |
| distributed app sees many heterogeneous platforms | middleware boundary |

## Baseline / context

### Three hardware/software models

| Model | Memory | Coupling | Typical communication |
|---|---|---|---|
| Multiprocessor/SMP | physically shared | tight | loads/stores + locks |
| Multicomputer | private per node | tight/interconnect | messages, RPC, DSM |
| Distributed system | private per computer | loose/network | protocols + middleware |

### SMP OS organization

The chapter compares:

1. one OS copy/data partition per CPU;
2. master–slave OS;
3. symmetric multiprocessing (SMP).

Modern SMP gives every CPU access to the same kernel but therefore requires correct synchronization of shared kernel structures.

## Read-only checks

1. Identify UMA vs NUMA.
2. Identify whether the bottleneck is memory bandwidth, coherence, locking or scheduling.
3. For a hot lock, inspect:
   - lock hold time;
   - number of contenders;
   - polling frequency;
   - cache-line size/content sharing.
4. Verify whether waiters use plain reads before atomic TSL/SWP attempts.
5. Check whether exponential backoff is bounded.
6. Compare expected lock hold time with context-switch cost before choosing spin vs sleep.
7. Check CPU affinity and whether the thread's previous cache/TLB locality is reusable.
8. For related threads, verify whether they are co-scheduled.
9. On a multicomputer, count every data copy from sender memory to receiver memory.
10. For RPC, identify all marshalled values and any pointer/global-state dependency.
11. For DSM, locate page owner/replicas and identify false sharing.
12. For load balancing, determine current regime:
    - heavy load → sender probing can amplify traffic;
    - light load → receiver probing can create search traffic while idle capacity is abundant.
13. For distributed files, identify the exact consistency/session rule.
14. For middleware, identify which layer owns naming, location, transport and synchronization.

## Interpretation

### Lock traffic

Naive repeated `TSL` writes force exclusive cache ownership and can move an entire cache line back and forth.

Better source pattern:

```text
while ordinary_read(lock) != FREE:
    wait/backoff

attempt atomic TSL once
```

The read is only a hint. Atomic TSL still decides the winner.

### Spin vs context switch

Spin when the expected lock wait is shorter than the cost of switching away and back. Sleep/switch when lock hold times are much longer.

The chapter describes adaptive behavior based on recent observed wait times.

### Affinity

Running a thread on the same CPU can preserve:
- useful cache blocks;
- TLB entries.

Affinity does not itself guarantee useful physical pages remain resident.

### Multicomputer communication

Minimum conceptual path:

`source RAM → source NIC → interconnect → destination NIC → destination RAM`.

Additional kernel copies increase latency and reduce throughput.

### RPC

```text
client → client stub → marshal → kernel/network
       → server stub → unmarshal → server procedure
       → result returns in reverse direction
```

RPC fails to behave like a local call when parameters or state cannot be represented cleanly across address spaces/machines.

### DSM

```text
LOAD/STORE on nonlocal page
  → page fault/trap
  → locate current owner
  → move/copy page
  → map locally
  → restart instruction
```

Read-only replication improves locality. Writes require invalidation/update rules. False sharing can make unrelated variables force page migration.

### Load balancing

- sender-initiated: overloaded node searches for destination;
- receiver-initiated: idle node searches for work;
- hybrid: use both and history when useful.

### Distributed-system middleware

Document model → Web/URL  
File-system model → global/distributed files + consistency semantics  
Object model → CORBA/ORB/IDL  
Interaction model → Linda tuple space / publish-subscribe

## Next action

For a scaling problem:

`classify model → locate shared state/communication path → measure contention/copies → choose narrower synchronization or communication primitive → verify throughput + correctness`.

## Modifying action

State-changing chapter operations include:

- acquire/release atomic locks;
- alter polling/backoff intervals;
- move a thread between CPUs;
- alter processor allocation/gang scheduling;
- pin/unpin communication pages;
- send/receive messages;
- move DSM pages or invalidate replicas;
- migrate a process between nodes;
- change sender/receiver load-balancing policy;
- publish/remove Linda tuples;
- change distributed-file caching/consistency behavior.

State changes can affect correctness as well as performance.

## Verification / acceptance checks

- mutual exclusion still holds;
- lock acquisition eventually progresses;
- bus/coherence traffic decreases after lock optimization;
- affinity does not create unacceptable imbalance;
- message/RPC data arrive with correct values and types;
- DSM has at most the allowed writable ownership/replica state;
- load balancing reduces idle/overloaded nodes without excessive probing;
- distributed-file behavior matches the declared consistency semantics;
- middleware location transparency does not hide failed/incorrect remote state.

## Rollback

- Lock/backoff change: restore previous synchronization policy if liveness/performance regresses.
- Affinity/scheduling change: restore prior placement policy.
- Page pinning/RDMA: unpin only after I/O completion; exact platform lifecycle `[Needs confirmation]`.
- DSM consistency change: restore previous page ownership/replica policy; application recovery `[Needs confirmation]`.
- Process migration: return only if process/resource ownership remains unambiguous; exact rollback `[Needs confirmation]`.
