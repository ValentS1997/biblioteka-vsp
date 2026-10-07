# Source-confirmed commands, APIs and synchronization primitives

Scope: chapter 2 RAG only, PDF pages 111–213.

## Process inspection and lifecycle

| Item | Class | Source-grounded effect | Risk / verification / rollback |
|---|---|---|---|
| `ps` | read-only | Displays running processes in UNIX-like systems | Verify expected processes appear. |
| Task Manager | read-only / may have modifying actions | Windows tool mentioned for viewing processes | Viewing is read-only; termination actions are state-changing. |
| `fork()` | workload-generating / state-changing | Creates a child process in UNIX | Adds process/resource load; verify parent/child PIDs. Rollback: terminate child when appropriate. |
| `execve(...)` | state-changing | Replaces current process image | Current image is replaced; rollback `[Needs confirmation]`. |
| `exit(...)` | state-changing | Terminates caller | Process ends. |
| `kill(...)` | state-changing / potentially destructive | Sends a signal that can terminate another process | Requires permission; rollback `[Needs confirmation]`. |
| `CreateProcess` | workload-generating / state-changing | Creates a process and loads program on Windows | Adds process/resource load. |
| `ExitProcess` | state-changing | Terminates current Windows process | Process ends. |
| `TerminateProcess` | state-changing / potentially destructive | Terminates another Windows process | Requires suitable authority; rollback `[Needs confirmation]`. |

Source shell examples:

```sh
cat chapter1 chapter2 chapter3 | grep tree
```

Read-only with respect to the named input files; demonstrates a pipeline of cooperating processes.

```sh
cc foo.c
```

Workload-generating and normally artifact-producing; used in the chapter as a process-termination/error example.

## POSIX Threads

From the chapter's Pthreads tables:

| Function | Class | Effect |
|---|---|---|
| `pthread_create` | workload-generating / state-changing | Creates a new thread |
| `pthread_exit` | state-changing | Terminates calling thread |
| `pthread_join` | synchronization / potentially blocking | Waits for specified thread to exit |
| `pthread_yield` | scheduling state-changing | Voluntarily yields CPU to another thread |
| `pthread_attr_init` | state-changing in process memory | Initializes thread attribute structure |
| `pthread_attr_destroy` | state-changing in process memory | Destroys attribute structure |

## Pthreads mutexes

| Function | Class | Effect |
|---|---|---|
| `pthread_mutex_init` | state-changing | Creates/initializes mutex |
| `pthread_mutex_destroy` | state-changing | Destroys mutex |
| `pthread_mutex_lock` | synchronization / potentially blocking | Acquires mutex or blocks |
| `pthread_mutex_trylock` | synchronization | Attempts acquisition; returns error if already locked |
| `pthread_mutex_unlock` | synchronization / state-changing | Releases mutex and may wake one waiter |

## Pthreads condition variables

| Function | Class | Effect |
|---|---|---|
| `pthread_cond_init` | state-changing | Creates/initializes condition variable |
| `pthread_cond_destroy` | state-changing | Destroys condition variable |
| `pthread_cond_wait` | synchronization / blocking | Atomically releases mutex and waits for signal |
| `pthread_cond_signal` | synchronization | Wakes one waiter |
| `pthread_cond_broadcast` | synchronization | Wakes all waiters |

The chapter explicitly warns that condition-variable signals are **not remembered** when nobody is waiting.

## Low-level synchronization mechanisms

| Primitive | Class | Source-grounded role |
|---|---|---|
| `sleep` / `wakeup` | synchronization | Block and activate process; naive use can lose wakeups |
| semaphore `down` / `up` | synchronization | Atomic decrement/block and increment/wakeup |
| `mutex_lock` / `mutex_unlock` | synchronization | Mutual exclusion |
| `TSL` | atomic hardware instruction | Test-and-set lock word |
| `XCHG` | atomic hardware instruction | Atomic exchange; x86 synchronization mechanism |
| `send(destination,&message)` | IPC / potentially blocking | Sends message |
| `receive(source,&message)` | IPC / potentially blocking | Receives message |
| `barrier` | synchronization / blocking | Blocks participant until all reach phase boundary |

These are mechanisms/examples, not necessarily user-shell commands.

## Scheduling

| Item | Class | Effect |
|---|---|---|
| `nice` | state-changing scheduling parameter | UNIX command described as voluntarily lowering a process priority |

Changing scheduling policy or priority can alter latency/starvation behavior. Restore the previous value to roll back; the prior value is environment-specific `[Needs confirmation]`.

## Exercise-only file locking

Question 58 supplies this lock acquisition expression:

```sh
ln file file.lock
```

Class: state-changing filesystem operation.

Source intent: use successful creation of the hard-link entry as a lock around the read-increment-append critical section. Exact retry loop, stale-lock handling, verification and unlock command are not specified in the chapter and remain `[Needs confirmation]`.
