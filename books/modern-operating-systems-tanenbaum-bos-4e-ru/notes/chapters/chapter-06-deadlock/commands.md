# Source-confirmed APIs and control operations

Scope: chapter 6 RAG only, PDF pages 488–526.

| Item | Class | Source-grounded role | Risk / verification / rollback |
|---|---|---|---|
| `request` | state-changing | Explicitly request a resource in systems exposing such a system call | May block when unavailable. Verify acquisition before use. |
| `open` | state-changing | Acquire an exclusive device represented as a special file | May block if already in use. Release/close procedure is platform-specific in this chapter. |
| `down(&resource)` | state-changing | Acquire a semaphore-protected resource | Can block; acquisition order can create deadlock. |
| `up(&resource)` | state-changing | Release a semaphore-protected resource | Verify matching ownership/protocol. |
| `acquire lock(...)` | state-changing | Blocking lock acquisition in the livelock example | Incorrect ordering can deadlock. |
| `try lock(...)` | state-changing | Nonblocking attempt to acquire a lock; returns failure if unavailable | Symmetric retry loops can livelock. |
| `release lock(...)` | state-changing | Release a previously acquired lock | Verify the intended owner held the lock. |
| `wait fixed time()` | state-changing | Fixed delay before retry in the source livelock example | Identical fixed timing may preserve synchronization and livelock. |
| `fork` | state-changing | Create a process; finite process-table capacity is used as a livelock/resource example | Can fail when the process table is full. |
| `send` | state-changing | Send a message in a communication protocol | Retry can duplicate effects if the first message was not actually lost. |
| `receive` | state-changing | Block waiting for a message from a specified process | Selective waits can participate in communication deadlock. |

## Source pseudo-code: one protected resource

```c
down(&resource_1);
use_resource_1();
up(&resource_1);
```

## Source pseudo-code: safe common ordering

```c
down(&resource_1);
down(&resource_2);
use_both_resources();
up(&resource_2);
up(&resource_1);
```

If every process acquires the same resources in a consistent global order, the circular-wait condition can be structurally removed.

## Source livelock pattern

```c
acquire_lock(resource_1);
while (try_lock(resource_2) == FAIL) {
    release_lock(resource_1);
    wait_fixed_time();
    acquire_lock(resource_1);
}
```

The chapter's listing contains two symmetric processes and demonstrates that fixed, synchronized retries can yield livelock.

## Safety boundary

The chapter provides concurrency primitives and algorithms, not current Linux/Windows commands for inspecting or killing production deadlocks. Do not invent production commands from model memory in this RAG-only artifact.
