# Review answers — RAG-grounded

These answers are derived from chapter 2 only. They are not an official publisher answer key. Calculations use the models stated in the chapter. Unsupported environment-dependent details remain `[Needs confirmation]`.

1. The missing direct transitions are **ready → blocked** and **blocked → running**. Ready → blocked is not meaningful because a process must actually run before it can execute an operation that blocks. Blocked → running is represented as two logical transitions: blocked → ready when the event occurs, then ready → running when the scheduler selects it. If no other process is running, those two may occur immediately one after another.

2. Hardware would need the execution context that the process table stores: program counter, registers, stack pointer, processor status, memory-map/context information and a way to identify the next runnable process. A possible design would atomically save the current context into a process descriptor, select another ready descriptor, load its context and resume from its saved program counter.

3. The chapter states that saving/restoring registers and changing the stack pointer cannot in general be expressed entirely in a high-level language such as C. The low-level entry/exit sequence therefore needs assembly.

4. A separate kernel stack keeps privileged interrupt/system-call execution independent of the interrupted user stack and lets the kernel save/restore state using its own protected execution context. The chapter describes the stack switch but does not give a longer formal rationale.

5. With `p = 0.5` and `n = 5`, CPU idle probability is `p^n = 0.5^5 = 0.03125`. **3.125%** of CPU time is idle.

6. Memory available to processes is 3.5 GiB. At 256 MiB per process, `n = 14`. For 99% utilization:
   `1 - p^14 = 0.99` → `p = 0.01^(1/14) ≈ 0.7197`.
   Thus each process may spend about **72%** of its time waiting for I/O under this approximate model.

7. One job needing 10 CPU-minutes while waiting for I/O 50% of elapsed time takes about 20 minutes alone. Sequentially the second completes after **40 min**. With two such jobs, the CPU is idle only when both wait: `0.5² = 0.25`, so utilization is 75%. Twenty CPU-minutes of total work then require about **26.7 min**.

8. `1 - 0.4^6 = 0.995904` → about **99.59% CPU utilization**.

9. Split the byte range into disjoint ranges and assign each range to a separate thread, potentially using different mirrors. The threads download concurrently into the correct regions; completion requires all ranges to finish. The achievable gain depends on network/server bottlenecks `[Needs confirmation]`.

10. Separate processes have separate address spaces, so a single in-memory cache cannot naturally be shared like it can by threads in one process. Per-process caches are possible but duplicate memory and do not automatically form one coherent shared cache.

11. Not in the same way. A single-threaded process cannot execute `fork` while its only thread is blocked waiting for keyboard input. The problematic duplication arises specifically because another thread can execute `fork` while a different thread is blocked.

12. **Kernel-level threads.** With only blocking `read`, a user-level thread that blocks in the kernel can block the entire process because the kernel does not know about the other user threads. Kernel threads allow another thread of the same process to run.

13. Yes. If requests are very short and never perform blocking operations, thread-management/synchronization overhead may provide no benefit. The chapter also presents a one-thread model as the simplest blocking design; the exact workload threshold is `[Needs confirmation]`.

14. Registers are part of an execution stream. Each thread needs its own saved program counter/register set so the physical CPU registers can be loaded with the selected thread's state during a context switch.

15. With user-level threads and no timer preemption, the runtime may regain control only when the running thread voluntarily enters the runtime. `thread_yield` therefore allows other ready threads to make progress.

16. A kernel-managed thread can be preempted by timer interrupt because the kernel schedules threads. A purely user-level thread is not independently visible to the kernel; the kernel can preempt the containing process, while switching between its user threads requires the user runtime or an extra timer/upcall mechanism.

17. Single-thread average request time is `15 + (1/3)×75 = 40 ms` → **25 requests/s**. With enough threads, disk waits can overlap and CPU work is 15 ms/request → theoretical CPU-side limit about **66.7 requests/s**, assuming no other bottleneck.

18. Main advantage: thread operations/switching can occur entirely in user space, cheaply and even on an OS without native thread support. Main disadvantage: a blocking system call or page fault can block the whole process; also a running user thread is not naturally preempted by a per-thread timer.

19. Yes. The creator can synchronize after each creation—for example, wait for the just-created thread to finish/announce completion before creating the next. The chapter provides `pthread_join` for waiting on a specified thread.

20. The chapter defines this private-global mechanism specifically as storage of a pointer and does not state that storing arbitrary values directly is equivalent. A generic direct-value implementation would need type/size semantics not supplied here. **[Needs confirmation]** for a fully general value-based replacement.

21. The timer can interrupt the runtime while it is modifying its own thread table/scheduler state, causing re-entry and corruption/inconsistent state. A source-consistent remedy is to protect runtime critical sections from such timer-driven re-entry or make the runtime synchronization/re-entry safe; exact implementation is `[Needs confirmation]`.

22. In principle yes: arm a timer before a potentially blocking call so the blocked call is interrupted and the runtime regains control to run another user thread. This is cumbersome and adds overhead; it is a workaround for the absence of `select`-style prechecks.

