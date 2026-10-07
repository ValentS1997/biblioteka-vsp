# Review answers — RAG-grounded

These answers are derived from chapter 6 only. They are not an official publisher answer key. Figure-dependent details absent from the text RAG and actual program execution results remain `[Needs confirmation]`.

1. Example: two processes acquire two exclusive resources in opposite orders. A acquires R1 and waits for R2; B acquires R2 and waits for R1. The policy permits hold-and-wait plus circular wait, so both can remain blocked forever.

2. Deadlock can occur when two or more jobs each fill part of the finite spool area, none has enough remaining disk space to finish producing its complete output file, and the print daemon refuses to print incomplete files. Avoid it by admission control/reservation so a job is accepted only when enough spool space exists to complete it, or by another policy that prevents partial jobs from collectively exhausting the spool resource.

3. The spool-disk space is, in principle, a reclaimable/preemptable storage resource if partial jobs can be deleted/restarted. The physical printer is the nonpreemptable resource while a print operation is in progress. Exact recovery semantics for deleting partial jobs are workload-specific.

4. Releasing in reverse acquisition order is conventional and often natural for nested use, but deadlock prevention depends primarily on acquisition ordering, not release ordering. Once both resources are held and work is complete, another release order does not by itself create the original circular wait.

5. With multiple instances of resource types, a cycle in a resource graph need not imply that the involved processes can never proceed; another instance may later be released by a process outside the cycle and break the wait. The four conditions become sufficient in the simple model with one instance of each resource type and an actual circular wait among processes that cannot be preempted.

6. “Do not block the box” prevents a vehicle from acquiring the intersection while it cannot acquire the next required road segment; it attacks hold-and-wait. Another approach is to impose a global ordering/one-way priority on intersections or use traffic signals that admit only movements whose downstream space is reserved.

7. In the described state no car is holding an exclusive intersection resource; each waits for another car's action/right-of-way event. Under the chapter's distinction this is closest to a communication/cooperation deadlock, not a classic resource deadlock.

8. Yes. Example: two printers P1/P2 and one scanner S. Process A holds P1 and waits for S; B holds P2 and waits for S; C holds S and waits for any printer. No printer or scanner can be released because all three processes are blocked.

9. Yes. In the one-instance-per-resource graph, a single exclusive resource node cannot have assignment edges to two processes simultaneously. A graph showing R→A and R→B at the same time violates the model.

10. The exact edge/request order on figure 6.2 is not encoded in the text RAG. The question requires the unavailable graphical state. **[Needs confirmation]**.

11. Let A and B form a cycle: A waits for a resource held by B, and B waits for one held by A. Let C wait for a resource held by A. C is blocked forever because A can never finish, even though C itself is not on the A↔B cycle. Thus the deadlocked set can include processes downstream of the cycle.

12. Communication deadlock. The reopen/control message is lost, so A waits for B to resume only after a state change B never learns about, while B waits for permission from A.

13. The administrator can terminate one or more processes to free process-table entries or other finite table slots, thereby allowing blocked creation/open operations to proceed. This is recovery by process destruction; lost work must be considered.

14. This item introduces the state used by questions 15–16. The normalized matrices are:
   - `C1=(0,1,1,1,2)`, `C2=(0,1,0,1,0)`, `C3=(0,0,0,0,1)`, `C4=(2,1,0,0,0)`;
   - `R1=(1,1,0,2,1)`, `R2=(0,1,0,2,1)`, `R3=(0,2,0,3,1)`, `R4=(0,2,1,1,0)`;
   - `E=(2,4,1,4,4)`, `A=(0,1,0,2,1)`.
   
   Check: column-sum(`C`) + `A` = `E`.

15. Initially only P2 has `R2 ≤ A`. Let P2 finish and release `C2`:
   `A=(0,2,0,3,1)`.
   Then P3 can finish and release `C3`:
   `A=(0,2,0,3,2)`.
   P1 still needs one unit of resource 1, none is available; P4 still needs one unit of resource 3, none is available. No further process can finish. Therefore **P1 and P4 are deadlocked**.

