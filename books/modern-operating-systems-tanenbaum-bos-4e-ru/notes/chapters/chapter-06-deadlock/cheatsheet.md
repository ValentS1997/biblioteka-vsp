# Chapter 6 cheatsheet — Взаимоблокировка

## Symptom / problem framing

Before changing state, classify the loss of progress:

| Symptom | Likely class |
|---|---|
| threads blocked forever in a closed ownership/wait cycle | deadlock |
| requests keep failing/retrying and CPU activity continues, but no useful work completes | livelock |
| one process never receives a resource while others continue completing | starvation |
| long wait with an eventual owner/release path | contention, not proven deadlock |
| all parties wait for messages/events, no owned resource cycle | communication deadlock |

## Baseline / context

### Resource lifecycle

```text
request → acquire → use → release
```

### Coffman conditions

All four are necessary for classic resource deadlock:

1. mutual exclusion;
2. hold and wait;
3. no preemption;
4. circular wait.

Destroying any one condition makes that class of deadlock structurally impossible.

### Resource graph

```text
resource → process   = resource assigned to process
process  → resource  = process waiting for resource
```

With one instance of each resource type:

`cycle ⇔ deadlock`.

With multiple instances, a cycle alone is not sufficient; use the matrix algorithm.

## Read-only checks

1. List all resources and whether each is preemptable.
2. List current owners.
3. List blocked/retrying processes and their requested resources/events.
4. For a one-instance model, build a resource/wait-for graph and search for cycles.
5. For multiple resource instances, capture:
   - `E`: total instances;
   - `A`: currently available instances;
   - `C`: currently allocated instances per process;
   - `R`: remaining requests per process.
6. Verify the invariant for each resource class:
   `allocated + available = existing`.
7. Run detection conceptually: find an unfinished process with `R_i ≤ A`, assume it finishes, add `C_i` back to `A`, repeat.
8. Any unmarked processes after no further progress are deadlocked under the chapter's model.
9. For an avoidance question, distinguish current deadlock from unsafe state.
10. For retry loops, verify whether contenders use identical fixed timing; synchronized retries are a livelock risk.
11. For starvation, inspect the allocation policy, not only the lock graph.

## Interpretation

### Four strategies

| Strategy | Principle | Cost / limitation |
|---|---|---|
| Ignore | accept rare deadlocks | operational recovery may be manual |
| Detect + recover | allow deadlock, then find and break it | detection/recovery overhead, lost work |
| Avoid | grant only requests that preserve a safe state | requires advance maximum-demand information |
| Prevent | make one Coffman condition impossible | may reduce utilization or flexibility |

### Safe vs unsafe

A state is **safe** when at least one completion sequence exists that guarantees all declared maximum demands can be satisfied.

A state is **unsafe** when no such guarantee exists.

`unsafe ≠ already deadlocked`.

### Detection: multiple instances

```text
while exists unfinished Pi with Ri <= A:
    A = A + Ci
    mark Pi finished

unfinished processes after convergence = deadlocked set
```

### Recovery

- **Preempt resource:** usable only when the resource can be taken and later restored safely.
- **Rollback:** restore a checkpoint from before a needed resource was acquired; all work after that checkpoint is lost/repeated.
- **Terminate process:** simplest but potentially destructive; prefer a process that can safely restart.

### Prevention mapping

| Coffman condition | Source strategy |
|---|---|
| Mutual exclusion | spool/virtualize exclusive device where possible |
| Hold and wait | request all resources before starting, or release held set before reacquiring the complete set |
| No preemption | make resources preemptable/virtualize them where feasible |
| Circular wait | impose global resource ordering |

### Banker

Grant a request only if the resulting state remains safe. The chapter emphasizes the practical limitation: real processes often cannot declare reliable maximum future demand, process counts change, and resources can disappear.

### Communication deadlock

Timeout + retry can restore progress, but duplicate requests can be dangerous. A retry protocol must account for the possibility that the original request succeeded and only the response was delayed/lost.

### Livelock

```text
acquire R1
try R2 → fail
release R1
wait fixed time
retry
```

Two symmetric processes can remain perfectly synchronized forever. They are runnable, but useful progress is zero.

### Starvation

A "shortest job first" style allocation can indefinitely postpone a very large request. FIFO allocation prevents that specific starvation pattern.

## Next action

For a suspected deadlock:

`capture owners/waiters → prove dependency cycle or deadlocked matrix set → classify resource/event model → choose least-destructive recovery → verify progress → fix acquisition policy/order`.

## Modifying action

Potentially state-changing actions described by the chapter include:

- acquire/release semaphores, mutexes or exclusive resources;
- delay/deny a request to preserve safety;
- preempt a resource when safe;
- roll a process back to a checkpoint;
- terminate a process;
- restart a communication request after timeout;
- change lock ordering;
- change admission policy to request all resources before irreversible work;
- enforce FIFO allocation to prevent starvation.

State-changing recovery can lose work or duplicate effects. Do not execute a recovery action until the affected resource semantics are known.

## Verification / acceptance checks

After recovery or policy change verify:

- the former wait cycle is gone;
- at least one previously stuck process makes forward progress;
- released resources are again accounted for in `A`;
- `allocated + available = existing` still holds;
- no transaction/output effect was duplicated after rollback/retry;
- acquisition order is globally consistent when ordering is the prevention mechanism;
- livelock retries are desynchronized or otherwise guaranteed to converge;
- a starvation fix eventually services the oldest waiting process.

## Rollback

- Lock-order or allocation-policy changes: restore the previous policy if the new ordering causes regressions.
- Process termination: no generic rollback; application restart/data recovery is workload-specific — `[Needs confirmation]`.
- Resource preemption: restoration procedure is resource-specific — `[Needs confirmation]`.
- Checkpoint rollback is itself the chapter's recovery mechanism; work after the checkpoint is intentionally discarded.
- Communication retry may be unsafe without duplicate suppression/idempotence; exact protocol rollback is `[Needs confirmation]`.