23. Under the chapter's shared-memory model, strict alternation using the shared `turn` variable still enforces one-at-a-time entry even on multiple CPUs, but it remains a poor solution because it uses busy waiting and violates the progress condition when the other process is outside its critical section. Hardware memory-ordering issues are outside this chapter.

24. With strict priority scheduling it can fail to make progress: a high-priority process may spin waiting for a low-priority process that cannot run to leave its critical section. With non-priority/round-robin scheduling the other process eventually runs, so Peterson's algorithm can make progress under the chapter's assumptions.

25. Yes, if the user-level runtime itself uses strict priorities: a high-priority thread can spin/wait for a low-priority lock holder that the runtime never schedules. The issue is scheduling policy, not whether threads live in kernel space.

26. No indefinite H/L lockup of that form: round-robin eventually gives L a quantum so it can leave the critical section and release the resource.

27. **One stack per thread** in both models. For user-level threads the stacks are managed in the process address space by the runtime; for kernel threads the kernel tracks per-thread execution state. Kernel-internal stacks may additionally exist, but exact layout is system-specific `[Needs confirmation]`.

28. Yes. A race does not require simultaneous physical execution; it requires an unsafe interleaving whose result depends on ordering. A sequential simulator can model such interleavings instruction by instruction.

29. Yes, provided all producers/consumers use the same atomic semaphore protocol: `empty/full` count buffer state and `mutex` protects the shared buffer. The mutex serializes actual buffer modification.

30. This item only supplies the P0 half of the proposed solution; the source asks for evaluation after defining P1 in question 31. No separate conclusion is required.

31. **No.** P0 leaves the critical section by setting `turn = 0`; P1 analogously sets `turn = 1`. With initial `turn = 0`, P0 can repeatedly proceed while P1 can wait forever. The solution therefore fails the no-indefinite-wait/progress requirements.

32. On a uniprocessor, implement `down/up` as atomic kernel operations by disabling interrupts while the semaphore value is tested/changed and while the process is placed on or removed from the wait queue.

33. Same core mechanism: protect the short semaphore critical operation by interrupt blocking so no scheduler/interrupt handler can interleave another semaphore operation. On multiprocessors the chapter additionally requires an atomic lock such as TSL/XCHG around the semaphore.

34. Yes. A barrier with two participants is a valid rendezvous: each process waits until the other finishes the current phase. It may be more general machinery than necessary, but its semantics still make sense.

35. Kernel threads: **yes**, because blocking one thread on the kernel semaphore need not block its sibling, which can later signal it. Pure user-level threads: a blocking kernel semaphore operation can block the entire process, preventing the sibling user thread from running and signaling; therefore this arrangement is not suitable.

36. Implementing arbitrary `waituntil(predicate)` would require the monitor/runtime to know when any state relevant to an arbitrary predicate changes and to re-evaluate potentially many predicates. The generality makes implementation and runtime checking expensive/complex compared with explicit condition variables and signals.

37. It is a pipeline: each sequential worker/stage receives work from the previous stage and passes results to the next. The UNIX analogy is cooperating processes connected by pipes/message queues so the output of one becomes input to another.

38. Assuming send/receive/mailbox operations themselves are atomic, this does not create a race merely because failure is reported instead of blocking. It creates **busy waiting**, repeatedly consuming CPU until the mailbox state changes.

39. Each process receives about `1/n` of the processor with zero switching overhead, so a job requiring T seconds alone needs **nT seconds**.

40. First `fork` makes 2 processes; both execute the second `fork`, producing 4 total processes. Number of newly created child processes: **3**.

41. A process appearing twice gets roughly twice as many round-robin turns/CPU share. That can intentionally implement a higher effective weight/priority.

42. Source code alone is not a reliable classification because behavior depends on runtime input and environment. At runtime, measure CPU bursts versus blocking/I/O behavior—for example the fraction of a quantum used before blocking, as discussed in the chapter.

43. Small Q improves responsiveness but increases context-switch overhead; large Q reduces overhead but can increase interactive latency. With switch cost S, Q should be much larger than S while remaining short enough for acceptable response time.

44. Ignoring final partial bursts:
   - a) `Q = ∞`: **T/(T+S)**;
   - b) `Q > T`: **T/(T+S)**;
   - c) `S < Q < T`: approximately **Q/(Q+S)**;
   - d) `Q = S`: **1/2**;
   - e) `Q ≈ 0`: efficiency tends to **0**.

45. Shortest-job-first minimizes average response/turnaround when all are ready. Sort `{3,5,6,9,x}` ascending:
   - `x ≤ 3`: x, 3, 5, 6, 9;
   - `3 < x ≤ 5`: 3, x, 5, 6, 9;
   - `5 < x ≤ 6`: 3, 5, x, 6, 9;
   - `6 < x ≤ 9`: 3, 5, 6, x, 9;
   - `x > 9`: 3, 5, 6, 9, x.
   Equal-length ties may be ordered arbitrarily.

46. Using the assumptions in the question:
   - a) fair processor-sharing/round-robin completion times: C=10, D=18, B=24, E=28, A=30 → average **22 min**;
   - b) priority order B, E, A, C, D → completion 6,14,24,26,30 → average **20 min**;
   - c) FCFS A,B,C,D,E → completion 10,16,18,22,30 → average **19.2 min**;
   - d) SJF C,D,B,E,A → completion 2,6,12,20,30 → average **14 min**.