16. 
   - a) Preemption: take a required resource from P1 or P4 if that resource can be safely preempted, so the other can finish and release its resources.
   - b) Rollback: restore P1 or P4 to a checkpoint from before it acquired the blocking resource; the released resource lets the peer finish.
   - c) Termination: kill P1 or P4; either action releases resources and breaks the deadlocked set. Prefer the process that can be restarted with the least lost/duplicated work.

17. `Cij + Rij > Ej` means process `Pi` claims it needs, in total, more instances of resource class `j` than exist in the system. Its declared request can never be fully satisfied, so the state/request specification is impossible under the model.

18. On a multiprocessor, A and B can execute simultaneously, so both instruction counters can advance during the same interval. The trajectory can therefore have a diagonal component. The chapter explicitly says the horizontal/vertical restriction follows from the single-CPU model.

19. The idea generalizes, but three processes require a three-dimensional state space rather than the two-dimensional plane of figure 6.6. Forbidden/unsafe regions become 3-D volumes. For more processes the construction becomes higher-dimensional and loses practical visual usefulness.

20. Only if the system knows enough about future maximum resource needs to determine which states are safe. That is exactly the assumption used by the banker's algorithm. The chapter emphasizes that in real systems such future maximum demands are often unknown, which limits practical use.

21. Yes: an **unsafe but not deadlocked** state. The chapter's figure 6.8b is the explicit example. The system can still run and might escape if a process releases resources early, but there is no guaranteed completion sequence if all processes later demand their declared maximums.

22. In state 6.9b the chapter says that with two free units only C can be allowed to complete. If D receives one extra unit, one remains; D still cannot complete and C can no longer receive the two units that make its completion guaranteed, so the resulting state is unsafe. If C receives one of the two units, C remains the only candidate and can receive the remaining unit/finish; the state remains safe.

23. No. Worst case, each process holds one resource and asks for a second. One of the three resources is still free; give it to either process. That process finishes and releases two resources, after which the other can finish.

24. To guarantee freedom from deadlock, after every process has obtained at most `m-1` resources there must still be at least one resource left to let some process reach `m` and finish. Thus:
   **`r ≥ p(m-1) + 1`**, equivalently **`r > p(m-1)`**.

25. The numeric allocation/need rows of figure 6.10 are not encoded in the text RAG. Although the text gives total/used/available vectors, it does not provide enough process-A detail to prove the resulting safe sequence. **[Needs confirmation]**.

26. The safety check may need up to `n` completion rounds; each round can scan up to `n` processes, and comparing one process need vector with `A` costs `m` component comparisons. Therefore the straightforward complexity is **O(m n²)**, so **a=1, b=2**. The source expression itself is extraction-damaged.

27. Using the extracted table, **no finite `x` exists**. For resource 5, only two instances exist in the extracted state: one allocated to A and one available. But A's declared maximum is three, so A can never reach its declared maximum regardless of `x`, which changes only resource 3. This conflicts with the wording asking for a smallest `x`; intended source value/result is **[Needs confirmation]**.

28. Some tasks require simultaneous ownership of multiple resources. The chapter's example is copying from a tape to a printer: forcing the process to hold only one at a time makes the intended operation impossible or impractical.

29. Fix A's order as 1→2→3. B is guaranteed safe whenever its first lock is also 1, because whichever process acquires resource 1 first serializes the other before either can create a cycle. The safe B orders are `1,2,3` and `1,3,2`: **2/6 = 1/3**.

30. Yes. A set of processes can each execute `receive` from another process in the set while no matching sender can run past its own receive. There are no shared resources, so this is a **communication deadlock**.

31. Give every account a global order, such as increasing account number, and require every transaction to lock the lower-numbered account first and the higher-numbered account second. This removes circular wait while still holding both locks until the transfer commits.

32. When a process needs an additional resource, treat its old resources plus the new resource as one combined set: release the current set, then reacquire the complete required set atomically/all-or-nothing, blocking until the whole set can be granted. This preserves the no-hold-and-wait property without letting the process continue with only a partial set.

33. Poor as a general resource-deadlock solution. A timeout does not magically make the unavailable resource available; if the process simply continues, it may operate without a resource it requires. If it retries, it can merely convert the failure into repeated retries/livelock. Timeouts are useful in communication protocols only together with retry/duplicate-handling semantics.

