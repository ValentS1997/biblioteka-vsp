# Source-confirmed commands, APIs and mechanisms

Scope: chapter 3 RAG only, PDF pages 214–300.

The chapter is primarily about OS/MMU mechanisms. It does **not** provide a generic shell runbook for changing virtual-memory policy.

## Explicit command/tool references

| Item | Class | Source-grounded effect | Risk / verification / rollback |
|---|---|---|---|
| `ld *.o –lc –lm` | state-changing / artifact-producing | UNIX linker example: links object files and scans C/math libraries | Produces/updates an executable artifact; exact output name, verification and rollback are `[Needs confirmation]`. |
| `file` utility | read-only | Question 51 suggests using it to identify executable files that are not scripts | Exact invocation is not supplied by the source. |

## Explicit APIs / OS mechanisms

| Mechanism | Class | Source-grounded role |
|---|---|---|
| `fork` | workload-generating / state-changing | Creates a child process; chapter uses it to explain shared pages and copy-on-write |
| file mapping system call (name not supplied) | state-changing mapping | Maps a file into part of a process virtual address space |
| MMU page-table update | state-changing mapping | Changes virtual-page → physical-frame mapping |
| TLB fill/replacement | state-changing hardware cache | Adds/replaces a cached translation |
| page fault handler | state-changing / may block on I/O | Resolves missing mappings/pages and restarts the faulting instruction |
| page replacement | state-changing | Reclaims a frame; dirty pages must be written before reuse |
| page pinning | state-changing | Prevents an I/O/DMA page from being selected for replacement |
| swap in / swap out | state-changing / heavy I/O | Moves an entire process between RAM and backing storage |
| copy-on-write protection fault | state-changing mapping | Copies a shared data page on first write and changes both copies to READ-WRITE |
| mapped-file unmap/process exit | state-changing | Modified mapped pages are written back according to the described model |

## Hardware state used by algorithms

- page-table present/absent bit;
- protection bits;
- referenced bit `R`;
- modified bit `M`;
- physical page-frame number;
- TLB valid/used, virtual-page, protection and frame fields;
- working-set last-use time;
- WSClock circular pointer.

These are not shell commands. Do not infer OS-specific tools such as `sysctl`, `vmstat`, `mmap` command-line wrappers or Linux `/proc` controls from model memory; the chapter does not supply them.

## Safety boundary

Page-table, protection, swapping and replacement changes can change process correctness and persistence behavior. For real infrastructure, exact mutation/verification/rollback commands are platform-specific and remain `[Needs confirmation]`.