47. CTSS quanta grow 1,2,4,8,16…; 30 quanta are covered by five admissions (cumulative 1,3,7,15,31). Thus **5 swaps/admissions** are implied. The Russian wording “перекачан на диск” does not make the in/out direction completely clear, so the exact direction is **[Needs confirmation]**.

48. Utilization demand:
   `2×(1/5) + 11/33 = 0.7333`.
   Since this is ≤ 1, **yes**, it passes the chapter's schedulability test.

49. Add another `11/33`: total ≈ **1.0667 > 1**, so **no**.

50. With a=1/2, the newest measurement has weight 1/2, previous 1/4, etc.:
   `40/8 + 20/8 + 40/4 + 15/2 = 25 ms`.
   Forecast: **25 ms**.

51. `35/50 + 20/100 + 10/200 + x/250 ≤ 1`.
   Known utilization = 0.95, so `x/250 ≤ 0.05` → **x ≤ 12.5 ms**.

52. **Yes, it breaks the circular-wait pattern** because neighboring philosophers do not all acquire forks in the same direction. Under the stated protocol, a complete circular chain of one-fork holders cannot form.

53. Voice utilization `2×1/6 = 1/3`; video period is 40 ms at 25 fps, so `20/40 = 1/2`. Total = **5/6 ≈ 0.833 < 1**, so **yes**.

54. Keep the thread-dispatch mechanism in the kernel but expose parameters/system calls that let a process or user-space manager assign/change priorities or other scheduling parameters for its threads. This is the policy/mechanism split described in §2.4.5.

55. `test(i)` grants eating only when `state[i] == HUNGRY` and neither neighbor is eating. Setting HUNGRY before testing records that the philosopher is requesting forks and allows later neighbor tests to wake it when forks become available.

56. If `state[i]` remains EATING while the two neighbor tests run, each neighbor sees i as still eating and cannot become eligible. Eligible neighbors may therefore fail to be awakened; progress/fairness is broken.

57. Three useful formulations consistent with the chapter:
   1. **Reader preference:** new readers may enter while readers are active; writers can starve.
   2. **Writer preference:** once a writer waits, new readers wait behind it; the writer runs after existing readers leave.
   3. **Fair/no-category preference:** preserve arrival/queue order so neither class can continually bypass the other.
   Exact queue implementation for the third variant is not supplied by the chapter.

58. The race covers the compound operation **read last value → compute +1 → append**. Two instances can read the same old value and append duplicates. The source suggests using atomic success/failure of `ln file file.lock` as a lock acquisition around this whole critical section. Exact retry/unlock shell code is not supplied and remains **[Needs confirmation]**.

59. Use the producer-consumer semaphore pattern as a mailbox: `empty` counts free message slots, `full` counts queued messages, and `mutex` protects queue mutation. `send`: down(empty), down(mutex), enqueue, up(mutex), up(full). `receive`: down(full), down(mutex), dequeue, up(mutex), up(empty).

60. A monitor can own philosopher states and one condition variable per philosopher. `take_forks(i)`: enter monitor, set HUNGRY, test whether both neighbors are not EATING, otherwise wait on condition i. `put_forks(i)`: set THINKING, then test/signal both neighbors. Mutual exclusion is provided by the monitor.

61. Keep protected state `mode ∈ {empty,women,men}` plus occupant count, guarded by a mutex/monitor and condition variables. Entry waits while the opposite mode is active; first entrant sets the mode; same-category entrants increment count; leaving decrements count; last leaver sets empty and wakes opposite waiters. Exact fairness policy is **[Needs confirmation]**.

62. A direct N-process extension of strict alternation can maintain `turn` in `0..N-1` and advance it cyclically. It still inherits the chapter's defect: a process can be blocked by the designated next process even when that process is outside its critical section or inactive. Thus it is not an acceptable general mutual-exclusion solution.

63. With unrestricted shared-buffer access and only naive `sleep/wakeup`, the chapter's lost-wakeup race remains possible. The time until it appears is nondeterministic and depends on scheduling/timing, so **[Needs confirmation]** must come from the experiment.

64. Multiple queue entries or program instances can obtain a larger share of CPU scheduling opportunities. The exercise itself notes that on an otherwise idle personal computer no improvement is expected from merely duplicating CPU-bound work; with competing processes, multiple instances may capture a larger share. Exact speedup is workload/system dependent **[Needs confirmation]**.

65. Partition candidate divisors among P threads so no candidate is checked twice. Each thread tests its range and adds discovered divisors to shared state protected by a synchronization primitive such as a mutex. Parent/main thread joins all workers, sums the divisors and compares with N. The source notes the search can be reduced by considering candidates through `sqrt(N)`.

66. Split the file into N assigned segments, let each thread build an intermediate frequency count for its segment, join all threads, then merge the intermediate counts into the final frequency table. Boundary/tokenization details are not specified by the chapter and remain **[Needs confirmation]**.
