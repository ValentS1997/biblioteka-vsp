# Chapter 1 cheatsheet — Введение

## Symptom / problem framing

A computer exposes low-level hardware that is inconvenient, shared and potentially unsafe for applications to manage directly.

The chapter frames the OS problem as two simultaneous requirements:

- present **usable abstractions** instead of raw hardware details;
- **manage and protect shared resources** among programs and users.

## Baseline / context

### Execution boundary

| Layer | Source-grounded role |
|---|---|
| Hardware | CPUs, memory, disks/SSDs, controllers, buses, I/O devices |
| Kernel mode | privileged OS code; full hardware/instruction access |
| User mode | restricted application and service execution |
| Shell / GUI | user-space interfaces using OS abstractions; not automatically part of the kernel |

### Two OS views

| View | Question it answers |
|---|---|
| Extended machine | “What convenient abstraction should applications see?” |
| Resource manager | “Who gets which resource, when, and under what protection?” |

### Multiplexing

- **Time multiplexing:** CPU, printer scheduling and other resources used in turns.
- **Space multiplexing:** memory and disk space partitioned among simultaneous users/processes.

## Read-only checks

For a chapter-grounded analysis of an OS problem, identify:

1. Which abstraction is involved: process, address space, file, I/O, security.
2. Whether the failing component is in user mode or kernel mode.
3. Which physical resource is underneath the abstraction.
4. Which API/system-call boundary is crossed.
5. Whether sharing is primarily in time, space, or both.
6. Which OS structural model is relevant: monolithic, layered, microkernel, client-server, VM, exokernel.

These are conceptual checks, not a universal command runbook.

## Interpretation

### Core abstractions

- **Process:** executing program plus address space, registers, open files and other execution state.
- **Address space:** process-visible address range separated from physical memory; supports protection and virtual memory.
- **File:** device-independent storage abstraction; files are organized in directories and accessed through descriptors after open.
- **I/O:** split between device-independent OS code and device-specific drivers/controllers.
- **Security:** OS controls access, including UNIX-style owner/group/other `rwx` permissions.
- **Pipe:** file-like IPC abstraction connecting processes.

### System-call boundary

UNIX examples in the chapter:

- process lifecycle: `fork`, `waitpid`, `execve`, `exit`;
- files: `open`, `close`, `read`, `write`, `lseek`, `stat`, `fstat`;
- directories/filesystems: `mkdir`, `rmdir`, `link`, `unlink`, `mount`, `umount`;
- misc: `chdir`, `chmod`, `kill`, `time`.

Win32 is presented as an API layer whose calls need not map one-to-one to kernel system calls.

### OS structure trade-off

- **Monolithic:** high direct-call efficiency, large kernel failure domain.
- **Layered:** explicit boundaries and ordering between layers.
- **Microkernel:** minimize privileged code; move drivers/services to user space to reduce blast radius.
- **Client-server:** clients request services by messages; can extend across a network.
- **Virtual machine:** reproduce/virtualize a machine so multiple OS instances can coexist.
- **Exokernel:** allocate resources directly to separate environments while preventing interference.

## Next action

When reading later chapters, map each detailed mechanism back to this chapter’s abstraction:

- chapter 2 → processes/threads;
- chapter 3 → address spaces/memory;
- chapter 4 → filesystems;
- chapter 5 → I/O;
- chapter 6 → deadlocks;
- chapters 7–9 → virtualization, multiprocessors, security.

## Modifying action

This chapter contains modifying API examples, but it is not a change runbook.

Examples include `mkdir`, `rmdir`, `link`, `unlink`, `mount`, `umount`, `chmod`, process creation/termination and signals. Before using them operationally, the target object, expected effect and environment-specific rollback must be known.

## Verification / acceptance checks

Source-supported verification patterns include:

- use returned status/PID from process-management calls;
- use `stat`/`fstat` to inspect file metadata;
- reopen/read the relevant file after a file operation;
- verify the expected path appears through the mounted filesystem;
- verify permissions after `chmod`.

Exact environment-specific commands are `[Needs confirmation]` unless explicitly present in the chapter.

## Rollback

- `mount` → source supplies `umount` as the inverse operation.
- `mkdir` → `rmdir` can remove an empty directory.
- `link` → `unlink` can remove a directory entry; file deletion semantics depend on remaining links.
- `chmod` → restoration requires the previous mode, which the chapter does not supply automatically.
- destructive file/process changes → rollback is otherwise `[Needs confirmation]`.