34. These mechanisms primarily serve multiprogramming/resource sharing, not deadlock recovery. CPU preemption enables time sharing; memory paging/swapping frees memory for other processes. Their costs include context-switch/scheduling overhead and, for memory, potentially expensive disk I/O. Exact costs are platform/workload dependent — **[Needs confirmation]**.

35. 
   - **Deadlock:** participants are blocked and none can produce the event/resource needed by the others.
   - **Livelock:** participants continue executing/retrying but make no useful progress.
   - **Starvation:** the system progresses, but one participant can be postponed indefinitely by the allocation policy.

36. This is **livelock**: both processes remain runnable and repeatedly perform seeks, but no read completes. Serialize the seek+read operation as one protected device request or place full requests in a driver queue so one operation completes before another repositions the head.

37. 
   - a) Livelock: stations are active and repeatedly collide.
   - b) Break synchronization with different/randomized retry delays rather than immediate identical retry.
   - c) Yes, starvation is possible in principle if one station repeatedly loses contention while others succeed.

38. This is a resource deadlock rather than a pure communication deadlock because the consumer holds the mutex, an exclusive resource, while waiting for the producer; the producer cannot produce because it waits for that same mutex. Fix the acquisition order: wait for data/space availability before acquiring the mutex that protects the buffer, then release the mutex after the buffer operation.

39. The two computers remain synchronized: both request Woofer, both observe the conflict, both cancel, and then can repeat the same behavior. That is **livelock**, not ordinary deadlock, because actions continue. The described behavior is not classic starvation either; neither side is being bypassed while the other successfully completes. The negotiation as a whole simply fails to converge.

40. One source-consistent semaphore design for westbound baboons:

```c
semaphore west_mutex = 1;  /* protects west_count only */
semaphore rope = 1;        /* shared between directions */
int west_count = 0;

westbound() {
    down(&west_mutex);
    west_count++;
    if (west_count == 1)
        down(&rope);        /* first westbound reserves direction */
    up(&west_mutex);

    cross_west();

    down(&west_mutex);
    west_count--;
    if (west_count == 0)
        up(&rope);          /* last westbound releases rope */
    up(&west_mutex);
}
```

The opposite direction must use its own direction-count mutex while sharing the same `rope` semaphore. This prevents a waiter on `rope` from holding the mutex needed by the opposite direction to leave. Actual compilation/test result: **[Needs confirmation]**.

41. Add a fairness/turnstile rule: once an opposite-direction baboon is waiting, stop admitting new members of the current direction. Let the current group drain; then hand the rope to the waiting direction before reopening admission. The essential acceptance criterion is that continuous arrivals from one side cannot indefinitely postpone an already waiting baboon from the other side. Exact implementation/test result: **[Needs confirmation]**.

42. Simulator design:
   1. store current allocation and declared maximum/remaining need;
   2. for each request, tentatively subtract it from `A` and add it to the client's allocation;
   3. run the safety algorithm;
   4. commit the request only if all clients can be marked finishable; otherwise revert the tentative change;
   5. log request, decision and resulting state.
   
   Actual run/log output: **[Needs confirmation]**.

43. Program design:
   1. read process count, resource-type count, `E`, `C`, `R`;
   2. derive `A = E - column_sum(C)`;
   3. repeatedly find an unmarked process with `R_i ≤ A`;
   4. mark it and add `C_i` to `A`;
   5. after convergence, output every unmarked process ID as deadlocked.
   
   Actual implementation/test output: **[Needs confirmation]**.

44. Build directed edges `resource→process` for held resources and `process→resource` for pending requests. Run cycle detection/DFS. In the one-instance model, every process on a detected cycle is deadlocked; processes waiting permanently on that cycle may also be unable to finish. Actual implementation/test output: **[Needs confirmation]**.

45. Break symmetry by assigning a deterministic initiator, for example by unique participant ID:

```c
meet(my_id, other_id) {
    if (my_id < other_id) {
        bow();
        signal_bowed();
        wait_for_other_bow();
        straighten();
    } else {
        wait_for_other_bow();
        bow();
        signal_bowed();
        straighten();
    }
}
```

Only one side is permitted to initiate; the other side is explicitly the responder, so simultaneous initiation cannot occur. The exact event/signal implementation is **[Needs confirmation]**.
