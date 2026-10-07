# Chapter 2 cheatsheet — Процессы и потоки

## Symptom / problem framing

Concurrent execution creates two distinct classes of problems:

1. **progress/scheduling:** which runnable process or thread gets CPU time;
2. **correctness/synchronization:** what happens when execution streams share or exchange data.

Do not treat a blocked process as merely “slow”, and do not treat a race as a scheduler performance problem.

## Baseline / context

### Process state model

| State | Meaning |
|---|---|
| Running | currently using a CPU |
| Ready | runnable, but CPU is assigned elsewhere |
| Blocked | cannot proceed until an external/event condition changes |

Transitions are driven by blocking operations/events and by the scheduler.

### Process vs thread

| Property | Process | Thread |
|---|---|---|
| Address space | separate from other processes | shared with threads of same process |
| Open files/resources | process-owned/grouped | shared within process |
| Program counter/registers | saved per process execution state | own per thread |
| Stack | process execution stack | own per thread |
| Scheduling entity | process in process model | thread when threading implementation exposes it |

### Thread implementation

- **User level:** runtime library owns thread table/scheduling; fast switching and no kernel trap for local operations.
- **Kernel level:** kernel owns thread table and can schedule another thread when one blocks.
- **Hybrid:** user threads are multiplexed over kernel threads.
- **Scheduler activations:** kernel notifies user runtime via upcalls about blocking/unblocking events.

## Read-only checks

When diagnosing concurrency behavior, establish:

1. Is the execution unit a process or a thread?
2. Is it running, ready or blocked?
3. If blocked, what event/resource is awaited?
4. If CPU-active, is it doing useful work or active waiting/spinning?
5. What data/resource is shared?
6. What protects the critical section?
7. Is the synchronization primitive counting events (semaphore), providing exclusion (mutex), waiting for a predicate (condition/monitor), exchanging data (messages), or synchronizing phases (barrier)?
8. What scheduling policy is in effect and what is the quantum/context-switch overhead?
9. Is there starvation, priority inversion or a circular wait?
10. For user-level threads, could a blocking syscall/page fault stop the entire process?

## Interpretation

### Race and critical section

A race exists when the result depends on execution order while shared state is accessed.

An acceptable critical-section solution in the chapter must satisfy:

1. no two processes simultaneously in their critical sections;
2. no assumptions about CPU count/speed;
3. a process outside its critical section must not block another;
4. no indefinite waiting to enter.

### Synchronization primitives

| Primitive | Main purpose | Main caution |
|---|---|---|
| Busy wait / spin | very short wait for atomic state | wastes CPU; priority inversion risk |
| Semaphore `down/up` | event counting + synchronization; binary semaphore can provide exclusion | ordering mistakes can deadlock |
| Mutex | mutual exclusion | programmer must lock/unlock correctly |
| Condition variable | sleep until condition becomes true | signals are not remembered |
| Monitor | language-level encapsulation + synchronization | depends on language/runtime semantics |
| `send/receive` | information exchange, including across machines | buffering, loss/acknowledgement, addressing |
| Barrier | phase synchronization for a group | all participants must reach barrier |
| RCU | read-mostly lockless update pattern | reclamation must wait for a grace period |

### Scheduling

- **Batch:** throughput, turnaround, CPU utilization.
- **Interactive:** response time and proportional behavior.
- **Real-time:** deadlines and predictability.

Important algorithms: FCFS, shortest job first, shortest remaining time, round-robin, priority, multilevel queues, guaranteed, lottery and fair-share.

For round-robin: a shorter quantum improves responsiveness but increases context-switch overhead; an excessively long quantum approaches FCFS behavior.

## Next action

For a suspected concurrency defect:

`state → shared resource → critical section → synchronization primitive → scheduler interaction → reproduce/measure`.

Change only one mechanism at a time and remeasure.

## Modifying action

State-changing examples in this chapter include process/thread creation/termination, changing priorities, mutex/condition operations, signaling, hard-link based exercise locking and explicit scheduling/synchronization calls.

Before using them in a real system, confirm target PID/thread/resource and the expected effect. The chapter is conceptual material, not an environment-specific production runbook.

## Verification / acceptance checks

A concurrency fix is acceptable when:

- protected invariants remain valid under repeated interleavings;
- no second execution stream enters an exclusive critical section concurrently;
- blocked work is eventually awakened when its condition occurs;
- no lost wakeup is observed;
- no starvation/deadlock is introduced;
- scheduler changes improve the intended metric without disproportionate context-switch overhead.

Exact OS-specific observability commands are `[Needs confirmation]` unless listed in `commands.md`.

## Rollback

- Priority/scheduling changes require restoring the prior policy/priority; previous value is environment-specific `[Needs confirmation]`.
- Created threads/processes terminate through their corresponding lifecycle mechanisms.
- Mutex/condition initialization is paired with destroy operations in Pthreads.
- File-locking exercise rollback requires removal of the lock entry; exact command is not supplied by the source and is `[Needs confirmation]`.
- Synchronization algorithm changes require reverting to the previously verified implementation.
